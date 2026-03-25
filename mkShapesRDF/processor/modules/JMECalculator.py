import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import os
import re

class JMECalculator(Module):
    """
    This module calculates the JES/JER for jets and MET objects and stores the nominal values and the variations (up/down) in the output tree.
    """

    def __init__(
        self,
        jet_object,
        jes_unc,
        year="",
        met_collections=["PuppiMET"],
        do_Jets=True,
        do_MET=True,
        do_JER=True,
        do_XYMET=True,
        store_nominal=True,
        store_variations=True,
        isMC = True,
        sampleName = "",
    ):
        """
        JMECalculator module

        Parameters
        ----------
        jsonFile : str
            path to json file for JEC and JER
        JEC_era : str
            JEC era to use
        JER_era : str
            JER era to use
        jsonFileSmearingTool : str
            path to json file to smearing tool
        jet_object : str
            Jet Collection to use (e.g. ``CleanJet``)
        met_collections : list, optional, default: ``["PuppiMET", "MET"]``
            MET collections to use
        do_Jets : bool, optional, default: ``True``
            Whether to calculate JES/JER for jets
        do_MET : bool, optional, default: ``True``
            Whether to calculate JES/JER for MET objects
        do_JER : bool, optional, default: ``True``
            Whether to calculate JER
        store_nominal : bool, optional, default: ``True``
            Whether to store the nominal values (corrected or smeared)
        store_variations : bool, optional
            Whether to store the variations (up/down) for JES/JER
        """
        super().__init__("JMECalculator")
        self.jet_object = jet_object        
        self.jes_unc = jes_unc
        self.year = year
        self.met_collections = met_collections
        self.do_Jets = do_Jets
        self.do_MET = do_MET
        self.do_JER = do_JER
        self.do_XYMET = do_XYMET
        self.store_nominal = store_nominal
        self.store_variations = store_variations
        self.isMC = isMC 
        self.sampleName = sampleName
        # The isMC flag is used to denote MC samples and is used as a condition to choose the correct JEC key and to ensure that do_JER is set to True only for MC

        # This might be redundant, but I think is useful to have a cross-setting to False for these flags
        if not self.isMC:
            self.do_JER = False
            self.store_variations = False

        self.json = ""
        self.JEC_era = ""
        self.JER_era = ""
        self.jsonFileSmearingTool = ""

        self.isXYCorrJson = ""
        self.isXYCorrEra  = ""
        
        if year in ["Full2024v15", "Full2025v15"]:
            self.do_XYMET = False
        
        if self.year in JetMakerCfg.keys():
            self.json = JetMakerCfg[self.year]["jet_jerc"]
            if self.isMC:
                self.JEC_era = JetMakerCfg[self.year]["JEC"]
            else:
                self.JEC_era = JetMakerCfg[self.year]["JEC_data"]
            self.JER_era = JetMakerCfg[self.year]["JER"]
            self.jsonFileSmearingTool = JetMakerCfg[self.year]["jer_smear"]
            if self.do_XYMET:
                self.isXYCorrJson = JetMakerCfg[self.year]["met_xy_json"]
                self.isXYCorrEra = JetMakerCfg[self.year]["met_xy_era"]

    def runModule(self, df, values):
        ROOT.gInterpreter.Declare(
            """
            using namespace ROOT;

            RVecU revertIndicesMask(RVecU sortedIndices, uint size){
                auto tmp = ROOT::VecOps::Range(size);
                RVecU r {};

                for (uint i = 0; i < tmp.size(); i++){
                    for (uint j = 0; j < sortedIndices.size(); j++){
                        if (tmp[i] == sortedIndices[j]){
                            r.push_back(j);
                        }
                    }
                }
                return r;

            }
        """
        )
        
        from CMSJMECalculators import loadJMESystematicsCalculators

        loadJMESystematicsCalculators()
        
        jsonFile 	= self.json
        jetAlgo 	= self.jet_object
        jecTag  	= self.JEC_era
        jes_unc     = self.jes_unc
        year        = self.year
        jerTag 		= ""
        jsonFileSmearingTool = self.jsonFileSmearingTool
        jecLevel    = "L1L2L3Res"
        L1JecTag    = ""
        ROOT.gROOT.ProcessLine("std::vector<string> jesUnc{}")
        jesUnc = getattr(ROOT, "jesUnc")
        for jes_var in jes_unc:
            if "YEAR" in jes_var:
                print(jes_var.replace("YEAR", self.year.split("Full")[1].split("v")[0]))
                jesUnc.push_back(jes_var.replace("YEAR", self.year.split("Full")[1].split("v")[0]))
            else:
                print(jes_var)
                jesUnc.push_back(jes_var)
        addHEM      = "false"
        smearingTool= "JERSmear"
        maxDR       = 0.2
        maxDPT      = 3
        
        # For 2023 pre-BPix, we have two sets of corrections based on the computing version.
        # These conditions ensure that the correct set of corrections is applied.
        if any(v in self.sampleName for v in ["v1", "v2", "v3"]) and not self.isMC and year == 'Full2023v12':
            jecTag = self.JEC_era[0]
        elif "v4" in self.sampleName and not self.isMC and year == 'Full2023v12':
            jecTag = self.JEC_era[1]

        # The same logic applies for 2022 post-EE data, where the condition is based on the run number.
        if "22EE" in jsonFile and not self.isMC:
            if 'Run2022E' in self.sampleName:
                jecTag = self.JEC_era[0]
            elif 'Run2022F' in self.sampleName:
                jecTag = self.JEC_era[1]
            elif 'Run2022G' in self.sampleName:
                jecTag = self.JEC_era[2]

        print(f"Final JEC tag: {jecTag}")

        if self.do_Jets:
            if self.do_JER:
                jerTag = self.JER_era
                ROOT.gROOT.ProcessLine(f"JetVariationsCalculator myJetVariationsCalculator = JetVariationsCalculator::create(\"{jsonFile}\", \"{jetAlgo}\", \"{jecTag}\", \"{jecLevel}\", {jesUnc}, {addHEM}, \"{jerTag}\", \"{jsonFileSmearingTool}\", \"{smearingTool}\", false, true, {maxDR}, {maxDPT});")
            else:
                ROOT.gROOT.ProcessLine(f"JetVariationsCalculator myJetVariationsCalculator = JetVariationsCalculator::create(\"{jsonFile}\", \"{jetAlgo}\", \"{jecTag}\", \"{jecLevel}\", std::vector<std::string>{{}}, {addHEM}, \"\", \"\", \"\", false, true, {maxDR}, {maxDPT});")
            calc = getattr(ROOT, "myJetVariationsCalculator")
            jesSources = calc.available()
            jesSources = calc.available()[1:][::2]
            jesSources = [str(source).replace('up', '') for source in jesSources]
            print(jesSources)
            
            # list of columns to be passed to myJetVarCal produce
            cols = []

            # nre reco jet coll
            JetColl = "CorrectedJet"

            cols.append("Jet_pt")
            cols.append("Jet_eta")
            cols.append("Jet_phi")
            cols.append("Jet_mass")
            cols.append("Jet_rawFactor")
            cols.append("Jet_area")
            cols.append("Jet_jetId")

            # rho
            cols.append("Rho_fixedGridRhoFastjetAll")

            if self.isMC: 
                cols.append("Jet_genJetIdx")
                cols.append("Jet_partonFlavour")
                # seed
                cols.append(
                    f"(run<<20) + (luminosityBlock<<10) + event + 1 + int(Jet_eta.size()>0 ? Jet_eta[0]/.01 : 0)"
                )
                cols.append("-1.0")    
                # gen jet coll
                cols.append("GenJet_pt")
                cols.append("GenJet_eta")
                cols.append("GenJet_phi")
                cols.append("GenJet_mass")
            else:
                # Basically, these variables are nedded for the smearing and don't exist for data, so we set those to empty vectors
                cols.append("ROOT::RVecI{}") # Jet_genJetIdx
                cols.append("ROOT::RVecI{}") # Jet_partonFlavour
                cols.append("0")  # seed, I don't think that setting this to zero points to no calculation, in anycase, this is used only for smearing, which is not done for data
                cols.append("run")
                cols.append("ROOT::RVecF{}") # GenJet_pt
                cols.append("ROOT::RVecF{}") # GenJet_eta
                cols.append("ROOT::RVecF{}") # GenJet_phi
                cols.append("ROOT::RVecF{}") # GenJet_mass

            df = df.Define("jetVars", f'myJetVariationsCalculator.produce({", ".join(cols)})')

            if self.store_nominal:
                df = df.Define(f"{JetColl}_pt", "jetVars.pt(0)")
                df = df.Define(f"{JetColl}_mass", "jetVars.mass(0)")
                    
                df = df.Define(f"{JetColl}_sorting", f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort({JetColl}_pt))")
                df = df.Define(f"{JetColl}_pt", f"Take({JetColl}_pt, {JetColl}_sorting)")
                df = df.Define(f"{JetColl}_eta", f"Take(Jet_eta, {JetColl}_sorting)")
                df = df.Define(f"{JetColl}_phi", f"Take(Jet_phi, {JetColl}_sorting)")
                df = df.Define(f"{JetColl}_mass", f"Take({JetColl}_mass, {JetColl}_sorting)")
                df = df.Define(f"{JetColl}_jetIdx", "ROOT::VecOps::Range(nJet)")       
            else:
                df = df.Define(f"{JetColl}_sorting", f"Range({JetColl}_pt.size())")

            if self.store_variations:
                for i, source in enumerate(jesSources):
                    variations_pt = []
                    variations_jetIdx = []
                    variations_mass = []
                    variations_phi = []
                    variations_eta = []
                    for j, tag in enumerate(["up", "down"]):
                        variation_pt = f"jetVars.pt({2*i+1+j})"
                        variation_mass = f"jetVars.mass({2*i+1+j})"
                        
                        df = df.Define(
                            f"tmp_{JetColl}_pt__JES_{source}_{tag}",
                            variation_pt,
                        )
                        df = df.Define(
                            f"tmp_{JetColl}_pt__JES_{source}_{tag}_sorting",
                            f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(tmp_{JetColl}_pt__JES_{source}_{tag}))",
                        )
                        variations_pt.append(
                            f"Take(tmp_{JetColl}_pt__JES_{source}_{tag}, tmp_{JetColl}_pt__JES_{source}_{tag}_sorting)"
                        )

                        df = df.Define(
                            f"{JetColl}_JetIdx_preJES_{source}_{tag}",
                            f"tmp_{JetColl}_pt__JES_{source}_{tag}_sorting",
                        )

                        variations_jetIdx.append(
                            f"Take({JetColl}_jetIdx, tmp_{JetColl}_pt__JES_{source}_{tag}_sorting)",
                        )

                        df = df.Define(
                            f"tmp_{JetColl}_mass__JES_{source}_{tag}",
                            f"Take({variation_mass}, tmp_{JetColl}_pt__JES_{source}_{tag}_sorting)",
                        )
                        variations_mass.append(f"tmp_{JetColl}_mass__JES_{source}_{tag}")

                        variations_phi.append(
                            f"Take({JetColl }_phi, tmp_{JetColl}_pt__JES_{source}_{tag}_sorting)"
                        )
                        variations_eta.append(
                            f"Take({JetColl}_eta, tmp_{JetColl}_pt__JES_{source}_{tag}_sorting)"
                        )

                    tags = ["up", "do"]
                    df = df.Vary(
                        f"{JetColl}_pt",
                        "ROOT::RVec<ROOT::RVecF>{"
                        + variations_pt[0]
                        + ", "
                        + variations_pt[1]
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        f"{JetColl}_jetIdx",
                        "ROOT::RVec<ROOT::RVecI>{" + variations_jetIdx[0]
                        + ", " + variations_jetIdx[1]
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        f"{JetColl}_mass",
                        "ROOT::RVec<ROOT::RVecF>{" + variations_mass[0]
                        + ", " + variations_mass[1]
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        f"{JetColl}_phi",
                        "ROOT::RVec<ROOT::RVecF>{" + variations_phi[0]
                        + ", " + variations_phi[1]
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        f"{JetColl}_eta",
                        "ROOT::RVec<ROOT::RVecF>{" + variations_eta[0]
                        + ", " + variations_eta[1]
                        + "}",
                        tags,
                        source,
                    )

                    df = df.DropColumns("tmp_*")

            df = df.Define(f"n{JetColl}", f"{JetColl}_pt.size()")
            df = df.DropColumns("jetVars*")
            df = df.DropColumns(f"{JetColl}_sorting")
            df = df.DropColumns("*preJES*")
        
        if self.do_MET:
            L1JecTag        = "L1FastJet"
            unclEnThr       = 15.
            emEnFracThr     = 0.9
            isT1smearedMET  = "false"

            isXYCorrected = "false"
            met_xy_json = ""
            met_xy_era = ""
            if self.do_XYMET :
                isXYCorrected = "true"
                met_xy_json = self.isXYCorrJson
                met_xy_era = self.isXYCorrEra

            is_mc = "false"
            if self.isMC:
                is_mc = "true"
            
            for MET in self.met_collections:
                if self.do_JER and "Puppi" in MET:
                    jerTag          = self.JER_era
                    isT1smearedMET  = "true"
                    ROOT.gROOT.ProcessLine(f"Type1METVariationsCalculator my{MET}VarCalc = Type1METVariationsCalculator::create(\"{jsonFile}\", \"{jetAlgo}\", \"{jecTag}\", \"{jecLevel}\", \"{L1JecTag}\", {unclEnThr}, {emEnFracThr}, {jesUnc}, {addHEM}, {isT1smearedMET}, {isXYCorrected}, \"{met_xy_json}\", \"{met_xy_era}\", {is_mc}, \"{jerTag}\", \"{jsonFileSmearingTool}\", \"{smearingTool}\", false, true, {maxDR}, {maxDPT});")
                else:
                    ROOT.gROOT.ProcessLine(f"Type1METVariationsCalculator my{MET}VarCalc = Type1METVariationsCalculator::create(\"{jsonFile}\", \"{jetAlgo}\", \"{jecTag}\", \"{jecLevel}\", \"{L1JecTag}\", {unclEnThr}, {emEnFracThr}, std::vector<std::string>{{}}, {addHEM}, {isT1smearedMET}, {isXYCorrected}, \"{met_xy_json}\", \"{met_xy_era}\", {is_mc}, \"\", \"\", \"\", false, true, {maxDR}, {maxDPT});")
                calcMET = getattr(ROOT, f"my{MET}VarCalc")
                METSources = calcMET.available()
                METSources = calcMET.available()[1:][::2]
                METSources = [str(source).replace('up', '') for source in METSources]
                
                # list of columns to be passed to myJetVarCal produce
                cols = []

                cols.append("Jet_pt")
                cols.append("Jet_eta")
                cols.append("Jet_phi")
                cols.append("Jet_mass")
                cols.append("Jet_rawFactor")
                cols.append("Jet_area")
                cols.append("Jet_muonSubtrFactor")
                cols.append("Jet_neEmEF")
                cols.append("Jet_chEmEF")
                cols.append("Jet_jetId")
    
                # rho
                cols.append("Rho_fixedGridRhoFastjetAll")

                if self.isMC: 
                    cols.append("Jet_genJetIdx")
                    cols.append("Jet_partonFlavour")
                    # seed
                    cols.append(
                        f"(run<<20) + (luminosityBlock<<10) + event + 1 + int(Jet_eta.size()>0 ? Jet_eta[0]/.01 : 0)"
                    )
                    cols.append("-1.0")    
                    # gen jet coll
                    cols.append("GenJet_pt")
                    cols.append("GenJet_eta")
                    cols.append("GenJet_phi")
                    cols.append("GenJet_mass")
                else:
                    # Basically, these variables are nedded for the smearing and don't exist for data, so we set those to empty vectors
                    cols.append("ROOT::RVecI{}") # Jet_genJetIdx
                    cols.append("ROOT::RVecI{}") # Jet_partonFlavour
                    cols.append("0")  # seed, I don't think that setting this to zero points to no calculation, in anycase, this is used only for smearing, which is not done for data
                    cols.append("run")
                    cols.append("ROOT::RVecF{}") # GenJet_pt
                    cols.append("ROOT::RVecF{}") # GenJet_eta
                    cols.append("ROOT::RVecF{}") # GenJet_phi
                    cols.append("ROOT::RVecF{}") # GenJet_mass

                if "v15" in self.year:
                    RawMET = "RawPFMET" if "Puppi" not in MET else "RawPuppiMET"
                else:
                    RawMET = "RawMET" if "Puppi" not in MET else "RawPuppiMET"
                cols.append(f"{RawMET}_phi")
                cols.append(f"{RawMET}_pt")

                df = df.Define('EmptyLowPtJet', 'ROOT::RVecF{}')
                cols.append("CorrT1METJet_rawPt")
                cols.append("CorrT1METJet_eta")
                cols.append("CorrT1METJet_phi")
                cols.append("CorrT1METJet_area")
                cols.append("CorrT1METJet_muonSubtrFactor")
                cols.append("ROOT::RVecF {}")
                cols.append("ROOT::RVecF {}")

                ## Always use the differences defined as the following, for all Run3 eras.
                if "Puppi" not in MET:
                    if "v15" in self.year:
                        df = df.Define(
                            "PFMET_MetUnclustEnUpDeltaX",
                            "PFMET_pt * std::cos(PFMET_phi) - PFMET_ptUnclusteredUp * std::cos(PFMET_phiUnclusteredUp)"
                        )
                        df = df.Define(
                            "PFMET_MetUnclustEnUpDeltaY",
                            "PFMET_pt * std::sin(PFMET_phi) - PFMET_ptUnclusteredUp * std::cos(PFMET_phiUnclusteredUp)"
                        )
                        cols.append("PFMET_MetUnclustEnUpDeltaX")
                        cols.append("PFMET_MetUnclustEnUpDeltaY")
                    else:
                        cols.append("MET_MetUnclustEnUpDeltaX")
                        cols.append("MET_MetUnclustEnUpDeltaY")
                else :     
                    df = df.Define(
                        "PuppiMET_MetUnclustEnUpDeltaX",
                        "PuppiMET_pt * std::cos(PuppiMET_phi) - PuppiMET_ptUnclusteredUp * std::cos(PuppiMET_phiUnclusteredUp)"
                    )
                    df = df.Define(
                        "PuppiMET_MetUnclustEnUpDeltaY",
                        "PuppiMET_pt * std::sin(PuppiMET_phi) - PuppiMET_ptUnclusteredUp * std::sin(PuppiMET_phiUnclusteredUp)"
                    )
                    cols.append("PuppiMET_MetUnclustEnUpDeltaX")
                    cols.append("PuppiMET_MetUnclustEnUpDeltaY")

                cols.append("PV_npvsGood")                    
                                       
                df = df.Define(
                    f"{MET}Vars", f"my{MET}VarCalc.produce({', '.join(cols)})"
                )
                
                if self.store_nominal:
                    df = df.Define(f"{MET}_pt", f"Jet_pt.size() > 0 ? {MET}Vars.pt(0) : {RawMET}_pt")
                    df = df.Define(f"{MET}_phi", f"Jet_pt.size() > 0 ? {MET}Vars.phi(0) : {RawMET}_phi")
                
                if self.store_variations:
                    for variable in [MET + "_pt", MET + "_phi"]:
                        for i, source in enumerate(METSources):
                            up = f"{MET}Vars.{variable.split('_')[-1]}({2*i+1})"
                            do = f"{MET}Vars.{variable.split('_')[-1]}({2*i+1+1})"
                            df = df.Vary(
                                variable,
                                "ROOT::RVecD{" + up + ", " + do + "}",
                                ["up", "do"],
                                source,
                            )
                df = df.DropColumns(f"{MET}Vars*")
                print("MET variables run succesfully!")

        return df
