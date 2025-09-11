import json
from mkShapesRDF.processor.framework.module import Module


class FakeSel(Module):
    def __init__(self):
        super().__init__("FakeSel")

    def runModule(self, df, values):

        if "MET_pt" not in df.GetColumnNames():
            df = df.Define("MET_pt", "PuppiMET_pt")
        
        df = df.Filter("((MET_pt < 20 || PuppiMET_pt < 20) && mtw1 < 20)")

        return df

