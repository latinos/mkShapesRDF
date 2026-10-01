# Cross section DB for Run3 samples
# Units in pb

# References:
#
# A: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MATRIXCrossSectionsat13p6TeV (or https://cms-gen.gitbook.io/cms-generator-central-place/about-cross-sections/higher-order-calculation/matrix_di_boson_xsec_13p6_tev)
# B: https://github.com/cms-sw/genproductions/blob/master/Utilities/calculateXSectionAndFilterEfficiency/calculateXSectionAndFilterEfficiency.sh
# C: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
# D: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef
# E: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap
# F: https://cms-gen.gitbook.io/cms-generator-central-place/about-cross-sections
# G: https://xsecdb-xsdb-official.app.cern.ch/xsdb/
# H: http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2023_179_v6.pdf
# I: https://cms-generators.docs.cern.ch/useful-tools-and-links/HowToGenXSecAnalyzer/
# X: reference unknown. Please provide a valid reference!

xs_db = {}


# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
# BR (H-->WW) = 0.2152
# BR (H-->tt) = 0.06256
# BR (H-->bb) = 0.5824
# BR (H-->ZZ) = 0.02641

# https://pdg.lbl.gov/2024/listings/rpp2024-list-w-boson.pdf
# BR (W-->lv) = 0.1086
# BR (W-->qq) = 0.6741
# BR (W-->m vm) = 0.1078
# BR (W-->e ve) = 0.1071
# BR (W-->t vt) = 0.1138

# https://pdg.lbl.gov/2018/listings/rpp2018-list-z-boson.pdf
# BR (Z-->ee) = 0.033632  
# BR (Z-->mm) = 0.033662
# BR (Z-->tt) = 0.033696
# BR (Z-->qq) = 0.69911

# Higgs xs at 125.38 GeV from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap
# ggH - XS = 51.96 pb
# VBF - XS = 4.067 pb
# WH  - XS = 1.442 pb
# W+H - XS = 0.8801 pb
# W-H - XS = 0.5620 pb 
# ZH  - XS = 0.9361 pb
# qqZH - XS = 0.8014 pb
# ggZH - XS =  0.1347 pb
# ttH - XS = 0.564 pb

### Higgs
xs_db["GluGluHToWWTo2L2Nu_M125"] = ["xsec=1.17381", "kfact=1.000", "ref=E"] # 51.960*0.2152*(3*0.108)*(3*0.108)
xs_db["GluGluHToZZTo4L_M125"] = ["xsec=0.0140", "kfact=1.000", "ref=E"] # 51.960*0.02641*(0.033632+0.033662+0.033696)**2
xs_db["VBFHToWWTo2L2Nu_M125"]    = ["xsec=0.09187", "kfact=1.000", "ref=E"] #  4.067*0.2152*(3*0.108)*(3*0.108)

xs_db["ZH_Hto2Wto2L2Nu_M125"] = ["xsec=0.018104", "kfact=1.000", "ref=E"] # 0.8014 * 0.2152*(3*0.108)*(3*0.108) 
xs_db["ZH_Zto2L_Hto2Wto2L2Nu_M125"] = ["xsec=0.001828", "kfact=1.000", "ref=E"] # 0.8014 * (0.033632+0.033662+0.033696)*0.2152*(3*0.108)*(3*0.108)
xs_db["ZH_Zto2L_Hto2Wto4Q_M125"] = ["xsec=0.007914", "kfact=1.000", "ref=E"] # 0.8014 * (0.033632+0.033662+0.033696)*0.2152*0.6741*0.6741
xs_db["ZH_Zto2L_Hto2WtoLNu2Q_M125"] = ["xsec=0.003803", "kfact=1.000", "ref=E"] # 0.8014 * (0.033632+0.033662+0.033696)*0.2152*0.6741*(3*0.108)
xs_db["ZH_Zto2Q_Hto2Wto2L2Nu_M125"] = ["xsec=0.026333", "kfact=1.000", "ref=E"] # 0.8014 * 0.69911*0.2152*0.6741*(3*0.108)

xs_db["GluGluZH_Hto2Wto2L2Nu_M125"] = ["xsec=0.003043", "kfact=1.000", "ref=E"] # 0.1347 * 0.2152*(3*0.108)*(3*0.108)
xs_db["GluGluZH_Zto2L_Hto2Wto2L2Nu_M125"] = ["xsec=0.000307", "kfact=1.000", "ref=E"] # 0.1347 * (0.033632+0.033662+0.033696)*0.2152*(3*0.108)*(3*0.108)
xs_db["GluGluZH_Zto2L_Hto2Wto4Q_M125"] = ["xsec=0.0013303", "kfact=1.000", "ref=E"] # 0.1347 * (0.033632+0.033662+0.033696)*0.2152*0.6741*0.6741 
xs_db["GluGluZH_Zto2L_Hto2WtoLNu2Q_M125"] = ["xsec=0.000639", "kfact=1.000", "ref=E"] # 0.1347 * (0.033632+0.033662+0.033696)*0.2152*0.6741*(3*0.108)  
xs_db["GluGluZH_Zto2Q_Hto2Wto2L2Nu_M125"] = ["xsec=0.004426", "kfact=1.000", "ref=E"] # 0.1347 * 0.69911*0.2152*0.6741*(3*0.108)  

xs_db["HWplusJ_HToWWTo2L2Nu_WToLNu_M125"] = ["xsec=0.006441", "kfact=1.000", "ref=E"] # 0.8801 * (3*0.108) * 0.2152*(3*0.108)*(3*0.108)
xs_db["HWplusJ_HToWWTo2L2Nu_WTo2Q_M125"] = ["xsec=0.013403", "kfact=1.000", "ref=E"] # 0.8801 * 0.6741 * 0.2152*(3*0.108)*(3*0.108)  
xs_db["HWminusJ_HToWWTo2L2Nu_WToLNu_M125"] = ["xsec=0.004113", "kfact=1.000", "ref=E"] # 0.5620 * (3*0.108) * 0.2152*(3*0.108)*(3*0.108)  
xs_db["HWminusJ_HToWWTo2L2Nu_WTo2Q_M125"] = ["xsec=0.008558", "kfact=1.000", "ref=E"] # 0.5620 * 0.6741 * 0.2152*(3*0.108)*(3*0.108)

