from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *


class L1TightSelection(Module):
    def __init__(self, era):
        super().__init__("L1TightSelection")

        self.era = era
        self.ElectronWP = ElectronWP
        self.MuonWP = MuonWP

    def runModule(self, df, values):

        first = True
        lepton1_selection = ""

        for wp in self.ElectronWP[self.era]["TightObjWP"]:
            if first:
                lepton1_selection += f"Lepton_isTightElectron_{wp}[0]>0.5"
                first = False
            else:
                lepton1_selection += f" || Lepton_isTightElectron_{wp}[0]>0.5"

        for wp in self.MuonWP[self.era]["TightObjWP"]:
            if first:
                lepton1_selection += f"Lepton_isTightMuon_{wp}[0]>0.5"
                first = False
            else:
                lepton1_selection += f" || Lepton_isTightMuon_{wp}[0]>0.5"

        df = df.Filter(f"({lepton1_selection})")

        # Remove temporary corrected AK4/AK8 jet collections
        df = df.DropColumns("nCorrectedJet").DropColumns("CorrectedJet*").DropColumns("CleanJet_correctedjetIdx")
        df = df.DropColumns("nCorrectedFatJet").DropColumns("CorrectedFatJet*").DropColumns("CleanFatJet_correctedjetIdx")

        return df
