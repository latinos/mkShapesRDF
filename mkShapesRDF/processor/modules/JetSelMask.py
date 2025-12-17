import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import correctionlib
import os
correctionlib.register_pyroot_binding()

class JetSelMask(Module):
    def __init__(self, jetId, puJetId, minPt, maxEta, UL2016fix=False, year="", doMask = True, eventMask=False):
        super().__init__("JetSelMask")
        self.jetId = jetId
        self.minPt = minPt
        self.maxEta = maxEta
        self.doMask = doMask
        self.doJetId = False
        self.UL2016fix = UL2016fix
        self.eventMask = eventMask
        self.year = year

        if self.year in JetMakerCfg.keys():
            if self.doMask == True:
                self.pathToJson = JetMakerCfg[year]["vetomap"]
                self.globalTag = JetMakerCfg[year]["vetokey"]
            if "jetId" in JetMakerCfg[self.year].keys():
                self.doJetId = True
                self.jetIdJson = JetMakerCfg[self.year]["jetId"]["json"]
                self.key = JetMakerCfg[self.year]["jetId"]["key"]
                self.key_veto = JetMakerCfg[self.year]["jetId"]["key_veto"]
        
    def runModule(self, df, values):
        # jetId = 2
        # wp = "loose"
        # minPt = 15.0
        # maxEta = 4.7
        # UL2016fix = False

        if "v12" in self.year:
            ROOT.gInterpreter.Declare(
                """
                RVecI Jet_ID(
                    RVecF Jet_eta,
                    RVecF Jet_neHEF,
                    RVecF Jet_neEmEF,
                    RVecF Jet_chEmEF,
                    RVecF Jet_muEF,
                    RVecI Jet_jetId){

                    RVecI Jet_JetId(Jet_eta.size(), 0);

                    for (int i = 0; i < Jet_eta.size(); i++) {

                        float eta = fabs(Jet_eta[i]);
                        int jetid = Jet_jetId[i];

                        bool tight = (jetid & (1 << 1)) && ((eta <= 2.7) || (eta <= 3.0 && Jet_neHEF[i] < 0.99) || (eta >  3.0 && Jet_neEmEF[i] < 0.40));

                        bool tightLepVeto = tight && (eta > 2.7 || (Jet_muEF[i] < 0.80 && Jet_chEmEF[i] < 0.80));

                        Jet_JetId[i] = tightLepVeto ? 6 : (tight ? 2 : 0);

                    }

                    return Jet_JetId;
                }
                """
            )
            df = df.Redefine("Jet_jetId", "Jet_ID(Jet_eta,Jet_neHEF,Jet_neEmEF,Jet_chEmEF,Jet_muEF,Jet_jetId)")
        
        if self.doJetId:

            jetIdJson = self.jetIdJson
            key = self.key
            key_veto = self.key_veto

            print(jetIdJson)
            print(key)
            print(key_veto)
            
            ROOT.gROOT.ProcessLine(f'auto jetIdFile = correction::CorrectionSet::from_file("{jetIdJson}");')
            ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tight = (correction::Correction::Ref) jetIdFile->at("{key}");')
            ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tightlepveto = (correction::Correction::Ref) jetIdFile->at("{key_veto}");')

            ROOT.gInterpreter.Declare(
                """
                RVecI Jet_ID(
                    RVecF Jet_eta,
                    RVecF Jet_chHEF,
                    RVecF Jet_neHEF,
                    RVecF Jet_chEmEF,
                    RVecF Jet_neEmEF,
                    RVecF Jet_muEF,
                    RVecI Jet_chMultiplicity,
                    RVecI Jet_neMultiplicity){

                    RVecI Jet_JetId(Jet_eta.size(), 0);
                    
                    for (int i=0; i<Jet_eta.size(); i++){

                        int multiplicity = Jet_chMultiplicity[i] + Jet_neMultiplicity[i];

                        int pass_id = cset_jet_id_tight->evaluate({Jet_eta[i], Jet_chHEF[i], Jet_neHEF[i], Jet_chEmEF[i], Jet_neEmEF[i], Jet_muEF[i], Jet_chMultiplicity[i], Jet_neMultiplicity[i], multiplicity});
                        int pass_lepveto = cset_jet_id_tightlepveto->evaluate({Jet_eta[i], Jet_chHEF[i], Jet_neHEF[i], Jet_chEmEF[i], Jet_neEmEF[i], Jet_muEF[i], Jet_chMultiplicity[i], Jet_neMultiplicity[i], multiplicity});

                        if (pass_lepveto) Jet_JetId[i] = 6;
                        else if (pass_id) Jet_JetId[i] = 2;
                        else Jet_JetId[i] = 0;
                    }

                    return Jet_JetId;
                }
                """
            )

            df = df.Define("Jet_jetId", "Jet_ID(Jet_eta,Jet_chHEF,Jet_neHEF,Jet_chEmEF,Jet_neEmEF,Jet_muEF,Jet_chMultiplicity,Jet_neMultiplicity)")

        jetIdCut = f"Take(Jet_jetId, CleanJet_jetIdx) >= {self.jetId}"

        df = df.Define("BaseCleanJetMask", f"(CleanJet_pt >= {self.minPt} && abs(CleanJet_eta) <= {self.maxEta} && {jetIdCut})")
        values.append([df.Define("test", "CleanJet_pt.size()").Sum("test"), "Original size of CleanJet"])
        
        print("Branch redefinition!")
        for prop in ["jetIdx", "pt", "eta", "phi", "mass"]:
            df = df.Redefine(f"CleanJet_{prop}", f"CleanJet_{prop}[BaseCleanJetMask]")

        values.append([df.Define("test", "CleanJet_pt.size()").Sum("test"), "Final size of CleanJet"])

        if self.doMask:

            ROOT.gROOT.ProcessLine(
                f"""
                auto jetMaskFile = correction::CorrectionSet::from_file("{self.pathToJson}");
                correction::Correction::Ref cset_jet_Map = (correction::Correction::Ref) jetMaskFile->at("{self.globalTag}");
                """
            )

            ROOT.gInterpreter.Declare(
                """
                bool getJetMask(ROOT::RVecF CleanJet_pt,ROOT::RVecF CleanJet_eta, ROOT::RVecF CleanJet_phi, ROOT::RVecF Jet_neEmEF, ROOT::RVecF Jet_chEmEF, ROOT::RVecI Jet_jetId, ROOT::RVecI CleanJet_jetIdx){
                    float tmp_value;
                    float eta, phi;
                    float cleanJet_EM;
                    float jet_id_veto;
                    for (int i=0; i<CleanJet_pt.size(); i++){
                        phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
                        cleanJet_EM = Jet_neEmEF[CleanJet_jetIdx[i]] + Jet_chEmEF[CleanJet_jetIdx[i]];
                        jet_id_veto = Jet_jetId[CleanJet_jetIdx[i]];
                        tmp_value = cset_jet_Map->evaluate({"jetvetomap", eta, phi});
                        if (cleanJet_EM < 0.9 && jet_id_veto == 6 && CleanJet_pt[i] > 15 && tmp_value!=0.0){
                            return false;
                        }
                    }
                    return true;
                }
                """
            )

            if self.eventMask:
                ROOT.gInterpreter.Declare(
                    """
                    bool getEventMask(ROOT::RVecF CleanJet_pt,ROOT::RVecF CleanJet_eta, ROOT::RVecF CleanJet_phi, ROOT::RVecF Jet_neEmEF, ROOT::RVecF Jet_chEmEF, ROOT::RVecI Jet_jetId, ROOT::RVecI CleanJet_jetIdx){
                        float tmp_value;
                        float eta, phi;
                        float cleanJet_EM;
                        float jet_id_veto;
                        for (int i=0; i<CleanJet_pt.size(); i++){
                            phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
                            eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
                            cleanJet_EM = Jet_neEmEF[CleanJet_jetIdx[i]] + Jet_chEmEF[CleanJet_jetIdx[i]];
                            jet_id_veto = Jet_jetId[CleanJet_jetIdx[i]];
                            tmp_value = cset_jet_Map->evaluate({"jetvetomap_eep", eta, phi});
                            if (cleanJet_EM < 0.9 && jet_id_veto == 6 && CleanJet_pt[i] > 15 && tmp_value!=0.0){
                                return false;
                            }
                        }
                        return true;
                    }
                    """
                )

                df = df.Define("CleanEventMask", "getEventMask(CleanJet_pt,CleanJet_eta,CleanJet_phi,Jet_neEmEF,Jet_chEmEF,Jet_jetId,CleanJet_jetIdx)")
                df = df.Filter("CleanEventMask")
                df = df.DropColumns("CleanEventMask")
            
            df = df.Define("JetVetoMask", "getJetMask(CleanJet_pt,CleanJet_eta,CleanJet_phi,Jet_neEmEF,Jet_chEmEF,Jet_jetId,CleanJet_jetIdx)")

            print("Applying jet veto map")
            df = df.Filter("JetVetoMask")
            df = df.DropColumns("JetVetoMask")

        df = df.DropColumns("BaseCleanJetMask")

        return df
