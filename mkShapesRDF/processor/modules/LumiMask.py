from mkShapesRDF.processor.framework.module import Module
import json
import os

class LumiMask(Module):
    def __init__(self, basePath, inPath):
        super().__init__("LumiMask")
        self.base_path = basePath
        self.jsonFile = self.base_path + inPath

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
