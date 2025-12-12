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
        
    def runModule(self, df, values):
        # jetId = 2
        # wp = "loose"
        # minPt = 15.0
        # maxEta = 4.7
        # UL2016fix = False
        
        if self.doJetId:

            jetIdJson = self.jetIdJson
            key = self.key

            print(jetIdJson)
            print(key)
            
            ROOT.gROOT.ProcessLine(f'auto jetIdFile = correction::CorrectionSet::from_file("{jetIdJson}");')
            ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id = (correction::Correction::Ref) jetIdFile->at("{key}");')

            ROOT.gInterpreter.Declare(
                """
                RVecB Jet_ID(
                    RVecF Jet_eta,
                    RVecF Jet_chHEF,
                    RVecF Jet_neHEF,
                    RVecF Jet_chEmEF,
                    RVecF Jet_neEmEF,
                    RVecF Jet_muEF,
                    RVecI Jet_chMultiplicity,
                    RVecI Jet_neMultiplicity){

                    RVecB Jet_JetId(Jet_eta.size(), 0);
                    
                    for (int i=0; i<Jet_eta.size(); i++){

                        int multiplicity = Jet_chMultiplicity[i] + Jet_neMultiplicity[i];

                        Jet_JetId[i] = cset_jet_id->evaluate({Jet_eta[i], Jet_chHEF[i], Jet_neHEF[i], Jet_chEmEF[i], Jet_neEmEF[i], Jet_muEF[i], Jet_chMultiplicity[i], Jet_neMultiplicity[i], multiplicity});
                    }

                    return Jet_JetId;
                }
                """
            )

            df = df.Define(
                "Jet_jetId",
                "Jet_ID(Jet_eta,Jet_chHEF,Jet_neHEF,Jet_chEmEF,Jet_neEmEF,Jet_muEF,Jet_chMultiplicity,Jet_neMultiplicity)"
            )
            jetIdCut = "Take(Jet_jetId, CleanJet_jetIdx) >= 1"
        else:
            jetIdCut = f"Take(Jet_jetId, CleanJet_jetIdx) > {self.jetId}"

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
                bool getJetMask(ROOT::RVecF CleanJet_pt,ROOT::RVecF CleanJet_eta, ROOT::RVecF CleanJet_phi){
                    float tmp_value;
                    float eta, phi;
                    for (int i=0; i<CleanJet_pt.size(); i++){
                        phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
                        tmp_value = cset_jet_Map->evaluate({"jetvetomap", eta, phi});
                        if (tmp_value!=0.0){
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
                    bool getEventMask(ROOT::RVecF CleanJet_pt,ROOT::RVecF CleanJet_eta, ROOT::RVecF CleanJet_phi){
                        float tmp_value;
                        float eta,phi;
                        for (int i=0; i<CleanJet_pt.size(); i++){
                            phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
                            eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
                            tmp_value = cset_jet_Map->evaluate({"jetvetomap_eep", eta, phi});
                            if (tmp_value!=0.0){
                                return false;
                            }
                        }
                        return true;
                    }
                    """
                )

                df = df.Define(
                    "CleanEventMask",
                    "getEventMask(CleanJet_pt,CleanJet_eta,CleanJet_phi)"
                )
                df = df.Filter("CleanEventMask")
                df = df.DropColumns("CleanEventMask")
            
            df = df.Define(
                "JetVetoMask",
                "getJetMask(CleanJet_pt,CleanJet_eta,CleanJet_phi)"
            )
            print("Applying jet veto map")
            df = df.Filter("JetVetoMask")
            df = df.DropColumns("JetVetoMask")

        df = df.DropColumns("BaseCleanJetMask")

        return df
