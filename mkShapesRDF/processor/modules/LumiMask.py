from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.Lumi_cfg import LumiCfg
import json
import os

class LumiMask(Module):
    def __init__(self, year):
        super().__init__("LumiMask")
        self.base_path = ""
        if "processor" in os.path.dirname(os.path.dirname(__file__)):
            self.base_path = (
                os.path.dirname(os.path.dirname(__file__)).split("processor")[0]
            )

        self.jsonFile = self.base_path + LumiCfg[year]

    def runModule(self, df, values):

        with open(self.jsonFile) as file:
            d = json.load(file)

        filters = []  # will do an or of all the filters
        for run, lumiRanges in d.items():
            subFilters = []  # will do an or of all the subfilters
            for lumiRange in lumiRanges:
                subFilters.append(
                    f"( luminosityBlock >= {lumiRange[0]} && luminosityBlock <= {lumiRange[1]} )"
                )
            subFiltersMerged = " || ".join(subFilters)
            filters.append(f"( run == {run} && ( {subFiltersMerged} ) )")

        total_filter = " || ".join(filters)
        # print(filter)

        df = df.Filter(total_filter)

        return df
