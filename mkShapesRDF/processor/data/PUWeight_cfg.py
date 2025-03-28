####################### PU Weight CFG ##################################

PUCfg = {
    'Full2022v12': {
        'srcfile'     : "auto",
        'targetfiles' : {
            '1-1' : '/processor/data/PUweights/2022/2022BCD_LUM.root',
        },
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True,
    },

    'Full2022EEv12': {
        'srcfile'     : "auto",
        'targetfiles' : {
            '1-2' : '/processor/data/PUweights/2022/2022EFG_LUM.root',
        } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True,
    },

    'Full2022EEv11': {
        'srcfile'     : "auto",
        'targetfiles' : {
            '1-1' : '/processor/data/PUweights/2022/2022_PU.root',
        } ,
        'srchist'     : ["PV_npvsGood", "Rho_fixedGridRhoFastjetCentralCalo", "Rho_fixedGridRhoFastjetCentralChargedPileUp"],
        'targethist'  : ["PV_npvsGood", "Rho_fixedGridRhoFastjetCentralCalo", "Rho_fixedGridRhoFastjetCentralChargedPileUp"],
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : ["PV_npvsGood", "Rho_fixedGridRhoFastjetCentralCalo", "Rho_fixedGridRhoFastjetCentralChargedPileUp"],
        'doSysVar'    : True,
    },

    'Full2018v9' : {
        'srcfile'     : "auto",
        'targetfiles' : {
            '1-1' : '/processor/data/PUweights/2018/UL2018_PU.root',
        },
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True,
    },

    'Full2017v9' : {
        'srcfile'     : "auto",
        'targetfiles' : {
            '1-1' : '/processor/data/PUweights/2017/UL2017B_PU.root',
            '2-2' : '/processor/data/PUweights/2017/UL2017C_PU.root',
            '3-3' : '/processor/data/PUweights/2017/UL2017D_PU.root',
            '4-4' : '/processor/data/PUweights/2017/UL2017E_PU.root',
            '5-5' : '/processor/data/PUweights/2017/UL2017F_PU.root',
        } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True,
    },

    'Full2016v9noHIPM' : {
        'srcfile'     : "auto",
        'targetfiles' : {
            '4-4' : '/processor/data/PUweights/2016/UL2016BCDEF_PU.root',
            '5-7' : '/processor/data/PUweights/2016/UL2016GH_PU.root',
        } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True,
    },

    'Full2016v9HIPM' : {
        'srcfile'     : "auto",
        'targetfiles' : {
            '1-3' : '/processor/data/PUweights/2016/UL2016BCDEF_PU.root',
        } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight",
        'norm'        : True,
        'verbose'     : False,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True,
    },
}
