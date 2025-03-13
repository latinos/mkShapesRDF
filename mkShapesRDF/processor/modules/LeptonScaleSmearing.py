from mkShapesRDF.processor.framework.module import Module
import os
import re
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

class LeptonScaleSmearing(Module):
    def __init__(self, era, isMC, framework_path=None):
        super().__init__("LeptonScaleSmearing")

        self.isMC = isMC
        self.scale_path = ""
        self.columnsToDrop = []
        self.correction_file = ""
        
        if framework_path:
            self.scale_path = framework_path.split("framework")[0] + "/processor/data/muon_scale"
        else:
            self.scale_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/muon_scale"        
            
        if "2022" or "2023" in era:
            self.prodTime = "Summer"
        else:
            print("LeptonScaleSmearing")
            print("-------------------")
            print("Warning: Production season unknown for " + era)
            print("Please check!!")
            
        year = re.findall(r'\d+', era)[0]
        key = era.split("Full20")[1].split("v")[0]
        self.correction_file = self.scale_path + "/" + year + "_" + self.prodTime + key + ".json"

        print(f"LeptonScaleSmearing: running scale and smearing corrections for muons from {era}")
        
    def runModule(self, df, values):

        ROOT.gROOT.ProcessLine(
            f'auto cset = correction::CorrectionSet::from_file("{self.correction_file}");'
        )
        ROOT.gROOT.ProcessLine(f'#include "{self.scale_path}/MuonScaRe.cc"')

        ## Function to loop over muons and run the scale corrections
        if not hasattr(ROOT, "doMuonScale"):
            ROOT.gInterpreter.Declare(
                """
                std::vector<RVecF> doMuonScale(RVecF Lepton_pt,
                                               RVecF Lepton_phi,
                                               RVecF Lepton_eta,
                                               RVecI Muon_charge,
                                               RVecI Lepton_pdgId,
                                               RVecI Lepton_muonIdx,
                                               RVecI Muon_nTrackerLayers,
                                               bool isMC)
                {
                    
                    float tmpScale_mc;
                    RVecF Lepton_newPt = Lepton_pt;
                    RVecF Lepton_newPt_ScaleUp = Lepton_pt;
                    RVecF Lepton_newPt_ScaleDn = Lepton_pt;
                    RVecF Lepton_newPt_ResUp = Lepton_pt;
                    RVecF Lepton_newPt_ResDn = Lepton_pt;
                    
                    std::vector<RVecF> results = {Lepton_newPt, Lepton_newPt_ScaleUp, Lepton_newPt_ScaleDn, Lepton_newPt_ResUp, Lepton_newPt_ResDn};
                    
                    if (!isMC){
                        for (unsigned int i=0; i<Lepton_pt.size(); i++){
                            if (abs(Lepton_pdgId[i])==13)
                            Lepton_newPt[i] = pt_scale(1, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);                            
                        }
                        results[0] = Lepton_newPt;
                    }else{
                        for (unsigned int i=0; i<Lepton_pt.size(); i++){
                            tmpScale_mc = -99.9;
                            if (abs(Lepton_pdgId[i])==13){
                                tmpScale_mc = pt_scale(isMC, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);
                                Lepton_newPt[i] = pt_resol(tmpScale_mc, Lepton_eta[i], (float)Muon_nTrackerLayers[Lepton_muonIdx[i]]);
                                Lepton_newPt_ScaleUp[i] = pt_scale_var(Lepton_newPt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]], "up");
                                Lepton_newPt_ScaleDn[i] = pt_scale_var(Lepton_newPt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]], "dn");
                                Lepton_newPt_ResUp[i] = pt_resol_var(tmpScale_mc, Lepton_newPt[i], Lepton_eta[i], "up");
                                Lepton_newPt_ResDn[i] = pt_resol_var(tmpScale_mc, Lepton_newPt[i], Lepton_eta[i], "dn");
                            }
                        }
                        results[0] = Lepton_newPt;
                        results[1] = Lepton_newPt_ScaleUp;
                        results[2] = Lepton_newPt_ScaleDn;
                        results[3] = Lepton_newPt_ResUp;
                        results[4] = Lepton_newPt_ResDn;                    
                    }
                    return results;
                }
                """
            )

        # Order pT again
        if not hasattr(ROOT, "sortedIndices"):
            ROOT.gInterpreter.Declare(
                """
                ROOT::RVecI sortedIndices(ROOT::RVecF variable){
                    return Reverse(Argsort(variable));
                }
                """
            )

        # Correct MET by new Lepton pT
        if not hasattr(ROOT, "CorrectMET"):
            ROOT.gInterpreter.Declare(
                """
                RVecD CorrectMET(RVecF Lepton_pt,
                                 RVecF Lepton_newPt,
                                 RVecF Lepton_phi,
                                 RVecF Lepton_eta,
                                 RVecI Lepton_pdgId,
                                 float MET_pt,
                                 float MET_phi)
                {
                    TLorentzVector MET;
                    TLorentzVector Lepton;
                    TLorentzVector Lepton_new;

                    MET.SetPtEtaPhiM(MET_pt, 0.0, MET_phi, 0.0);
                    for (unsigned int i=0; i<Lepton_pt.size(); i++){
                        if (abs(Lepton_pdgId[i])!=13)
                            continue;

                        Lepton.SetPtEtaPhiM(Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], 0.0);
                        Lepton_new.SetPtEtaPhiM(Lepton_newPt[i], Lepton_eta[i], Lepton_phi[i], 0.0);
                        MET = MET + Lepton_new - Lepton;
                    }
                    return {MET.Pt(), MET.Phi()};
                }
                """
            )

        #### Compute the muon scale and smearing corrections

        isMC = str(self.isMC).lower()
        df = df.Define(
            "Lepton_ScaleSmearing",
            f"doMuonScale(Lepton_pt, Lepton_phi, Lepton_eta, Muon_charge, Lepton_pdgId, Lepton_muonIdx, Muon_nTrackerLayers, {isMC})"
        )

        df = df.Define(
            "Lepton_newPt",
            "Lepton_ScaleSmearing[0]"
        )
        self.columnsToDrop.append("Lepton_newPt")
        if self.isMC:
            df = df.Define(
                "Lepton_pt_ScaleUp",
                "Lepton_ScaleSmearing[1]"
            )
            df = df.Define(
                "Lepton_pt_ScaleDo",
                "Lepton_ScaleSmearing[2]"
	    )
            df = df.Define(
                "Lepton_pt_ResUp",
                "Lepton_ScaleSmearing[3]"
	    )
            df = df.Define(
                "Lepton_pt_ResDo",
                "Lepton_ScaleSmearing[4]"
	    )

            #### Vary lepton pT for the following l2kin, l3kin, ....

            tags = ["up", "do"]
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_ScaleUp, Lepton_pt_ScaleDo}",
                ["up", "do"],
                "muonScale"
            )
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_ResUp, Lepton_pt_ResDo}",
                ["up", "do"],
                "muonResolution"
            )

        df = df.DropColumns("Lepton_ScaleSmearing")

        ### Recompute MET with the corrected muon-pT
        df = df.Define(
            "PuppiMET_MuonScale",
            "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PuppiMET_pt, PuppiMET_phi)"
        )
        df = df.Define(
            "MET_MuonScale",
            "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PuppiMET_pt, PuppiMET_phi)"
        )
        self.columnsToDrop.append("PuppiMET_MuonScale")
        self.columnsToDrop.append("MET_MuonScale")
        
        df = df.Redefine("PuppiMET_pt", "PuppiMET_MuonScale[0]")
        df = df.Redefine("PuppiMET_phi", "PuppiMET_MuonScale[1]")

        df = df.Redefine("MET_pt", "MET_MuonScale[0]")
        df = df.Redefine("MET_phi", "MET_MuonScale[1]")

        #### Re-order lepton-pT again
            
        df = df.Define("Lepton_sorting",     "sortedIndices(Lepton_newPt)")
        df = df.Define("Lepton_rochesterSF", "Take(Lepton_newPt/Lepton_pt, Lepton_sorting)")
        df = df.Redefine("Lepton_pt",        "Take(Lepton_newPt, Lepton_sorting)")
            
        for branch in df.GetColumnNames():
            if branch.startswith("Lepton_") and branch!="Lepton_pt":
                df = df.Redefine(branch, f"Take({branch}, Lepton_sorting)")

        self.columnsToDrop.append("Lepton_sorting")

        for dropBranch in self.columnsToDrop:
            df = df.DropColumns(dropBranch)

        return df
