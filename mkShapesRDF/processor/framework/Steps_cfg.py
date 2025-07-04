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

    ### 2022
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "l2tight",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "l3Kin",
            "l4Kin",
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "fakeSel",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "finalSnapshot_MC",
        ]
    },

   "MCl2loose2022v12__addTnPMuon": {
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
	    "trigMCnoSF",
            "puW",
	    "addTnPMuon",
        ]
    },

    "MCl2loose2022v12__addTnPElectron": {
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
            "trigMCnoSF",
            "puW",
	    "addTnPElectron",
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "l2tight",
            "finalSnapshot_DATA",
        ],
    },

   "DATAl2loose2022v12__addTnPMuon": {
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
            "formulasDATA",
            "addTnPMuon",
        ],
    },

    "DATAl2loose2022v12__addTnPElectron": {
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
            "formulasDATA",
            "addTnPElectron",
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
            "formulasDATA",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2022v12": {
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
            "formulasDATA",
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "fakeW",
            "formulasFAKE",
            "finalSnapshot_DATA",
        ],
    },

    ### 2022 EE
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "l2tight",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "finalSnapshot_JES",
        ]
    },

    "MCl2loose2022EEv12__addTnPMuon": {
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
	    "trigMCnoSF",
            "puW",
	    "addTnPMuon",
        ]
    },

    "MCl2loose2022EEv12__addTnPElectron": {
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
	    "trigMCnoSF",
            "puW",
	    "addTnPElectron",
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "leptonScale_mc",
            "l2Kin",
            "l3Kin",
            "l4Kin",
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
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
            "formulasDATA",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2022EEv12": {
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
            "formulasDATA",
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
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "fakeW",
            "formulasFAKE",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl2loose2022EEv12__addTnPMuon": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>1)"',
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
            "addTnPMuon"
        ],
    },

    "DATAl2loose2022EEv12__addTnPElectron": {
        "isChain": True,
        "do4MC": False,
        "do4Data": True,
        "selection": '"((nElectron+nMuon)>1)"',
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
            "addTnPElectron"
        ],
    },

    ### 2023
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
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
            "formulasDATA",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2023v12": {
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
            "formulasDATA",
            "finalSnapshot_DATA",
        ],
    },
	
    "DATAl2loose2023v12__addTnPMuon": {
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
            "formulasDATA",
            "addTnPMuon",
        ],
    },
    "DATAl2loose2023v12__addTnPElectron": {
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
            "formulasDATA",
            "addTnPElectron",
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "fakeW",
            "formulasFAKE",
            "finalSnapshot_DATA",
        ],
    },
	
    "MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight": {
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "l2tight",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "finalSnapshot_JES",
        ]
    },
	
    "MCl1loose2023v12__MCCorr2023v12JetScaling__fakeSel": {
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "fakeSel",
            "finalSnapshot_MC",
        ]
    },
    
    "MCl2loose2023v12__addTnPMuon": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>1)"',
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
            "puW",
	    "addTnPMuon",
        ]
    },
	
    "MCl2loose2023v12__addTnPElectron": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>1)"',
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
            "puW",
	    "addTnPElectron",
        ]
    },	

    ### 2023BPix
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
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
            "formulasDATA",
            "fakeSel",
            "finalSnapshot_DATA",
        ],
    },

    "DATAl1loose2023BPixv12": {
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
            "formulasDATA",
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
            "JES_modules_DATA",
            "leptonScale_data",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "fakeW",
            "formulasFAKE",
            "finalSnapshot_DATA",
        ],
    },
	
    "DATAl2loose2023BPixv12__addTnPMuon": {
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
            "formulasDATA",
            "addTnPMuon",
        ],
    },
	
    "DATAl2loose2023BPixv12__addTnPElectron": {
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
            "formulasDATA",
            "addTnPElectron",
        ],
    },
	
    "MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight": {
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "l2tight",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "finalSnapshot_JES",
	]
    },
	
    "MCl1loose2023BPixv12__MCCorr2023BPixv12JetScaling__fakeSel": {
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "fakeSel",
            "finalSnapshot_MC",
        ]
    },
    
    "MCl2loose2023BPixv12__addTnPMuon": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>1)"',
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
            "puW",
	    "addTnPMuon",
        ]
    },
	
    "MCl2loose2023BPixv12__addTnPElectron": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>1)"',
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
            "puW",
	    "addTnPElectron",
        ]
    },

    ######
    ###### 2024
    ######
    
    "DATAl2loose2024v15__addTnPMuon": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "addTnPMuon",
        ],
    },
	
    "DATAl2loose2024v15__addTnPElectron": {
        "isChain" : True,
        "do4MC" : False,
        "do4Data" : True,
        "selection" : '"((nElectron+nMuon)>1)"',
        "subTargets" : [
            "lumiMask",
            "leptonMaker",
            "lepSel",
            "jetSelMask",
            "l2Kin",
            "l3Kin",
            "l4Kin",
            "trigData",
            "formulasDATA",
            "addTnPElectron",
        ],
    },
	
    "MCl2loose2024v15__addTnPMuon": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>1)"',
        "subTargets": [
            "leptonMaker",
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
            "puW",
            "addTnPMuon",
        ]
    },
	
    "MCl2loose2024v15__addTnPElectron": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>1)"',
        "subTargets": [
            "leptonMaker",
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
            "puW",
            "addTnPElectron",
        ]
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
            "formulasFAKE",
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules_MC",
            "l2Kin",
            "formulasMC",
            "l2tight",
            "finalSnapshot_JES",
        ]
    },

    ###
    ### Full set of corrections for Run2022E+FG Prompt : Summer22EE MC campaign
    ###
    "testrecipes": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>=0)"',
        "subTargets": [
            "leptonMaker_nofilter",
            "lepFiller_tthMVA",
            "lepSel_testrecipes",
            "trigMC",
            "leptonSF",
            "finalSnapshot_MC"
        ]
    },
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "JES_modules_MC",
            "l2Kin",
            "formulasMC",
            "l2tight",
            "finalSnapshot_JES",
        ]
    },

    "MCl1loose2022EEv12__MCCorr2022EEv12JetScaling__fakeSel": {
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
            "btagPerJet_DeepJet_shape",
            "btagPerJet_PNet_shape",
            "btagPerJet_PTransformer_shape",
            "trigMC",
            "leptonSF",
            "puW",
            "formulasMC",
            "JES_modules_MC",
            "leptonScale_mc",
            "l2Kin",
            "fakeSel",
            "finalSnapshot_MC",
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
            "formulasMCnoSF",
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
            "formulasMCnoSF",
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
            # "JES_modules_MC_18UL",
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

##### testrecipes ####
    "testrecipes": {
        "isChain": True,
        "do4MC": True,
        "do4Data": False,
        "selection": '"((nElectron+nMuon)>=0)"',
        "subTargets": [
            "leptonMaker_nofilter",
            "lepFiller_tthMVA",
            "lepSel_testrecipes",
            "trigMC",
            "leptonSF",
            "finalSnapshot_MC"
        ]
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


    "leptonMaker_nofilter": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonMaker",
        "declare": "leptonMaker = lambda : LeptonMaker(min_lep_pt=0.)",
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

    "lepSel_testrecipes":{
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonSel",
        "declare": 'leptonSel = lambda : LeptonSel("Loose", 1, "RPLME_CMSSW", True)',
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
    
    "JES_modules_MC": {
        "isChain" : False,
        "do4MC"   : True,
        "do4Data" : False,
        "import"  : "mkShapesRDF.processor.modules.JMECalculator",
        "declare" : 'jmeCalculator = lambda : JMECalculator(jet_object="AK4PFPuppi", jes_unc=["Total"], \
        year = "RPLME_CMSSW", do_Jets=True, do_MET=True, do_Unclustered=True, met_collections = ["PuppiMET", "MET", "RawMET"],do_JER=True, store_nominal=True, store_variations=True, isMC=True, sampleName = "RPLME_SAMPLENAME")',
        "module"  : "jmeCalculator()",
    },

    "JES_modules_DATA": {
        "isChain" : False,
        "do4MC"   : False,
        "do4Data" : True,
        "import"  : "mkShapesRDF.processor.modules.JMECalculator",
        "declare" : 'jmeCalculator = lambda : JMECalculator(jet_object="AK4PFPuppi", jes_unc=["Total"], \
        year = "RPLME_CMSSW", do_Jets=True, do_MET=True, do_Unclustered=True, met_collections = ["PuppiMET", "MET", "RawMET"],do_JER=False, store_nominal=True, store_variations=False, isMC=False, sampleName = "RPLME_SAMPLENAME")',
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

    "leptonScale_data": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonScaleSmearing",
        "declare": "LeptonSS = lambda : LeptonScaleSmearing('RPLME_CMSSW', True, 'RPLME_FW')",
        "module": "LeptonSS()",
    },
    
    "leptonScale_mc": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.LeptonScaleSmearing",
        "declare": "LeptonSS = lambda : LeptonScaleSmearing('RPLME_CMSSW', False, 'RPLME_FW')",
        "module": "LeptonSS()",
    },
    
    "formulasDATA": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_DATA_RunIII",
        "declare": "formulasDATA = lambda : formulasToAdd_DATA_RunIII('RPLME_CMSSW')",
        "module": "formulasDATA()",
    },
    
    "formulasMC": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MC_RunIII",
        "declare": "formulasMC = lambda : formulasToAdd_MC_RunIII('RPLME_CMSSW')",
        "module": "formulasMC()",
    },

    "formulasMCnoSF": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_MCnoSF_RunIII",
        "declare": "formulasMC = lambda : formulasToAdd_MCnoSF_RunIII('RPLME_CMSSW')",
        "module": "formulasMC()",
    },
    
    "formulasFAKE": {
        "isChain": False,
        "do4MC": False,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.formulasToAdd_FAKE_RunIII",
        "declare": "formulasFAKE = lambda : formulasToAdd_FAKE_RunIII('RPLME_CMSSW')",
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
    ######## btagging SF
    ## Shape
    "btagPerJet_DeepJet_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepJet_shape = lambda : btagSFProducerLatinos("RPLME_CMSSW", "deepJet", ["shape"], "shape", "RPLME_FW", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_DeepJet_shape()",
    },    
    "btagPerJet_PNet_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PNet_shape = lambda : btagSFProducerLatinos("RPLME_CMSSW", "particleNet", ["shape"], "shape", "RPLME_FW", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_PNet_shape()",
    },    
    "btagPerJet_PTransformer_shape": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PTransformer_shape = lambda : btagSFProducerLatinos("RPLME_CMSSW", "robustParticleTransformer", ["shape"], "shape", "RPLME_FW", ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD","jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal","jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB","jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"])',
        "module": "btagPerJet_PTransformer_shape()",
    },
    ### Fixed WP
    "btagPerJet_DeepJet_light": {
        "isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_DeepJet_light = lambda : btagSFProducerLatinos("RPLME_CMSSW", "deepJet", ["L", "M", "T"], "light", "RPLME_FW", [])',
        "module": "btagPerJet_DeepJet_light()",
    },    
    "btagPerJet_PNet_light": {
	"isChain": False,
	"do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PNet_light = lambda : btagSFProducerLatinos("RPLME_CMSSW", "particleNet", ["L", "M", "T"], "light", "RPLME_FW", [])',
        "module": "btagPerJet_PNet_light()",
    },    
    "btagPerJet_PTransformer_light": {
	"isChain": False,
        "do4MC": True,
        "do4Data": False,
        "import": "mkShapesRDF.processor.modules.btagSFProducerLatinos",
        "declare": 'btagPerJet_PTransformer_light = lambda : btagSFProducerLatinos("RPLME_CMSSW", "robustParticleTransformer", ["L", "M", "T"], "light", "RPLME_FW", [])',
        "module": "btagPerJet_PTransformer_light()",
    },
    ## --- End b-tagging modules
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

    "addTnPMuon": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.addTnPTree",
        "declare": "doTnP_muon = lambda : addTnPTree('RPLME_CMSSW', 'Muon', True, 'RPLME_EOSPATH', 'RPLME_OUTPUTFILENAME')",
        "module": "doTnP_muon()",
    },
    "addTnPElectron": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.addTnPTree",
        "declare": "doTnP_electron = lambda : addTnPTree('RPLME_CMSSW', 'Electron', True, 'RPLME_EOSPATH', 'RPLME_OUTPUTFILENAME')",
        "module": "doTnP_electron()",
    },
	
    "l2tight": {
        "isChain": False,
        "do4MC": True,
        "do4Data": True,
        "import": "mkShapesRDF.processor.modules.L2TightSelection",
        "declare": "l2tightFilter = lambda : L2TightSelection('RPLME_CMSSW')",
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
