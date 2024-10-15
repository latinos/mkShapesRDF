# Cross section DB for Ultra-Legacy samples
# Units in pb
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

xs_db = {}


# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
# BR (H-->WW) = 0.2152
# BR (H-->tt) = 0.06256
# BR (H-->ZZ) = 0.02641

# Higgs xs at 125.38 GeV from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap
# ggH - XS = 51.96 pb
# VBF - XS = 4.067 pb 
# 51.96*0.2152*(3*0.108)*(3*0.108)
xs_db["GluGluHToWWTo2L2Nu_M125"] = ["xsec=1.1738", "kfact=1.000", "ref=E"]
xs_db["VBFHToWWTo2L2Nu_M125"] = ["xsec=0.9187", "kfact=1.000", "ref=E"]

xs_db["GluGlutoContintoWWtoENuENu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoENuMuNu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoENuTauNu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoMuNuENu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoMuNuMuNu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoMuNuTauNu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoTauNuENu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoTauNuMuNu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]
xs_db["GluGlutoContintoWWtoTauNuTauNu"] = ["xsec=0.0688", "kfact=1.000", "ref=E"]

xs_db["WZ"] = ["xsec=54.3", "kfact=1.000", "ref=E"]   ### MATRIX, SMP-22-017
xs_db["WZG"] = ["xsec=0.08425", "kfact=1.000", "ref=E"]
xs_db["WZtoLNu2Q"] = ["xsec=6.44", "kfact=1.000", "ref=E"]
xs_db["WZTo3LNu"] = ["xsec=5.36", "kfact=1.000", "ref=E"]  ###  54.3 * 0.10097 * 0.1086 * 3 * 3 
xs_db["ZZ"] = ["xsec=16.7", "kfact=1.000", "ref=E"]
xs_db["ZZTo2L2Nu"] = ["xsec=1.1341", "kfact=1.000", "ref=E"]
xs_db["ZZTo2Q2Nu"] = ["xsec=4.67", "kfact=1.000", "ref=E"]
xs_db["ZZTo2L2Q"] = ["xsec=7.4668", "kfact=1.000", "ref=E"]
xs_db["ZZTo4L"] = ["xsec=1.5290", "kfact=1.000", "ref=E"]
xs_db["WWTo2L2Nu"] = ["xsec=12.98", "kfact=1.000", "ref=E"]  ### 122.3 * 0.1086 * 0.1086 * 9
xs_db["WW"] = ["xsec=122.3", "kfact=1.000", "ref=E"]   ## 13 TeV values with 4% expected increase with MCFM
#xs_db["QCD_Pt_15to20"] = ["xsec=", "kfact=1.000", "ref=E"]
#xs_db["QCD_Pt_30to50"] = ["xsec=", "kfact=1.000", "ref=E"]
xs_db["WWW"] = ["xsec=0.23280", "kfact=1.000", "ref=E"]
xs_db["WWZ"] = ["xsec=0.18510", "kfact=1.000", "ref=E"]
xs_db["WZZ"] = ["xsec=0.06206", "kfact=1.000", "ref=E"]
xs_db["ZZZ"] = ["xsec=0.01591", "kfact=1.000", "ref=E"]
xs_db["ZGToLLG"] = ["xsec=1.075", "kfact=1.000", "ref=E"]
xs_db["TTTo2L2Nu"] = ["xsec=98.036", "kfact=1.000", "ref=E"]   ### 923.6 from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO * 9 * 0.1086
xs_db["TTTo2L2Nu_TuneCP5Up"] = ["xsec=98.036", "kfact=1.000", "ref=E"]
xs_db["TTTo2L2Nu_TuneCP5Down"] = ["xsec=98.036", "kfact=1.000", "ref=E"]
xs_db["TTToSemiLeptonic"] = ["xsec=406.82", "kfact=1.000", "ref=E"]   #### 923.6 * 0.6760 * 0.1086 * 3 * 2 
xs_db["TTToSemiLeptonic_TuneCP5Up"] = ["xsec=406.82", "kfact=1.000", "ref=E"]
xs_db["TTToSemiLeptonic_TuneCP5Down"] = ["xsec=406.82", "kfact=1.000", "ref=E"]
xs_db["WToLNu-2Jets"] = ["xsec=64481.58", "kfact=1.000", "ref=E"]  ## 64481.58 from SMP-22-017  ## 67710.0 from XSDB
xs_db["DYJetsToLL_M-50-LO"] = ["xsec=6345.99", "kfact=1.000", "ref=E"]
xs_db["DYto2L-2Jets_MLL-10to50"] = ["xsec=19982.5", "kfact=1.000", "ref=E"]
xs_db["DYto2L-2Jets_MLL-50"] = ["xsec=6345.99", "kfact=1.000", "ref=E"]
xs_db["ST_t-channel_top"] = ["xsec=145.0", "kfact=1.000", "ref=E"]
xs_db["ST_t-channel_antitop"] = ["xsec=87.2", "kfact=1.000", "ref=E"]
xs_db["ST_tW_top"] = ["xsec=43.95", "kfact=1.000", "ref=E"]
xs_db["ST_tW_antitop"] = ["xsec=43.95", "kfact=1.000", "ref=E"]
xs_db["ST_s-channel_plus"] = ["xsec=2.278", "kfact=1.000", "ref=E"]
xs_db["ST_s-channel_minus"] = ["xsec=1.43", "kfact=1.000", "ref=E"]
#xs_db["QCD_HT70to100"] = ["xsec=", "kfact=1.000", "ref=E"]
#xs_db["QCD_HT1200to1500"] = ["xsec=", "kfact=1.000", "ref=E"]
#xs_db["QCD_HTto2000"] = ["xsec=", "kfact=1.000", "ref=E"]
xs_db["WWTo2L2Nu_LL"] = ["xsec=0.488", "kfact=1.000", "ref=E"]   ## 4.598 * 9 * BR(W->lnu) * BR(W->lnu) / BR(W->lnu) = 0.1086
xs_db["WWTo2L2Nu_TT"] = ["xsec=6.266", "kfact=1.000", "ref=E"]   ## 59.03
xs_db["WWTo2L2Nu_LT"] = ["xsec=0.911", "kfact=1.000", "ref=E"]   ## 8.582
xs_db["WWTo2L2Nu_TL"] = ["xsec=0.911", "kfact=1.000", "ref=E"]   ## 8.582
xs_db["ggWW_LL"] = ["xsec=0.025", "kfact=1.000", "ref=E"]       ## 0.239
xs_db["ggWW_TT"] = ["xsec=0.329", "kfact=1.000", "ref=E"]       ## 3.104
xs_db["ggWW_LT"] = ["xsec=0.0087", "kfact=1.000", "ref=E"]       ## 0.08195
xs_db["ggWW_TL"] = ["xsec=0.0087", "kfact=1.000", "ref=E"]       ## 0.08195


