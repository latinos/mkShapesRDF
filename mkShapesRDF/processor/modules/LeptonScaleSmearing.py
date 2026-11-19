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
        self.era = era
        
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

        # We use the EtDependent corrections, as recommended here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammSFandSSRun3 
        self.muoncorrection_file = MuonWP[era]["ScaleAndSmearing"]
        self.elecorrection_file = ElectronWP[era]["ScaleAndSmearing"]

        self.runPeriods = None
        if type(MuonWP[era]["ScaleAndSmearing"]) == dict:
            self.runPeriods = MuonWP[era]["ScaleAndSmearing"].keys() # Assume same runPeriods for electrons and muons

        # This section computes the `year_key` needed to access the correct part of the correction files.  
        # Since valid year_keys are ['2022preEE', '2022postEE', '2023preBPIX', '2023postBPIX', '2024'],  
        # the `year_key` must include at least one letter.

        if self.runPeriods:
            self.year_key = {}
            for run in self.runPeriods:
                evaluator = correctionlib.CorrectionSet.from_file(self.elecorrection_file[run])
                keys = list(evaluator.keys())
                for key in keys:
                    year_key = key.split('_')[-1]
                    if not any(c.isalpha() for c in year_key):
                        self.year_key[run] = year_key  
                        break
                    else:
                        self.year_key[run] = year_key
        else:
            evaluator = correctionlib.CorrectionSet.from_file(self.elecorrection_file)
            keys = list(evaluator.keys())
            for key in keys:
                year_key = key.split('_')[-1]
                if not any(c.isalpha() for c in year_key):
                    self.year_key = year_key  
                    break
                else:
                    self.year_key = year_key
                
        print(self.elecorrection_file)
        print(self.year_key)

        print(f"LeptonScaleSmearing: running scale and smearing corrections for leptons from {era}")
        
    def runModule(self, df, values):
        # Note that the elecset_scale is a CompoundCorrection object

        if self.runPeriods:
            for run in self.runPeriods:
                ROOT.gROOT.ProcessLine(
                    f'std::shared_ptr<correction::CorrectionSet> cset_{run} = correction::CorrectionSet::from_file("{self.muoncorrection_file[run]}");'
                    f'std::shared_ptr<correction::CorrectionSet> elecset_{run} = correction::CorrectionSet::from_file("{self.elecorrection_file[run]}");'
                    f'correction::CompoundCorrection::Ref elecset_scale_{run} = elecset_{run}->compound().at("Scale");'
                    f'correction::Correction::Ref elecset_smear_{run} = elecset_{run}->at("EGMSmearAndSyst_ElePT_{self.year_key[run]}");'
                )
        else:
            ROOT.gROOT.ProcessLine(
                f'auto cset = correction::CorrectionSet::from_file("{self.muoncorrection_file}");'
                f'auto elecset = correction::CorrectionSet::from_file("{self.elecorrection_file}");'
                f'correction::CompoundCorrection::Ref elecset_scale = elecset->compound().at("Scale");'
                #f'correction::CompoundCorrection::Ref elecset_smear = elecset->compound().at("SmearAndSyst");'
                f'auto elecset_smear = elecset->at("EGMSmearAndSyst_ElePT_{self.year_key}");'
            )            

        #### re-write csets to include run_period as an argument for scale corrections
        text_to_add = ""
        if self.runPeriods:
            # Default-constructed globals; no need to rely on the leftover `run` from the loop
            ROOT.gROOT.ProcessLine(
                'std::shared_ptr<correction::CorrectionSet> cset;'
                'correction::CompoundCorrection::Ref elecset_scale;'
                'correction::Correction::Ref elecset_smear;'
            )

            for run in self.runPeriods:
                text_to_add += f"""
                if (run_period == {run}) {{
                    cset = cset_{run};
                    elecset_scale = elecset_scale_{run};
                    elecset_smear = elecset_smear_{run};
                }}
                """

        ROOT.gROOT.ProcessLine(f'#include "{self.muonscale_path}/MuonScaRe.cc"')
        ROOT.gROOT.ProcessLine(f'#include "{self.macroele_path}/scEta.cc"')
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
                                               bool is_data,
                                               int run_period=-1)
                {
                    static TRandom3 rng(125);

                    """ + text_to_add + """

                    const unsigned int n_leptons = Lepton_pt.size();
                    RVecF Lepton_newPt = Lepton_pt;

                    if (is_data)
                    {
                        // Apply data scale corrections per lepton flavour
                        for (unsigned int i = 0; i < n_leptons; ++i)
                        {
                            const int abs_pdg = std::abs(Lepton_pdgId[i]);
                            if (abs_pdg == 13)
                            {
                                Lepton_newPt[i] = pt_scale(is_data, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);
                            }
                            else if (abs_pdg == 11)
                            {
                                const float sc_eta = Lepton_eta[i] + Electron_deltaEtaSC[Lepton_electronIdx[i]];
                                Lepton_newPt[i] = ele_scale(run, sc_eta, Electron_r9[Lepton_electronIdx[i]], Lepton_pt[i], static_cast<float>(Electron_seedGain[Lepton_electronIdx[i]]));
                            }
                        }

                        // Keep variation slots populated with nominal corrected pT in data
                        return {
                            Lepton_newPt,
                            Lepton_newPt, Lepton_newPt, Lepton_newPt, Lepton_newPt,
                            Lepton_newPt, Lepton_newPt, Lepton_newPt, Lepton_newPt
                        };
                    }

                    // Store per-lepton MC scale factors and Gaussian draws so each lepton keeps its own values
                    RVecF muon_scale_mc(n_leptons, -99.9f);
                    RVecF ele_rand_gaus(n_leptons, 0.0f);

                    // Step 1: Compute nominal corrected pT for both flavours before evaluating variations
                    for (unsigned int i = 0; i < n_leptons; ++i)
                    {
                        const int abs_pdg = std::abs(Lepton_pdgId[i]);
                        if (abs_pdg == 13)
                        {
                            const float scale_mc = pt_scale(is_data, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);
                            muon_scale_mc[i] = scale_mc;
                            Lepton_newPt[i] = pt_resol(scale_mc, Lepton_eta[i], static_cast<float>(Muon_nTrackerLayers[Lepton_muonIdx[i]]));
                        }
                        else if (abs_pdg == 11)
                        {
                            const float sc_eta = Lepton_eta[i] + Electron_deltaEtaSC[Lepton_electronIdx[i]];
                            const float z = static_cast<float>(rng.Gaus(0.0, 1.0));
                            ele_rand_gaus[i] = z;
                            Lepton_newPt[i] = ele_smear(Lepton_pt[i], Electron_r9[Lepton_electronIdx[i]], sc_eta, z);
                        }
                    }

                    // Initialize variation vectors from nominal corrected pT so the non-varied flavour stays at nominal
                    RVecF Lepton_newPt_muoScaleUp = Lepton_newPt;
                    RVecF Lepton_newPt_muoScaleDn = Lepton_newPt;
                    RVecF Lepton_newPt_muoResUp   = Lepton_newPt;
                    RVecF Lepton_newPt_muoResDn   = Lepton_newPt;
                    RVecF Lepton_newPt_eleScaleUp = Lepton_newPt;
                    RVecF Lepton_newPt_eleScaleDn = Lepton_newPt;
                    RVecF Lepton_newPt_eleResUp   = Lepton_newPt;
                    RVecF Lepton_newPt_eleResDn   = Lepton_newPt;

                    // Step 2: Apply scale and resolution variations starting from the corrected nominal pT
                    for (unsigned int i = 0; i < n_leptons; ++i)
                    {
                        const int abs_pdg = std::abs(Lepton_pdgId[i]);
                        if (abs_pdg == 13)
                        {
                            const int m_idx = Lepton_muonIdx[i];
                            const float pt_corr = Lepton_newPt[i];
                            const float scale_mc = muon_scale_mc[i];

                            Lepton_newPt_muoScaleUp[i] = pt_scale_var(pt_corr, Lepton_eta[i], Lepton_phi[i], Muon_charge[m_idx], "up");
                            Lepton_newPt_muoScaleDn[i] = pt_scale_var(pt_corr, Lepton_eta[i], Lepton_phi[i], Muon_charge[m_idx], "dn");
                            Lepton_newPt_muoResUp[i]   = pt_resol_var(scale_mc, pt_corr, Lepton_eta[i], "up");
                            Lepton_newPt_muoResDn[i]   = pt_resol_var(scale_mc, pt_corr, Lepton_eta[i], "dn");
                        }
                        else if (abs_pdg == 11)
                        {
                            const int e_idx = Lepton_electronIdx[i];
                            const float sc_eta = Lepton_eta[i] + Electron_deltaEtaSC[e_idx];
                            const float pt_corr = Lepton_newPt[i];
                            const double z = static_cast<double>(ele_rand_gaus[i]);

                            Lepton_newPt_eleScaleUp[i] = ele_unc_scale(run, sc_eta, Electron_r9[e_idx], Lepton_pt[i], static_cast<float>(Electron_seedGain[e_idx]), pt_corr, "up");
                            Lepton_newPt_eleScaleDn[i] = ele_unc_scale(run, sc_eta, Electron_r9[e_idx], Lepton_pt[i], static_cast<float>(Electron_seedGain[e_idx]), pt_corr, "dn");
                            Lepton_newPt_eleResUp[i]   = ele_unc_smear(Lepton_pt[i], Electron_r9[e_idx], sc_eta, z, "up");
                            Lepton_newPt_eleResDn[i]   = ele_unc_smear(Lepton_pt[i], Electron_r9[e_idx], sc_eta, z, "dn");
                        }
                    }

                    // Preserve exact index order expected by downstream RDataFrame column definitions
                    return {
                        Lepton_newPt,
                        Lepton_newPt_muoScaleUp,
                        Lepton_newPt_muoScaleDn,
                        Lepton_newPt_muoResUp,
                        Lepton_newPt_muoResDn,
                        Lepton_newPt_eleScaleUp,
                        Lepton_newPt_eleScaleDn,
                        Lepton_newPt_eleResUp,
                        Lepton_newPt_eleResDn
                    };
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
                        MET = MET - Lepton_new + Lepton;
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
            f"doLeptonScale(Lepton_pt, Lepton_phi, Lepton_eta, Muon_charge, Lepton_pdgId, Lepton_muonIdx, Muon_nTrackerLayers,  Electron_seedGain, Electron_r9, Lepton_electronIdx, Electron_deltaEtaSC, run, {isData}, run_period)"
        )

        df = df.Define(
            "Lepton_newPt",
            "Lepton_ScaleSmearing[0]"
        )
        self.columnsToDrop.append("Lepton_newPt")
        if not self.isData:
            df = df.Define(
                "Lepton_pt_muoScaleUp",
                "Lepton_ScaleSmearing[1]"
            )
            df = df.Define(
                "Lepton_pt_muoScaleDo",
                "Lepton_ScaleSmearing[2]"
	        )
            df = df.Define(
                "Lepton_pt_muoResUp",
                "Lepton_ScaleSmearing[3]"
	        )
            df = df.Define(
                "Lepton_pt_muoResDo",
                "Lepton_ScaleSmearing[4]"
	        )
            df = df.Define(
                "Lepton_pt_eleScaleUp",
                "Lepton_ScaleSmearing[5]"
            )
            df = df.Define(
                "Lepton_pt_eleScaleDo",
                "Lepton_ScaleSmearing[6]"
	        )
            df = df.Define(
                "Lepton_pt_eleResUp",
                "Lepton_ScaleSmearing[7]"
	        )
            df = df.Define(
                "Lepton_pt_eleResDo",
                "Lepton_ScaleSmearing[8]"
	        )

            #### Vary lepton pT for the following l2kin, l3kin, ....

            tags = ["up", "do"]
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_muoScaleUp, Lepton_pt_muoScaleDo}",
                ["up", "do"],
                "muonScale"
            )
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_muoResUp, Lepton_pt_muoResDo}",
                ["up", "do"],
                "muonResolution"
            )
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_eleScaleUp, Lepton_pt_eleScaleDo}",
                ["up", "do"],
                "electronScale"
            )
            df = df.Vary(
                "Lepton_pt",
                "ROOT::RVec<ROOT::RVecF>{Lepton_pt_eleResUp, Lepton_pt_eleResDo}",
                ["up", "do"],
                "electronResolution"
            )

        df = df.DropColumns("Lepton_ScaleSmearing")

        ### Recompute MET with the corrected lepton-pT
        df = df.Define(
            "PuppiMET_LeptonScale",
            "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PuppiMET_pt, PuppiMET_phi)"
        )
        if "24" in self.era or "25" in self.era or "RunIII" in self.era:
            df = df.Define(
                "PFMET_LeptonScale",
                "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PFMET_pt, PFMET_phi)"
            )
            df = df.Redefine("PFMET_pt", "PFMET_LeptonScale[0]")
            df = df.Redefine("PFMET_phi", "PFMET_LeptonScale[1]")
            self.columnsToDrop.append("PFMET_LeptonScale")
        else:
            df = df.Define(
                "MET_LeptonScale",
                "CorrectMET(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, MET_pt, MET_phi)"
            )
            df = df.Redefine("MET_pt", "MET_LeptonScale[0]")
            df = df.Redefine("MET_phi", "MET_LeptonScale[1]")
            self.columnsToDrop.append("MET_LeptonScale")

        self.columnsToDrop.append("PuppiMET_LeptonScale")
        
        df = df.Redefine("PuppiMET_pt", "PuppiMET_LeptonScale[0]")
        df = df.Redefine("PuppiMET_phi", "PuppiMET_LeptonScale[1]")

        #### Re-order lepton-pT again

        # Capture only flat per-lepton arrays. The permutation, correction
        # temporaries, and already sorted products must never enter this loop.
        # mRDF propagates a nominal Redefine to its registered variations, so
        # those generated columns must not also be reordered independently.
        varied_columns = set(df.GetVariedColumns(df.GetColumnNames()))
        excluded_columns = set(self.columnsToDrop) | varied_columns | {
            "Lepton_pt",
            "Lepton_sorting",
            "Lepton_rochesterSF",
        }
        lepton_columns = []
        for branch in df.GetColumnNames():
            if (
                branch.startswith("Lepton_") or branch == "isLoose"
            ) and branch not in excluded_columns:
                column_type = df.df.GetColumnType(branch)
                if column_type.count("<") == 1 and (
                    "RVec<" in column_type
                    or column_type.startswith(("vector<", "std::vector<"))
                ):
                    lepton_columns.append(branch)

        df = df.Define("Lepton_sorting",     "sortedIndices(Lepton_newPt)")
        df = df.Define("Lepton_rochesterSF", "Take(Lepton_newPt/Lepton_pt, Lepton_sorting)")
        df = df.Redefine("Lepton_pt",        "Take(Lepton_newPt, Lepton_sorting)")

        # Lepton_newPt has no leptonScale/leptonResolution variations. Reorder
        # the existing pT variations explicitly with the nominal permutation;
        # downstream kinematics then see the same object associations.
        for branch in df.GetVariedColumns(["Lepton_pt"]):
            df = df.Define(
                branch, f"Take({branch}, Lepton_sorting)", excludeVariations=["*"]
            )
        for branch in lepton_columns:
            df = df.Redefine(branch, f"Take({branch}, Lepton_sorting)")

        self.columnsToDrop.append("Lepton_sorting")

        for dropBranch in self.columnsToDrop:
            df = df.DropColumns(dropBranch)

        return df