xs_db["ttHToNonbb_M125"] = ["xsec=0.235526", "kfact=1.000", "ref=E"] # 0.564 * (1 - 0.5824)

xs_db["GluGluHToTauTau_M125_Powheg"] = ["xsec=3.250617", "kfact=1.000", "ref=E"] # 51.960 * 0.06256
xs_db["VBFHToTauTau_M125"] = ["xsec=0.254431", "kfact=1.000", "ref=E"] # 4.067 * 0.06256

### WW
xs_db["WW"]        = ["xsec=122.1", "kfact=1.000", "ref=A"]  # (XS(pp -> e mu ve vmu) - XS(gg -> e mu ve vmu)) / (BR(W -> mu vmu)*BR(W -> e ve)) = (1.5589-0.1497)/(0.1078*0.1071)
xs_db["WWTo2L2Nu"] = ["xsec=12.96", "kfact=1.000", "ref=A"]  # 122.1 * 0.1086 * 0.1086 * 9
xs_db["WWToLNu2Q"] = ["xsec=53.6", "kfact=1.000", "ref=A"]  # 122.1 * 2 * BR(W->qq) * BR(W->l nu) = 122.1 * 2 * 0.6741 * 0.3258
xs_db["WWTo4Q"]    = ["xsec=55.5", "kfact=1.000", "ref=A"]  # 122.1 * BR(W->qq)^2 = 122.1 * 0.6741 * 0.6741

xs_db["GluGlutoContintoWWtoENuENu"]     = ["xsec=0.0744", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoENuMuNu"]    = ["xsec=0.0749", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoENuTauNu"]   = ["xsec=0.0790", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoMuNuENu"]    = ["xsec=0.0749", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoMuNuMuNu"]   = ["xsec=0.0753", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoMuNuTauNu"]  = ["xsec=0.0795", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoTauNuENu"]   = ["xsec=0.0790", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoTauNuMuNu"]  = ["xsec=0.0795", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoTauNuTauNu"] = ["xsec=0.0840", "kfact=1.000", "ref=A"]

xs_db["WpWmJJ_EWK_noTop"] = ["xsec=0.1012", "kfact=1.000", "ref=I"] # GenXSecAnalyzer output: 1.012e-01 +/- 4.467e-05

xs_db["WpWmJJ_EWK_noTop"] = ["xsec=0.101", "kfact=1.000", "ref=I"] #inclusive in polarization
xs_db["WpWmJJ_EWK_noTop_pol_LL"] = ["xsec=0.005605", "kfact=1.000", "ref=I"] #also cross-checked by calculating the quantity of XS(pp -> W{0}W{0}jj)*(3*BR(W -> lnu))^2
xs_db["WpWmJJ_EWK_noTop_pol_LT"] = ["xsec=0.01684", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_EWK_noTop_pol_TL"] = ["xsec=0.01767", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_EWK_noTop_pol_TT"] = ["xsec=0.05965", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_EWK_noTop_CMWW_pol_LL"] = ["xsec=0.00757", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_EWK_noTop_CMWW_pol_LT"] = ["xsec=0.01589", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_EWK_noTop_CMWW_pol_TL"] = ["xsec=0.01679", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_EWK_noTop_CMWW_pol_TT"] = ["xsec=0.05956", "kfact=1.000", "ref=I"]
xs_db["WpWmJJ_QCD_noTop"] = ["xsec=2.675", "kfact=1.000", "ref=I"]

xs_db["WWTo2L2Nu_LL"] = ["xsec=0.488",  "kfact=1.000", "ref=X"] ## 4.598 * 9 * BR(W->lnu) * BR(W->lnu) / BR(W->lnu) = 0.1086
xs_db["WWTo2L2Nu_TT"] = ["xsec=6.266",  "kfact=1.000", "ref=X"] ## 59.03
xs_db["WWTo2L2Nu_LT"] = ["xsec=0.911",  "kfact=1.000", "ref=X"] ## 8.582
xs_db["WWTo2L2Nu_TL"] = ["xsec=0.911",  "kfact=1.000", "ref=X"] ## 8.582
xs_db["ggWW_LL"]      = ["xsec=0.025",  "kfact=1.000", "ref=X"] ## 0.239
xs_db["ggWW_TT"]      = ["xsec=0.329",  "kfact=1.000", "ref=X"] ## 3.104
xs_db["ggWW_LT"]      = ["xsec=0.0087", "kfact=1.000", "ref=X"] ## 0.08195
xs_db["ggWW_TL"]      = ["xsec=0.0087", "kfact=1.000", "ref=X"] ## 0.08195

xs_db["WWG"]        = ["xsec=0.3959", "kfact=1.0", "ref=G"]      # inclusive WWγ
xs_db["WWGtoLNu2QG"] = ["xsec=0.359", "kfact=1.0", "ref=G"]      # lν qq γ final state

### SS WW
xs_db['VBS_SSWW']           = ["xsec=0.05891", "kfact=1.0", "ref=I"] #inclusive in polarization
# xs_db['WpWp_EWK_PWG']       = ["xsec=", "kfact=1.0", "ref=I"] #inclusive in polarization, only ++ charge
# xs_db['WmWm_EWK_PWG']       = ["xsec=", "kfact=1.0", "ref=I"] #inclusive in polarization, only -- charge
xs_db['VBS_SSWW_LL']        = ["xsec=0.002183", "kfact=1.0", "ref=I"]
xs_db['VBS_SSWW_WWCM_LL']   = ["xsec=0.003213", "kfact=1.0", "ref=I"]
xs_db['VBS_SSWW_TL']        = ["xsec=0.01150", "kfact=1.0", "ref=I"]
xs_db['VBS_SSWW_WWCM_TL']   = ["xsec=0.009951", "kfact=1.0", "ref=I"]
xs_db['VBS_SSWW_TT']        = ["xsec=0.01762", "kfact=1.0", "ref=I"]
xs_db['VBS_SSWW_WWCM_TT']   = ["xsec=0.01813", "kfact=1.0", "ref=I"]

