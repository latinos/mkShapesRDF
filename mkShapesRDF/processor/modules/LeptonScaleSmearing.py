from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *
import os
import re
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

class LeptonScaleSmearing(Module):
    def __init__(self, era, isData, framework_path=None):
        super().__init__("LeptonScaleSmearing")

        self.isData = isData
        self.muonscale_path = ""
        self.elescale_path = ""
        self.macroele_path = ""
        self.columnsToDrop = []
        self.muoncorrection_file = ""
        self.elecorrection_file = ""
        
        # The JSON files were recently added to cvmfs. If you can't find them in /processor/data/jsonpog-integration/POG/EGM, reinstall mkShapesRDF.

        # The muon_scale folder contains the MuonScaRe.cc macro, which defines the functions for computing corrections. This folder also includes the necessary JSON files.

        # The electron_scale folder contains the EleScaRe.cc and scEta.cc macros. EleScaRe.cc handles correction calculations, while scEta.cc computes the supercluster eta.

        if framework_path:
            self.muonscale_path = framework_path.split("framework")[0] + "/processor/data/muon_scale"
            self.elescale_path = framework_path.split("framework")[0] + "/processor/data/jsonpog-integration/POG/EGM"
            self.macroele_path = framework_path.split("framework")[0] + "/processor/data/electron_scale"
        else:
            self.muonscale_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/muon_scale"
            self.elescale_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/jsonpog-integration/POG/EGM"
            self.macroele_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/electron_scale"      
            
        if "2022" in era or "2023" in era or "2024" in era:
            self.prodTime = "Summer"
        else:
            print("LeptonScaleSmearing")
            print("-------------------")
            print("Warning: Production season unknown for " + era)
            print("Please check!!")
            
        year = re.findall(r'\d+', era)[0]
        key = era.split("Full20")[1].split("v")[0]

        # We use the EtDependent corrections, as recommended here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammSFandSSRun3 
        self.muoncorrection_file = MuonWP[era]["ScaleAndSmearing"]
        self.elecorrection_file = ElectronWP[era]["ScaleAndSmearing"]        
        
        # This section computes the `year_key` needed to access the correct part of the correction files.  
        # Since valid year_keys are ['2022preEE', '2022postEE', '2023preBPIX', '2023postBPIX'],  
        # the `year_key` must include at least one letter.  

        evaluator = correctionlib.CorrectionSet.from_file(self.elecorrection_file)
        keys = list(evaluator.keys())
        for key in keys:
            year_key = key.split('_')[-1]            
            if any(c.isalpha() for c in year_key):  
                self.year_key = year_key  
                break
            else:
                self.year_key = year_key
                
        print(self.elecorrection_file)
        print(self.year_key) 

        print(f"LeptonScaleSmearing: running scale and smearing corrections for leptons from {era}")
        
    def runModule(self, df, values):
        # Note that the elecset_scale is a CompoundCorrection object
        ROOT.gROOT.ProcessLine(
            f'auto cset = correction::CorrectionSet::from_file("{self.muoncorrection_file}");'
            f'auto elecset = correction::CorrectionSet::from_file("{self.elecorrection_file}");'
            f'correction::CompoundCorrection::Ref elecset_scale = elecset->compound().at("EGMScale_Compound_Ele_{self.year_key}");'
            f'auto elecset_smear = elecset->at("EGMSmearAndSyst_ElePTsplit_{self.year_key}");'
        )

        ROOT.gROOT.ProcessLine(f'#include "{self.muonscale_path}/MuonScaRe.cc"')
        ROOT.gROOT.ProcessLine(f'#include "{self.macroele_path}/scEta.cc"')
        if "2024" in self.year_key:
            ROOT.gROOT.ProcessLine(f'#include "{self.macroele_path}/EleScaRe_2024.cc"')
        else:
            ROOT.gROOT.ProcessLine(f'#include "{self.macroele_path}/EleScaRe.cc"')
        ROOT.gROOT.ProcessLine('#include <TRandom3.h>')

        # Function to loop over leptons and run the scale corrections. For more details, refer to the macros.
        if not hasattr(ROOT, "doLeptonScale"):
            ROOT.gInterpreter.Declare(
                """
                std::vector<RVecF> doLeptonScale(RVecF Lepton_pt,
                                               RVecF Lepton_phi,
                                               RVecF Lepton_eta,
                                               RVecI Muon_charge,
                                               RVecI Lepton_pdgId,
                                               RVecI Lepton_muonIdx,
                                               RVecI Muon_nTrackerLayers,
                                               RVecF Electron_seedGain,
                                               RVecF Electron_r9,
                                               RVecI Lepton_electronIdx,
                                               RVecF Electron_deltaEtaSC,
                                               float run,
                                               bool is_data)
                {
                    
                    float tmpScale_mc;
                    RVecF Lepton_newPt = Lepton_pt;
                    RVecF Lepton_newPt_ScaleUp = Lepton_pt;
                    RVecF Lepton_newPt_ScaleDn = Lepton_pt;
                    RVecF Lepton_newPt_ResUp = Lepton_pt;
                    RVecF Lepton_newPt_ResDn = Lepton_pt;

                    static TRandom3 rng(125);
                    
                    std::vector<RVecF> results = {Lepton_newPt, Lepton_newPt_ScaleUp, Lepton_newPt_ScaleDn, Lepton_newPt_ResUp, Lepton_newPt_ResDn};
                    
                    if (is_data){
                        for (unsigned int i=0; i<Lepton_pt.size(); i++)
                        {
                            if (abs(Lepton_pdgId[i])==13)
                            {
                                Lepton_newPt[i] = pt_scale(is_data, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);
                            }
                            else if (abs(Lepton_pdgId[i])==11)
                            {
                                float sc_eta = Lepton_eta[i] + Electron_deltaEtaSC[Lepton_electronIdx[i]];
                                Lepton_newPt[i] = ele_scale(run, sc_eta, Electron_r9[Lepton_electronIdx[i]], Lepton_pt[i], (float)Electron_seedGain[Lepton_electronIdx[i]]);

                            }
                        }
                        results[0] = Lepton_newPt;
                    }else{
                        for (unsigned int i=0; i<Lepton_pt.size(); i++)
                        {
                            tmpScale_mc = -99.9;
                            if (abs(Lepton_pdgId[i])==13)
                            {
                                tmpScale_mc = pt_scale(is_data, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);
                                Lepton_newPt[i] = pt_resol(tmpScale_mc, Lepton_eta[i], (float)Muon_nTrackerLayers[Lepton_muonIdx[i]]);
                                Lepton_newPt_ScaleUp[i] = pt_scale_var(Lepton_newPt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]], "up");
                                Lepton_newPt_ScaleDn[i] = pt_scale_var(Lepton_newPt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]], "dn");
                                Lepton_newPt_ResUp[i] = pt_resol_var(tmpScale_mc, Lepton_newPt[i], Lepton_eta[i], "up");
                                Lepton_newPt_ResDn[i] = pt_resol_var(tmpScale_mc, Lepton_newPt[i], Lepton_eta[i], "dn");
                            }
                            else if (abs(Lepton_pdgId[i])==11)
                            {
                                float sc_eta = Lepton_eta[i] + Electron_deltaEtaSC[Lepton_electronIdx[i]];
                                double random_number = rng.Gaus(0.0, 1.0);
                                Lepton_newPt[i] = ele_smear(Lepton_pt[i], Electron_r9[Lepton_electronIdx[i]], sc_eta, random_number);
                                Lepton_newPt_ScaleUp[i] = ele_unc_scale(run, sc_eta, Electron_r9[Lepton_electronIdx[i]], Lepton_pt[i], (float)Electron_seedGain[Lepton_electronIdx[i]], Lepton_newPt[i], "up");
                                Lepton_newPt_ScaleDn[i] = ele_unc_scale(run, sc_eta, Electron_r9[Lepton_electronIdx[i]], Lepton_pt[i], (float)Electron_seedGain[Lepton_electronIdx[i]], Lepton_newPt[i], "dn");
                                Lepton_newPt_ResUp[i] = ele_unc_smear(Lepton_pt[i], Electron_r9[Lepton_electronIdx[i]], sc_eta, random_number, "up");
                                Lepton_newPt_ResDn[i] = ele_unc_smear(Lepton_pt[i], Electron_r9[Lepton_electronIdx[i]], sc_eta, random_number, "dn");
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
                    for (unsigned int i=0; i<Lepton_pt.size(); i++)
                    {
                        if ((abs(Lepton_pdgId[i]) != 13) && (abs(Lepton_pdgId[i]) != 11))
                            continue;
                        Lepton.SetPtEtaPhiM(Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], 0.0);
                        Lepton_new.SetPtEtaPhiM(Lepton_newPt[i], Lepton_eta[i], Lepton_phi[i], 0.0);
                        MET = MET + Lepton_new - Lepton;
                    }
                    return {MET.Pt(), MET.Phi()};
                }
                """
            )

        #### Compute the lepton scale and smearing corrections

        isData = str(self.isData).lower()
        print(isData)
        df = df.Define(
            "Lepton_ScaleSmearing",
            f"doLeptonScale(Lepton_pt, Lepton_phi, Lepton_eta, Muon_charge, Lepton_pdgId, Lepton_muonIdx, Muon_nTrackerLayers,  Electron_seedGain, Electron_r9, Lepton_electronIdx, Electron_deltaEtaSC, run, {isData})"
        )

        df = df.Define(
            "Lepton_newPt",
            "Lepton_ScaleSmearing[0]"
        )
        self.columnsToDrop.append("Lepton_newPt")
        if not self.isData:
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
                "leptonScale"
            )
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_ResUp, Lepton_pt_ResDo}",
                ["up", "do"],
                "leptonResolution"
            )

        df = df.DropColumns("Lepton_ScaleSmearing")

        ### Recompute MET with the corrected lepton-pT
        df = df.Define(
            "PuppiMET_LeptonScale",
            "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PuppiMET_pt, PuppiMET_phi)"
        )
        df = df.Define(
            "MET_LeptonScale",
            "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PuppiMET_pt, PuppiMET_phi)"
        )
        self.columnsToDrop.append("PuppiMET_LeptonScale")
        self.columnsToDrop.append("MET_LeptonScale")
        
        df = df.Redefine("PuppiMET_pt", "PuppiMET_LeptonScale[0]")
        df = df.Redefine("PuppiMET_phi", "PuppiMET_LeptonScale[1]")

        df = df.Redefine("MET_pt", "MET_LeptonScale[0]")
        df = df.Redefine("MET_phi", "MET_LeptonScale[1]")

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
