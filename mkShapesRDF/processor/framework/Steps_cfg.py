Steps = {

    ##############
    ### Chains ###
    ##############
    
    # 2018
    "DATAl1loose2018v9": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>0)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepSel",
            "jetSelUL",
            "l2Kin",
            "trigData",
            "finalSnapshot_DATA",
        ],
    },

    # 2022
    "MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight": {
        "isChain" : True,
        "do4MC" : True,
        "do4Data" : False,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "btagPerJet_Summer22EE_DeepJet_shape",
            "btagPerJet_Summer22EE_PNet_shape",
            "btagPerJet_Summer22EE_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "formulasMC_2022",
            "l2tight",
            "finalSnapshot_JES",
        ]
    },

    "MCl1loose2022v12__MCCorr2022v12JetScaling__fakeSel": {
        "isChain" : True,
        "do4MC" : True,
        "do4Data" : False,
        "selection" : '"((nElectron+nMuon)>0)"',
        "subTargets" : [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "btagPerJet_Summer22EE_DeepJet_shape",
            "btagPerJet_Summer22EE_PNet_shape",
            "btagPerJet_Summer22EE_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules",
            "l2Kin",
            "formulasMC_2022",
            "fakeSel",
            "finalSnapshot_MC",
        ]
    },

    "DATAl2loose2022v12__l2tight": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2022",
            "l2tight",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2022v12__fakeSel": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>0)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "trigData",
            "formulasDATA_2022",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2022v12__fakeW": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2022",
            "fakeW",
            "formulasFAKE_2022",
            "finalSnapshot_DATA",
        ],
    },

    # 2022 EE
    "MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight": {
        "isChain" : True,
        "do4MC" : True,
        "do4Data" : False,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "btagPerJet_Summer22EE_DeepJet_shape",
            "btagPerJet_Summer22EE_PNet_shape",
            "btagPerJet_Summer22EE_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "formulasMC_2022EE",
            "l2tight",
            "finalSnapshot_JES",
        ]
    },

    "MCl2loose2022EEv12__MCCorr2022EEv12__lepID": {
        "isChain" : True,
        "do4MC" : True,
        "do4Data" : False,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "leptonMaker",
            "lepSel",
            "jetSelMaskFilter",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "btagPerJet_Summer22EE_DeepJet_shape",
            "btagPerJet_Summer22EE_PNet_shape",
            "btagPerJet_Summer22EE_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "formulasMC_2022EE",
            "finalSnapshot_MC",
        ]
    },

    "DATAl2loose2022EEv12__l2tight": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMaskFilter",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2022EE",
            "l2tight",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2022EEv12__fakeSel": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>0)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMaskFilter",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2022EE",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2022EEv12__fakeW": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMaskFilter",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2022EE",
            "fakeW",
            "formulasFAKE_2022EE",
            "finalSnapshot_DATA",
        ],
    },

    # 2023
    "DATAl2loose2023v12__l2tight": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2023",
            "l2tight",
            "finalSnapshot_DATA",
        ],
    },
    "DATAl1loose2023v12__fakeSel": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2023",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },
    "DATAl1loose2023v12__fakeW": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2023",
            "fakeW",
            "formulasFAKE_2023",
            "finalSnapshot_DATA",
        ],
    },

    # 2023BPix
    "DATAl2loose2023BPixv12__l2tight": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2023BPix",
            "l2tight",
            "finalSnapshot_DATA",
        ],
    },
    "DATAl1loose2023BPixv12__fakeSel": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2023BPix",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },
    "DATAl1loose2023BPixv12__fakeW": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "lumiMask",
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA_2023BPix",
            "fakeW",
            "formulasFAKE_2023BPix",
            "finalSnapshot_DATA",
        ],
    },

    # "fakeSel": {
    #     "isChain": True,
    #     "do4MC": False,
    #     "do4Data": True,
    #     "selection": '"((MET_pt < 20 || PuppiMET_pt < 20) && mtw1 < 20)"',
    #     "subTargets": [
    #         "finalSnapshot_DATA",
    #     ],
    # },
    
    "fakeSelKinMC": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "baseW",
            "trigMCnoSF",
            "l2Kin",
            "l3Kin",
            "puW",
            "formulasMCnoSF",
            "fakeSel",
            "finalSnapshot_MC",
        ],
    },
    
    "fakeW": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"(Lepton_pt.size()>0)"',
        "subTargets": [
            "fakeW_2022EE",
            "formulasFAKE_2022EE",
            "finalSnapshot_DATA",
        ],
    },

    "l2loose": {
        "isChain": True,
        "do4MC": True,
        "do4Data": True,
        "selection": '"(Lepton_pt.size()>1)"',
        "subTargets": [
            "finalSnapshot_MC",
        ],
    },

    "l2tightOR2022v11": {
        "isChain": True,
        "do4MC": True,
        "do4Data": True,
        "selection": '"(Lepton_pt.size()>1 && Lepton_pt[0]>18 && Lepton_pt[1]>8) && \
        (Lepton_isTightElectron_cut_Tight_HWWW[0] > 0.5    \
        || Lepton_isTightElectron_cut_Tight_HWWW_tthmva70[0] > 0.5  \
        || Lepton_isTightElectron_cut_Medium_HWWW[0] > 0.5   \
        || Lepton_isTightElectron_mvaWinter22V2Iso_WP90[0] > 0.5   \
        || Lepton_isTightElectron_mvaWinter22V2Iso_WP90_tthmva70[0] > 0.5  \
        || Lepton_isTightMuon_cut_Tight_HWWW[0] > 0.5   \
        || Lepton_isTightMuon_cut_Medium_HWWW[0] > 0.5  \
        || Lepton_isTightMuon_cut_Tight_HWWW_tthmva_80[0] > 0.5   \
        || Lepton_isTightMuon_cut_Medium_HWWW_tthmva_80[0] > 0.5) && \
        (Lepton_isTightElectron_cut_Tight_HWWW[1] > 0.5   \
        || Lepton_isTightElectron_cut_Tight_HWWW_tthmva70[1] > 0.5  \
        || Lepton_isTightElectron_cut_Medium_HWWW[1] > 0.5   \
        || Lepton_isTightElectron_mvaWinter22V2Iso_WP90[1] > 0.5   \
        || Lepton_isTightElectron_mvaWinter22V2Iso_WP90_tthmva70[1] > 0.5  \
        || Lepton_isTightMuon_cut_Tight_HWWW[1] > 0.5   \
        || Lepton_isTightMuon_cut_Medium_HWWW[1] > 0.5  \
        || Lepton_isTightMuon_cut_Tight_HWWW_tthmva_80[1] > 0.5   \
        || Lepton_isTightMuon_cut_Medium_HWWW_tthmva_80[1] > 0.5 ) "',
        "subTargets": [
            "finalSnapshot_MC",
        ],
    },

    ### 
    ### Full set of corrections for Run2022BCD ReReco : Summer22 campaign     
    ###
    "MCl1loose2022v12__MCCorr2022v12__l2tight": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "btagPerJet_Summer22_DeepJet_shape",
            "btagPerJet_Summer22_PNet_shape",
            "btagPerJet_Summer22_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules",
            "l2Kin",
            "formulasMC_2022",
            "l2tight",
            "finalSnapshot_JES",
        ]
    },

    ###
    ### Full set of corrections for Run2022E+FG Prompt : Summer22EE MC campaign
    ###
    "MCl1loose2022EEv12__MCCorr2022EEv12__l2tight": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMaskFilter",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "btagPerJet_Summer22EE_DeepJet_shape",
            "btagPerJet_Summer22EE_PNet_shape",
            "btagPerJet_Summer22EE_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules",
            "l2Kin",
            "formulasMC",
            "l2tight",
            "finalSnapshot_JES",
        ]
    },

    "MCl1loose2022v12__fakeSelKinMC": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMask",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "trigMCnoSF",
            "l2Kin",
            "puW",
            "formulasMCnoSF_2022",
            "fakeSel",
            "finalSnapshot_MC",
        ]
    },
    "MCl1loose2022EEv12__fakeSelKinMC": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "leptonMaker",
            "lepFiller_tthMVA",
            "lepSel",
            "jetSelMaskFilter",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
            "baseW",
            "trigMCnoSF",
            "l2Kin",
            "puW",
            "formulasMCnoSF_2022",
            "fakeSel",
            "finalSnapshot_MC",
        ]
    },
    "MCl1loose2018v9": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>0)"',
        "subTargets": [
            "leptonMaker",
            "lepSel",
            "jetSelUL",
            "PromptParticlesGenVars",
            "GenVar",
            "GenLeptonMatch",
            "HiggsGenVars",
            "TopGenVars",
            "WGammaStar",
            "DressedLeptons",
        ]
        # 'wwNLL','ggHTheoryUncertainty', 'qqHTheoryUncertainty', 'EFTGen'],
    },
    "MCCorr2018v9": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "subTargets": [
            "baseW",
            # "JES_modules_18UL",
            # "JERsMCUL",
            # # "FatJERsMCUL",
            "btagPerJet_DeepCSV_2018UL",
            "btagPerJet_DeepJet_2018UL",
            # "JetPUID_SF_UL",
            # "rochesterMC",
            "trigMC",
            # "leptonSF",
            # "puW",
            "l2Kin",
            # # "l3Kin",
            # # "l4Kin",
            # "formulasMC",
            # # "EmbeddingVeto",
            # # "wwNLOEWK",
            # # "wwNLOEWK2",
            # # "wzNLOEWK",
            # # "zzNLOEWK",
            # # "zNLOEWK",
            # # "wNLOEWK",
            # # "qqHTheoryUncertainty",
            # # "CleanFatJet",
            # # "BoostedWtagSF",
            # "leptonMVAFiller",
        ],
    },
    "MCFull2018v9": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "subTargets": [
            "MCl1loose2018v9",
            "MCCorr2018v9",
            "finalSnapshot_MC",
        ],
    },

    ########################
    ### Individual steps ###
    ########################

    "leptonMaker": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonMaker",
        "declare": "leptonMaker = lambda : LeptonMaker()",
        "module": "leptonMaker()",
    },

    "lepFiller_hwwMVA": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonFiller_HWWMVA",
        "declare": 'leptonFill_hwwMVA = lambda : LeptonFiller_HWWMVA("RPLME_FW/processor/data/ttH-Run3-LeptonMVA/")',
        "module": "leptonFill_hwwMVA()",
    },

    # For the moment, we use the 2022EE training for all eras.
    "lepFiller_tthMVA": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonFiller_ttHMVA",
        "declare": 'leptonFill_tthMVA = lambda : LeptonFiller_ttHMVA("RPLME_FW/processor/data/ttH-Run3-LeptonMVA", "Muon-mvaTTH.2022EE.weights.xml", "Electron-mvaTTH.2022EE.weights_mvaISO.xml")',
        "module": "leptonFill_tthMVA()",
    },
    
    "lepSel": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonSel",
        "declare": 'leptonSel = lambda : LeptonSel("Loose", 1, "RPLME_CMSSW")',
        "module": "leptonSel()",
    },
    
    "jetSelUL": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.JetSel",
        # jetid=2,pujetid='loose',minpt=15.0,maxeta=4.7, UL2016fix=False "
        "declare": 'jetSel = lambda : JetSel(2,"loose",15.0,4.7,False)',
        "module": "jetSel()",
    },
    
    "jetSelMaskFilter": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.JetSelMask",
        "declare": 'jetSelMask = lambda : JetSelMask(2,"loose",15.0,4.7,False,"RPLME_CMSSW",True)',
        "module": "jetSelMask()",
    },
    
    "jetSelMask": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.JetSelMask",
        "declare": 'jetSelMask = lambda : JetSelMask(2,"loose",15.0,4.7,False,"RPLME_CMSSW")',
        "module": "jetSelMask()",
    },
    
    "fakeSel": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import":  "mkShapesRDF.processor.modules.FakeSel",
        "declare": "fakeSel = lambda : FakeSel()",
        "module":  "fakeSel()",
    },
    
    "lumiMask": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LumiMask",
        "declare": 'lumiMask = lambda : LumiMask("RPLME_FW","RPLME_LUMI")',
        "module": "lumiMask()",
    },
    
    "PromptParticlesGenVars": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.PromptParticlesGenVarsProducer",
        "declare": "PromptParticlesGenVars = lambda : PromptParticlesGenVarsProducer()",
        "module": "PromptParticlesGenVars()",
    },
    
    "GenVar": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.GenVarProducer",
        "declare": "GenVar = lambda : GenVarProducer()",
        "module": "GenVar()",
    },
    
    "GenLeptonMatch": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.GenLeptonMatchProducer",
        "declare": "GenLeptonMatch = lambda : GenLeptonMatchProducer()",
        "module": "GenLeptonMatch()",
    },
    
    "HiggsGenVars": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.HiggsGenVarsProducer",
        "declare": "HiggsGenVars = lambda : HiggsGenVarsProducer()",
        "module": "HiggsGenVars()",
    },
    
    "TopGenVars": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.TopGenVarsProducer",
        "declare": "TopGenVars = lambda : TopGenVarsProducer()",
        "module": "TopGenVars()",
    },
    
    "WGammaStar": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.WGammaStarProducer",
        "declare": "WGammaStar = lambda : WGammaStarProducer()",
        "module": "WGammaStar()",
    },
    
    "DressedLeptons": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.DressedLeptonProducer",
        "declare": "DressedLeptons = lambda : DressedLeptonProducer(0.3)",
        "module": "DressedLeptons()",
    },
    
    "baseW": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.BaseW",
        "declare": "baseW = lambda : BaseW(sampleName, files, xs_db, RPLME_genEventSumw)",
        "module": "baseW()",
    },
    
    "JES_modules": {
        "isChain" : False,
        "do4MC"   : True,
        "do4Data" : False,
        "import"  : "mkShapesRDF.processor.modules.JMECalculator",
        "declare" : 'jmeCalculator = lambda : JMECalculator("RPLME_CMSSW", jet_object="AK4PFPuppi", jes_unc=["Total"], \
        do_Jets=True, do_MET=True, do_Unclustered=True, met_collections = ["PuppiMET", "MET", "RawMET"],do_JER=True, store_nominal=True, store_variations=True)',
        "module"  : "jmeCalculator()",
    },
    
    "l2Kin": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.l2KinProducer",
        "declare": "l2Kin = lambda : l2KinProducer()",
        "module": "l2Kin()",
    },
    
    "l3Kin": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.l3KinProducer",
        "declare": "l3Kin = lambda : l3KinProducer()",
        "module": "l3Kin()",
    },
    
    "l4Kin": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.l4KinProducer",
        "declare": "l4Kin = lambda : l4KinProducer()",
        "module": "l4Kin()",
    },
    
    "puW": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.runDependentPuW",
        "declare": "puWeight = lambda : runDependentPuW('RPLME_CMSSW', files)",
        "module": "puWeight()",
    },
    
    "leptonSF": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonSF",
        "declare": "leptonSF = lambda : LeptonSF('RPLME_CMSSW')",
        "module": "leptonSF()",
    },
    
    # "formulasDATA": {
    #     "isChain": False,
    #     "do4MC": False,
    #     "do4Data": True,
    #     "import": "mkShapesRDF.processor.modules.formulasToAdd_DATA_Full2022EEv11",
    #     "declare": "formulasDATA = lambda : formulasToAdd_DATA_Full2022EEv11()",
    #     "module": "formulasDATA()",
    # },
    
    "formulasDATA_2022EE": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_DATA_Full2022EEv12",
        "declare": "formulasDATA = lambda : formulasToAdd_DATA_Full2022EEv12()",
        "module": "formulasDATA()",
    },
    
    "formulasDATA_2022": {
        "isChain" : False,
        "do4MC" : False,
        "do4Data" : True,
        "import" : "mkShapesRDF.processor.modules.formulasToAdd_DATA_Full2022v12",
        "declare" : "formulasDATA = lambda : formulasToAdd_DATA_Full2022v12()",
        "module" : "formulasDATA()",
    },
    
    "formulasMC": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MC_Full2022EEv11",
        "declare": "formulasMC = lambda : formulasToAdd_MC_Full2022EEv11()",
        "module": "formulasMC()",
    },
    
    "formulasMCnoSF": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MCnoSF_Full2022EEv11",
        "declare": "formulasMC = lambda : formulasToAdd_MCnoSF_Full2022EEv11()",
        "module": "formulasMC()",
    },
    
    "formulasMC_2022": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MC_Full2022v12",
        "declare": "formulasMC = lambda : formulasToAdd_MC_Full2022v12()",
        "module": "formulasMC()",
    },
    
    "formulasMC_2022EE": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MC_Full2022EEv12",
        "declare": "formulasMC = lambda : formulasToAdd_MC_Full2022EEv12()",
        "module": "formulasMC()",
    },

    "formulasMCnoSF_2022": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MCnoSF_Full2022v12",
        "declare": "formulasMC = lambda : formulasToAdd_MCnoSF_Full2022v12()",
        "module": "formulasMC()",
    },
    
    "formulasFAKE_2022FG": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_FAKE_Full2022EEv11",
        "declare": "formulasFAKE = lambda : formulasToAdd_FAKE_Full2022EEv11()",
        "module": "formulasFAKE()",
    },
    
    "formulasFAKE_2022EE": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_FAKE_Full2022EEv12",
        "declare": "formulasFAKE = lambda : formulasToAdd_FAKE_Full2022EEv12()",
        "module": "formulasFAKE()",
    },
    
    "formulasFAKE_2022": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_FAKE_Full2022v12",
        "declare": "formulasFAKE = lambda : formulasToAdd_FAKE_Full2022v12()",
        "module": "formulasFAKE()",
    },
    
    "btagPerJet_DeepCSV_2018UL": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepCSV_2018UL = lambda : btagSFProducerLatinos(2018, "deepCSV", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2018_UL/btagging.json.gz", ["jes","jesAbsolute","jesAbsolute_2018","jesBBEC1","jesBBEC1_2018","jesEC2","jesEC2_2018","jesFlavorQCD","jesHF","jesHF_2018","jesRelativeBal","jesRelativeSample_2018"])',
        "module": "btagPerJet_DeepCSV_2018UL()",
    },
    
    "btagPerJet_DeepJet_2018UL": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepJet_2018UL = lambda : btagSFProducerLatinos(2018, "deepJet", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2018_UL/btagging.json.gz", ["jes","jesAbsolute","jesAbsolute_2018","jesBBEC1","jesBBEC1_2018","jesEC2","jesEC2_2018","jesFlavorQCD","jesHF","jesHF_2018","jesRelativeBal","jesRelativeSample_2018"])',
        "module": "btagPerJet_DeepJet_2018UL()",
    },
    
    ######## 2022 btagging SF
    ## Shape
    "btagPerJet_Summer22_DeepJet_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepJet_shape = lambda : btagSFProducerLatinos(2022, "deepJet", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_DeepJet_shape()",
    },
    
    "btagPerJet_Summer22_PNet_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PNet_shape = lambda : btagSFProducerLatinos(2022, "particleNet", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_PNet_shape()",
    },
    
    "btagPerJet_Summer22_PTransformer_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PTransformer_shape = lambda : btagSFProducerLatinos(2022, "robustParticleTransformer", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2022_Summer22/btagging.json.gz", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_PTransformer_shape()",
    },
    
    "btagPerJet_Summer22EE_DeepJet_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepJet_shape = lambda : btagSFProducerLatinos(2022, "deepJet", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_DeepJet_shape()",
    },
    
    "btagPerJet_Summer22EE_PNet_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PNet_shape = lambda : btagSFProducerLatinos(2022, "particleNet", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_PNet_shape()",
    },
    
    "btagPerJet_Summer22EE_PTransformer_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PTransformer_shape = lambda : btagSFProducerLatinos(2022, "robustParticleTransformer", ["shape"], "shape", "RPLME_FW/processor/data/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_PTransformer_shape()",
    },
    
    ### Fixed WP
    "btagPerJet_Summer22EE_DeepJet_light": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepJet_light = lambda : btagSFProducerLatinos(2022, "deepJet", ["L", "M", "T"], "light", "RPLME_FW/processor/data/scale_factors_BTV/Full2022EEv12/btagging_Summer22EE.json", [])',
        "module": "btagPerJet_DeepJet_light()",
    },
    
    "btagPerJet_Summer22EE_PNet_light": {
	"isChain": False,
	"do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PNet_light = lambda : btagSFProducerLatinos(2022, "particleNet", ["L", "M", "T"], "light", "RPLME_FW/processor/data/scale_factors_BTV/Full2022EEv12/btagging_Summer22EE.json", [])',
        "module": "btagPerJet_PNet_light()",
    },
    
    "btagPerJet_Summer22EE_PTransformer_light": {
	"isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PTransformer_light = lambda : btagSFProducerLatinos(2022, "robustParticleTransformer", ["L", "M", "T"], "light", "RPLME_FW/processor/data/scale_factors_BTV/Full2022EEv12/btagging_Summer22EE.json", [])',
        "module": "btagPerJet_PTransformer_light()",
    },
    
    "trigMC": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.TrigMaker",
        "declare": 'trigMC = lambda : TrigMaker("RPLME_CMSSW", isData=False, keepRunP=False)',
        "module": "trigMC()",
    },
    
    "trigMCnoSF": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.TrigMaker",
        "declare": 'trigMC = lambda : TrigMaker("RPLME_CMSSW", isData=False, keepRunP=False, computeSF=False)',
        "module": "trigMC()",
    },
    
    "trigData": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.TrigMaker",
        "declare": 'trigData = lambda : TrigMaker("RPLME_CMSSW", isData=True, keepRunP=False)',
        "module": "trigData()",
    },
    
    "fakeW": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonFakeWMaker",
        "declare": "fakeW = lambda : LeptonFakeWMaker('RPLME_CMSSW')",
        "module": "fakeW()",
    },
    
    "l2tight": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.L2TightSelection",
        "declare": "l2tightFilter = lambda : L2TightSelection('Full2022v12')",
        "module": "l2tightFilter()",
    },
    
    "finalSnapshot_MC": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.Snapshot",
        "declare": "snapshot = lambda : Snapshot( \
                tmpOutputFilename=RPLME_OUTPUTFILENAMETMP+'/RPLME_OUTPUTFILENAME', \
                columns=['*'], \
                eosPath='RPLME_EOSPATH', outputFilename='RPLME_OUTPUTFILENAME', \
                includeVariations=False, splitVariations=False, storeNominals=True )",
        "module": "snapshot()",
    },
    
    "finalSnapshot_Variations": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.Snapshot",
        "declare": "snapshot = lambda : Snapshot( \
                tmpOutputFilename=RPLME_OUTPUTFILENAMETMP+'/RPLME_OUTPUTFILENAME', \
                columns=['*'], \
                eosPath='RPLME_EOSPATH', outputFilename='RPLME_OUTPUTFILENAME', \
                includeVariations=True, splitVariations=True, storeNominals=False )",
        "module": "snapshot()",
    },
    
    "finalSnapshot_DATA": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.Snapshot",
        "declare": "snapshot = lambda : Snapshot( \
                tmpOutputFilename=RPLME_OUTPUTFILENAMETMP+'/RPLME_OUTPUTFILENAME', \
                columns=['*'], \
                eosPath='RPLME_EOSPATH', outputFilename='RPLME_OUTPUTFILENAME', \
                includeVariations=False, splitVariations=False, storeNominals=True )",
        "module": "snapshot()",
    },
    
    "finalSnapshot_JES": {
        "isChain" : False,
        "do4MC"   : True,
        "do4Data" : False,
        "import"  : "mkShapesRDF.processor.modules.Snapshot",
        "declare" : "snapshot = lambda : Snapshot( \
                tmpOutputFilename=RPLME_OUTPUTFILENAMETMP+'/RPLME_OUTPUTFILENAME', \
                columns=['*'], \
                eosPath='RPLME_EOSPATH', outputFilename='RPLME_OUTPUTFILENAME', \
                includeVariations=True, splitVariations=True, storeNominals=True,\
                )",
        "module": "snapshot()",
    },

    # "finalSnapshot_JES": {
    #     "isChain": False,
    #     "do4MC": True,
    #     "do4Data": False,
    #     "import": "mkShapesRDF.processor.modules.Snapshot",
    #     "declare": "snapshot = lambda : Snapshot( \
    #             tmpOutputFilename=RPLME_OUTPUTFILENAMETMP+'/RPLME_OUTPUTFILENAME', \
    #             columns=['*'], \
    #             eosPath='RPLME_EOSPATH', outputFilename='RPLME_OUTPUTFILENAME', \
    #             includeVariations=True, splitVariations=True, storeNominals=True,\
    #             outputMap={'JES':['JER_0', 'JER_1', 'JER_2', 'JER_3', 'JER_4', 'JER_5', 'JESCorrelationGroupbJES', 'JESCorrelationGroupIntercalibration', 'JESFlavorPureQuark', 'JESFlavorPureGluon', 'JESFlavorPhotonJet', 'JESFlavorZJet', 'JESTotalNoFlavorNoTime', 'JESCorrelationGroupFlavor', 'JESTotalNoTime', 'JESTotalNoFlavor', 'JESTotal', 'JESSubTotalMC', 'JESSubTotalAbsolute', 'JESSubTotalScale', 'JESFlavorPureCharm', 'JESSubTotalPt', 'JESSubTotalPileUp', 'JESPileUpMuZero', 'JESCorrelationGroupUncorrelated', 'JESPileUpEnvelope', 'JESRelativeJERHF', 'JESRelativePtHF', 'JESRelativeJEREC2','JESSubTotalRelative', 'JESRelativeStatFSR', 'JESRelativeJEREC1', 'JESTimePtEta', 'JESFragmentation', 'JESFlavorQCD', 'JESAbsoluteMPFBias', 'JESRelativePtEC1', 'JESAbsoluteFlavMap', 'JESSinglePionECAL', 'JESAbsoluteScale', 'JESSinglePionHCAL', 'JESRelativeFSR', 'JESFlavorPureBottom', 'JESPileUpPtEC1', 'JESPileUpDataMC', 'JESAbsoluteStat', 'JESRelativePtEC2', 'JESPileUpPtEC2', 'JESRelativeBal', 'JESAbsoluteSample', 'JESRelativeSample', 'JESRelativePtBB', 'JESRelativeStatEC', 'JESRelativeStatHF', 'JESPileUpPtRef', 'JESCorrelationGroupMPFInSitu', 'JESPileUpPtBB', 'JESPileUpPtHF'], 'MET':['JER_0', 'JER_1', 'JER_2', 'JER_3', 'JER_4', 'JER_5', 'JESCorrelationGroupbJES', 'JESCorrelationGroupIntercalibration', 'JESFlavorPureQuark', 'JESFlavorPureGluon', 'JESFlavorPhotonJet', 'JESFlavorZJet', 'JESTotalNoFlavorNoTime', 'JESCorrelationGroupFlavor', 'JESTotalNoTime', 'JESTotalNoFlavor', 'JESTotal', 'JESSubTotalMC', 'JESSubTotalAbsolute', 'JESSubTotalScale', 'JESFlavorPureCharm', 'JESSubTotalPt', 'JESSubTotalPileUp', 'JESPileUpMuZero', 'JESCorrelationGroupUncorrelated', 'JESPileUpEnvelope', 'JESRelativeJERHF', 'JESRelativePtHF', 'JESRelativeJEREC2', 'JESSubTotalRelative', 'JESRelativeStatFSR', 'JESRelativeJEREC1', 'JESTimePtEta', 'JESFragmentation', 'JESFlavorQCD', 'JESAbsoluteMPFBias', 'JESRelativePtEC1', 'JESAbsoluteFlavMap', 'JESSinglePionECAL', 'JESAbsoluteScale', 'JESSinglePionHCAL', 'JESRelativeFSR', 'JESFlavorPureBottom', 'JESPileUpPtEC1', 'JESPileUpDataMC', 'JESAbsoluteStat', 'JESRelativePtEC2', 'JESPileUpPtEC2', 'JESRelativeBal', 'JESAbsoluteSample', 'JESRelativeSample', 'JESRelativePtBB', 'JESRelativeStatEC', 'JESRelativeStatHF', 'JESPileUpPtRef', 'JESCorrelationGroupMPFInSitu', 'JESPileUpPtBB', 'JESPileUpPtHF'],} )",
    #     "module": "snapshot()",
    # },
    # "finalSnapshot_JESnoJER": {
    #     "isChain": False,
    #     "do4MC": True,
    #     "do4Data": False,
    #     "import": "mkShapesRDF.processor.modules.Snapshot",
    #     "declare": "snapshot = lambda : Snapshot( \
    #             tmpOutputFilename=RPLME_OUTPUTFILENAMETMP+'/RPLME_OUTPUTFILENAME', \
    #             columns=['*'], \
    #             eosPath='RPLME_EOSPATH', outputFilename='RPLME_OUTPUTFILENAME', \
    #             includeVariations=True, splitVariations=True, storeNominals=True,\
    #             outputMap={'JES':['JESCorrelationGroupbJES', 'JESCorrelationGroupIntercalibration', 'JESFlavorPureQuark', 'JESFlavorPureGluon', 'JESFlavorPhotonJet', 'JESFlavorZJet', 'JESTotalNoFlavorNoTime', 'JESCorrelationGroupFlavor', 'JESTotalNoTime', 'JESTotalNoFlavor', 'JESTotal', 'JESSubTotalMC', 'JESSubTotalAbsolute', 'JESSubTotalScale', 'JESFlavorPureCharm', 'JESSubTotalPt', 'JESSubTotalPileUp', 'JESPileUpMuZero', 'JESCorrelationGroupUncorrelated', 'JESPileUpEnvelope', 'JESRelativeJERHF', 'JESRelativePtHF', 'JESRelativeJEREC2','JESSubTotalRelative', 'JESRelativeStatFSR', 'JESRelativeJEREC1', 'JESTimePtEta', 'JESFragmentation', 'JESFlavorQCD', 'JESAbsoluteMPFBias', 'JESRelativePtEC1', 'JESAbsoluteFlavMap', 'JESSinglePionECAL', 'JESAbsoluteScale', 'JESSinglePionHCAL', 'JESRelativeFSR', 'JESFlavorPureBottom', 'JESPileUpPtEC1', 'JESPileUpDataMC', 'JESAbsoluteStat', 'JESRelativePtEC2', 'JESPileUpPtEC2', 'JESRelativeBal', 'JESAbsoluteSample', 'JESRelativeSample', 'JESRelativePtBB', 'JESRelativeStatEC', 'JESRelativeStatHF', 'JESPileUpPtRef', 'JESCorrelationGroupMPFInSitu', 'JESPileUpPtBB', 'JESPileUpPtHF'], 'MET':['JESCorrelationGroupbJES', 'JESCorrelationGroupIntercalibration', 'JESFlavorPureQuark', 'JESFlavorPureGluon', 'JESFlavorPhotonJet', 'JESFlavorZJet', 'JESTotalNoFlavorNoTime', 'JESCorrelationGroupFlavor', 'JESTotalNoTime', 'JESTotalNoFlavor', 'JESTotal', 'JESSubTotalMC', 'JESSubTotalAbsolute', 'JESSubTotalScale', 'JESFlavorPureCharm', 'JESSubTotalPt', 'JESSubTotalPileUp', 'JESPileUpMuZero', 'JESCorrelationGroupUncorrelated', 'JESPileUpEnvelope', 'JESRelativeJERHF', 'JESRelativePtHF', 'JESRelativeJEREC2', 'JESSubTotalRelative', 'JESRelativeStatFSR', 'JESRelativeJEREC1', 'JESTimePtEta', 'JESFragmentation', 'JESFlavorQCD', 'JESAbsoluteMPFBias', 'JESRelativePtEC1', 'JESAbsoluteFlavMap', 'JESSinglePionECAL', 'JESAbsoluteScale', 'JESSinglePionHCAL', 'JESRelativeFSR', 'JESFlavorPureBottom', 'JESPileUpPtEC1', 'JESPileUpDataMC', 'JESAbsoluteStat', 'JESRelativePtEC2', 'JESPileUpPtEC2', 'JESRelativeBal', 'JESAbsoluteSample', 'JESRelativeSample', 'JESRelativePtBB', 'JESRelativeStatEC', 'JESRelativeStatHF', 'JESPileUpPtRef', 'JESCorrelationGroupMPFInSitu', 'JESPileUpPtBB', 'JESPileUpPtHF'],} )",
    #     "module": "snapshot()",
    # },

    "histogram": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.Histogram",
        "declare": "histogram = lambda : Histogram( \
                outputFilename='output2.root', \
                variables=[(('mjj', 'mjj', 100, 10, 1000), 'new_fw_mjj', 'baseW * genWeight')] \
                    )",
        "module": "histogram()",
    },
}