### Top
xs_db["TTTo2L2Nu"]                    = ["xsec=98.036", "kfact=1.000", "ref=C"] # 923.6 * (3*0.1086) * (3*0.1086)
xs_db["TTTo2L2Nu_TuneCP5Up"]          = ["xsec=98.036", "kfact=1.000", "ref=C"]
xs_db["TTTo2L2Nu_TuneCP5Down"]        = ["xsec=98.036", "kfact=1.000", "ref=C"]
xs_db["TTToSemiLeptonic"]             = ["xsec=406.82", "kfact=1.000", "ref=C"] # 923.6 * 0.6760 * 0.1086 * 3 * 2 
xs_db["TTToSemiLeptonic_TuneCP5Up"]   = ["xsec=406.82", "kfact=1.000", "ref=C"]
xs_db["TTToSemiLeptonic_TuneCP5Down"] = ["xsec=406.82", "kfact=1.000", "ref=C"]
xs_db["TTTo4Q"]                       = ["xsec=419.69", "kfact=1.000", "ref=C"] # 923.6 * 0.6741 * 0.6741

xs_db["ST_tW_top"]        = ["xsec=19.30", "kfact=1.000", "ref=D"] # 43.95 * 2*(3*0.1086*0.6741)
xs_db["ST_tW_antitop"]    = ["xsec=19.30", "kfact=1.000", "ref=D"] # 43.95 * 2*(3*0.1086*0.6741)
xs_db["TWminusto2L2Nu"]   = ["xsec=4.665", "kfact=1.000", "ref=D"] # 43.95 * (3*0.1086) * (3*0.1086)
xs_db["TbarWplusto2L2Nu"] = ["xsec=4.665", "kfact=1.000", "ref=D"] # 43.95 * (3*0.1086) * (3*0.1086)

xs_db["ST_t-channel_top"]     = ["xsec=145.0", "kfact=1.000", "ref=D"]
xs_db["ST_t-channel_antitop"] = ["xsec=87.2",  "kfact=1.000", "ref=D"]
xs_db["ST_s-channel_plus"]    = ["xsec=2.360", "kfact=1.000", "ref=D"] # 7.244 * (3*0.1086)
xs_db["ST_s-channel_minus"]   = ["xsec=1.477", "kfact=1.000", "ref=D"] # 4.534 * (3*0.1086)

### TTX
xs_db["TTNuNu"] = ["xsec=0.1638", "kfact=1.000", "ref=G"]
xs_db["TTLL_MLL-4to50"] = ["xsec=0.03949", "kfact=1.000", "ref=G"]
xs_db["TTLL_MLL-50"] = ["xsec=0.08646", "kfact=1.000", "ref=G"]
xs_db["TTZ-ZtoQQ"] = ["xsec=0.6603", "kfact=1.000", "ref=G"]
xs_db["TTLNu"] = ["xsec=0.2505", "kfact=1.000", "ref=G"]
xs_db["TTW-WtoQQ"] = ["xsec=0.4678", "kfact=1.000", "ref=G"]
xs_db["TTHtoNon2B"] = ["xsec=0.2398", "kfact=1.000", "ref=G"] # 0.5742 * [1 - BR(H->bb)] = 0.5742 * (1 - 0.5824) = 0.2398
xs_db["TTHto2B"] = ["xsec=0.3344", "kfact=1.000", "ref=G"] # 0.5742 * BR(H->bb) = 0.5742 * 0.5824 = 0.3344
xs_db["TTTT"] = ["xsec=0.009652", "kfact=1.000", "ref=G"]

### TTG
xs_db["TTG"] = ["xsec=4.63", "kfact=1.000", "ref=G"]
xs_db["TTG_PTG-10to100"] = ["xsec=4.22", "kfact=1.000", "ref=G"]
xs_db["TTG_PTG-100to200"] = ["xsec=0.41", "kfact=1.000", "ref=G"]
xs_db["TTG_PTG-200"] = ["xsec=0.13", "kfact=1.000", "ref=G"]

### TXX
xs_db["THW"] = ["xsec=0.133", "kfact=1.000", "ref=G"]
xs_db["THQ"] = ["xsec=0.744", "kfact=1.000", "ref=G"]
xs_db["TZQB-ZTo2L"] = ["xsec=0.07968", "kfact=1.000", "ref=G"]
#xs_db["TWZ"] = ["xsec=", "kfact=1.000", "ref="]

### WZ
xs_db["WZTo3LNu"]  = ["xsec=5.32",    "kfact=1.000", "ref=A"] # (XS(pp->e- e+ μ-  ̄vμ) + XS(pp->e- e+ μ+ vμ)) * 9 * BR(ZW->ll lv) / BR(ZW->ee mv)  (0.2385 + 0.3474) * 9 *  0.0036552588 / 0.0036255296
xs_db["WZ"]        = ["xsec=53.9",    "kfact=1.000", "ref=A"] # XS(WZTo3LNu) / (3*9*BR(WZ->lv ll))
xs_db["WZTo2L2Q"]  = ["xsec=3.67",    "kfact=1.000", "ref=A"] # XS(WZ) * 3*BR(Z->ll) * BR(W->qq)
xs_db["WZToLNu2Q"] = ["xsec=11.87", "kfact=1.000", "ref=A"]  # XS(WZ) * 3* BR(W->l nu) * BR(Z->qq) = 53.9 * 0.3258 * 0.6760
xs_db["WZToL3Nu"] = ["xsec=3.51", "kfact=1.000", "ref=A"] # 53.9 * (3*0.1086) * 0.20
xs_db["WZTo2Q2Nu"] = ["xsec=7.26", "kfact=1.000", "ref=A"] # 53.9 * 0.6741 * 0.20
xs_db["WZG"]       = ["xsec=0.08425", "kfact=1.000", "ref=X"]

