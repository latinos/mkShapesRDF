from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import correctionlib
import os
import ROOT
correctionlib.register_pyroot_binding()


class JetSel(Module):
    def __init__(self, jetId, puJetId, minPt, maxEta, UL2016fix=False):
        super().__init__("JetSel")
        self.jetId = jetId
        self.puJetId = puJetId
        self.minPt = minPt
        self.maxEta = maxEta
        self.UL2016fix = UL2016fix

    def runModule(self, df, values):
        # jetId = 2
        # wp = "loose"
        # minPt = 15.0
        # maxEta = 4.7
        # UL2016fix = False

        if self.UL2016fix:
            wp_dict = {
                "loose": "(1<<0)",
                "medium": "(1<<1)",
                "tight": "(1<<2)",
            }
        else:
            wp_dict = {
                "loose": "(1<<2)",
                "medium": "(1<<1)",
                "tight": "(1<<0)",
            }

        df = df.Define(
            "CleanJetMask",
            "(CleanJet_pt <= 50 \
                && (Take(Jet_puId, CleanJet_jetIdx) \
                && ROOT::RVecI (CleanJet_pt.size(), {})) \
                ) || (CleanJet_pt > 50)".format(
                wp_dict[self.puJetId]
            ),
        )

        df = df.Define(
            "CleanJetMask",
            f"CleanJetMask && CleanJet_pt >= {self.minPt} && CleanJet_eta <= {self.maxEta} && Take(Jet_jetId, CleanJet_jetIdx) >= {self.jetId}",
        )

        values.append(
            [
                df.Define("test", "CleanJet_pt.size()").Sum("test"),
                "Original size of CleanJet",
            ]
        )

        branches = ["jetIdx", "pt", "eta", "phi", "mass"]
        for prop in branches:
            df = df.Redefine(f"CleanJet_{prop}", f"CleanJet_{prop}[CleanJetMask]")

        df = df.DropColumns("CleanJetMask")

        values.append(
            [
                df.Define("test", "CleanJet_pt.size()").Sum("test"),
                "Final size of CleanJet",
            ]
        )

        return df
