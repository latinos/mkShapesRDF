import json
from mkShapesRDF.processor.framework.module import Module


class FakeSelMC(Module):
    def __init__(self):
        super().__init__("FakeSelMC")

    def runModule(self, df, values):

        df = df.Filter("((MET_pt < 20 || PuppiMET_pt < 20) && mtw1 < 20)")

        return df