### VH
xs_db["WminusH-HtoBB_WToLNu"] = ["xsec=0.1066", "kfact=1.000", "ref=E"]  # 0.562032 * BR(H->bb) * BR(W->l nu) = 0.562032 * 0.5824 * 0.3258
xs_db["WplusH-HtoBB_WToLNu"]  = ["xsec=0.1669", "kfact=1.000", "ref=E"]  # 0.880114 * BR(H->bb) * BR(W->l nu) = 0.880114 * 0.5824 * 0.3258
xs_db["WminusH-HtoBB_WTo2Q"]  = ["xsec=0.2213", "kfact=1.000", "ref=E"]  # 0.562032 * BR(H->bb) * BR(W->qq) = 0.562032 * 0.5824 * 0.6760
xs_db["WplusH-HtoBB_WTo2Q"]   = ["xsec=0.3467", "kfact=1.000", "ref=E"]  # 0.880114 * BR(H->bb) * BR(W->qq) = 0.880114 * 0.5824 * 0.6760

xs_db["VH-HToNon2B"]          = ["xsec=0.9939", "kfact=1.000", "ref=E"]  # (0.880114 + 0.562032 + 0.9361) * [1 - BR(H->bb)] = 2.378246 * (1 - 0.5824)
xs_db["WplusH-HtoNon2B"]          = ["xsec=0.3675", "kfact=1.000", "ref=E"]  # 0.880114 * [1 - BR(H->bb)] = 0.880114 * 0.4176 = 0.3675
xs_db["WminusH-HtoNon2B"]          = ["xsec=0.2347", "kfact=1.000", "ref=E"]  # 0.562032 * [1 - BR(H->bb)] = 0.562032 * 0.4176 = 0.2347

xs_db["ZH-HtoNon2B"]      = ["xsec=0.391", "kfact=1.000", "ref=E"]  # 0.9361 * [1 - BR(H->bb)] = 0.9361 * 0.4176 = 0.391
xs_db["ZH-HTo2B_ZTo2Nu"]      = ["xsec=0.1090", "kfact=1.000", "ref=E"]  # 0.9361 * BR(H->bb) * BR(Z->nu nu) = 0.9361 * 0.5824 * 0.2000

### Zg
xs_db["ZGToLLG"]     = ["xsec=1.075", "kfact=1.000", "ref=X"]
xs_db["ZG"]          = ["xsec=1.075", "kfact=1.000", "ref=X"]
xs_db["ZG2JtoG2L2J"] = ["xsec=1.075", "kfact=0.1142", "ref=G"]

### Wg
#xs_db["WGtoLNuG-1J_PTG10to100"]  = ["xsec=662.2",    "kfact=1.000", "ref=G"]
#xs_db["WGtoLNuG-1J_PTG100to200"] = ["xsec=2.221",    "kfact=1.000", "ref=G"]
#xs_db["WGtoLNuG-1J_PTG200to400"] = ["xsec=0.2908",   "kfact=1.000", "ref=G"]
#xs_db["WGtoLNuG-1J_PTG400to600"] = ["xsec=0.02231",  "kfact=1.000", "ref=G"]
#xs_db["WGtoLNuG-1J_PTG600"]      = ["xsec=0.004907", "kfact=1.000", "ref=G"]

### WG
xs_db['WGtoLNuG-1J']             = ["xsec=671.5",    "kfact=1.000", "ref=G"] # XSDB 
xs_db['WGtoLNuG-1J_PTG10to100']  = ["xsec=215.7",    "kfact=1.000", "ref=G"] # XS * BR (W-->lv) = 0.1086*3 --> The BR is an error in the config a k-factor should be added to match the XSDB value
xs_db['WGtoLNuG-1J_PTG100to200'] = ["xsec=0.7236",   "kfact=1.000", "ref=G"] # XS * BR (W-->lv) = 0.1086*3 --> The BR is an error in the config a k-factor should be added to match the XSDB value
xs_db['WGtoLNuG-1J_PTG200to400'] = ["xsec=0.09474",  "kfact=1.000", "ref=G"] # XS * BR (W-->lv) = 0.1086*3 --> The BR is an error in the config a k-factor should be added to match the XSDB value
xs_db['WGtoLNuG-1J_PTG400to600'] = ["xsec=0.007269", "kfact=1.000", "ref=G"] # XS * BR (W-->lv) = 0.1086*3 --> The BR is an error in the config a k-factor should be added to match the XSDB value
xs_db['WGtoLNuG-1J_PTG100']      = ["xsec=0.8352",   "kfact=1.000", "ref=B"] # XS * BR (W-->lv) = 0.1086*3 --> The BR is an error in the config a k-factor should be added to match the XSDB value
# xs_db['WGtoLNuG-1J_PTG200']      = ["xsec=",   "kfact=1.000", "ref="]
# xs_db['WGtoLNuG-1J_PTG400']      = ["xsec=0.02661",  "kfact=1.000", "ref=G"]
xs_db['WGtoLNuG-1J_PTG600']      = ["xsec=0.001599", "kfact=1.000", "ref=G"] # XS * BR (W-->lv) = 0.1086*3 --> The BR is an error in the config a k-factor should be added to match the XSDB value

### ZZ
xs_db["ZZ"]        = ["xsec=16.7",   "kfact=1.000", "ref=X"]
xs_db["ZZTo2L2Nu"] = ["xsec=1.1341", "kfact=1.000", "ref=X"]
xs_db["ZZTo2Q2Nu"] = ["xsec=4.67",   "kfact=1.000", "ref=X"]
xs_db["ZZTo2L2Q"]  = ["xsec=7.4668", "kfact=1.000", "ref=X"]
xs_db["ZZTo4L"]    = ["xsec=1.5290", "kfact=1.000", "ref=X"]

# VVV
xs_db["WWW"] = ["xsec=0.23280", "kfact=1.000", "ref=X"]
xs_db["WWZ"] = ["xsec=0.18510", "kfact=1.000", "ref=X"]
xs_db["WZZ"] = ["xsec=0.06206", "kfact=1.000", "ref=X"]
xs_db["ZZZ"] = ["xsec=0.01591", "kfact=1.000", "ref=X"]

# W+Jets
xs_db["WToLNu-2Jets"] = ["xsec=63396.0", "kfact=1.000", "ref=A"]

