from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *
import os
import re
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

class MuonScaleSmearing(Module):
    def __init__(self, era, isData, framework_path=None):
        super().__init__("MuonScaleSmearing")

        self.isData = isData
        self.muonscale_path = ""
        self.columnsToDrop = []
        self.muoncorrection_file = ""
        self.era = era
        
        # The JSON files were recently added to cvmfs. If you can't find them in /processor/data/jsonpog-integration/POG/EGM, reinstall mkShapesRDF.

        # The muon_scale folder contains the MuonScaRe.cc macro, which defines the functions for computing corrections. This folder also includes the necessary JSON files.

        # The electron_scale folder contains the EleScaRe.cc and scEta.cc macros. EleScaRe.cc handles correction calculations, while scEta.cc computes the supercluster eta.

        if framework_path:
            self.muonscale_path = framework_path.split("framework")[0] + "/processor/data/muon_scale"
        else:
            self.muonscale_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/muon_scale"   

        # We use the EtDependent corrections, as recommended here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammSFandSSRun3 
        self.muoncorrection_file = MuonWP[era]["ScaleAndSmearing"]

        self.runPeriods = None
        if type(MuonWP[era]["ScaleAndSmearing"]) == dict:
            self.runPeriods = MuonWP[era]["ScaleAndSmearing"].keys() # Assume same runPeriods for electrons and muons

        # This section computes the `year_key` needed to access the correct part of the correction files.  
        # Since valid year_keys are ['2022preEE', '2022postEE', '2023preBPIX', '2023postBPIX', '2024'],  
        # the `year_key` must include at least one letter.

        if self.runPeriods:
            self.year_key = {}
            for run in self.runPeriods:
                evaluator = correctionlib.CorrectionSet.from_file(self.muoncorrection_file[run])
                keys = list(evaluator.keys())
                for key in keys:
                    year_key = key.split('_')[-1]
                    if not any(c.isalpha() for c in year_key):
                        self.year_key[run] = year_key  
                        break
                    else:
                        self.year_key[run] = year_key
        else:
            evaluator = correctionlib.CorrectionSet.from_file(self.muoncorrection_file)
            keys = list(evaluator.keys())
            for key in keys:
                year_key = key.split('_')[-1]
                if not any(c.isalpha() for c in year_key):
                    self.year_key = year_key  
                    break
                else:
                    self.year_key = year_key
                
        print(self.muoncorrection_file)
        print(self.year_key)

        print(f"MuonScaleSmearing: running scale and smearing corrections for leptons from {era}")
        
    def runModule(self, df, values):
        # Note that the elecset_scale is a CompoundCorrection object

        if self.runPeriods:
            for run in self.runPeriods:
                ROOT.gROOT.ProcessLine(
                    f'std::shared_ptr<correction::CorrectionSet> cset_{run} = correction::CorrectionSet::from_file("{self.muoncorrection_file[run]}");'
                )
        else:
            ROOT.gROOT.ProcessLine(
                f'auto cset = correction::CorrectionSet::from_file("{self.muoncorrection_file}");'
            )            

        #### re-write csets to include run_period as an argument for scale corrections
        text_to_add = ""
        if self.runPeriods:
            # Default-constructed globals; no need to rely on the leftover `run` from the loop
            ROOT.gROOT.ProcessLine(
                'std::shared_ptr<correction::CorrectionSet> cset;'
            )

            #ROOT.gROOT.ProcessLine(
            #    f'auto cset = cset_{run};'
            #    f'correction::CompoundCorrection::Ref elecset_scale = elecset_scale_{run};'
            #    f'auto elecset_smear = elecset_{run};'
            #) ## Temporary for initialization

            for run in self.runPeriods:
                text_to_add += f"""
                if (run_period == {run}) {{
                    cset = cset_{run};
                }}
                """

        ROOT.gROOT.ProcessLine(f'#include "{self.muonscale_path}/MuonScaRe.cc"')
        ROOT.gROOT.ProcessLine('#include <TRandom3.h>')

        # Function to loop over leptons and run the scale corrections. For more details, refer to the macros.
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
                                               RVecI Lepton_electronIdx,
                                               float run,
                                               bool is_data,
                                               int run_period=-1)
                {
                    
                    float tmpScale_mc;
                    RVecF Lepton_newPt = Lepton_pt;
                    RVecF Lepton_newPt_ScaleUp = Lepton_pt;
                    RVecF Lepton_newPt_ScaleDn = Lepton_pt;
                    RVecF Lepton_newPt_ResUp = Lepton_pt;
                    RVecF Lepton_newPt_ResDn = Lepton_pt;

                    static TRandom3 rng(125);
                    
                    """ + text_to_add + """

                    std::vector<RVecF> results = {Lepton_newPt, Lepton_newPt_ScaleUp, Lepton_newPt_ScaleDn, Lepton_newPt_ResUp, Lepton_newPt_ResDn};
                    
                    if (is_data){
                        for (unsigned int i=0; i<Lepton_pt.size(); i++)
                        {
                            if (abs(Lepton_pdgId[i])==13)
                            {
                                Lepton_newPt[i] = pt_scale(is_data, Lepton_pt[i], Lepton_eta[i], Lepton_phi[i], Muon_charge[Lepton_muonIdx[i]]);
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
        if not hasattr(ROOT, "CorrectMETMuon"):
            ROOT.gInterpreter.Declare(
                """
                RVecD CorrectMETMuon(RVecF Lepton_pt,
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
                        if ((abs(Lepton_pdgId[i]) != 13))
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
            "Muon_ScaleSmearing",
            f"doMuonScale(Lepton_pt, Lepton_phi, Lepton_eta, Muon_charge, Lepton_pdgId, Lepton_muonIdx, Muon_nTrackerLayers, Lepton_electronIdx, run, {isData}, run_period)"
        )

        df = df.Define(
            "Lepton_newPt",
            "Muon_ScaleSmearing[0]"
        )
        self.columnsToDrop.append("Lepton_newPt")
        if not self.isData:
            df = df.Redefine(
                "Lepton_pt_ScaleUp",
                "Muon_ScaleSmearing[1]"
            )
            df = df.Redefine(
                "Lepton_pt_ScaleDo",
                "Muon_ScaleSmearing[2]"
	        )
            df = df.Redefine(
                "Lepton_pt_ResUp",
                "Muon_ScaleSmearing[3]"
	        )
            df = df.Redefine(
                "Lepton_pt_ResDo",
                "Muon_ScaleSmearing[4]"
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

        df = df.DropColumns("Muon_ScaleSmearing")

        ### Recompute MET with the corrected lepton-pT
        df = df.Define(
            "PuppiMET_MuonScale",
            "CorrectMETMuon(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PuppiMET_pt, PuppiMET_phi)"
        )
        if "24" in self.era or "25" in self.era or "RunIII" in self.era:
            df = df.Define(
                "PFMET_MuonScale",
                "CorrectMETMuon(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, PFMET_pt, PFMET_phi)"
            )
            df = df.Redefine("PFMET_pt", "PFMET_MuonScale[0]")
            df = df.Redefine("PFMET_phi", "PFMET_MuonScale[1]")
            self.columnsToDrop.append("PFMET_MuonScale")
        else:
            df = df.Define(
                "MET_MuonScale",
                "CorrectMETMuon(Lepton_pt, Lepton_newPt, Lepton_phi, Lepton_eta, Lepton_pdgId, MET_pt, MET_phi)"
            )
            df = df.Redefine("MET_pt", "MET_MuonScale[0]")
            df = df.Redefine("MET_phi", "MET_MuonScale[1]")
            self.columnsToDrop.append("MET_MuonScale")

        self.columnsToDrop.append("PuppiMET_MuonScale")
        
        df = df.Redefine("PuppiMET_pt", "PuppiMET_MuonScale[0]")
        df = df.Redefine("PuppiMET_phi", "PuppiMET_MuonScale[1]")

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
