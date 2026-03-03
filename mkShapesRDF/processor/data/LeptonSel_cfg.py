LepFilter_dict = {
    "Loose": "isLoose",
    "Veto": "isVeto",
    "WgStar": "isWgs",
    "isLoose": "FakeObjWP",
    "isVeto": "VetoObjWP",
    "isWgs": "WgStarObjWP",
}

ElectronWP = {

    "Full2018v9": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "True": ["False"],
                },
            },
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            # ----- mvaFall17V2Iso
            "mvaFall17V2Iso_WP90": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaFall17V2Iso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  { 
                    '1-1' : '/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz'
                } ,
                'wpSF':  {
                    '1-1' : 'data/scale_factor/Full2018v9/egammaEffi_TightHWW_2018.txt',
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2018v9/mvaFall17V2Iso_WP90/',
            }
        },
    },
    "Full2022v12": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "True": ["False"],
                },
            },
        },
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            "testrecipes":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt>10",
                        #"ROOT::VecOps::abs(Electron_eta) < 2.5",
                        #"Electron_mvaIso_WP80",
                        #"Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/latest/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "wp80iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/latest/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022v12/wp80iso/',
            },
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022v12/wp90iso/',
            },
            "mvaWinter22V2Iso_WP90": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "passingMVA90_HWW", 'data/scale_factor/Full2022v12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022v12/mvaWinter22V2Iso_WP90/',
            },
            "cutBased_LooseID_tthMVA_Run3": {
                 "cuts": {
                     "ROOT::RVecB (Electron_pt.size(), true)": [
                         "ROOT::VecOps::abs(Electron_eta) < 2.5",
                         "Electron_cutBased >= 2",
                         "Electron_tthMVA > 0.90",
                         "Electron_convVeto",
                     ],
                     "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                         "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                         "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                     ],
                     "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                         "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                         "ROOT::VecOps::abs(Electron_dz) <  0.2",
                     ],
                 },
                 'tkSF':  {
                     '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz"]
                 } ,
                 'wpSF':  {
                     '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2022v12/electron.json'],
                 } ,
                 'fakeW' : 'data/fake_prompt_rates/Full2022v12/cutBased_LooseID_tthMVA/',
            },
            "cutBased_LooseID_tthMVA_HWW": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                    "Electron_pt <= 20.0": [
                        "Electron_tthMVA > 0.35",
                    ],
                    "Electron_pt > 20.0": [
                        "Electron_tthMVA > 0.90",
                    ],
                },
                'tkSF':  {
                     '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz"]
                 },
                'wpSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "passingTTHMVA_HWW", 'data/scale_factor/Full2022v12/electron.json'], # To be added
                },
                #'fakeW' : 'data/fake_prompt_rates/',
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
    },
    "Full2022EEv12": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "True": ["False"],
                },
            },
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            "testrecipes":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt>10",
                        #"ROOT::VecOps::abs(Electron_eta) < 2.5",
                        #"Electron_mvaIso_WP80",
                        #"Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/latest/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "wp80iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/latest/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/wp80iso/',
            },
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/wp90iso/',
            },
            "mvaWinter22V2Iso_WP90": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "passingMVA90_HWW", 'data/scale_factor/Full2022EEv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/mvaWinter22V2Iso_WP90/',
            },
            "cutBased_LooseID_tthMVA_Run3": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_tthMVA > 0.90",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2022EEv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/cutBased_LooseID_tthMVA/',
            },
            "cutBased_LooseID_tthMVA_HWW": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                    "Electron_pt <= 20.0": [
                        "Electron_tthMVA > 0.35",
                    ],
                    "Electron_pt > 20.0": [
                        "Electron_tthMVA > 0.90",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz"]
                },
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "passingTTHMVA_HWW", 'data/scale_factor/Full2022EEv12/electron.json'], # To be added
                },
                #'fakeW' : 'data/fake_prompt_rates/',
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
    },
    "Full2023v12": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "True": ["False"],
                },
            },
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            "testrecipes":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt>10",
                        #"ROOT::VecOps::abs(Electron_eta) < 2.5",
                        #"Electron_mvaIso_WP80",
                        #"Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/latest/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "wp80iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/latest/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023v12/wp80iso/',
            },
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023v12/wp90iso/',
            },
            "mvaWinter22V2Iso_WP90": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "passingMVA90_HWW", 'data/scale_factor/Full2023v12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023v12/mvaWinter22V2Iso_WP90/',
            },
            "cutBased_LooseID_tthMVA_Run3": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_tthMVA > 0.90",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2023v12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023v12/cutBased_LooseID_tthMVA/',
            },
            "cutBased_LooseID_tthMVA_HWW": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                    "Electron_pt <= 20.0": [
                        "Electron_tthMVA > 0.35",
                    ],
                    "Electron_pt > 20.0": [
                        "Electron_tthMVA > 0.90",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz"]
                },
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "passingTTHMVA_HWW", 'data/scale_factor/Full2023v12/electron.json'], # To be added
                },
                #'fakeW' : 'data/fake_prompt_rates/',
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
    },
    "Full2023BPixv12": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "True": ["False"],
                },
            },
        },
        # ------------                                                                                                                                                  
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    # Barrel                                                                                                                                            
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap                                                                                                                                            
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            "testrecipes":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt>10",
                        #"ROOT::VecOps::abs(Electron_eta) < 2.5",
                        #"Electron_mvaIso_WP80",
                        #"Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/latest/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "wp80iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/latest/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/wp80iso/',
            },
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/wp90iso/',
            },
            "mvaWinter22V2Iso_WP90": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "passingMVA90_HWW", 'data/scale_factor/Full2023BPixv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/mvaWinter22V2Iso_WP90/',
            },
            "cutBased_LooseID_tthMVA_Run3": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_tthMVA > 0.90",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2023BPixv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/cutBased_LooseID_tthMVA/',
            },
            "cutBased_LooseID_tthMVA_HWW": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                    "Electron_pt <= 20.0": [
                        "Electron_tthMVA > 0.35",
                    ],
                    "Electron_pt > 20.0": [
                        "Electron_tthMVA > 0.90",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz"]
                },
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "passingTTHMVA_HWW", 'data/scale_factor/Full2023BPixv12/electron.json'], # To be added
                },
                #'fakeW' : 'data/fake_prompt_rates/',
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
    },
    "Full2024v15": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "True": ["False"],
                },
            },
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                } ,
                #'fakeW' : 'data/fake_prompt_rates/',
            },
            "testrecipes":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt>10",
                        #"ROOT::VecOps::abs(Electron_eta) < 2.5",
                        #"Electron_mvaIso_WP80",
                        #"Electron_convVeto",
                    ],
                },
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "wp80iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/electron.json.gz'],
                } ,
            },
            "mvaWinter22V2Iso_WP90": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                },
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2024PromptCDE+Re-recoFGHI", "Electron-ID-SF", "NUM_passingMVA90_HWW_DEN_wp90iso", 'data/scale_factor/Full2024v15/electron.json'],
                },
                #'fakeW' : 'data/fake_prompt_rates/',  
            },
            "cutBased_LooseID_tthMVA_Run3": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_promptMVA > 0.90",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  { 
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                },
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2024PromptCDE+Re-recoFGHI", "Electron-ID-SF", "NUM_passingTTHMVA_DEN_LooseID", 'data/scale_factor/Full2024v15/electron.json'],
                },
                #'fakeW' : 'data/fake_prompt_rates/',  
            },
            "cutBased_LooseID_tthMVA_HWW": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                    "Electron_pt <= 20.0": [
                        "Electron_promptMVA > 0.35",
                    ],
                    "Electron_pt > 20.0": [
                        "Electron_promptMVA > 0.90",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                },
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                },
                'tthMvaSF':  {
                    '1-1' : ["2024PromptCDE+Re-recoFGHI", "Electron-ID-SF", "passingTTHMVA_HWW", 'data/scale_factor/Full2024v15/electron.json'],
                },
                #'fakeW' : 'data/fake_prompt_rates/',
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electronSS_EtDependent.json.gz",
    },
    ###Full2025v15 is just a copy of Full2024v15. to be modified once 2025 selections available.
    "Full2025v15": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "True": ["False"],
                },
            },
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 3",
                        "Electron_convVeto == 1",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta)  <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    # EndCap
                    "ROOT::VecOps::abs(Electron_eta)  > 1.479": [
                        "Electron_sieie  < 0.03",
                        "ROOT::VecOps::abs(Electron_eInvMinusPInv) < 0.014",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.2",
                    ],
                },
            },
        },
        "TightObjWP": {
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },# using 2024 SFs while processing only data. To be updated when processing MC
                'tkSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                } , # using 2024 SFs while processing only data. To be updated when processing MC
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                } , # using 2024 SFs while processing only data. To be updated when processing MC
                #'fakeW' : 'data/fake_prompt_rates/',
            },
            "testrecipes":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt>10",
                        #"ROOT::VecOps::abs(Electron_eta) < 2.5",
                        #"Electron_mvaIso_WP80",
                        #"Electron_convVeto",
                    ],
                },
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "wp80iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                } , # using 2024 SFs while processing only data. To be updated when processing MC
            },
            "mvaWinter22V2Iso_WP90": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                        "Electron_pfRelIso03_all < 0.06",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "wp90iso", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                'tthMvaSF':  {
                    '1-1' : ["2024PromptCDE+Re-recoFGHI", "Electron-ID-SF", "NUM_passingMVA90_HWW_DEN_wp90iso", 'data/scale_factor/Full2024v15/electron.json'],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                #'fakeW' : 'data/fake_prompt_rates/',  
            },
            "cutBased_LooseID_tthMVA_Run3": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_promptMVA > 0.90",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                },
                'tkSF':  { 
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                'tthMvaSF':  {
                    '1-1' : ["2024PromptCDE+Re-recoFGHI", "Electron-ID-SF", "NUM_passingTTHMVA_DEN_LooseID", 'data/scale_factor/Full2024v15/electron.json'],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                #'fakeW' : 'data/fake_prompt_rates/',  
            },
            "cutBased_LooseID_tthMVA_HWW": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_cutBased >= 2",
                        "Electron_convVeto",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                    ],
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "ROOT::VecOps::abs(Electron_dxy) < 0.1",
                        "ROOT::VecOps::abs(Electron_dz) <  0.2",
                    ],
                    "Electron_pt <= 20.0": [
                        "Electron_promptMVA > 0.35",
                    ],
                    "Electron_pt > 20.0": [
                        "Electron_promptMVA > 0.90",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz"]
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                'wpSF':  {
                    '1-1' : ["2024Prompt", "Electron-ID-SF", "Loose", '/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electron.json.gz'],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                'tthMvaSF':  {
                    '1-1' : ["2024PromptCDE+Re-recoFGHI", "Electron-ID-SF", "passingTTHMVA_HWW", 'data/scale_factor/Full2024v15/electron.json'],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                #'fakeW' : 'data/fake_prompt_rates/',
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-12-03/electronSS_EtDependent.json.gz",
    },
}

MuonWP = {
    # ____________________Full2018v9__________________________
    "Full2018v9": {
        # ------------
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    # dxy for pT < 20 GeV
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        # ------------
        "TightObjWP": {
            "cut_Tight_HWWW": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId == 4",
                    ],
                    # dxy for pT < 20 GeV
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": [
                        "data/scale_factor/Full2018v9/NUM_TightHWW_DEN_TrackerMuons_eta_pt.root"
                    ],
                },
                "isoSF": {
                    "1-1": [
                        "data/scale_factor/Full2018v9/NUM_TightHWW_ISO_DEN_TightHWW_eta_pt.root"
                    ],
                },
                "fakeW": "data/fake_prompt_rates/Full2018v9/cut_Tight_HWWW/",
            },
            # "cut_Tight_HWWW_tthmva_80": {
            #     "cuts": {
            #         # Common cuts
            #         "ROOT::RVecB (Muon_pt.size(), true)": [
            #             "ROOT::VecOps::abs(Muon_eta) < 2.4",
            #             "Muon_tightId",
            #             "ROOT::VecOps::abs(Muon_dz) < 0.1",
            #             "Muon_pfIsoId == 4",
            #             "Muon_mvaTTH > 0.8",
            #         ],
            #         # dxy for pT < 20 GeV
            #         "Muon_pt <= 20.0": [
            #             "ROOT::VecOps::abs(Muon_dxy) < 0.01",
            #         ],
            #         # dxy for pT > 20 GeV
            #         "Muon_pt > 20.0": [
            #             "ROOT::VecOps::abs(Muon_dxy) < 0.02",
            #         ],
            #     },
            #     # Update with new SFs
            #     "idSF": {
            #         "1-1": "LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2018v9/NUM_TightHWW_DEN_TrackerMuons_eta_pt.root",
            #     },
            #     "isoSF": {
            #         "1-1": "LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2018v9/NUM_TightHWW_ISO_DEN_TightHWW_eta_pt.root",
            #     },
            #     "tthMvaSF": {
            #         "1-1": [
            #             "NUM_TightHWW_tth_ISO_DEN_TightHWW_ISO_eta_pt",  # Hist name
            #             "LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2018v9/NUM_TightHWW_tth_ISO_DEN_TightHWW_ISO_eta_pt.root",
            #         ]  # Nominal+Stat+Syst
            #         # 'LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2018v7/ttHMVA0p8_TightHWWCut_SFs_SYS_2018.root', ] # Syst
            #     },
            #     "fakeW": "data/fake_prompt_rates/Full2018v9/cut_Tight_HWWW_tthmva_80/",
            # },
        },
    },    
    ### ------------------- Full2022 --------------------
    "Full2022v12": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        "TightObjWP": {
            "cut_TightID_POG": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "Muon_pt > 15.0",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022v12/cut_Tight_HWW/",
            },
            "cut_Tight_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022v12/cut_Tight_HWW/",
            },
            "cut_TightID_pfIsoTight_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_TightIso_tthMVA_DEN_TightPFIso", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022v12/cut_TightID_HWW_TightPFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022v12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                        "Muon_tthMVA > 0.20",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                        "Muon_tthMVA > 0.67",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_HWW_DEN_LoosePFIso", "data/scale_factor/Full2022v12/muonSF_latinos_HWW_ttHMVA_alt.json"], # To be added
                },
                #"fakeW": "data/fake_prompt_rates/Full2022v12/cut_TightID_HWW_LoosePFIso_tthMVA_HWW/",
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2025-08-14/muon_scalesmearing.json.gz",
    },
    "Full2022EEv12": {
        # ------------                                                                                                                                                  
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        # ------------                                                                                                                                                  
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    # dxy for pT < 20 GeV                                                                                                                               
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV                                                                                                                               
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        # ------------                                                                                                                                                  
        "TightObjWP": {
            "cut_TightID_POG": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "Muon_pt > 15.0",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_Tight_HWW/",
            },
            "cut_Tight_HWW": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                    ],
                    # dxy for pT < 20 GeV                                                                                                                               
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV                                                                                                                               
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_Tight_HWW/",
            },
            "cut_TightID_pfIsoTight_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_TightIso_tthMVA_DEN_TightPFIso", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_TightID_HWW_TightPFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                        "Muon_tthMVA > 0.20",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                        "Muon_tthMVA > 0.67",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_HWW_DEN_LoosePFIso", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW_ttHMVA_alt.json"], # To be added
                },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_tthMVA_HWW/",
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-08-14/muon_scalesmearing.json.gz",
    },
    "Full2023v12": {
        # ------------                                                                                                                                                  
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        # ------------                                                                                                                                                  
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    # dxy for pT < 20 GeV                                                                                                                               
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV                                                                                                                               
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        # ------------                                                                                                                                                  
        "TightObjWP": {
            "cut_TightID_POG": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "Muon_pt > 15.0",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023v12/cut_Tight_HWW/",
            },
            "cut_Tight_HWW": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                    ],
                    # dxy for pT < 20 GeV                                                                                                                               
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV                                                                                                                               
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023v12/cut_Tight_HWW/",
            },
            "cut_TightID_pfIsoTight_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },                
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_TightIso_tthMVA_DEN_TightPFIso", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023v12/cut_TightID_HWW_TightPFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023v12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                        "Muon_tthMVA > 0.20",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                        "Muon_tthMVA > 0.67",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_HWW_DEN_LoosePFIso", "data/scale_factor/Full2023v12/muonSF_latinos_HWW_ttHMVA_alt.json"], # To be added
                },
                #"fakeW": "data/fake_prompt_rates/Full2023v12/cut_TightID_HWW_LoosePFIso_tthMVA_HWW/",
            },
        },        
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2025-08-14/muon_scalesmearing.json.gz",
    },
    "Full2023BPixv12": {
        # ------------                                                                                                                                                  
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        # ------------                                                                                                                                                  
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    # dxy for pT < 20 GeV                                                                                                                               
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV                                                                                                                               
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        # ------------                                                                                                                                                  
        "TightObjWP": {
            "cut_TightID_POG": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "Muon_pt > 15.0",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-08-14/muon_Z.json.gz"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_Tight_HWW/",
            },
            "cut_Tight_HWW": {
                "cuts": {
                    # Common cuts                                                                                                                                       
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                    ],
                    # dxy for pT < 20 GeV                                                                                                                               
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV                                                                                                                               
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_Tight_HWW/",
            },
            "cut_TightID_pfIsoTight_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_TightIso_tthMVA_DEN_TightPFIso", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_TightID_HWW_TightPFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "Muon_tthMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                        "Muon_tthMVA > 0.20",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                        "Muon_tthMVA > 0.67",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_HWW_DEN_LoosePFIso", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW_ttHMVA_alt.json"], # To be added
                },
                #"fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_TightID_HWW_LoosePFIso_tthMVA_HWW/",
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-08-14/muon_scalesmearing.json.gz",
    },
    "Full2024v15": {
        # ------------
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    # dxy for pT < 20 GeV
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        "TightObjWP": {
            "cut_TightID_POG": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "Muon_pt > 15.0",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_Z.json.gz"],
                },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_POG/",
            },
            "cut_Tight_HWW": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                    ],
                    # dxy for pT < 20 GeV
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_Tight_HWW/",
            },
            "cut_TightID_pfIsoTight_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                        "Muon_promptMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_TightIso_tthMVA_DEN_TightPFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_TightPFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "Muon_promptMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                     ],
                     "Muon_pt <= 20.0": [
                         "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                         "Muon_promptMVA > 0.20",
                     ],
                     "Muon_pt > 20.0": [
                         "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                         "Muon_promptMVA > 0.67",
                     ],
                 },
                 "idSF": {
                     "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                 },
                 "isoSF": {
                     "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                 },
                 "tthMvaSF": {
                     "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_HWW_DEN_LoosePFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                 },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_tthMVA_HWW/",
            },
            "cut_TightID_pfIsoLoose_HWW_PNet": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "(Muon_pnScore_prompt + Muon_pnScore_tau) > 0.989",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_PNet_DEN_LoosePFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_PNet/",  
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_scalesmearing.json.gz",
    },

    "Full2025v15": {
        # Copied from Full2024v15. To be updated when processing MC.
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_pt > 10.0",
                    ]
                },
            }
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfRelIso04_all < 0.4",
                    ],
                    # dxy for pT < 20 GeV
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
            },
        },
        "TightObjWP": {
            "cut_TightID_POG": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "Muon_pt > 15.0",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_Z.json.gz"],
                }, # using 2024 SFs while processing only data. To be updated when processing MC
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_Z.json.gz"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_POG/",
            },
            "cut_Tight_HWW": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                    ],
                    # dxy for pT < 20 GeV
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    # dxy for pT > 20 GeV
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                },# using 2024 SFs while processing only data. To be updated when processing also MC
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_Tight_HWW/",
            },
            "cut_TightID_pfIsoTight_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 4",
                        "Muon_promptMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_TightIso_tthMVA_DEN_TightPFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_TightPFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_67": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "Muon_promptMVA > 0.67",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
            "cut_TightID_pfIsoLoose_HWW_tthmva_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                     ],
                     "Muon_pt <= 20.0": [
                         "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                         "Muon_promptMVA > 0.20",
                     ],
                     "Muon_pt > 20.0": [
                         "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                         "Muon_promptMVA > 0.67",
                     ],
                 },
                 "idSF": {
                     "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                 }, # using 2024 SFs while processing only data. To be updated when processing also MC
                 "isoSF": {
                     "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                 }, # using 2024 SFs while processing only data. To be updated when processing also MC
                 "tthMvaSF": {
                     "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_HWW_DEN_LoosePFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                 }, # using 2024 SFs while processing only data. To be updated when processing also MC
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_tthMVA_HWW/",
            },
            "cut_TightID_pfIsoLoose_HWW_PNet": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_pfIsoId >= 2",
                        "(Muon_pnScore_prompt + Muon_pnScore_tau) > 0.989",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_HWW_DEN_TrackerMuons", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                "isoSF": {
                    "1-1": ["NUM_LoosePFIso_DEN_TightID_HWW", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                "tthMvaSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_PNet_DEN_LoosePFIso", "data/scale_factor/Full2024v15/muonSF_latinos_HWW.json"],
                }, # using 2024 SFs while processing only data. To be updated when processing also MC
                #"fakeW": "data/fake_prompt_rates/Full2024v15/cut_TightID_HWW_LoosePFIso_PNet/",  
            },
        },
        "ScaleAndSmearing" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-11-27/muon_scalesmearing.json.gz",
    },    
}
