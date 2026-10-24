from mkShapesRDF.processor.framework.module import Module


class FatJetSel(Module):
    def __init__(self,
            jetId=2,
            minPt=200.,
            maxEta=2.4,
            max_tau21=None,
            mass_range=None,
            pt_max=None,
            DeltaRlep=0.8,
            DeltaRjet=0.8):
        super().__init__("FatJetSel")
        self.jetId = jetId
        self.minPt = minPt
        self.maxEta = maxEta
        self.max_tau21 = max_tau21
        self.mass_range = mass_range
        self.pt_max = pt_max
        self.DeltaRlep = DeltaRlep
        self.DeltaRjet = DeltaRjet

    def runModule(self, df, values):

        selection = f"CleanFatJet_pt >= {self.minPt} && abs(CleanFatJet_eta) <= {self.maxEta} && ((CleanFatJet_jetId & {self.jetId}) == {self.jetId})"

        if self.pt_max is not None:
            selection += f" && CleanFatJet_pt <= {self.pt_max}"

        if self.mass_range is not None:
            selection += f" && CleanFatJet_msoftdrop >= {self.mass_range[0]} && CleanFatJet_msoftdrop <= {self.mass_range[1]}"

        if self.max_tau21 is not None:
            selection += f" && CleanFatJet_tau1 > 0 && CleanFatJet_tau2 <= {self.max_tau21} * CleanFatJet_tau1"

        df = df.Define("CleanFatJetMask", selection)

        values.append([
            df.Define("nFatBeforeSel", "int(CleanFatJet_pt.size())").Sum("nFatBeforeSel"),
            "Original size of CleanFatJet",
        ])

        branches = [str(col) for col in df.GetColumnNames() if str(col).startswith("CleanFatJet_") and "RVec" in str(df.GetColumnType(str(col)))]

        for branch in branches:
            df = df.Redefine(branch, f"{branch}[CleanFatJetMask]")

        df = df.Redefine("nCleanFatJet", "int(CleanFatJet_pt.size())")
        df = df.DropColumns("CleanFatJetMask")

        values.append([
            df.Define("nFatAfterSel", "int(CleanFatJet_pt.size())").Sum("nFatAfterSel"),
            "Final size of CleanFatJet",
        ])

        # Update overlap masks after the additional selection.
        columns = set(str(col) for col in df.GetColumnNames())

        if "CleanJet_notFatJet" in columns:
            df = df.Redefine("CleanJet_notFatJet", f"mkShapesAK8::separated(CleanJet_eta, CleanJet_phi, CleanFatJet_eta, CleanFatJet_phi, {self.DeltaRjet})")

        if "Lepton_notFatJet" in columns:
            df = df.Redefine("Lepton_notFatJet", f"mkShapesAK8::separated(Lepton_eta, Lepton_phi, CleanFatJet_eta, CleanFatJet_phi, {self.DeltaRlep})")

        for kind, branch in (("Muon", "muonIdx"), ("Electron", "electronIdx")):
            if f"{kind}NotFat_Idx" in columns and f"Lepton_{branch}" in columns:
                df = df.Redefine(f"{kind}NotFat_Idx", f"Lepton_{branch}[Lepton_notFatJet && (Lepton_{branch} >= 0)]")

        return df

