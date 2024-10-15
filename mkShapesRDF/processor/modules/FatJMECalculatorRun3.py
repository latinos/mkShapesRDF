import ROOT
from mkShapesRDF.processor.framework.module import Module


class FatJMECalculator(Module):
    """
    This module calculates the JES/JER for fatjet objects and stores the nominal values and the variations (up/down) in the output tree.
    """

    def __init__(
        self,
        jsonFile,
        JEC_era,
        JER_era,
        jes_unc,
	jsonFileSmearingTool,
        jet_object,
        jsonFileSubjet,
        JEC_era_subjet,
        subjet_object,
        do_JER=True,
        store_nominal=True,
        store_variations=True,
    ):
        """
        JMECalculator module

        Parameters
        ----------
        jsonFile : str
            path to FatJet json file for JEC and JER
        JEC_era : str
            FatJet JEC era to use
        JER_era : str
            FatJet JER era to use
        JER_era : list
            list of JER uncertainties
        jsonFileSmearingTool : str
            path to json file to smearing tool
        jet_object : str
            FatJet algorithm to consider (e.g. ``AK8PFPuppi``)
        jsonFileSubjet: str
            path to SubJet json file for JEC and JER
        JEC_era_subjet: str 
            SubJet JEC era to use
        subjet_object: str
            SubJet algorithm to consider (e.g. ``AK4PFPuppi``)
        do_JER : bool, optional, default: ``True``
            Whether to calculate JER
        store_nominal : bool, optional, default: ``True``
            Whether to store the nominal values (corrected or smeared)
        store_variations : bool, optional
            Whether to store the variations (up/down) for JES/JER
        """
        super().__init__("JMECalculator")
        self.json = jsonFile
        self.JEC_era = JEC_era
        self.JER_era = JER_era
        self.jsonSubJet = jsonFileSubjet
        self.JEC_era_subjet = JEC_era_subjet
        self.jsonFileSmearingTool = jsonFileSmearingTool
        self.jet_object = jet_object
        self.jes_unc = jes_unc
        self.subjet_object = subjet_object
        self.do_JER = do_JER
        self.store_nominal = store_nominal
        self.store_variations = store_variations

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
        jerTag 		= ""
        jes_unc     = self.jes_unc
        jsonFileSmearingTool = self.jsonFileSmearingTool
        jecLevel    = "L1L2L3Res"
        jsonFileSubjet =  self.jsonSubJet
        jetAlgoSubjet = self.subjet_object 
        jecTagSubjet =  self.JEC_era_subjet
        jecLevelSubjet = jecLevel
        ROOT.gROOT.ProcessLine("std::vector<string> jesUnc{}")
        jesUnc = getattr(ROOT, "jesUnc")
        for jes_var in jes_unc:
            jesUnc.push_back(jes_var)
        addHEM      = "false"
        smearingTool= "JERSmear"
        maxDR       = 0.2
        maxDPT      = 3
        
        if self.do_JER:
            jerTag          = self.JER_era

        ROOT.gROOT.ProcessLine(f"FatJetVariationsCalculator myFatJetVariationsCalculator = FatJetVariationsCalculator::create(\"{jsonFile}\", \"{jetAlgo}\", \"{jecTag}\", \"{jecLevel}\", {jesUnc}, {addHEM}, \"{jerTag}\", \"{jsonFileSmearingTool}\", \"{smearingTool}\", false, true, {maxDR}, {maxDPT}, \"{jsonFileSubjet}\", \"{jetAlgoSubjet}\", \"{jecTagSubjet}\", \"{jecLevelSubjet}\");")
        calc = getattr(ROOT, "myFatJetVariationsCalculator")
        jesSources = calc.available()
        jesSources = calc.available()[1:][::2]
        jesSources = [str(source).replace('up', '') for source in jesSources]
        print(jesSources)
        
        # list of columns to be passed to myJetVarCal produce
        cols = []

        # nre reco jet coll
        JetColl = "newFatJet"

        df = df.Define("newFatJet_pt", "CleanFatJet_pt")
        df = df.Define("newFatJet_eta", "CleanFatJet_eta")
        df = df.Define("newFatJet_phi", "CleanFatJet_phi")
        df = df.Define("newFatJet_jetIdx", "CleanFatJet_jetIdx")

        cols.append(f"{JetColl}_pt")
        cols.append(f"{JetColl}_eta")
        cols.append(f"{JetColl}_phi")
        cols.append("CleanFatJet_mass")
        cols.append(f"Take(FatJet_rawFactor, {JetColl}_jetIdx)")
        cols.append(f"Take(FatJet_area, {JetColl}_jetIdx)")
        cols.append(f"Take(FatJet_msoftdrop, {JetColl}_jetIdx)")
        cols.append(f"Take(FatJet_subJetIdx1, {JetColl}_jetIdx)")
        cols.append(f"Take(FatJet_subJetIdx2, {JetColl}_jetIdx)")

        cols.append("SubJet_pt")
        cols.append("SubJet_eta")
        cols.append("SubJet_phi")
        cols.append("SubJet_mass")
        cols.append("SubJet_rawFactor")

        
        cols.append("FatJet_jetId")

        # rho
        cols.append("Rho_fixedGridRhoFastjetAll") #in Run2 is fixedGridRhoFastjetAll

        cols.append(f"Take(FatJet_genJetAK8Idx, {JetColl}_jetIdx)")
        cols.append("event")
        # gen jet coll
        cols.append("GenJetAK8_pt")
        cols.append("GenJetAK8_eta")
        cols.append("GenJetAK8_phi")
        cols.append("GenJetAK8_mass")

        df = df.Define("jetVars", f'myFatJetVariationsCalculator.produce({", ".join(cols)})')
        if self.store_nominal:
            df = df.Define("CleanFatJet_pt", "jetVars.pt(0)")
            df = df.Define("CleanFatJet_mass", "jetVars.mass(0)")
            df = df.Define("CleanFatJet_msoftdrop", "jetVars.msoftdrop(0)")
            df = df.Define(
                "CleanFatJet_sorting",
                "ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(CleanFatJet_pt))",
            )

            df = df.Define("CleanFatJet_pt", "Take( CleanFatJet_pt, CleanFatJet_sorting)")
            df = df.Define("CleanFatJet_eta", "Take( CleanFatJet_eta, CleanFatJet_sorting)")
            df = df.Define("CleanFatJet_phi", "Take( CleanFatJet_phi, CleanFatJet_sorting)")
            df = df.Define("CleanFatJet_mass", "Take( CleanFatJet_mass, CleanFatJet_sorting)")
            df = df.Define("CleanFatJet_msoftdrop", "Take( CleanFatJet_msoftdrop, CleanFatJet_sorting)")
            df = df.Define("CleanFatJet_jetIdx", "Take( CleanFatJet_jetIdx, CleanFatJet_sorting)")

        else:
            df = df.Define(
                "CleanFatJet_sorting",
                "Range(CleanFatJet_pt.size())",
            )

        if self.store_variations:
            for i, source in enumerate(jesSources):
                variations_pt = []
                variations_jetIdx = []
                variations_mass = []
                variations_msoftdrop = []
                variations_phi = []
                variations_eta = []
                for j, tag in enumerate(["up", "down"]):
                    variation_pt = f"jetVars.pt({2*i+1+j})"
                    variation_mass = f"jetVars.mass({2*i+1+j})"
                    variation_msoftdrop = f"jetVars.msoftdrop({2*i+1+j})"
                    
                    df = df.Define(
                        f"tmp_CleanFatJet_pt__JES_{source}_{tag}",
                        variation_pt,
                    )
                    df = df.Define(
                        f"tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting",
                        f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(tmp_CleanFatJet_pt__JES_{source}_{tag}))",
                    )
                    variations_pt.append(
                        f"Take(tmp_CleanFatJet_pt__JES_{source}_{tag}, tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting)"
                    )

                    df = df.Define(
                        f"CleanFatJet_cleanFatJetIdx_preJES_{source}_{tag}",
                        f"tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting",
                    )

                    variations_jetIdx.append(
                        f"Take({JetColl}_jetIdx, tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting)",
                    )

                    df = df.Define(
                        f"tmp_CleanFatJet_mass__JES_{source}_{tag}",
                        f"Take({variation_mass}, tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting)",
                    )
                    variations_mass.append(f"tmp_CleanFatJet_mass__JES_{source}_{tag}")

                    df = df.Define(
                        f"tmp_CleanFatJet_msoftdrop__JES_{source}_{tag}",
                        f"Take({variation_msoftdrop}, tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting)",
                    )
                    variations_msoftdrop.append(f"tmp_CleanFatJet_msoftdrop__JES_{source}_{tag}")

                    variations_phi.append(
                        f"Take({JetColl}_phi, tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting)"
                    )
                    variations_eta.append(
                        f"Take({JetColl}_eta, tmp_CleanFatJet_pt__JES_{source}_{tag}_sorting)"
                    )



                tags = ["up", "do"]
                df = df.Vary(
                    "CleanFatJet_pt",
                    "ROOT::RVec<ROOT::RVecF>{"
                    + variations_pt[0]
                    + ", "
                    + variations_pt[1]
                    + "}",
                    tags,
                    source,
                )

                df = df.Vary(
                    "CleanFatJet_jetIdx",
                    "ROOT::RVec<ROOT::RVecI>{" + variations_jetIdx[0]
                    + ", " + variations_jetIdx[1]
                    + "}",
                    tags,
                    source,
                )

                df = df.Vary(
                    "CleanFatJet_mass",
                    "ROOT::RVec<ROOT::RVecF>{" + variations_mass[0]
                    + ", " + variations_mass[1]
                    + "}",
                    tags,
                    source,
                )

                df = df.Vary(
                    "CleanFatJet_phi",
                    "ROOT::RVec<ROOT::RVecF>{" + variations_phi[0]
                    + ", " + variations_phi[1]
                    + "}",
                    tags,
                    source,
                )

                df = df.Vary(
                    "CleanFatJet_eta",
                    "ROOT::RVec<ROOT::RVecF>{" + variations_eta[0]
                    + ", " + variations_eta[1]
                    + "}",
                    tags,
                    source,
                )

                df = df.Vary(
                    "CleanFatJet_msoftdrop",
                    "ROOT::RVec<ROOT::RVecF>{" + variations_msoftdrop[0]
                    + ", " + variations_msoftdrop[1]
                    + "}",
                    tags,
                    source,
                )

                df = df.DropColumns("tmp_*")

            df = df.DropColumns("jetVars*")
            df = df.DropColumns("CleanFatJet_sorting")
        return df