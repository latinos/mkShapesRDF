####################### PU Weight CFG ##################################

PUCfg = {
    'Full2022v12': {
        'srcfile'     : "auto" ,
        'targetfiles' : { '1-1' : '/processor/data/PUweights/2022/2022BCD_LUM.root' } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight" ,
        'norm'        : True       ,
        'verbose'     : False      ,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True ,
    } ,
    'Full2022EEv12': {
        'srcfile'     : "auto" ,
        'targetfiles' : { '1-2' : '/processor/data/PUweights/2022/2022EFG_LUM.root' } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight" ,
        'norm'        : True       ,
        'verbose'     : False      ,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : True ,
    } ,
    'Full2023v12': {
        'srcfile'     : "auto" ,
        'targetfiles' : { '1-1' : '/processor/data/PUweights/2023/2023BC_LUM.root' } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight" ,
        'norm'        : True       ,
        'verbose'     : False      ,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : False ,
    } ,
    'Full2023BPixv12': {
        'srcfile'     : "auto" ,
        'targetfiles' : { '1-1' : '/processor/data/PUweights/2023/2023D_LUM.root' } ,
        'srchist'     : "pileup",
        'targethist'  : "pileup",
        'name'        : "puWeight" ,
        'norm'        : True       ,
        'verbose'     : False      ,
        'nvtx_var'    : "Pileup_nTrueInt",
        'doSysVar'    : False ,
    } ,
    'Full2022EEv11': {
        'srcfile'     : "auto" ,
        'targetfiles' : { '1-1' : '/processor/data/PUweights/2022/2022_PU.root' } ,
        'srchist'     : ["PV_npvsGood", "Rho_fixedGridRhoFastjetCentralCalo", "Rho_fixedGridRhoFastjetCentralChargedPileUp"],
        'targethist'  : ["PV_npvsGood", "Rho_fixedGridRhoFastjetCentralCalo", "Rho_fixedGridRhoFastjetCentralChargedPileUp"],
        'name'        : "puWeight" ,
        'norm'        : True       ,
        'verbose'     : False      ,
        'nvtx_var'    : ["PV_npvsGood", "Rho_fixedGridRhoFastjetCentralCalo", "Rho_fixedGridRhoFastjetCentralChargedPileUp"],
        'doSysVar'    : True ,
    } ,
}
