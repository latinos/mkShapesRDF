from mkShapesRDF.lib.utils import getFrameworkPath

####################### Jet Veto/JEC/JER/JES CFG ##################################

frameworkPath = getFrameworkPath() + "mkShapesRDF"

JetMakerCfg = {
    'Full2022v12': {
        "JEC": "Summer22_22Sep2023_V4_MC",
        "JEC_data": "Summer22_22Sep2023_RunCD_V4_DATA",
        "JER": "Summer22_22Sep2023_JRV2_MC",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jet": {
            "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/jetvetomaps.json.gz",
            "vetokey": "Summer22_23Sep2023_RunCD_V1",
            "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/jet_jerc.json.gz",
        },
        "fat_jet": {
            "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/fatJet_jerc.json.gz",
            "subjet_algorithm": "AK4PFPuppi",
             "fatjetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/jetid.json.gz",
                "tight": "AK8PUPPI_Tight",
                "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
       },
        "met_xy_json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05/met_xyCorrections_2022_2022.json.gz",
        "met_xy_era": "2022",
        },
    },

    'Full2022EEv12': {
        "JEC": "Summer22EE_22Sep2023_V4_MC",
        "JEC_data": "Summer22EE_22Sep2023_V4_DATA",
        "JER": "Summer22EE_22Sep2023_JRV2_MC",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jet": {
            "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/jetvetomaps.json.gz",
            "vetokey": "Summer22EE_23Sep2023_RunEFG_V1",
            "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/jet_jerc.json.gz",
        },
        "fat_jet": {
            "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/fatJet_jerc.json.gz",
            "subjet_algorithm": "AK4PFPuppi",
             "fatjetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/jetid.json.gz",
                "tight": "AK8PUPPI_Tight",
                "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
       },
        "met_xy_json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05/met_xyCorrections_2022_2022EE.json.gz",
        "met_xy_era": "2022EE",
        },
    },

    'Full2023v12': {
        "JEC": "Summer23Prompt23_V4_MC",
        "JEC_data": "Summer23Prompt23_V4_DATA",
        "JER": "Summer23Prompt23_RunCv1234_JRV3_MC",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jet": {
            "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-07-15/jetvetomaps.json.gz",
            "vetokey": "Summer23Prompt23_RunC_V1",
            "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-07-15/jet_jerc.json.gz",
        },
        "fat_jet": {
            "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-07-15/fatJet_jerc.json.gz",
            "subjet_algorithm": "AK4PFPuppi",
             "fatjetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-07-15/jetid.json.gz",
                "tight": "AK8PUPPI_Tight",
                "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
       },
        "met_xy_json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2026-07-15/met_xyCorrections_2023_2023.json.gz",
        "met_xy_era": "2023",
        },
    },

    'Full2023BPixv12': {
        "JEC": "Summer23BPixPrompt23_V4_MC",
        "JEC_data": "Summer23BPixPrompt23_V4_DATA",
        "JER": "Summer23BPixPrompt23_RunD_JRV3_MC",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jet": {
            "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-07-15/jetvetomaps.json.gz",
            "vetokey": "Summer23BPixPrompt23_RunD_V1",
            "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-07-15/jet_jerc.json.gz",
        },
        "fat_jet": {
            "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-07-15/fatJet_jerc.json.gz",
            "subjet_algorithm": "AK4PFPuppi",
             "fatjetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-07-15/jetid.json.gz",
                "tight": "AK8PUPPI_Tight",
                "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
       },
        "met_xy_json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2026-07-15/met_xyCorrections_2023_2023BPix.json.gz",
        "met_xy_era": "2023BPix",
        },
    },

    'Full2024v15': {
        "JEC": "Summer24Prompt24_V5_MC",
        "JEC_data": "Summer24Prompt24_V5_DATA",
        "JER": "Summer24Prompt24_JRV2_MC",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jet": {
            "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jetvetomaps.json.gz",
            "vetokey": "Summer24Prompt24_RunBCDEFGHI_V1",
            "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jet_jerc.json.gz",
            "jetId": {
                "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                "tight": "AK4PUPPI_Tight",
                "tightleptonveto": "AK4PUPPI_TightLeptonVeto",
            },
        },
        "fat_jet": {
            "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/fatJet_jerc.json.gz",
            "subjet_algorithm": "AK4PFPuppi",
            "fatjetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                "tight": "AK8PUPPI_Tight",
                "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
            },
        },
    },

    'Full2025v15': {
        "JEC": "Summer24Prompt25_V3_MC",
        "JEC_data": "Summer24Prompt25_V3_DATA",
        "JER": "Summer24Prompt25_JRV2_MC",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jet": {
            "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jetvetomaps.json.gz",
            "vetokey": "Summer24Prompt25_RunCDEFG_V1",
            "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jet_jerc.json.gz",
            "jetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                "tight": "AK4PUPPI_Tight",
                "tightleptonveto": "AK4PUPPI_TightLeptonVeto",
            },
        },
        "fat_jet": {
            "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/fatJet_jerc.json.gz",
            "subjet_algorithm": "AK4PFPuppi",
            "fatjetId": {
                "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                "tight": "AK8PUPPI_Tight",
                "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
            },
        },
    },

    'FullRunIIIv15': {
        "1": {
            "year": "2024",
            "JEC": "Summer24Prompt24_V5_MC",
            "JEC_data": "Summer24Prompt24_V5_DATA",
            "JER": "Summer24Prompt24_JRV2_MC",
            "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
            "jet": {
                "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jetvetomaps.json.gz",
                "vetokey": "Summer24Prompt24_RunBCDEFGHI_V1",
                "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jet_jerc.json.gz",
                "jetId": {
                    "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                    "tight": "AK4PUPPI_Tight",
                    "tightleptonveto": "AK4PUPPI_TightLeptonVeto",
                },
            },
            "fat_jet": {
                "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/fatJet_jerc.json.gz",
                "subjet_algorithm": "AK4PFPuppi",
                "fatjetId": {
                    "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                    "tight": "AK8PUPPI_Tight",
                    "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
                },
            },
        },

        "2": {
            "year": "2025",
            "JEC": "Summer24Prompt25_V3_MC",
            "JEC_data": "Summer24Prompt25_V3_DATA",
            "JER": "Summer24Prompt25_JRV2_MC",
            "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
            "jet": {
                "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jetvetomaps.json.gz",
                "vetokey": "Summer24Prompt25_RunCDEFG_V1",
                "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jet_jerc.json.gz",
                "jetId": {
                    "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                    "tight": "AK4PUPPI_Tight",
                    "tightleptonveto": "AK4PUPPI_TightLeptonVeto",
                },
            },
            "fat_jet": {
                "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/fatJet_jerc.json.gz",
                "subjet_algorithm": "AK4PFPuppi",
                "fatjetId": {
                    "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-25Prompt-Summer24-NanoAODv15/2026-07-16/jetid.json.gz",
                    "tight": "AK8PUPPI_Tight",
                    "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
                },
            },
        },

        "3": {
            "year": "2026",
            "JEC": "Summer24Prompt26_V1_MC",
            "JEC_data": "Summer24Prompt26_V1_DATA",
            "JER": "Summer24Prompt26_RunBD_JRV1_MC",
            "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
            "jet": {
                "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jetvetomaps.json.gz",
                "vetokey": "Summer24Prompt26_RunBCD_V1",
                "jet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jet_jerc.json.gz",
                "jetId": {
                    "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jetid.json.gz",
                    "tight": "AK4PUPPI_Tight",
                    "tightleptonveto": "AK4PUPPI_TightLeptonVeto",
                },
            },
            "fat_jet": {
                "fatjet_jerc": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/fatJet_jerc.json.gz",
                "subjet_algorithm": "AK4PFPuppi",
                "fatjetId": {
                    "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-26Prompt-Summer24-NanoAODv15/2026-07-15/jetid.json.gz",
                    "tight": "AK8PUPPI_Tight",
                    "tightleptonveto": "AK8PUPPI_TightLeptonVeto",
                },
            },
        },
    },
}

