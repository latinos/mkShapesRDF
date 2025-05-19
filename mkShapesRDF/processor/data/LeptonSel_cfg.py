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
            "wp80iso":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP80",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "wp80iso", 'data/jsonpog-integration/POG/EGM/2022_Summer22/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
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
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "passingMVA90", 'data/scale_factor/Full2022v12/electron.json'], ### Correctionlib parameters: [Era, Key, WP, path to json].
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
                    '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22/electron.json.gz"]
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
                     '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22/electron.json.gz"]
                 } ,
                 'wpSF':  {
                     '1-1' : ["2022Re-recoBCD", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2022v12/electron.json'],
                 } ,
                 'fakeW' : 'data/fake_prompt_rates/Full2022v12/cutBased_LooseID_tthMVA/',
             },
        },
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
            "wp80iso":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP80",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "wp80iso", 'data/jsonpog-integration/POG/EGM/2022_Summer22EE/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
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
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "passingMVA90", 'data/scale_factor/Full2022EEv12/electron.json'],
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
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electron.json.gz"]
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
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2022_Summer22EE/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2022Re-recoE+PromptFG", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2022EEv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/cutBased_LooseID_tthMVA/',
            },
        },
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
            "wp80iso":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP80",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "wp80iso", 'data/jsonpog-integration/POG/EGM/2023_Summer23/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
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
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "passingMVA90", 'data/scale_factor/Full2023v12/electron.json'],
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
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23/electron.json.gz"]
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
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptC", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2023v12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023v12/cutBased_LooseID_tthMVA/',
            },
        },
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
            "wp80iso":{
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP80",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "wp80iso", 'data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electron.json.gz'], ### Correctionlib parameters: [Era, Key, WP, path to json].
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
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "passingMVA90", 'data/scale_factor/Full2023BPixv12/electron.json'],
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
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "passingMVA90_HWW", 'data/scale_factor/Full2023BPixv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/mvaWinter22V2Iso_WP90/',
            },
            "cutBased__LooseID_tthMVA_Run3": {
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
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "data/jsonpog-integration/POG/EGM/2023_Summer23BPix/electron.json.gz"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023PromptD", "Electron-ID-SF", "passingTTHMVA", 'data/scale_factor/Full2023BPixv12/electron.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/cutBased_LooseID_tthMVA/',
            },
        },
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
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/jsonpog-integration/POG/MUO/2022_Summer22/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "data/jsonpog-integration/POG/MUO/2022_Summer22/muon_Z.json.gz"],
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
                "tthSF": {
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
                "tthSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2022v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022v12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
        },
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
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/jsonpog-integration/POG/MUO/2022_Summer22EE/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "data/jsonpog-integration/POG/MUO/2022_Summer22EE/muon_Z.json.gz"],
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
                "tthSF": {
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
                "tthSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2022EEv12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
        },
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
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/jsonpog-integration/POG/MUO/2023_Summer23/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "data/jsonpog-integration/POG/MUO/2023_Summer23/muon_Z.json.gz"],
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
                "tthSF": {
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
                "tthSF": {
                    "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2023v12/muonSF_latinos_HWW.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2023v12/cut_TightID_HWW_LoosePFIso_tthMVA/",
            },
        }, 
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
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/jsonpog-integration/POG/MUO/2023_Summer23BPix/muon_Z.json.gz"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightPFIso_DEN_TightID", "data/jsonpog-integration/POG/MUO/2023_Summer23BPix/muon_Z.json.gz"],
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
                "tthSF": {
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
                 "tthSF": {
                     "1-1": ["NUM_TightID_HWW_LooseIso_tthMVA_DEN_LoosePFIso", "data/scale_factor/Full2023BPixv12/muonSF_latinos_HWW.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_TightID_HWW_LoosePFIso_tthMVA/",
             },
        }, 
    },
}
