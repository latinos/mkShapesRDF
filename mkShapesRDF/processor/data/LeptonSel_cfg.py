import ROOT

LepFilter_dict = {
    "Loose"   : "isLoose",
    "Veto"    : "isVeto",
    "WgStar"  : "isWgs",
    "isLoose" : "FakeObjWP",
    "isVeto"  : "VetoObjWP",
    "isWgs"   : "WgStarObjWP",
}

# DeepJet working points
bWP_loose_deepFlavB_2018  = '0.0490'
bWP_medium_deepFlavB_2018 = '0.2783'

# Linear interpolation of DeepJet discriminant
ROOT.gInterpreter.Declare(
    """
    ROOT::RVecB smoothBFlav(ROOT::RVecF Lepton_pt, ROOT::RVecI Lepton_jetIdx, ROOT::RVecF Lepton_jetRelIso, ROOT::RVecF Jet_btagDeepFlavB, float wploose, float wpmedium){
        float ptmin = 20;
        float ptmax = 45;
        ROOT::RVecB result(Lepton_pt.size(), false);
        for (int i=0; i < Lepton_pt.size(); i++){
            if (Lepton_jetIdx[i] > -1){
                float cone_pt = 0.9*Lepton_pt[i]*(1 + Lepton_jetRelIso[i]);
                float x = std::min(std::max(0.0f, cone_pt - ptmin)/(ptmax - ptmin), 1.0f);
                float y = x * wploose * (1 - x) * wpmedium;
                result[i] = Jet_btagDeepFlavB[Lepton_jetIdx[i]] < y;
            }
        }
        return result;
    }
    """
)

# DeepJet selection: we need to be sure that the Lepton has an associated jet
ROOT.gInterpreter.Declare(
    """
    ROOT::RVecB Lepton_btagDeepFlavB(ROOT::RVecI Lepton_jetIdx, ROOT::RVecF Jet_btagDeepFlavB, float wpmedium){
        ROOT::RVecB result(Lepton_jetIdx.size(), false);
        for (int i=0; i < Lepton_jetIdx.size(); i++){
            if (Lepton_jetIdx[i] > -1){
                result[i] = Jet_btagDeepFlavB[Lepton_jetIdx[i]] < wpmedium;
            }
        }
        return result;
    }
    """
)

# Cone-pT definition
ROOT.gInterpreter.Declare(
    """
    ROOT::RVecB Leptoon_conePt(ROOT::RVecF Lepton_pt, ROOT::RVecF Lepton_jetRelIso){
        ROOT::RVecF result(Lepton_pt.size(), false);
        for (int i=0; i < Lepton_pt.size(); i++){
            result[i] = 0.90 * (Lepton_pt[i]) * (1 + Lepton_jetRelIso[i]);
        }
        return result;
    }
    """
)


##################
### Selections ###
##################

