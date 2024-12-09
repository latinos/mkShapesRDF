from mkShapesRDF.processor.framework.module import Module
import os
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

class LeptonFiller_ttHMVA(Module):
    def __init__(self, script_path="processor/data/ttH-Run3-LeptonMVA/"):
        super().__init__("LeptonFiller_ttHMVA")
        self.script_path = script_path
        
    def runModule(self, df, values):

        if not hasattr(ROOT, "getJetPtRatio"):
            ROOT.gInterpreter.Declare(
                """
		ROOT::RVecF getJetPtRatio(ROOT::RVecF Muon_jetRelIso){
                    ROOT::RVecF result(Muon_jetRelIso.size(), 1.5);
                    float tmp_value = 0.0;
                    for (int i=0; i<Muon_jetRelIso.size(); i++){
                        tmp_value = 1.0 / (1.0 + Muon_jetRelIso[i]);
                        if (tmp_value<1.5){
                            result[i] = tmp_value;
                        }
                    }
                    return result;
                }
		"""
            )
        
        ROOT.gROOT.ProcessLineSync(f".L {self.script_path}/Muon_tthMVAFiller.cc+")
        ROOT.gInterpreter.Declare(f'Muon_tthMVAFiller evaluateTTH_muon("{self.script_path}");')

        ROOT.gROOT.ProcessLineSync(f".L {self.script_path}/Electron_tthMVAFiller.cc+")
        ROOT.gInterpreter.Declare(f'Electron_tthMVAFiller evaluateTTH_electron("{self.script_path}");')
        
        if "Muon_log_dxy" not in df.GetColumnNames():
            df = df.Define("Muon_miniRelIsoNeutral", "Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg")
            df = df.Define("Muon_jetPtRatio", "getJetPtRatio(Muon_jetRelIso)")
            df = df.Define("Muon_jetBTagDeepFlavB", "ROOT::VecOps::Take(Jet_btagDeepFlavB,Muon_jetIdx,float(0.0))")
            df = df.Define("Muon_log_dxy", "ROOT::VecOps::log(abs(Muon_dxy))")
            df = df.Define("Muon_log_dz", "ROOT::VecOps::log(abs(Muon_dz))")
        
            df = df.Define("Electron_miniRelIsoNeutral", "Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg")
            df = df.Define("Electron_jetPtRatio", "getJetPtRatio(Electron_jetRelIso)")
            df = df.Define("Electron_jetBTagDeepFlavB", "ROOT::VecOps::Take(Jet_btagDeepFlavB,Electron_jetIdx,float(0.0))")
            df = df.Define("Electron_log_dxy", "ROOT::VecOps::log(abs(Electron_dxy))")
            df = df.Define("Electron_log_dz", "ROOT::VecOps::log(abs(Electron_dz))")        

        df = df.Define(
            "Muon_tthMVA",
            "evaluateTTH_muon(Muon_pt, Muon_eta, Muon_pfRelIso03_all, Muon_miniPFRelIso_chg, Muon_miniRelIsoNeutral, Muon_jetNDauCharged, Muon_jetPtRelv2, Muon_jetBTagDeepFlavB, Muon_jetPtRatio, Muon_sip3d, Muon_log_dxy, Muon_log_dz, Muon_segmentComp)"
        )
        df = df.Define(
            "Electron_tthMVA",
            "evaluateTTH_electron(Electron_pt,Electron_eta,Electron_pfRelIso03_all,Electron_miniPFRelIso_chg,Electron_miniRelIsoNeutral,Electron_jetNDauCharged,Electron_jetPtRelv2,Electron_jetBTagDeepFlavB,Electron_jetPtRatio,Electron_sip3d,Electron_log_dxy,Electron_log_dz,Electron_mvaIso)"
        )
        
        return df
