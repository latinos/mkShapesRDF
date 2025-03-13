from mkShapesRDF.processor.framework.module import Module

from mkShapesRDF.processor.data.LeptonSel_cfg import LepFilter_dict, ElectronWP, MuonWP


class formulasToAdd_MC_RunIII(Module):
    def __init__(self, era):
        super().__init__("formulasToAdd_MC_RunIII")
        self.era = era

    def runModule(self, df, values):

        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Run_3_2022_and_2023_data_and_MC
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

        df = df.Define(
            "SFweight2l",
            "_2lepOk ? puWeight * \
            (HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || \
            HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || \
            HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || \
            HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || \
            HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || \
            HLT_IsoMu24 || \
            HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || \
            HLT_Ele30_WPTight_Gsf) * \
            TriggerSFWeight_2l * \
            Lepton_RecoSF[0] * \
            Lepton_RecoSF[1]  \
            : 0.0",
        )

        df = df.Define(
            "SFweight3l",
            "_3lepOk ? puWeight * \
            (HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || \
            HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || \
            HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || \
            HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || \
            HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || \
            HLT_IsoMu24 || \
            HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || \
            HLT_Ele30_WPTight_Gsf) * \
            TriggerSFWeight_3l * \
            Lepton_RecoSF[0] * \
            Lepton_RecoSF[1] * \
            Lepton_RecoSF[2]   \
            : 0.0",
        )

        df = df.Define(
            "SFweight4l",
            "_4lepOk ? puWeight * \
            (HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || \
            HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || \
            HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || \
            HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || \
            HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || \
            HLT_IsoMu24 || \
            HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || \
            HLT_Ele30_WPTight_Gsf) * \
            TriggerSFWeight_4l * \
            Lepton_RecoSF[0] * \
            Lepton_RecoSF[1] * \
            Lepton_RecoSF[2] * \
            Lepton_RecoSF[3]   \
            : 0.0",
        )

        muWPlist = [wp for wp in MuonWP[self.era]["TightObjWP"]]
        eleWPlist = [wp for wp in ElectronWP[self.era]["TightObjWP"]]

        for eleWP in eleWPlist:
            for muWP in muWPlist:
                df = df.Define(
                    "LepSF2l__ele_" + eleWP + "__mu_" + muWP,
                    "_2lepOk ? Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF"
                    + "[0]*\
                    Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF"
                    + "[1]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF"
                    + "[0]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF"
                    + "[1] \
                    : 0.0",
                )

                df = df.Define(
                    "LepSF3l__ele_" + eleWP + "__mu_" + muWP,
                    "_3lepOk ? Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[0]*\
                    Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[1]*\
                    Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[2]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[0]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[1]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[2]\
                    : 0.0",
                )

                df = df.Define(
                    "LepSF4l__ele_" + eleWP + "__mu_" + muWP,
                    "_4lepOk ? Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[0]*\
                    Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[1]*\
                    Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[2]*\
                    Lepton_tightElectron_"
                    + eleWP
                    + "_IdIsoSF[3]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[0]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[1]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[2]*\
                    Lepton_tightMuon_"
                    + muWP
                    + "_IdIsoSF[3] \
                    : 0.0",
                )

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

        for eleWP in eleWPlist:
            df = df.Define(
                "LepSF2l__ele_" + eleWP + "__Up",
                "_2lepOk ? \
                ((abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[0])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 13)) * \
                ((abs(Lepton_pdgId[1]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[1])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 13)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF2l__ele_" + eleWP + "__Down",
                "_2lepOk ? \
                ((abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[0])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 13)) * \
                ((abs(Lepton_pdgId[1]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[1])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 13)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF3l__ele_" + eleWP + "__Up",
                "_3lepOk ? \
                ((abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[0])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 13)) * \
                ((abs(Lepton_pdgId[1]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[1])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 13)) * \
                ((abs(Lepton_pdgId[2]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[2])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 13)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF3l__ele_" + eleWP + "__Down",
                "_3lepOk ? \
                ((abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[0])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 13)) * \
                ((abs(Lepton_pdgId[1]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[1])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 13)) * \
                ((abs(Lepton_pdgId[2]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[2])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 13)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF4l__ele_" + eleWP + "__Up",
                "_4lepOk ? \
                ((abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[0])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 13)) * \
                ((abs(Lepton_pdgId[1]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[1])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 13)) * \
                ((abs(Lepton_pdgId[2]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[2])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 13))*\
                ((abs(Lepton_pdgId[3]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Up[3])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[3])+\
                (abs(Lepton_pdgId[3]) == 13)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF4l__ele_" + eleWP + "__Down",
                "_4lepOk ? \
                ((abs(Lepton_pdgId[0]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[0])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 13)) * \
                ((abs(Lepton_pdgId[1]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[1])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 13)) * \
                ((abs(Lepton_pdgId[2]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[2])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 13))*\
                ((abs(Lepton_pdgId[3]) == 11)*(Lepton_tightElectron_"
                + eleWP
                + "_TotSF_Down[3])/(Lepton_tightElectron_"
                + eleWP
                + "_TotSF[3])+\
                (abs(Lepton_pdgId[3]) == 13)) \
                : 0.0",
            )

        for muWP in muWPlist:
            df = df.Define(
                "LepSF2l__mu_" + muWP + "__Up",
                "_2lepOk ? \
                ((abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[0])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 11)) * \
                ((abs(Lepton_pdgId[1]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[1])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 11)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF2l__mu_" + muWP + "__Down",
                "_2lepOk ? \
                ((abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[0])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 11)) * \
                ((abs(Lepton_pdgId[1]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[1])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 11)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF3l__mu_" + muWP + "__Up",
                "_3lepOk ? \
                ((abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[0])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 11)) * \
                ((abs(Lepton_pdgId[1]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[1])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 11))*\
                ((abs(Lepton_pdgId[2]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[2])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 11)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF3l__mu_" + muWP + "__Down",
                "_3lepOk ? \
                ((abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[0])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 11)) * \
                ((abs(Lepton_pdgId[1]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[1])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 11))* \
                ((abs(Lepton_pdgId[2]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[2])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 11)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF4l__mu_" + muWP + "__Up",
                "_4lepOk ? \
                ((abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[0])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 11)) * \
                ((abs(Lepton_pdgId[1]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[1])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 11)) * \
                ((abs(Lepton_pdgId[2]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[2])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 11)) * \
                ((abs(Lepton_pdgId[3]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Up[3])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[3])+\
                (abs(Lepton_pdgId[3]) == 11)) \
                : 0.0",
            )

            df = df.Define(
                "LepSF4l__mu_" + muWP + "__Down",
                "_4lepOk ? \
                ((abs(Lepton_pdgId[0]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[0])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[0])+\
                (abs(Lepton_pdgId[0]) == 11)) * \
                ((abs(Lepton_pdgId[1]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[1])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[1])+\
                (abs(Lepton_pdgId[1]) == 11)) * \
                ((abs(Lepton_pdgId[2]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[2])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[2])+\
                (abs(Lepton_pdgId[2]) == 11)) * \
                ((abs(Lepton_pdgId[3]) == 13)*(Lepton_tightMuon_"
                + muWP
                + "_TotSF_Down[3])/(Lepton_tightMuon_"
                + muWP
                + "_TotSF[3])+\
                (abs(Lepton_pdgId[3]) == 11)) \
                : 0.0",
            )

        df = df.Define(
            "GenLepMatch2l",
            "_2lepOk ? Lepton_genmatched[0] * Lepton_genmatched[1] : 0.0",
        )

        df = df.Define(
            "GenLepMatch3l",
            "_3lepOk ? Lepton_genmatched[0] * Lepton_genmatched[1] * Lepton_genmatched[2] : 0.0",
        )

        df = df.Define(
            "GenLepMatch4l",
            "_4lepOk ? Lepton_genmatched[0] * Lepton_genmatched[1] * Lepton_genmatched[2] * Lepton_genmatched[3]: 0.0",
        )

        return df
