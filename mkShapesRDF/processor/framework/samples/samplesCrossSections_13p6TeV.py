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
#
# X: reference unknown. Please provide a valid reference!

xs_db = {}


# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
# BR (H-->WW) = 0.2152
# BR (H-->tt) = 0.06256
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


# Higgs xs at 125.38 GeV from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap
# ggH - XS = 51.96 pb
# VBF - XS = 4.067 pb 

### Higgs
xs_db["GluGluHToWWTo2L2Nu_M125"] = ["xsec=1.17381", "kfact=1.000", "ref=E"] # 51.960*0.2152*(3*0.108)*(3*0.108)
xs_db["VBFHToWWTo2L2Nu_M125"]    = ["xsec=0.09187", "kfact=1.000", "ref=E"] #  4.067*0.2152*(3*0.108)*(3*0.108)

### WW
xs_db["WW"]        = ["xsec=122.1", "kfact=1.000", "ref=A"]  # (XS(pp -> e mu ve vmu) - XS(gg -> e mu ve vmu)) / (BR(W -> mu vmu)*BR(W -> e ve)) = (1.5589-0.1497)/(0.1078*0.1071)
xs_db["WWTo2L2Nu"] = ["xsec=12.96", "kfact=1.000", "ref=A"]  # 122.1 * 0.1086 * 0.1086 * 9

xs_db["GluGlutoContintoWWtoENuENu"]     = ["xsec=0.0744", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoENuMuNu"]    = ["xsec=0.0749", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoENuTauNu"]   = ["xsec=0.0790", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoMuNuENu"]    = ["xsec=0.0749", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoMuNuMuNu"]   = ["xsec=0.0753", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoMuNuTauNu"]  = ["xsec=0.0795", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoTauNuENu"]   = ["xsec=0.0790", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoTauNuMuNu"]  = ["xsec=0.0795", "kfact=1.000", "ref=A"]
xs_db["GluGlutoContintoWWtoTauNuTauNu"] = ["xsec=0.0840", "kfact=1.000", "ref=A"]

xs_db["WWTo2L2Nu_LL"] = ["xsec=0.488",  "kfact=1.000", "ref=X"] ## 4.598 * 9 * BR(W->lnu) * BR(W->lnu) / BR(W->lnu) = 0.1086
xs_db["WWTo2L2Nu_TT"] = ["xsec=6.266",  "kfact=1.000", "ref=X"] ## 59.03
xs_db["WWTo2L2Nu_LT"] = ["xsec=0.911",  "kfact=1.000", "ref=X"] ## 8.582
xs_db["WWTo2L2Nu_TL"] = ["xsec=0.911",  "kfact=1.000", "ref=X"] ## 8.582
xs_db["ggWW_LL"]      = ["xsec=0.025",  "kfact=1.000", "ref=X"] ## 0.239
xs_db["ggWW_TT"]      = ["xsec=0.329",  "kfact=1.000", "ref=X"] ## 3.104
xs_db["ggWW_LT"]      = ["xsec=0.0087", "kfact=1.000", "ref=X"] ## 0.08195
xs_db["ggWW_TL"]      = ["xsec=0.0087", "kfact=1.000", "ref=X"] ## 0.08195

### Top
xs_db["TTTo2L2Nu"]                    = ["xsec=98.036", "kfact=1.000", "ref=C"] # 923.6 * (3*0.1086) * (3*0.1086)
xs_db["TTTo2L2Nu_TuneCP5Up"]          = ["xsec=98.036", "kfact=1.000", "ref=C"]
xs_db["TTTo2L2Nu_TuneCP5Down"]        = ["xsec=98.036", "kfact=1.000", "ref=C"]
xs_db["TTToSemiLeptonic"]             = ["xsec=406.82", "kfact=1.000", "ref=C"] # 923.6 * 0.6760 * 0.1086 * 3 * 2 
xs_db["TTToSemiLeptonic_TuneCP5Up"]   = ["xsec=406.82", "kfact=1.000", "ref=C"]
xs_db["TTToSemiLeptonic_TuneCP5Down"] = ["xsec=406.82", "kfact=1.000", "ref=C"]

xs_db["ST_tW_top"]        = ["xsec=19.30", "kfact=1.000", "ref=D"] # 43.95 * 2*(3*0.1086*0.6741)
xs_db["ST_tW_antitop"]    = ["xsec=19.30", "kfact=1.000", "ref=D"] # 43.95 * 2*(3*0.1086*0.6741)
xs_db["TWminusto2L2Nu"]   = ["xsec=4.665", "kfact=1.000", "ref=D"] # 43.95 * (3*0.1086) * (3*0.1086)
xs_db["TbarWplusto2L2Nu"] = ["xsec=4.665", "kfact=1.000", "ref=D"] # 43.95 * (3*0.1086) * (3*0.1086)

xs_db["ST_t-channel_top"]     = ["xsec=145.0", "kfact=1.000", "ref=D"]
xs_db["ST_t-channel_antitop"] = ["xsec=87.2",  "kfact=1.000", "ref=D"]
xs_db["ST_s-channel_plus"]    = ["xsec=2.360", "kfact=1.000", "ref=D"] # 7.244 * (3*0.1086)
xs_db["ST_s-channel_minus"]   = ["xsec=1.477", "kfact=1.000", "ref=D"] # 4.534 * (3*0.1086)

### WZ
xs_db["WZTo3LNu"]  = ["xsec=5.32",    "kfact=1.000", "ref=A"] # (XS(pp->e- e+ μ-  ̄vμ) + XS(pp->e- e+ μ+ vμ)) * 9 * BR(ZW->ll lv) / BR(ZW->ee mv)  (0.2385 + 0.3474) * 9 *  0.0036552588 / 0.0036255296
xs_db["WZ"]        = ["xsec=53.9",    "kfact=1.000", "ref=A"] # XS(WZTo3LNu) / (3*9*BR(WZ->lv ll))
xs_db["WZToLNu2Q"] = ["xsec=6.44",    "kfact=1.000", "ref=X"]
xs_db["WZG"]       = ["xsec=0.08425", "kfact=1.000", "ref=X"]

### Zg
xs_db["ZGToLLG"] = ["xsec=1.075", "kfact=1.000", "ref=X"]

### WG
xs_db['WGtoLNuG-1J_PTG10to100']  = ["xsec=215.7", "kfact=1.000", "ref=G"]        # XS * BR (W-->lv) = 0.1086*3
xs_db['WGtoLNuG-1J_PTG100to200'] = ["xsec=0.7236", "kfact=1.000", "ref=G"]
xs_db['WGtoLNuG-1J_PTG200to400'] = ["xsec=0.09474", "kfact=1.000", "ref=G"]
xs_db['WGtoLNuG-1J_PTG400to600'] = ["xsec=0.007269", "kfact=1.000", "ref=G"]
xs_db['WGtoLNuG-1J_PTG600']      = ["xsec=0.001599", "kfact=1.000", "ref=G"]

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
xs_db["WToLNu-2Jets"] = ["xsec=67710.0", "kfact=1.000", "ref=G"]

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

