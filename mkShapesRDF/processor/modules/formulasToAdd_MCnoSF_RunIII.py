from mkShapesRDF.processor.framework.module import Module

from mkShapesRDF.processor.data.LeptonSel_cfg import LepFilter_dict, ElectronWP, MuonWP


class formulasToAdd_MCnoSF_RunIII(Module):
    def __init__(self, era):
        super().__init__("formulasToAdd_MCnoSF_RunIII")
        self.era = era

    def runModule(self, df, values):
        df = df.Define(
            "METFilter_Common",
            "Flag_goodVertices * \
            Flag_globalSuperTightHalo2016Filter * \
            Flag_EcalDeadCellTriggerPrimitiveFilter * \
            Flag_BadPFMuonFilter * \
            Flag_BadPFMuonDzFilter * \
            Flag_hfNoisyHitsFilter * \
            Flag_ecalBadCalibFilter",
        )

        df = df.Define("METFilter_DATA", "METFilter_Common * Flag_eeBadScFilter")

        useGenW = "genWeight" in df.GetColumnNames()

        if useGenW:
            df = df.Define("XSWeight", "baseW * genWeight")
        else:
            df = df.Define("XSWeight", "baseW")

        df = df.Define("_2lepOk", "Lepton_pt.size() > 1")
        df = df.Define("_3lepOk", "Lepton_pt.size() > 2")
        df = df.Define("_4lepOk", "Lepton_pt.size() > 3")


        muWPlist = [wp for wp in MuonWP[self.era]["TightObjWP"]]
        eleWPlist = [wp for wp in ElectronWP[self.era]["TightObjWP"]]

        for eleWP in eleWPlist:
            for muWP in muWPlist:

                df = df.Define(
                    "LepCut2l__ele_" + eleWP + "__mu_" + muWP,
                    "_2lepOk ? (Lepton_isTightElectron_"
                    + eleWP
                    + "[0]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[0]>0.5) && (Lepton_isTightElectron_"
                    + eleWP
                    + "[1]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[1]>0.5) : false",
                )

                df = df.Define(
                    "LepCut3l__ele_" + eleWP + "__mu_" + muWP,
                    "_3lepOk ? (Lepton_isTightElectron_"
                    + eleWP
                    + "[0]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[0]>0.5) && (Lepton_isTightElectron_"
                    + eleWP
                    + "[1]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[1]>0.5) && (Lepton_isTightElectron_"
                    + eleWP
                    + "[2]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[2]>0.5) : false",
                )

                df = df.Define(
                    "LepCut4l__ele_" + eleWP + "__mu_" + muWP,
                    "_4lepOk ? (Lepton_isTightElectron_"
                    + eleWP
                    + "[0]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[0]>0.5) && (Lepton_isTightElectron_"
                    + eleWP
                    + "[1]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[1]>0.5) && (Lepton_isTightElectron_"
                    + eleWP
                    + "[2]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[2]>0.5) && (Lepton_isTightElectron_"
                    + eleWP
                    + "[3]>0.5 || Lepton_isTightMuon_"
                    + muWP
                    + "[3]>0.5) : false",
                )


        return df
