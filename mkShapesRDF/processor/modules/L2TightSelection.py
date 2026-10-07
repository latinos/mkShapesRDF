import json
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *

class L2TightSelection(Module):
    def __init__(self, era):
        super().__init__("L2TightSelection")

        self.era = era
        self.LepFilter = LepFilter_dict
        self.ElectronWP = ElectronWP
        self.MuonWP = MuonWP
        
    def runModule(self, df, values):

        # Reject short retained collections before evaluating either tight slot.
        df = df.Filter("Lepton_pt.size() >= 2")

        first = True
        
        lepton1_selection = ""
        lepton2_selection = ""
        for wp in self.ElectronWP[self.era]["TightObjWP"]:
            if first:
                lepton1_selection = lepton1_selection + f"Lepton_isTightElectron_{wp}[0]>0.5"
                lepton2_selection = lepton2_selection + f"Lepton_isTightElectron_{wp}[1]>0.5"
                first = False
            else:
                lepton1_selection = lepton1_selection + f" || Lepton_isTightElectron_{wp}[0]>0.5"
                lepton2_selection =	lepton2_selection + f" || Lepton_isTightElectron_{wp}[1]>0.5"

        for wp in self.MuonWP[self.era]["TightObjWP"]:
            lepton1_selection =	lepton1_selection + f" || Lepton_isTightMuon_{wp}[0]>0.5"
            lepton2_selection = lepton2_selection + f" || Lepton_isTightMuon_{wp}[1]>0.5"

        l2tight_selection = f"({lepton1_selection}) && ({lepton2_selection})"
        
        df = df.Filter(f"{l2tight_selection}")
        
        return df