ElectronWP = {

    # ____________________Full2018v9__________________________
    "Full2018v9": {
        "VetoObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "(0.9)*(Electron_pt)*(1. + Electron_jetRelIso) > 7.0",
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                        "Electron_sip3d < 8",
                        "Electron_miniPFRelIso_all < 0.4",
                        "Electron_lostHits <= 1",
                        "Electron_mvaFall17V2noIso_WPL",
                    ]
                },
            },
        },
        # ------------
        "FakeObjWP": {
            "HLTsafe": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "(0.9)*(Electron_pt)*(1. + Electron_jetRelIso) > 10.0",
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                        "Electron_sip3d < 8",
                        "Electron_miniPFRelIso_all < 0.4",
                        "Electron_hoe < 0.10",
                        "Electron_eInvMinusPInv > -0.04",
                        "Electron_convVeto == 1",
                        "Electron_lostHits == 0",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "Electron_sieie  < 0.011",
                    ],
                    # Endcaps
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "Electron_sieie  < 0.030",
                    ],
                    # Electron_tthMVA_UL > 0.90
                    "Electron_tthMVA_UL > 0.90": [
                        "Electron_mvaFall17V2noIso_WPL > 0",
                        f"Lepton_btagDeepFlavB(Electron_jetIdx, Jet_btagDeepFlavB, {bWP_medium_deepFlavB_2018})",
                    ],
                    # Electron_tthMVA_UL <= 0.90
                    "Electron_tthMVA_UL <= 0.90": [
                        "Electron_mvaFall17V2noIso_WP90 > 0",
                        "Electron_jetRelIso < 1.0",
                        f"smoothBFlav(Electron_pt, Electron_jetIdx, Electron_jetRelIso, Jet_btagDeepFlavB, {bWP_loose_deepFlavB_2018}, {bWP_medium_deepFlavB_2018})",
                    ],
                },
            },
        },
        "TightObjWP": {
            # ----- ttH_ID
            "ttH_ID": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "Electron_pt > 10.0",
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "ROOT::VecOps::abs(Electron_dxy) < 0.05",
                        "ROOT::VecOps::abs(Electron_dz)  < 0.1",
                        "Electron_sip3d < 8",
                        "Electron_miniPFRelIso_all < 0.4",
                        "Electron_hoe < 0.10",
                        "Electron_eInvMinusPInv > -0.04",
                        "Electron_convVeto == 1",
                        "Electron_lostHits == 0",
                        "Electron_mvaFall17V2noIso_WPL > 0",
                        f"Lepton_btagDeepFlavB(Electron_jetIdx, Jet_btagDeepFlavB, {bWP_medium_deepFlavB_2018})",
                        "Electron_tthMVA_UL > 0.90",
                    ],
                    # Barrel
                    "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
                        "Electron_sieie  < 0.011",
                    ],
                    # Endcaps
                    "ROOT::VecOps::abs(Electron_eta) > 1.479": [
                        "Electron_sieie  < 0.030",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["UL-Electron-ID-SF", "data/scale_factor/Full2018v9/electron.json"]
                    # '1-1' : ["Electron-RecoToLoose-SF", "data/scale_factor/Full2018v9/electronSF_2018_ttH_Reco.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["Electron-ID-SF", 'data/scale_factor/Full2018v9/electronSF_2018_ttH_ID.json'],
                } ,
                "isoSF": {
                    '1-1' : ["Electron-Iso-SF", "data/scale_factor/Full2018v9/electronSF_2018_ttH_Iso.json"],
                },
                'fakeW' : 'data/fake_prompt_rates/Full2022v12/mvaWinter22V2Iso_WP90/', # FIX!
            },
            # "mvaFall17V2Iso_WP90": {
            #     "cuts": {
            #         # Common cuts
            #         "ROOT::RVecB (Electron_pt.size(), true)": [
            #             "ROOT::VecOps::abs(Electron_eta) < 2.5",
            #             "Electron_mvaFall17V2Iso_WP90",
            #             "Electron_convVeto",
            #             "Electron_pfRelIso03_all < 0.06",
            #         ],
            #         # Barrel
            #         "ROOT::VecOps::abs(Electron_eta) <= 1.479": [
            #             "ROOT::VecOps::abs(Electron_dxy) < 0.05",
            #             "ROOT::VecOps::abs(Electron_dz)  < 0.1",
            #         ],
            #         # EndCap
            #         "ROOT::VecOps::abs(Electron_eta) > 1.479": [
            #             "ROOT::VecOps::abs(Electron_dxy) < 0.1",
            #             "ROOT::VecOps::abs(Electron_dz) <  0.2",
            #         ],
            #     },
            #     'tkSF':  { 
            #         '1-1' : '/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz'
            #     } ,
            #     'wpSF':  {
            #         '1-1' : 'data/scale_factor/Full2018v9/egammaEffi_TightHWW_2018.txt',
            #     } ,
            #     'fakeW' : 'data/fake_prompt_rates/Full2018v9/mvaFall17V2Iso_WP90/',
            # }
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
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["Electron-ID-SF", "data/scale_factor/Full2022v12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["Electron-ID-SF", 'data/scale_factor/Full2022v12/electron_POG.json'],
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
                    '1-1' : ["Electron-ID-SF", "data/scale_factor/Full2022v12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2022v12/electron_scale.json'],
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
                     '1-1' : ["Electron-ID-SF", "data/scale_factor/Full2022v12/electron_POG.json"]
                 } ,
                 'wpSF':  {
                     '1-1' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2022v12/electron_scale.json'],
                 } ,
                 'fakeW' : 'data/fake_prompt_rates/Full2022v12/mvaWinter22V2Iso_WP90/',
             },
        },
    },

    "Full2022EEv12": {
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
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-2' : ["2022FG-Electron-ID-SF", "data/scale_factor/Full2022EEv12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-2' : ["2022FG-Electron-ID-SF", 'data/scale_factor/Full2022EEv12/electron_POG.json'],
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
                    '1-2' : ["2022FG-Electron-ID-SF", "data/scale_factor/Full2022EEv12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2022EEv12/electron_IsoWinter22_Run2022E.json'],
                    '2-2' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2022EEv12/electron_IsoWinter22.json'],
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
                     '1-1' : ["2022FG-Electron-ID-SF", "data/scale_factor/Full2022EEv12/electron_POG.json"]
                 } ,
                 'wpSF':  {
                     '1-1' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2022EEv12/electron_scale.json'],
                 } ,
                 'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/mvaWinter22V2Iso_WP90/',
             },
        },
    },
    "Full2023v12": {
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
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023FG-Electron-ID-SF", "data/scale_factor/Full2023v12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023FG-Electron-ID-SF", 'data/scale_factor/Full2023v12/electron_POG.json'],
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
                    '1-2' : ["2023FG-Electron-ID-SF", "data/scale_factor/Full2023v12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2023v12/electron_IsoWinter22_Run2022E.json'], # FIX!!
                    '2-2' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2023v12/electron_IsoWinter22.json'],          # FIX!!
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
                    '1-1' : ["2023FG-Electron-ID-SF", "data/scale_factor/Full2023v12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["NUM_Electron_mvaWinter23V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2023v12/electron_scale.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023v12/mvaWinter23V2Iso_WP90/',
            },

    },

},