xs_db["WtoLNu-4Jets_MLNu-0to120_HT-40to100"] = ["xsec=4254", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-0to120_HT-100to400"] = ["xsec=1626", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-0to120_HT-400to800"] = ["xsec=59.99", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-0to120_HT-800to1500"] = ["xsec=6.23", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-0to120_HT-1500to2500"] = ["xsec=0.4477", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-0to120_HT-2500"] = ["xsec=0.03075", "kfact=1.000", "ref=G"]

xs_db["WtoLNu-4Jets_MLNu-120_HT-40to100"] = ["xsec=20.56", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-120_HT-100to400"] = ["xsec=10.19", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-120_HT-400to800"] = ["xsec=0.5239", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-120_HT-800to1500"] = ["xsec=0.06255", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-120_HT-1500to2500"] = ["xsec=0.005066", "kfact=1.000", "ref=G"]
xs_db["WtoLNu-4Jets_MLNu-120_HT-2500"] = ["xsec=0.0003788", "kfact=1.000", "ref=G"]

xs_db["WToENu-2Jet"] = ["xsec=21132.0", "kfact=1.000", "ref=A"]
xs_db["WToMuNu-2Jet"] = ["xsec=21132.0", "kfact=1.000", "ref=A"]
xs_db["WToTauNu-2Jet"] = ["xsec=21132.0", "kfact=1.000", "ref=A"]

xs_db["WToLNu-1Jet-LO"] = ["xsec=9084.0", "kfact=1.000", "ref=A"]
xs_db["WToLNu-2Jet-LO"] = ["xsec=2925.0", "kfact=1.000", "ref=A"]

# DY
xs_db["DYJetsToLL_M-50-LO"]      = ["xsec=6275.1",  "kfact=1.000", "ref=A"] # 2091.7 * 3
xs_db["DYto2L-2Jets_MLL-50"]     = ["xsec=6275.1",  "kfact=1.000", "ref=A"] # 2091.7 * 3
xs_db["DYto2L-2Jets_MLL-10to50"] = ["xsec=19982.5", "kfact=1.000", "ref=H"]

xs_db["DYto2E-2Jets_MLL-10to50"] = ["xsec=6660.8", "kfact=1.000", "ref=H"] # 19982.5 / 3 
xs_db["DYto2E-2Jets_MLL-50"]     = ["xsec=2091.7",  "kfact=1.000", "ref=A"]
xs_db["DYto2E-2Jets_MLL-50-LO"]  = ["xsec=2091.7",  "kfact=1.000", "ref=A"]

xs_db["DYto2Mu-2Jets_MLL-10to50"] = ["xsec=6660.8", "kfact=1.000", "ref=H"]
xs_db["DYto2Mu-2Jets_MLL-50"]     = ["xsec=2091.7",  "kfact=1.000", "ref=A"]
xs_db["DYto2Mu-2Jets_MLL-50-LO"]  = ["xsec=2091.7",  "kfact=1.000", "ref=A"]

xs_db["DYto2Tau-2Jets_MLL-10to50"] = ["xsec=6660.8", "kfact=1.000", "ref=H"]
xs_db["DYto2Tau-2Jets_MLL-50"]     = ["xsec=2091.7",  "kfact=1.000", "ref=A"]
xs_db["DYto2Tau-2Jets_MLL-50-LO"]  = ["xsec=2091.7",  "kfact=1.000", "ref=A"]

xs_db["DYto2Tau-2Jets_MLL-50_0J"]     = ["xsec=1682.0",  "kfact=1.000", "ref=A"] # Tbh, shamelessly copied from Htautau
xs_db["DYto2Tau-2Jets_MLL-50_1J"]     = ["xsec=318.1",  "kfact=1.000", "ref=A"]
xs_db["DYto2Tau-2Jets_MLL-50_2J"]     = ["xsec=120.6",  "kfact=1.000", "ref=A"]

# DYG
xs_db["DYGto2LG-1Jets_MLL-4to50_PTG-10to100"]      = ["xsec=88.17",     "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-4to50_PTG-10to100_ext1"] = ["xsec=88.17",     "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-4to50_PTG-100to200"]     = ["xsec=0.2413",    "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-4to50_PTG-200"]          = ["xsec=0.02224",   "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-50_PTG-10to100"]         = ["xsec=126.6",     "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-50_PTG-100to200"]        = ["xsec=0.3493",    "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-50_PTG-200to400"]        = ["xsec=0.04331",   "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-50_PTG-400to600"]        = ["xsec=0.00313",   "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_MLL-50_PTG-600"]             = ["xsec=0.0006528", "kfact=1.000", "ref=G"]
xs_db["DYGto2LG-1Jets_Bin-MLL-50"]                 = ["xsec=127.1",     "kfact=1.000", "ref=B"]
xs_db["DYGto2LG-1Jets_Bin-MLL-4to50"]              = ["xsec=88.45",     "kfact=1.000", "ref=B"]

# QCD
xs_db["QCD_PT-15to20_MuEnrichedPt5"]    = ["xsec=2960000.0", "kfact=1.000", "ref=G"]
xs_db["QCD_PT-20to30_MuEnrichedPt5"]    = ["xsec=2679000.0", "kfact=1.000", "ref=G"]
xs_db["QCD_PT-30to50_MuEnrichedPt5"]    = ["xsec=1497000.0", "kfact=1.000", "ref=G"]
xs_db["QCD_PT-50to80_MuEnrichedPt5"]    = ["xsec=409500.0",  "kfact=1.000", "ref=G"]
xs_db["QCD_PT-80to120_MuEnrichedPt5"]   = ["xsec=95130.0",   "kfact=1.000", "ref=G"]
xs_db["QCD_PT-120to170_MuEnrichedPt5"]  = ["xsec=22980.0",   "kfact=1.000", "ref=G"]
xs_db["QCD_PT-170to300_MuEnrichedPt5"]  = ["xsec=7763.0",    "kfact=1.000", "ref=G"]
xs_db["QCD_PT-300to470_MuEnrichedPt5"]  = ["xsec=699.1",     "kfact=1.000", "ref=G"]
xs_db["QCD_PT-470to600_MuEnrichedPt5"]  = ["xsec=68.24",     "kfact=1.000", "ref=G"]
xs_db["QCD_PT-600to800_MuEnrichedPt5"]  = ["xsec=21.37",     "kfact=1.000", "ref=G"]
xs_db["QCD_PT-800to1000_MuEnrichedPt5"] = ["xsec=3.913",     "kfact=1.000", "ref=G"]
xs_db["QCD_PT-1000_MuEnrichedPt5"]      = ["xsec=1.323",     "kfact=1.000", "ref=G"]

xs_db['QCD_PT-10to30_EMEnriched']   = ["xsec=6854000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-20to30_EMEnriched']   = ["xsec=5100000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-30to50_EMEnriched']   = ["xsec=6698000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-50to80_EMEnriched']   = ["xsec=2113000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-80to120_EMEnriched']  = ["xsec=394100.0",  "kfact=1.000", "ref=G"]
xs_db['QCD_PT-120to170_EMEnriched'] = ["xsec=70290.0",   "kfact=1.000", "ref=G"]
xs_db['QCD_PT-170to300_EMEnriched'] = ["xsec=17920.0",   "kfact=1.000", "ref=G"]
xs_db['QCD_PT-300toInf_EMEnriched'] = ["xsec=1224.0",    "kfact=1.000", "ref=G"]

xs_db['QCD_PT-15to20_bcToE']   = ["xsec=2283000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-20to30_bcToE']   = ["xsec=2045000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-30to80_bcToE']   = ["xsec=1322000.0", "kfact=1.000", "ref=G"]
xs_db['QCD_PT-80to170_bcToE']  = ["xsec=74510.0",   "kfact=1.000", "ref=G"]
xs_db['QCD_PT-170to250_bcToE'] = ["xsec=3898.0",    "kfact=1.000", "ref=G"]
xs_db['QCD_PT-250toInf_bcToE'] = ["xsec=963.4",     "kfact=1.000", "ref=G"]

### AC ggH (dummy values)
xs_db['H0PM_ToWWTo2L2Nu']    = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['H0PH_ToWWTo2L2Nu']    = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['H0M_ToWWTo2L2Nu']     = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['H0L1_ToWWTo2L2Nu']    = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['H0PHf05_ToWWTo2L2Nu'] = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['H0Mf05_ToWWTo2L2Nu']  = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['H0L1f05_ToWWTo2L2Nu'] = ["xsec=1.00",     "kfact=1.00", "ref=X"]

### AC VBF (dummy values)
xs_db['VBF_H0PM_ToWWTo2L2Nu']      = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['VBF_H0PH_ToWWTo2L2Nu']      = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['VBF_H0M_ToWWTo2L2Nu']       = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['VBF_H0L1_ToWWTo2L2Nu']      = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['VBF_H0PHf05_ToWWTo2L2Nu']   = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['VBF_H0Mf05_ToWWTo2L2Nu']    = ["xsec=1.00",     "kfact=1.00", "ref=X"] 
xs_db['VBF_H0L1f05_ToWWTo2L2Nu']   = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['VBF_H0LZgf05_ToWWTo2L2Nu']  = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['VBF_H0PHZgf05_ToWWTo2L2Nu'] = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['VBF_H0MZgf05_ToWWTo2L2Nu']  = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['VBF_H0PHggf05_ToWWTo2L2Nu'] = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['VBF_H0Mggf05_ToWWTo2L2Nu']  = ["xsec=1.00",     "kfact=1.00", "ref=X"]

### AC WH (dummy values)
xs_db['WH_H0PM_ToWWTo2L2Nu']     = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['WH_H0PH_ToWWTo2L2Nu']     = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['WH_H0M_ToWWTo2L2Nu']      = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['WH_H0L1_ToWWTo2L2Nu']     = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['WH_H0PHf05_ToWWTo2L2Nu']  = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['WH_H0Mf05_ToWWTo2L2Nu']   = ["xsec=1.00",     "kfact=1.00", "ref=X"]
xs_db['WH_H0L1f05_ToWWTo2L2Nu']  = ["xsec=1.00",     "kfact=1.00", "ref=X"]

# NPS-26-025 : DMsimp_spin0 samples
# ttDM inclusive pseudoscalar
xs_db['TTDMsimpSpin0_ps_mphi-10'] = ["xsec=0.5036", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-50'] = ["xsec=0.3467", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-100'] = ["xsec=0.2211", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-150'] = ["xsec=0.1446", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-200'] = ["xsec=0.1025", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-250'] = ["xsec=0.07033", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-300'] = ["xsec=0.04925", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-350'] = ["xsec=0.0286", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-400'] = ["xsec=0.01486", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-500'] = ["xsec=0.00687", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-600'] = ["xsec=0.003735", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-700'] = ["xsec=0.002241", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-800'] = ["xsec=0.001406", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-1000'] = ["xsec=0.000064", "kfact=1.000", "ref=I"]

# ttDM inclusive pseudoscalar extension
xs_db['TTDMsimpSpin0_ps_mphi-10_ext1'] = ["xsec=0.5036", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-50_ext1'] = ["xsec=0.3467", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-100_ext1'] = ["xsec=0.2211", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-150_ext1'] = ["xsec=0.1446", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-200_ext1'] = ["xsec=0.1025", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-250_ext1'] = ["xsec=0.07033", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-300_ext1'] = ["xsec=0.04925", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-350_ext1'] = ["xsec=0.0286", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-400_ext1'] = ["xsec=0.01486", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-500_ext1'] = ["xsec=0.00687", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-600_ext1'] = ["xsec=0.003735", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-700_ext1'] = ["xsec=0.002241", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-800_ext1'] = ["xsec=0.001406", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_ps_mphi-1000_ext1'] = ["xsec=0.000064", "kfact=1.000", "ref=I"]

# ttDM inclusive scalar
xs_db['TTDMsimpSpin0_s_mphi-10'] = ["xsec=21.68", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-50'] = ["xsec=3.378", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-100'] = ["xsec=0.807", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-150'] = ["xsec=0.2759", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-200'] = ["xsec=0.116", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-250'] = ["xsec=0.06116", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-300'] = ["xsec=0.03719", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-350'] = ["xsec=0.02476", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-400'] = ["xsec=0.0149", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-500'] = ["xsec=0.006567", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-600'] = ["xsec=0.003555", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-700'] = ["xsec=0.002007", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-800'] = ["xsec=0.001282", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-1000'] = ["xsec=0.0005502", "kfact=1.000", "ref=I"]

# ttDM inclusive scalar extension
xs_db['TTDMsimpSpin0_s_mphi-10_ext1'] = ["xsec=21.68", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-50_ext1'] = ["xsec=3.378", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-100_ext1'] = ["xsec=0.807", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-150_ext1'] = ["xsec=0.2759", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-200_ext1'] = ["xsec=0.116", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-250_ext1'] = ["xsec=0.06116", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-300_ext1'] = ["xsec=0.03719", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-350_ext1'] = ["xsec=0.02476", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-400_ext1'] = ["xsec=0.0149", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-500_ext1'] = ["xsec=0.006567", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-600_ext1'] = ["xsec=0.003555", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-700_ext1'] = ["xsec=0.002007", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-800_ext1'] = ["xsec=0.001282", "kfact=1.000", "ref=I"]
xs_db['TTDMsimpSpin0_s_mphi-1000_ext1'] = ["xsec=0.0005502", "kfact=1.000", "ref=I"]

# ttDM dilepton pseudoscalar
xs_db['TTto2LDMsimpSpin0_ps_mphi-10'] = ["xsec=0.0566", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-50'] = ["xsec=0.0392", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-100'] = ["xsec=0.02461", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-150'] = ["xsec=0.01622", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-200'] = ["xsec=0.01137", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-250'] = ["xsec=0.007778", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-300'] = ["xsec=0.005589", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-350'] = ["xsec=0.003152", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-400'] = ["xsec=0.001648", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-500'] = ["xsec=0.000774", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-600'] = ["xsec=0.0004187", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-700'] = ["xsec=0.0002469", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-800'] = ["xsec=0.0001557", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-1000'] = ["xsec=0.000065", "kfact=1.000", "ref=I"]

# ttDM dilepton pseudoscalar extension
xs_db['TTto2LDMsimpSpin0_ps_mphi-10_ext1'] = ["xsec=0.0566", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-50_ext1'] = ["xsec=0.0392", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-100_ext1'] = ["xsec=0.02461", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-150_ext1'] = ["xsec=0.01622", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-200_ext1'] = ["xsec=0.01137", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-250_ext1'] = ["xsec=0.007778", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-300_ext1'] = ["xsec=0.005589", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-350_ext1'] = ["xsec=0.003152", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-400_ext1'] = ["xsec=0.001648", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-500_ext1'] = ["xsec=0.000774", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-600_ext1'] = ["xsec=0.0004187", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-700_ext1'] = ["xsec=0.0002469", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-800_ext1'] = ["xsec=0.0001557", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_ps_mphi-1000_ext1'] = ["xsec=0.000065", "kfact=1.000", "ref=I"]

# ttDM dilepton scalar
xs_db['TTto2LDMsimpSpin0_s_mphi-10'] = ["xsec=2.432", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-50'] = ["xsec=0.3894", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-100'] = ["xsec=0.09028", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-150'] = ["xsec=0.0304", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-200'] = ["xsec=0.01349", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-250'] = ["xsec=0.006868", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-300'] = ["xsec=0.004061", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-350'] = ["xsec=0.002694", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-400'] = ["xsec=0.001708", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-500'] = ["xsec=0.0007309", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-600'] = ["xsec=0.0003906", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-700'] = ["xsec=0.0002264", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-800'] = ["xsec=0.0001414", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-1000'] = ["xsec=0.00006", "kfact=1.000", "ref=I"]

# ttDM dilepton scalar extension
xs_db['TTto2LDMsimpSpin0_s_mphi-10_ext1'] = ["xsec=2.432", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-50_ext1'] = ["xsec=0.3894", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-100_ext1'] = ["xsec=0.09028", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-150_ext1'] = ["xsec=0.0304", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-200_ext1'] = ["xsec=0.01349", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-250_ext1'] = ["xsec=0.006868", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-300_ext1'] = ["xsec=0.004061", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-350_ext1'] = ["xsec=0.002694", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-400_ext1'] = ["xsec=0.001708", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-500_ext1'] = ["xsec=0.0007309", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-600_ext1'] = ["xsec=0.0003906", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-700_ext1'] = ["xsec=0.0002264", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-800_ext1'] = ["xsec=0.0001414", "kfact=1.000", "ref=I"]
xs_db['TTto2LDMsimpSpin0_s_mphi-1000_ext1'] = ["xsec=0.00006", "kfact=1.000", "ref=I"]

# tDM tW-channel inclusive pseudoscalar
xs_db['TWDMsimpSpin0_ps_mphi-10'] = ["xsec=0.0744", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-50'] = ["xsec=0.05643", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-100'] = ["xsec=0.04119", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-150'] = ["xsec=0.03047", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-200'] = ["xsec=0.02309", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-250'] = ["xsec=0.01758", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-300'] = ["xsec=0.01358", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-350'] = ["xsec=0.008529", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-400'] = ["xsec=0.004708", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-500'] = ["xsec=0.002483", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-600'] = ["xsec=0.001501", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-700'] = ["xsec=0.0009555", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-800'] = ["xsec=0.000626", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_ps_mphi-1000'] = ["xsec=0.0002904", "kfact=1.000", "ref=I"]

# tDM tW-channel inclusive scalar
xs_db['TWDMsimpSpin0_s_mphi-10'] = ["xsec=0.7919", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-50'] = ["xsec=0.1596", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-100'] = ["xsec=0.06339", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-150'] = ["xsec=0.038", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-200'] = ["xsec=0.02586", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-250'] = ["xsec=0.01905", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-300'] = ["xsec=0.01437", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-350'] = ["xsec=0.01103", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-400'] = ["xsec=0.007239", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-500'] = ["xsec=0.003412", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-600'] = ["xsec=0.00189", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-700'] = ["xsec=0.001133", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-800'] = ["xsec=0.0007245", "kfact=1.000", "ref=I"]
xs_db['TWDMsimpSpin0_s_mphi-1000'] = ["xsec=0.0003162", "kfact=1.000", "ref=I"]

# tDM tW-channel dilepton pseudoscalar
xs_db['TWto2LDMsimpSpin0_ps_mphi-10'] = ["xsec=0.008351", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-50'] = ["xsec=0.006291", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-100'] = ["xsec=0.004557", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-150'] = ["xsec=0.003375", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-200'] = ["xsec=0.002544", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-250'] = ["xsec=0.001968", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-300'] = ["xsec=0.001514", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-350'] = ["xsec=0.0009433", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-400'] = ["xsec=0.0005183", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-500'] = ["xsec=0.000276", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-600'] = ["xsec=0.0001658", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-700'] = ["xsec=0.0001048", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-800'] = ["xsec=6.97e-05", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_ps_mphi-1000'] = ["xsec=3.244e-05", "kfact=1.000", "ref=I"]

# tDM tW-channel dilepton scalar
xs_db['TWto2LDMsimpSpin0_s_mphi-10'] = ["xsec=0.0885", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-50'] = ["xsec=0.01754", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-100'] = ["xsec=0.007032", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-150'] = ["xsec=0.004174", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-200'] = ["xsec=0.002891", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-250'] = ["xsec=0.00211", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-300'] = ["xsec=0.001587", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-350'] = ["xsec=0.001222", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-400'] = ["xsec=0.0008075", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-500'] = ["xsec=0.0003812", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-600'] = ["xsec=0.0002099", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-700'] = ["xsec=0.0001262", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-800'] = ["xsec=8.002e-05", "kfact=1.000", "ref=I"]
xs_db['TWto2LDMsimpSpin0_s_mphi-1000'] = ["xsec=3.541e-05", "kfact=1.000", "ref=I"]

# tDM t-channel inclusive pseudoscalar
xs_db['TBDMsimpSpin0_ps_mphi-10'] = ["xsec=0.1835", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-50'] = ["xsec=0.1328", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-100'] = ["xsec=0.08664", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-150'] = ["xsec=0.05863", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-200'] = ["xsec=0.04009", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-250'] = ["xsec=0.02838", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-300'] = ["xsec=0.02029", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-350'] = ["xsec=0.01176", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-400'] = ["xsec=0.006235", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-500'] = ["xsec=0.003023", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-600'] = ["xsec=0.001696", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-700'] = ["xsec=0.00103", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-800'] = ["xsec=0.0006508", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_ps_mphi-1000'] = ["xsec=0.0002827", "kfact=1.000", "ref=I"]

# tDM tW-channel inclusive scalar
xs_db['TBDMsimpSpin0_s_mphi-10'] = ["xsec=3.106", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-50'] = ["xsec=0.7857", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-100'] = ["xsec=0.3028", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-150'] = ["xsec=0.152", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-200'] = ["xsec=0.08625", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-250'] = ["xsec=0.05301", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-300'] = ["xsec=0.03454", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-350'] = ["xsec=0.02326", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-400'] = ["xsec=0.01388", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-500'] = ["xsec=0.005561", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-600'] = ["xsec=0.002736", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-700'] = ["xsec=0.001496", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-800'] = ["xsec=0.0008878", "kfact=1.000", "ref=I"]
xs_db['TBDMsimpSpin0_s_mphi-1000'] = ["xsec=0.0003546", "kfact=1.000", "ref=I"]

# THIS IS OLD, AND COMES FROM RUN 2 UL!!
#
# Detailed references at: https://docs.google.com/spreadsheets/d/1IEfle0H1V3ih2JVFpYckmTd-ACTBqgBRIsFydegGgPQ/edit?usp=sharing
#
# References
#
# 	A	https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeV
# 	B	https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
# 	C	https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV
# 	D	https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
# 	E	https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
#       F       https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
# 	F2	https://github.com/latinos/LatinoAnalysis/blob/master/Tools/python/HiggsXSection.py
# 	G	https://twiki.cern.ch/twiki/bin/view/CMS/GenXsecTaskForce
# 	H	http://arxiv.org/pdf/1307.7403v1.pdf
# 	I	https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToGenXSecAnalyzer
# 	J	https://svnweb.cern.ch/cern/wsvn/LHCDMF/trunk/doc/tex/TTBar_Xsecs_Appendix.tex
# 	K	https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWW13TeVProductionMassScan (powheg numbers)
# 	L	https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWW13TeVProduction (powheg numbers)
#       M       https://github.com/shu-xiao/MadGraphScanning/blob/master/diffCrossSection/madGraph.txt
#       N       MCM
#       O       https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHXSWG/Higgs_XSBR_YR4_update.xlsx
#       P       https://drive.google.com/file/d/0B7mfFpGbPaMvb0ZtMlJfdXhJb2M/view
#       Q       #https://indico.cern.ch/event/448517/session/0/contribution/16/attachments/1164999/1679225/Long_Generators_WZxsec_05_10_15.pdf
# 	R	https://cms-pdmv.cern.ch/mcm/requests?page=0&prepid=B2G-RunIISummer15GS*&dataset_name=TTbarDMJets_*scalar_Mchi-*_Mphi-10000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
#       S       https://docs.google.com/spreadsheets/d/1b4qnWfZrimEGYc1z4dHl21-A9qyJgpqNUbhOlvCzjbE/edit?usp=sharing
#       T       https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
#       U       https://twiki.cern.ch/twiki/pub/CMS/MonoHCombination/crossSection_ZpBaryonic_gq0p25.txt
# 	V	https://twiki.cern.ch/twiki/bin/viewauth/CMS/SameSignDilepton2016
#       W       https://cms-gen-dev.cern.ch/xsdb/
#       Z       http://cms.cern.ch/iCMS/analysisadmin/cadilines?line=SMP-18-006
#       Y       https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBSMAt13TeV
#       A1      https://indico.cern.ch/event/673253/contributions/2756806/attachments/1541203/2416962/20171016_VJetsXsecsUpdate_PH-GEN.pdf
# 	X	Unknown! - Cross section not yet there

