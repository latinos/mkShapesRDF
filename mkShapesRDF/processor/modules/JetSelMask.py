import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import correctionlib
import os
import re
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
        self.columnsToDrop = []

        if self.year in JetMakerCfg.keys():
            if self.doMask == True:
                self.pathToJson = JetMakerCfg[year]["vetomap"]
                self.globalTag = JetMakerCfg[year]["vetokey"]
            if "jetId" in JetMakerCfg[self.year].keys():
                self.doJetId = True
                self.jetIdJson = JetMakerCfg[self.year]["jetId"]["json"]
                self.tight = JetMakerCfg[self.year]["jetId"]["tight"]
                self.tightleptonveto = JetMakerCfg[self.year]["jetId"]["tightleptonveto"]
        
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
            tight = self.tight
            tightleptonveto = self.tightleptonveto

            print(jetIdJson)
            print(tight)
            print(tightleptonveto)
                
            ROOT.gROOT.ProcessLine(f'auto jetIdFile = correction::CorrectionSet::from_file("{jetIdJson}");')
            ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tight = (correction::Correction::Ref) jetIdFile->at("{tight}");')
            ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tightlepveto = (correction::Correction::Ref) jetIdFile->at("{tightleptonveto}");')

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

        if self.doMask:

            ROOT.gROOT.ProcessLine(
                f"""
                auto jetMaskFile = correction::CorrectionSet::from_file("{self.pathToJson}");
                correction::Correction::Ref cset_jet_Map = (correction::Correction::Ref) jetMaskFile->at("{self.globalTag}");
                """
            )

            ROOT.gInterpreter.Declare(
                """
                bool getVetoMask(ROOT::RVecF Jet_pt,ROOT::RVecF Jet_eta, ROOT::RVecF Jet_phi, ROOT::RVecF Jet_neEmEF, ROOT::RVecF Jet_chEmEF, ROOT::RVecI Jet_jetId)
                {
                    float tmp_value;
                    float eta, phi;
                    float Jet_EM;
                    float jet_id_veto;
                    for (int i=0; i<Jet_pt.size(); i++){
                        phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_phi[i], 3.1415}), -3.1415});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_eta[i], 5.19}), -5.19});
                        Jet_EM = Jet_neEmEF[i] + Jet_chEmEF[i];
                        jet_id_veto = Jet_jetId[i];
                        tmp_value = cset_jet_Map->evaluate({"jetvetomap", eta, phi});
                        if (Jet_EM < 0.9 && jet_id_veto == 6 && Jet_pt[i] > 15 && tmp_value!=0.0){
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
                    bool getVetoMaskEE(ROOT::RVecF Jet_pt,ROOT::RVecF Jet_eta, ROOT::RVecF Jet_phi, ROOT::RVecF Jet_neEmEF, ROOT::RVecF Jet_chEmEF, ROOT::RVecI Jet_jetId){
                        float tmp_value;
                        float eta, phi;
                        float Jet_EM;
                        float jet_id_veto;
                        for (int i=0; i<Jet_pt.size(); i++){
                            phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_phi[i], 3.1415}), -3.1415});
                            eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_eta[i], 5.19}), -5.19});
                            Jet_EM = Jet_neEmEF[i] + Jet_chEmEF[i];
                            jet_id_veto = Jet_jetId[i];
                            tmp_value = cset_jet_Map->evaluate({"jetvetomap_eep", eta, phi});
                            if (Jet_EM < 0.9 && jet_id_veto == 6 && Jet_pt[i] > 15 && tmp_value!=0.0){
                                return false;
                            }
                        }
                        return true;
                    }
                    """
                )

                df = df.Define("VetoMaskEE", "getVetoMaskEE(Jet_pt,Jet_eta,Jet_phi,Jet_neEmEF,Jet_chEmEF,Jet_jetId)")
                df = df.Filter("VetoMaskEE")
                self.columnsToDrop.append("VetoMaskEE")
            
            df = df.Define("VetoMask", "getVetoMask(Jet_pt,Jet_eta,Jet_phi,Jet_neEmEF,Jet_chEmEF,Jet_jetId)")

            print("Applying jet veto map")
            df = df.Filter("VetoMask")
            self.columnsToDrop.append("VetoMask")

        ROOT.gInterpreter.Declare("""
        using namespace ROOT;
        using namespace ROOT::VecOps;
        ROOT::RVecB reduce_cond_any(ROOT::RVecB condition, uint size1, uint size2){
            ROOT::RVecB r;
            for (uint i = 0; i < size1; i++){
                bool c = false;
                for (uint j = 0; j < size2; j++){
                    if (condition[i * size2 + j]){
                        c = true; break;
                    }
                }
                r.push_back(c);
            }
            return r;
        }
        """)

        df = df.Define("LeptonMask_JC", "(Lepton_pt >= 10)")
        df = df.Define("Jet_Lepton_comb", "ROOT::VecOps::Combinations(Jet_pt.size(), Lepton_pt[LeptonMask_JC].size())")

        df = df.Define("dR2", """
            ROOT::VecOps::DeltaR2(
                Take(Jet_eta, Jet_Lepton_comb[0]), 
                Take(Lepton_eta, Jet_Lepton_comb[1]), 
                Take(Jet_phi, Jet_Lepton_comb[0]), 
                Take(Lepton_phi, Jet_Lepton_comb[1])
        )""")

        df = df.Define("CleanJet_geometrical", "! reduce_cond_any(dR2 < (0.3*0.3), Jet_pt.size(), Lepton_pt[LeptonMask_JC].size())")

        df = df.Define("CleanJetMask", f"(Jet_pt >= {self.minPt} && abs(Jet_eta) <= {self.maxEta} && Jet_jetId >= {self.jetId}) && CleanJet_geometrical")

        values.append([df.Define("test", "Jet_pt.size()").Sum("test"), "Original size of CleanJet"])

        print("Branch redefinition!")

        
        df = df.Define("CleanJet_jetIdx", "ROOT::VecOps::Range(nJet)[CleanJetMask]")
        for prop in ["pt", "eta", "phi", "mass"]:
            df = df.Define(f"CleanJet_{prop}", f"Jet_{prop}[CleanJetMask]")


        values.append([df.Define("test", "CleanJet_pt.size()").Sum("test"), "Final size of CleanJet"])

        self.columnsToDrop.append("CleanJet_geometrical")
        self.columnsToDrop.append("Jet_Lepton_comb")
        self.columnsToDrop.append("dR2")
        self.columnsToDrop.append("CleanJetMask")
        for col in self.columnsToDrop:
            df = df.DropColumns(col)

        return df