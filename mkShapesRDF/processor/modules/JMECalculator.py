import ROOT
from mkShapesRDF.processor.framework.module import Module


class JMECalculator(Module):
    """
    This module calculates the JES/JER for jets and MET objects and stores the nominal values and the variations (up/down) in the output tree.
    """

    def __init__(
        self,
        JEC_era,
        JER_era,
        jet_object,
        met_collections=["PuppiMET"],
        do_Jets=True,
        do_MET=True,
        do_JER=True,
        do_Unclustered=True,
        store_nominal=True,
        store_variations=True,
    ):
        """
        JMECalculator module

        Parameters
        ----------
        JEC_era : str
            JEC era to use
        JER_era : str
            JER era to use
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
        self.JEC_era = JEC_era
        self.JER_era = JER_era
        self.jet_object = jet_object
        self.met_collections = met_collections
        self.do_Jets = do_Jets
        self.do_MET = do_MET
        self.do_JER = do_JER
        self.do_Unclustered = do_Unclustered
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

        from CMSJMECalculators.jetdatabasecache import JetDatabaseCache

        jecDBCache = JetDatabaseCache("JECDatabase", repository="cms-jet/JECDatabase")
        jrDBCache = JetDatabaseCache("JRDatabase", repository="cms-jet/JRDatabase")

        JEC_era = self.JEC_era
        JER_era = self.JER_era

        print("Version for JEC: ", self.JEC_era)
        
        txtL1JEC = jecDBCache.getPayload(JEC_era, "L1FastJet", self.jet_object)

        txtJECs = []
        txtJECs.append(txtL1JEC)
        txtJECs.append(jecDBCache.getPayload(JEC_era, "L2Relative", self.jet_object))
        txtJECs.append(jecDBCache.getPayload(JEC_era, "L3Absolute", self.jet_object))
        txtJECs.append(jecDBCache.getPayload(JEC_era, "L2L3Residual", self.jet_object))

        txtUnc = jecDBCache.getPayload(
            JEC_era, "UncertaintySources", self.jet_object, ""
        )
        txtPtRes = jrDBCache.getPayload(JER_era, "PtResolution", self.jet_object)
        txtSF = jrDBCache.getPayload(JER_era, "SF", self.jet_object)
        print("Path for SF:", txtSF)

        from CMSJMECalculators import loadJMESystematicsCalculators

        loadJMESystematicsCalculators()


        if self.do_MET:
            for MET in self.met_collections:
                ROOT.gInterpreter.ProcessLine(
                    f"Type1METVariationsCalculator my{MET}" + "VarCalc{}"
                )
                calcMET = getattr(ROOT, f"my{MET}VarCalc")
                calcMET.setUnclusteredEnergyTreshold(15.0)
                # redo JEC, push_back corrector parameters for different levels
                jecParams = getattr(ROOT, "std::vector<JetCorrectorParameters>")()
                for txtJEC in txtJECs:
                    jecParams.push_back(ROOT.JetCorrectorParameters(txtJEC))
                calcMET.setJEC(jecParams)

                jecL1Params = getattr(ROOT, "std::vector<JetCorrectorParameters>")()
                jecL1Params.push_back(ROOT.JetCorrectorParameters(txtL1JEC))
                calcMET.setL1JEC(jecL1Params)
                # calculate JES uncertainties (repeat for all sources)

                with open(txtUnc) as f:
                    lines = f.read().split("\n")
                    sources = [
                        x for x in lines if x.startswith("[") and x.endswith("]")
                    ]
                    sources = [x[1:-1] for x in sources]

                for s in sources:
                    jcp_unc = ROOT.JetCorrectorParameters(txtUnc, s)
                    calcMET.addJESUncertainty(s, jcp_unc)

                if self.do_JER and "Puppi" in MET:
                    # Smear jets, with JER uncertainty
                    calcMET.setSmearing(
                        txtPtRes,
                        txtSF,
                        True,
                        False,
                        -1.0,
                        -1.0,  # decorrelate for different regions
                    )  # use hybrid recipe, matching parameters
                    calcMET.setIsT1SmearedMET(True)

                jesSources = calcMET.available()
                print("DEBUG module")
                skip = 1
                if self.do_JER and "Puppi" in MET:
                    skip += 6 * 2
                # first are JERs, last two are unclustered unc.
                jesSources = jesSources[skip:-2][::2]
                jesSources = list(map(lambda k: str(k)[3:-2], jesSources))
                # jesSources = sorted(jesSources)
                jesSources = list(map(lambda k: "JES" + k, jesSources))
                print(jesSources)

                # list of columns to be passed to myJetVarCal produce
                cols = []

                JetColl = "newJet"

                df = df.Define("newJet_pt", "CleanJet_pt")
                df = df.Define("newJet_eta", "CleanJet_eta")
                df = df.Define("newJet_phi", "CleanJet_phi")
                df = df.Define("newJet_jetIdx", "CleanJet_jetIdx")

                cols.append(f"{JetColl}_pt")
                cols.append(f"{JetColl}_eta")
                cols.append(f"{JetColl}_phi")
                cols.append(f"Take(Jet_mass, {JetColl}_jetIdx)")
                cols.append(f"Take(Jet_rawFactor, {JetColl}_jetIdx)")
                cols.append(f"Take(Jet_area, {JetColl}_jetIdx)")
                cols.append(f"Take(Jet_muonSubtrFactor, {JetColl}_jetIdx)")
                cols.append(f"Take(Jet_neEmEF, {JetColl}_jetIdx)")
                cols.append(f"Take(Jet_chEmEF, {JetColl}_jetIdx)")
                cols.append(f"Take(Jet_jetId, {JetColl}_jetIdx)")

                # rho
                cols.append("Rho_fixedGridRhoFastjetAll")

                cols.append(f"Take(Jet_partonFlavour, {JetColl}_jetIdx)")
                # seed
                cols.append(
                    f"(run<<20) + (luminosityBlock<<10) + event + 1 + int({JetColl}_eta.size()>0 ? {JetColl}_eta[0]/.01 : 0)"
                )

                # gen jet coll
                cols.append("GenJet_pt")
                cols.append("GenJet_eta")
                cols.append("GenJet_phi")
                cols.append("GenJet_mass")

                RawMET = "RawMET" if "Puppi" not in MET else "RawPuppiMET"
                #RawMET = MET
                cols.append(f"{RawMET}_phi")
                cols.append(f"{RawMET}_pt")

                cols.append("MET_MetUnclustEnUpDeltaX")
                cols.append("MET_MetUnclustEnUpDeltaY")

                df = df.Define('EmptyLowPtJet', 'ROOT::RVecF{}')
                #for _ in range(5):
                #    cols.append('EmptyLowPtJet')
                cols.append("CorrT1METJet_rawPt")
                cols.append("CorrT1METJet_eta")
                cols.append("CorrT1METJet_phi")
                cols.append("CorrT1METJet_area")
                cols.append("CorrT1METJet_muonSubtrFactor")
                cols.append("ROOT::RVecF {}")
                cols.append("ROOT::RVecF {}")

                df = df.Define(
                    f"{MET}Vars", f"my{MET}VarCalc.produce({', '.join(cols)})"
                )

                if self.store_nominal:
                    df = df.Define(f"{MET}_pt", f"{MET}Vars.pt(0)")
                    df = df.Define(f"{MET}_phi", f"{MET}Vars.phi(0)")

                if self.store_variations:
                    _sources = []

                    if self.do_JER and "Puppi" not in MET:
                        _sources = [f"JER_{i}" for i in range(6)]
                    _sources += jesSources
                    sources = _sources.copy()
                    METsources = _sources.copy()
                    if self.do_Unclustered:
                        METsources += ["MET"]  # last one is the unclustered variation

                    print("\n")
                    print("MET uncertainties: ")
                    print(METsources)

                    for variable in [MET + "_pt", MET + "_phi"]:
                        for i, source in enumerate(METsources):
                            up = f"{MET}Vars.{variable.split('_')[-1]}({2*i+1})"
                            do = f"{MET}Vars.{variable.split('_')[-1]}({2*i+1+1})"
                            df = df.Vary(
                                variable,
                                "ROOT::RVecD{" + up + ", " + do + "}",
                                ["up", "do"],
                                source,
                            )
                df = df.DropColumns(f"{MET}Vars")

        if self.do_Jets:
            ROOT.gInterpreter.ProcessLine("JetVariationsCalculator myJetVarCalc{}")
            calc = getattr(ROOT, "myJetVarCalc")
            # redo JEC, push_back corrector parameters for different levels
            jecParams = getattr(ROOT, "std::vector<JetCorrectorParameters>")()
            for txtJEC in txtJECs:
                jecParams.push_back(ROOT.JetCorrectorParameters(txtJEC))
            calc.setJEC(jecParams)
            # calculate JES uncertainties (repeat for all sources)

            with open(txtUnc) as f:
                lines = f.read().split("\n")
                sources = [x for x in lines if x.startswith("[") and x.endswith("]")]
                sources = [x[1:-1] for x in sources]

            for s in sources:
                jcp_unc = ROOT.JetCorrectorParameters(txtUnc, s)
                calc.addJESUncertainty(s, jcp_unc)

            if self.do_JER:
                # Smear jets, with JER uncertainty
                calc.setSmearing(
                    txtPtRes,
                    txtSF,
                    True,
                    False,
                    -1.0,
                    -1.0,  # decorrelate for different regions
                )  # use hybrid recipe, matching parameters
            jesSources = calc.available()
            skip = 1
            if self.do_JER:
                skip += 6 * 2
            jesSources = jesSources[skip:][::2]
            jesSources = list(map(lambda k: str(k)[3:-2], jesSources))
            jesSources = list(map(lambda k: "JES" + k, jesSources))

            # list of columns to be passed to myJetVarCal produce
            cols = []

            # nre reco jet coll
            JetColl = "newJet"

            df = df.Define("newJet_pt", "CleanJet_pt")
            df = df.Define("newJet_eta", "CleanJet_eta")
            df = df.Define("newJet_phi", "CleanJet_phi")
            df = df.Define("newJet_jetIdx", "CleanJet_jetIdx")

            cols.append(f"{JetColl}_pt")
            cols.append(f"{JetColl}_eta")
            cols.append(f"{JetColl}_phi")
            cols.append("CleanJet_mass")
            cols.append(f"Take(Jet_rawFactor, {JetColl}_jetIdx)")
            cols.append(f"Take(Jet_area, {JetColl}_jetIdx)")
            cols.append(f"Take(Jet_jetId, {JetColl}_jetIdx)")

            # rho
            cols.append("Rho_fixedGridRhoFastjetAll")

            cols.append(f"Take(Jet_partonFlavour, {JetColl}_jetIdx)")

            # seed
            cols.append(
                f"(run<<20) + (luminosityBlock<<10) + event + 1 + int({JetColl}_eta.size()>0 ? {JetColl}_eta[0]/.01 : 0)"
            )

            # gen jet coll
            cols.append("GenJet_pt")
            cols.append("GenJet_eta")
            cols.append("GenJet_phi")
            cols.append("GenJet_mass")

            df = df.Define("jetVars", f'myJetVarCalc.produce({", ".join(cols)})')

            if self.store_nominal:
                # ROOT.gInterpreter.Declare(
                #     """
                #     using namespace ROOT;
                #     RVecF propagateVector(RVecI jetIdx, RVecF jetVar, RVecF jetVar_raw) {
                #         RVecF out(jetVar_raw);
                #         for (int i = 0; i < jetIdx.size(); i++) {
                #             out[jetIdx[i]] = jetVar[i];
                #         }
                #         return out;
                #     }
                #     """
                # )
                df = df.Define("CleanJet_pt", "jetVars.pt(0)")
                df = df.Define("CleanJet_mass", "jetVars.mass(0)")

                df = df.Define(
                    "CleanJet_sorting",
                    "ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(CleanJet_pt))",
                )

                df = df.Define("CleanJet_pt", "Take( CleanJet_pt, CleanJet_sorting)")
                df = df.Define("CleanJet_eta", "Take( CleanJet_eta, CleanJet_sorting)")
                df = df.Define("CleanJet_phi", "Take( CleanJet_phi, CleanJet_sorting)")
                df = df.Define("CleanJet_mass", "Take( CleanJet_mass, CleanJet_sorting)")
                df = df.Define("CleanJet_jetIdx", "Take( CleanJet_jetIdx, CleanJet_sorting)")

                # stores the jet mass after JEC/JER and resorts it based on the new CleanJet_pt
                # df = df.Define(
                #     "Jet_mass",
                #     "propagateVector(CleanJet_jetIdx, Take(jetVars.mass(0), CleanJet_sorting), Jet_mass_raw)",
                # )

            else:
                df = df.Define(
                    "CleanJet_sorting",
                    "Range(CleanJet_pt.size())",
                )

            if self.store_variations:
                _sources = []
                if self.do_JER:
                    _sources = [f"JER_{i}" for i in range(6)]
                _sources += jesSources
                sources = _sources.copy()

                print("\n")
                print("JES uncertainties: ")
                print(sources)

                for i, source in enumerate(sources):
                    variations_pt = []
                    variations_jetIdx = []
                    variations_mass = []
                    variations_phi = []
                    variations_eta = []
                    for j, tag in enumerate(["up", "down"]):
                        variation_pt = f"jetVars.pt({2*i+1+j})"
                        variation_mass = f"jetVars.mass({2*i+1+j})"
                        df = df.Define(
                            f"tmp_CleanJet_pt__JES_{source}_{tag}",
                            variation_pt,
                        )
                        df = df.Define(
                            f"tmp_CleanJet_pt__JES_{source}_{tag}_sorting",
                            f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(tmp_CleanJet_pt__JES_{source}_{tag}))",
                        )
                        variations_pt.append(
                            f"Take(tmp_CleanJet_pt__JES_{source}_{tag}, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)"
                        )

                        df = df.Define(
                            f"CleanJet_cleanJetIdx_preJES_{source}_{tag}",
                            f"tmp_CleanJet_pt__JES_{source}_{tag}_sorting",
                        )

                        variations_jetIdx.append(
                            f"Take({JetColl}_jetIdx, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)",
                        )

                        df = df.Define(
                            f"tmp_CleanJet_mass__JES_{source}_{tag}",
                            f"Take({variation_mass}, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)",
                        )
                        variations_mass.append(f"tmp_CleanJet_mass__JES_{source}_{tag}")

                        variations_phi.append(
                            f"Take({JetColl}_phi, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)"
                        )
                        variations_eta.append(
                            f"Take({JetColl}_eta, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)"
                        )

                    tags = ["up", "do"]
                    df = df.Vary(
                        "CleanJet_pt",
                        "ROOT::RVec<ROOT::RVecF>{"
                        + variations_pt[0]
                        + ", "
                        + variations_pt[1]
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        "CleanJet_jetIdx",
                        "ROOT::RVec<ROOT::RVecI>{" + variations_jetIdx[0]
                        # + "CleanJet_jetIdx"
                        + ", " + variations_jetIdx[1]
                        # + "CleanJet_jetIdx"
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        "CleanJet_mass",
                        "ROOT::RVec<ROOT::RVecF>{" + variations_mass[0]
                        # + "CleanJet_mass"
                        + ", " + variations_mass[1]
                        # + "CleanJet_mass"
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        "CleanJet_phi",
                        "ROOT::RVec<ROOT::RVecF>{" + variations_phi[0]
                        # + "CleanJet_phi"
                        + ", " + variations_phi[1]
                        # + "CleanJet_phi"
                        + "}",
                        tags,
                        source,
                    )

                    df = df.Vary(
                        "CleanJet_eta",
                        "ROOT::RVec<ROOT::RVecF>{" + variations_eta[0]
                        # + "CleanJet_eta"
                        + ", " + variations_eta[1]
                        # + "CleanJet_eta"
                        + "}",
                        tags,
                        source,
                    )

                    df = df.DropColumns("tmp_*")

            df = df.DropColumns("jetVars")
            df = df.DropColumns("CleanJet_sorting")
        return df
