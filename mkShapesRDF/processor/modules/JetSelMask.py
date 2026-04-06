import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import correctionlib
import os
import re
correctionlib.register_pyroot_binding()

class JetSelMask(Module):
    def __init__(self, jetId, minPt, maxEta, UL2016fix=False, year="", doMask = True, eventMask=False):
        super().__init__("JetSelMask")
        self.jetId = jetId
        self.minPt = minPt
        self.maxEta = maxEta
        self.doMask = doMask
        self.UL2016fix = UL2016fix
        self.eventMask = eventMask
        self.year = year
        self.columnsToDrop = []

        if self.year in JetMakerCfg.keys():
            if self.doMask == True:
                self.pathToJson = JetMakerCfg[year]["vetomap"]
                self.globalTag = JetMakerCfg[year]["vetokey"]
        
    def runModule(self, df, values):

        if self.doMask:

            ROOT.gROOT.ProcessLine(
                f"""
                auto jetMaskFile = correction::CorrectionSet::from_file("{self.pathToJson}");
                correction::Correction::Ref cset_jet_Map = (correction::Correction::Ref) jetMaskFile->at("{self.globalTag}");
                """
            )

            ROOT.gInterpreter.Declare(
                """
                bool getVetoMask(ROOT::RVecF Jet_pt,ROOT::RVecF Jet_eta, ROOT::RVecF Jet_phi, ROOT::RVecF Jet_neEmEF, ROOT::RVecF Jet_chEmEF, ROOT::RVecI Jet_jetId, ROOT::RVecI CorrectedJet_jetIdx)
                {
                    float tmp_value;
                    float eta, phi;
                    float Jet_EM;
                    float jet_id_veto;
                    for (int i=0; i<Jet_pt.size(); i++){
                        phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_phi[i], 3.1415}), -3.1415});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_eta[i], 5.19}), -5.19});
                        Jet_EM = Jet_neEmEF[CorrectedJet_jetIdx[i]] + Jet_chEmEF[CorrectedJet_jetIdx[i]];
                        jet_id_veto = Jet_jetId[CorrectedJet_jetIdx[i]];
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
                    bool getVetoMaskEE(ROOT::RVecF Jet_pt,ROOT::RVecF Jet_eta, ROOT::RVecF Jet_phi, ROOT::RVecF Jet_neEmEF, ROOT::RVecF Jet_chEmEF, ROOT::RVecI Jet_jetId, ROOT::RVecI CorrectedJet_jetIdx){
                        float tmp_value;
                        float eta, phi;
                        float Jet_EM;
                        float jet_id_veto;
                        for (int i=0; i<Jet_pt.size(); i++){
                            phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_phi[i], 3.1415}), -3.1415});
                            eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{Jet_eta[i], 5.19}), -5.19});
                            Jet_EM = Jet_neEmEF[CorrectedJet_jetIdx[i]] + Jet_chEmEF[CorrectedJet_jetIdx[i]];
                            jet_id_veto = Jet_jetId[CorrectedJet_jetIdx[i]];
                            tmp_value = cset_jet_Map->evaluate({"jetvetomap_eep", eta, phi});
                            if (Jet_EM < 0.9 && jet_id_veto == 6 && Jet_pt[i] > 15 && tmp_value!=0.0){
                                return false;
                            }
                        }
                        return true;
                    }
                    """
                )

                df = df.Define("VetoMaskEE", "getVetoMaskEE(CorrectedJet_pt,CorrectedJet_eta,CorrectedJet_phi,Jet_neEmEF,Jet_chEmEF,Jet_jetId,CorrectedJet_jetIdx)")
                df = df.Filter("VetoMaskEE")
                self.columnsToDrop.append("VetoMaskEE")
            
            df = df.Define("VetoMask", "getVetoMask(CorrectedJet_pt,CorrectedJet_eta,CorrectedJet_phi,Jet_neEmEF,Jet_chEmEF,Jet_jetId,CorrectedJet_jetIdx)")

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
        df = df.Define("Jet_Lepton_comb", "ROOT::VecOps::Combinations(CorrectedJet_pt.size(), Lepton_pt[LeptonMask_JC].size())")

        df = df.Define("dR2", """
            ROOT::VecOps::DeltaR2(
                Take(CorrectedJet_eta, Jet_Lepton_comb[0]), 
                Take(Lepton_eta, Jet_Lepton_comb[1]), 
                Take(CorrectedJet_phi, Jet_Lepton_comb[0]), 
                Take(Lepton_phi, Jet_Lepton_comb[1])
        )""")

        df = df.Define("CleanJet_geometrical", "! reduce_cond_any(dR2 < (0.3*0.3), CorrectedJet_pt.size(), Lepton_pt[LeptonMask_JC].size())")
        df = df.Define("jetIdCut", f"Take(Jet_jetId, CorrectedJet_jetIdx) >= {self.jetId}")

        df = df.Define("CleanJetMask", f"(CorrectedJet_pt >= {self.minPt} && abs(CorrectedJet_eta) <= {self.maxEta} && jetIdCut && CleanJet_geometrical)")

        values.append([df.Define("test", "CorrectedJet_pt.size()").Sum("test"), "Original size of CleanJet"])

        print("Branch redefinition!")

        
        df = df.Define("CleanJet_correctedjetIdx", "ROOT::VecOps::Range(nCorrectedJet)[CleanJetMask]")
        df = df.Define("CleanJet_jetIdx", "CorrectedJet_jetIdx[CleanJetMask]")
        for prop in ["pt", "eta", "phi", "mass"]:
            df = df.Define(f"CleanJet_{prop}", f"CorrectedJet_{prop}[CleanJetMask]")


        values.append([df.Define("test", "CleanJet_pt.size()").Sum("test"), "Final size of CleanJet"])

        self.columnsToDrop.append("CleanJet_geometrical")
        self.columnsToDrop.append("Jet_Lepton_comb")
        self.columnsToDrop.append("dR2")
        self.columnsToDrop.append("CleanJetMask")
        self.columnsToDrop.append("LeptonMask_JC")
        self.columnsToDrop.append("jetIdCut")
        for col in self.columnsToDrop:
            df = df.DropColumns(col)

        return df