"Full2023BPixv12": {
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
            "wp90iso": {
                "cuts": {
                    "ROOT::RVecB (Electron_pt.size(), true)": [
                        "ROOT::VecOps::abs(Electron_eta) < 2.5",
                        "Electron_mvaIso_WP90",
                        "Electron_convVeto",
                    ],
                },
                'tkSF':  {
                    '1-1' : ["2023BPixFG-Electron-ID-SF", "data/scale_factor/Full2023BPixv12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["2023BPixFG-Electron-ID-SF", 'data/scale_factor/Full2023BPixv12/electron_POG.json'],
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
                    '1-2' : ["2023BPixFG-Electron-ID-SF", "data/scale_factor/Full2023BPixv12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2023BPixv12/electron_IsoWinter22_Run2022E.json'], # FIX!!
                    '2-2' : ["NUM_Electron_mvaWinter22V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2023BPixv12/electron_IsoWinter22.json'],          # FIX!!
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2022EEv12/mvaWinter22V2Iso_WP90/',
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
                    '1-1' : ["2023BPixFG-Electron-ID-SF", "data/scale_factor/Full2023BPixv12/electron_POG.json"]
                } ,
                'wpSF':  {
                    '1-1' : ["NUM_Electron_mvaWinter23V2IsoWP90_DEN_ElectronTrack", 'data/scale_factor/Full2023BPixv12/electron_scale.json'],
                } ,
                'fakeW' : 'data/fake_prompt_rates/Full2023BPixv12/mvaWinter23V2Iso_WP90/',
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
                        "(0.9)*(Muon_pt)*(1. + Muon_jetRelIso) > 5.0",
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "ROOT::VecOps::abs(Muon_dxy) < 0.05",
                        "ROOT::VecOps::abs(Muon_dz)  < 0.1",
                        "Muon_sip3d < 8",
                        "Muon_miniPFRelIso_all < 0.4",
                        "Muon_looseId",
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
                        "(0.9)*(Muon_pt)*(1. + Muon_jetRelIso) > 10.0",
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "ROOT::VecOps::abs(Muon_dxy) < 0.05",
                        "ROOT::VecOps::abs(Muon_dz)  < 0.1",
                        "Muon_sip3d < 8",
                        "Muon_miniPFRelIso_all < 0.4",
                        "Muon_looseId",
                    ],
                    # Muon_mvaTTH > 0.85
                    "Muon_mvaTTH > 0.85": [
                        f"Lepton_btagDeepFlavB(Muon_jetIdx, Jet_btagDeepFlavB, {bWP_medium_deepFlavB_2018})",
                    ],
                    # Muon_mvaTTH <= 0.85
                    "Muon_mvaTTH <= 0.85": [
                        "Muon_jetRelIso < 0.5",
                        f"smoothBFlav(Muon_pt, Muon_jetIdx, Muon_jetRelIso, Jet_btagDeepFlavB, {bWP_loose_deepFlavB_2018}, {bWP_medium_deepFlavB_2018})",
                    ],
                },
            },
        },
        # ------------
        "TightObjWP": {
            "ttH_ID": {
                "cuts": {
                    # Common cuts
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "Muon_pt > 10.0",
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "ROOT::VecOps::abs(Muon_dxy) < 0.05",
                        "ROOT::VecOps::abs(Muon_dz)  < 0.1",
                        "Muon_sip3d < 8",
                        "Muon_miniPFRelIso_all < 0.4",
                        "Muon_mediumId",
                        f"Lepton_btagDeepFlavB(Muon_jetIdx, Jet_btagDeepFlavB, {bWP_medium_deepFlavB_2018})",
                        "Muon_mvaTTH > 0.85",
                    ],
                },
                "idSF": {
                    '1-1': ["Muon-ID-SF", "data/scale_factor/Full2018v9/muonSF_2018_ttH_ID.json"],
                },
                "isoSF": {
                    "1-1": ["Muon-Iso-SF", "data/scale_factor/Full2018v9/muonSF_2018_ttH_Iso.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2018v9/cut_Tight_HWWW/", # FIX!
            },
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
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muon_scale.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022v12/muon_scale.json"],
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
                     "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022v12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-1": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2022v12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2022v12/cut_Tight_HWW/",
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
                     "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022v12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022v12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-1": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2022v12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2022v12/cut_Tight_HWW/",
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
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muon_scale_Run2022E.json"],
                    "2-2": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022EEv12/muon_scale_Run2022E.json"],
                    "2-2": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_Tight_HWW/",
            },
            "cut_TightMiniIso_HWW": {
                "cuts": {
                    "ROOT::RVecB (Muon_pt.size(), true)": [
                        "ROOT::VecOps::abs(Muon_eta) < 2.4",
                        "Muon_tightId",
                        "ROOT::VecOps::abs(Muon_dz) < 0.1",
                        "Muon_miniIsoId >= 3",
                    ],
                    "Muon_pt <= 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.01",
                    ],
                    "Muon_pt > 20.0": [
                        "ROOT::VecOps::abs(Muon_dxy) < 0.02",
                    ],
                },
                "idSF": {
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muon_scale_Run2022E.json"],
                    "2-2": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightIDMiniIso_DEN_TightID", "data/scale_factor/Full2022EEv12/muon_scale_Run2022E.json"],
                    "2-2": ["NUM_TightIDMiniIso_DEN_TightID", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_TightMiniIso_HWW/",
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
                     "1-2": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-2": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-2": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_Tight_HWW/",
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
                     "1-2": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-2": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-2": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2022EEv12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2022EEv12/cut_Tight_HWW/",
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
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muon_scale_Run2023BPix.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2023v12/muon_scale_Run2023BPix.json"],
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
                     "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2023v12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-1": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2023v12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2023v12/cut_Tight_HWW/",
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
                     "1-2": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2023v12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-2": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2023v12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-2": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2023v12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2023v12/cut_Tight_HWW/",
             },
    }, 
},
"Full2023Bpixv12": {
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
                    "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muon_scale_Run2023BPix.json"],
                },
                "isoSF": {
                    "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2023BPixv12/muon_scale_Run2023BPix.json"],
                },
                "fakeW": "data/fake_prompt_rates/Full203BPixv12/cut_Tight_HWW/",
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
                     "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2023Bpixv12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-1": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2023BPixv12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_Tight_HWW/",
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
                     "1-1": ["NUM_TightID_DEN_TrackerMuons", "data/scale_factor/Full2023BPixv12/muon_scale.json"],
                 },
                 "isoSF": {
                     "1-1": ["NUM_TightIDIso_DEN_TightID", "data/scale_factor/Full2023BPixv12/muon_scale.json"],
                 },
                 "tthSF": {
                     "1-1": ["NUM_tthMVA_67_DEN_TightIDIso", "data/scale_factor/Full2023BPixv12/muon_scale.json"],
                 },
                 "fakeW": "data/fake_prompt_rates/Full2023BPixv12/cut_Tight_HWW/",
             },
    }, 
},
}

