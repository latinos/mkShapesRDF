#!/usr/bin/env python
import ROOT
import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mplhep as hep
import os
import sys
from sys import argv
import argparse
import matplotlib.pyplot as plt
import hist
import copy
from hist import Hist
import mplhep as hep
from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)
hep.style.use("CMS")


def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-c",
        "--onlyCut",
        type=str,
        help="Cut to process",
        required=False,
        default="",
    )

    parser.add_argument(
        "-v",
        "--onlyVar",
        type=str,
        help="Cut to process",
        required=False,
        default="",
    )
    
    parser.add_argument(
        "-p",
        "--onlyPlot",
        type=str,
        help="Plot style: c, ratio, or diff",
        required=False,
        default="c",
    )

    parser.add_argument(
        "-o",
        "--outDir",
        type=str,
        help="Output directory",
        required=False,
        default=f"./plots/",
    )

    parser.add_argument(
        "-i",
        "--inFile",
        type=list,
        nargs="*",
        help="Input file",
        required=False,
        default=[],
    )

    parser.add_argument(
        "-b",
        "--brokenAxis",
        type=int,
        help="0 do analysis in batch, 1 check for errors in batch submission",
        required=False,
        default=0
    )
    
    return parser


def makePlots(samples, variables, nuisance, plot, cuts, lumi, onlyCut=[], plotStyle="c", inFile="", outDir="", onlyVar="", brokenAxis=False, brokenValue=-1):
    
    plotCuts = onlyCut if len(onlyCut)>0 else cuts
    

    print("======================================")
    print("   ")
    print("   ")
    print("        MAKE PLOTS (CAT STYLE)")
    print("   ")
    print("   ") 
    print("======================================")

    print("\n")
    print("Input file: ")
    print(inFile)
    
    
    df = uproot.open(inFile[0])

    df_year = {}
    for fileName in inFile:
        if "2016_postVFP" in fileName:
            df_year["2016_postVFP"] = uproot.open(fileName)
        elif "2016" in fileName:
            df_year["2016"] = uproot.open(fileName)
        elif "2017" in fileName:
            df_year["2017"] = uproot.open(fileName)
        elif "2018" in fileName:
            df_year["2018"] = uproot.open(fileName)
        elif "2022EE" in fileName:
            df_year["2022EE"] = uproot.open(fileName)
        elif "2022" in fileName:
            df_year["2022"] = uproot.open(fileName)
        elif "2023BPix" in fileName:
            df_year["2023BPix"] = uproot.open(fileName)
        elif "2023" in fileName:
            df_year["2023"] = uproot.open(fileName)
        elif "2024" in fileName:
            df_year["2024"] = uproot.open(fileName)
        elif "2025" in fileName:
            df_year["2025"] = uproot.open(fileName)
        elif "2026" in fileName:
            df_year["2026"] = uproot.open(fileName)
    
    plot_cfg = plot["groupPlot"]
    plot_cfg["DATA"] = plot["plot"]["DATA"]
    plot = plot["plot"]

    if onlyVar != "":
        variables_tmp = {}
        variables_tmp[onlyVar] = variables[onlyVar]
        variables = variables_tmp
    
    for cutName in plotCuts:
        
        print("------------- " + cutName + " -------------")        
        
        for variableName in variables:
            
            print(variableName)

            if brokenAxis:
                fig, (ax1, ax) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 1]}, figsize=(12, 13))
                fig.subplots_adjust(hspace=0.01)
                hep.cms.label("Preliminary", ax=ax1, data=True, loc=0)
                hep.cms.lumitext(str(lumi)+" $fb^{-1}$               ", ax=ax1)
            else:
                fig, ax = plt.subplots()                
                hep.cms.label("Preliminary", ax=ax, data=True, loc=0)
                hep.cms.lumitext(str(lumi)+" $fb^{-1}$               ", ax=ax)
            
            histograms = {}
            histogram_bkg = []
            histogram_stat = []
            histogram_sig = {}
            histogram_sig_alt = {}
            
            dummy_key = df[cutName+"/"+variableName].keys()[0]
            
            histogram_total = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            histogram_totalBkg = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            histogram_data = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            
            mynuisances = {}
            nuisanceHistos_up = {}
            nuisanceHistos_do = {}
            nuisance_signal_up = {}
            nuisance_signal_do = {}
            nuisance_signal_alt_up = {}
            nuisance_signal_alt_do = {}
            nuisance_bkg_up = {}
            nuisance_bkg_do = {}
            
            labels = []
            colors = []
            signals = []
            signals_alt = []
            backgrounds = []
            
            for plotName in plot_cfg.keys():
                
                histograms[plotName] = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
                
                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                    nuisance_signal_up[plotName] = {}
                    nuisance_signal_do[plotName] = {}
                elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]>1:
                    nuisance_signal_alt_up[plotName] = {}
                    nuisance_signal_alt_do[plotName] = {}
                else:
                    nuisance_bkg_up[plotName] = {}
                    nuisance_bkg_do[plotName] = {}
                
                if "samples" in plot_cfg[plotName].keys():
                
                    for sampleName in plot_cfg[plotName]["samples"]:

                        scale = 1.0
                        if "scale" in plot[sampleName].keys():
                            scale = plot[sampleName]["scale"]
                        
                        if "cuts" in plot[sampleName].keys() and cutName in plot[sampleName]["cuts"]:
                            scale = float(plot[sampleName]["cuts"][cutName])                            
                        
                        for key in df_year:

                            histograms[plotName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                            if "DATA" in sampleName:
                                continue

                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]>1:
                                continue
                            
                            histogram_total += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==0:
                                histogram_totalBkg += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                            
                        #### Do nuisances chain -------
                        for nuisanceName, nuisance in nuisances.items():
                            
                            if nuisanceName not in nuisanceHistos_up.keys():
                                nuisanceHistos_up[nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                nuisanceHistos_do[nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
            
                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                if nuisanceName not in nuisance_signal_up[plotName]:
                                    nuisance_signal_up[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                    nuisance_signal_do[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                            elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                if nuisanceName not in nuisance_signal_alt_up[plotName]:
                                    nuisance_signal_alt_up[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                    nuisance_signal_alt_do[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                            else:
                                if nuisanceName not in nuisance_bkg_up[plotName]:
                                    nuisance_bkg_up[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                    nuisance_bkg_do[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
            
                            if "cuts" in nuisance and cutName not in nuisance["cuts"]:
                                continue

                            if "cutspost" in nuisance and cutName not in nuisance["cutspost"]:
                                continue
            
                            if "stat" in nuisanceName:
                                continue
            
                            if "type" in nuisance.keys() and (nuisance["type"] == "rateParam" or nuisance["type"] == "lnU"):
                                continue
                            else:
                                mynuisances[nuisanceName] = nuisances[nuisanceName]
                                
                            if "type" in nuisance and nuisance["type"] == "lnN":
                                
                                if "samples" in nuisance:
                                    if sampleName not in nuisance["samples"]:
                                        values = "1.0"
                                    else:
                                        values = nuisance["samples"][sampleName]
                                else:
                                    values = nuisance["value"]
            
                                if "/" in values:
                                    variations = (float(values.split("/")[0]),float(values.split("/")[1]))
                                else:
                                    variations = (float(values), 2.0 - float(values))

                                    
                                year = ""
                                if "name" in nuisances[nuisanceName]:
                                    if "2016" in nuisances[nuisanceName]["name"]:
                                        year = "2016"
                                    elif "2017" in nuisances[nuisanceName]["name"]:
                                        year = "2017"
                                    elif "2018" in nuisances[nuisanceName]["name"]:
                                        year = "2018"
                                    elif "2022EE" in nuisances[nuisanceName]["name"]:
                                        year = "2022EE"
                                    elif "2022" in nuisances[nuisanceName]["name"]:
                                        year = "2022"
                                    elif "2023BPix" in nuisances[nuisanceName]["name"]:
                                        year = "2023BPix"
                                    elif "2023" in nuisances[nuisanceName]["name"]:
                                        year = "2023"
                                    elif "2024" in nuisances[nuisanceName]["name"]:
                                        year = "2024"
                                    elif "2025" in nuisances[nuisanceName]["name"]:
                                        year = "2025"
                                    elif "2026" in nuisances[nuisanceName]["name"]:
                                        year = "2026"
                                
                                for key	in df_year:
                                    if year != "" and year not in key:                                        
                                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        
                                            nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale                                            
                                        elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                            nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        else:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        
                                            nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                    else:
                                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
                                        
                                            nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                            nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
                                        elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                            nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                            nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
                                        else:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
                                            
                                            nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                            nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
            
                            else:                                            
                                year = ""
                                if "name" in nuisances[nuisanceName]:
                                    if "2016" in nuisances[nuisanceName]["name"]:
                                        year = "2016"
                                    elif "2017" in nuisances[nuisanceName]["name"]:
                                        year = "2017"
                                    elif "2018"	in nuisances[nuisanceName]["name"]:
                                        year = "2018"
                                    elif "2022EE" in nuisances[nuisanceName]["name"]:
                                        year = "2022EE"
                                    elif "2022" in nuisances[nuisanceName]["name"]:
                                        year = "2022"
                                    elif "2023BPix" in nuisances[nuisanceName]["name"]:
                                        year = "2023BPix"
                                    elif "2023" in nuisances[nuisanceName]["name"]:
                                        year = "2023"
                                    elif "2024" in nuisances[nuisanceName]["name"]:
                                        year = "2024"
                                    elif "2025" in nuisances[nuisanceName]["name"]:
                                        year = "2025"
                                    elif "2026" in nuisances[nuisanceName]["name"]:
                                        year = "2026"

                                for key in df_year:
                                    if year!="" and year not in key:
                                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        
                                            nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                            nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        else:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        
                                            nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                    elif "samples" in nuisances[nuisanceName]:
                                        if sampleName not in nuisances[nuisanceName]["samples"]:
                                                                                            
                                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                                nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            
                                                nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                                nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            else:
                                                nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                
                                                nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        else:
                                                
                                            if "name" in nuisances[nuisanceName]:
                                                extra = ""
                                                if "histo_"+sampleName+ "_"+nuisances[nuisanceName]["name"]+"Up" not in [key.split(";")[0] for key in df_year[key][cutName+"/"+variableName].keys()]:
                                                    extra = "CMS_"                                                
                                                    
                                                if (extra == "CMS_") and "histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up" not in [key.split(";")[0] for key in df_year[key][cutName+"/"+variableName].keys()]:
                                                    print("Nuisance missing: " + "histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up")
                                                    nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                    nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                    if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                                        nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                        nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                    else:
                                                        nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                        nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                                    continue
                                                
                                                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:                                                    
                                                    nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up"].to_hist() * scale
                                                    nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Down"].to_hist() * scale
                                                    
                                                    nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up"].to_hist() * scale
                                                    nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Down"].to_hist() * scale
                                                elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                                    nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up"].to_hist() * scale
                                                    nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Down"].to_hist() * scale
                                                else:
                                                    nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up"].to_hist() * scale
                                                    nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Down"].to_hist() * scale
                                                    
                                                    nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Up"].to_hist() * scale
                                                    nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+extra+nuisance["name"]+"Down"].to_hist() * scale
                                            else:
                                                
                                                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                                    nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                    nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                                    
                                                    nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                    nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                                elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                                    nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                    nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                                else:
                                                    nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                    nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                                    
                                                    nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                    nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                    else:
                                        if "name" in nuisance:
                                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                                nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                                
                                                nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                            elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                                nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                            else:
                                                    
                                                nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                                
                                                nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                        else:
                                            nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                                                nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                                
                                                nuisance_signal_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisance_signal_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                            elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                                                nuisance_signal_alt_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisance_signal_alt_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                            else:
                                                nuisanceHistos_up[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisanceHistos_do[nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                                
                                                nuisance_bkg_up[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisance_bkg_do[plotName][nuisanceName] += df_year[key][cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                
                                
                #### End of nuisance chain ------
                
                elif "DATA" == plotName:
                    for key in df_year:
                        histograms[plotName] += df_year[key][cutName+"/"+variableName+"/histo_DATA"].to_hist()
                
                if "DATA" not in plotName:
                    if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] == 1:
                        histogram_stat.append(histograms[plotName])
                        signals.append(plotName)
                    elif "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"] > 1:
                        signals_alt.append(plotName)
                    else:
                        histogram_stat.append(histograms[plotName])
                        histogram_bkg.append(histograms[plotName])
                        backgrounds.append(plotName)
                        labels.append(plot_cfg[plotName]["nameHR"] + f" [{np.round(histograms[plotName].sum().value, 1)}]")
                        colors.append(plot_cfg[plotName]["colorPlt"])

            past_signals = [] # stack signals
            for signal in signals:
                histogram_sig[signal] = histogram_totalBkg + histograms[signal]
                for past_sig in past_signals:
                    histogram_sig[signal] += histograms[past_sig]                    
                past_signals.append(signal)

            for signal in signals_alt:
                histogram_sig[signal] = histogram_totalBkg + histograms[signal]
                
            hist_data = copy.deepcopy(histograms["DATA"])
                                            
            #### Do plot ---------------
            # Bkg ------
            hep.histplot(histogram_bkg, stack=True, histtype='fill', ax=ax, color=colors, label=labels, alpha=0.7)
            if brokenAxis:
                hep.histplot(histogram_bkg, stack=True, histtype='fill', ax=ax1, color=colors, label=labels, alpha=0.7)
            # Signal ---
            for signal in signals:
                histogram_sig[signal].plot1d(ax=ax, stack=False, histtype='step', xerr=True, yerr=0.0, color=plot_cfg[signal]["colorPlt"], label=plot_cfg[signal]["nameHR"] + f" [{np.round(np.sum(histograms[signal].values()), 1)}]")
                if brokenAxis:
                    histogram_sig[signal].plot1d(ax=ax1, stack=False, histtype='step', xerr=True, yerr=0.0, color=plot_cfg[signal]["colorPlt"], label=plot_cfg[signal]["nameHR"] + f" [{np.round(histograms[signal].sum(), 1)}]")

            for signal in signals_alt:
                histogram_sig[signal].plot1d(ax=ax, stack=False, histtype='step', xerr=True, linestyle="dashed", yerr=0.0, color=plot_cfg[signal]["colorPlt"], label=plot_cfg[signal]["nameHR"] + f" [{np.round(histograms[signal].sum(), 1)}]")
                if brokenAxis:
                    histogram_sig[signal].plot1d(ax=ax1, stack=False, histtype='step', xerr=True, linestyle="dashed", yerr=0.0, color=plot_cfg[signal]["colorPlt"], label=plot_cfg[signal]["nameHR"] + f" [{np.round(histograms[signal].sum(), 1)}]")
                    
            # Data -----
            data_var_up = hist_data.variances() * 0.0
            data_var_do = hist_data.variances() * 0.0
            for i in range(len(data_var_up)):
                data_var_up[i] = GetPoissError(hist_data.values()[i], 0, 1)
                data_var_do[i] = GetPoissError(hist_data.values()[i], 1, 0)
                
            if plot_cfg["DATA"]["isBlind"]==1:               
                (hist_data*0.0).plot1d(ax=ax, stack=False, histtype='errorbar', xerr=True, yerr=[data_var_do,data_var_up], color='k', label = "Data", zorder=10)
                if brokenAxis:
                    (hist_data*0.0).plot1d(ax=ax1, stack=False, histtype='errorbar', xerr=True, yerr=[data_var_do,data_var_up], color='k', label = "Data", zorder=10)
            else:
                hist_data.plot1d(ax=ax, stack=False, histtype='errorbar', xerr=True, yerr=[data_var_do,data_var_up], color='k', label = "Data", zorder=10)
                if brokenAxis:
                    hist_data.plot1d(ax=ax1, stack=False, histtype='errorbar', xerr=True, yerr=[data_var_do,data_var_up], color='k', label = "Data", zorder=10)
                
            nuisances_err2_up = histogram_total.variances() * 0.0
            nuisances_err2_do = histogram_total.variances() * 0.0
            for histo in histogram_stat:
                nuisances_err2_up += histo.variances()
                nuisances_err2_do += histo.variances()               
                
            for nuisanceName in mynuisances.keys():

                up = nuisanceHistos_up[nuisanceName].values()
                do = nuisanceHistos_do[nuisanceName].values()

                up_is_up = up > histogram_total.values()

                dup2 = np.square(up - histogram_total.values())
                ddo2 = np.square(do - histogram_total.values())
                
                nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                nuisances_err2_do += np.where(up_is_up, ddo2, dup2)

            nuisances_err_up = np.sqrt(nuisances_err2_up)
            nuisances_err_do = np.sqrt(nuisances_err2_do)

            for i in range(len(histogram_total.values())):
                
                nominal = histogram_total.values()[i]
                var_up = nuisances_err_up[i]
                var_do = nuisances_err_do[i]

                x_center = histogram_total.axes.centers[0][i]
                x_low = histogram_total.axes.edges[0][i]
                x_high = histogram_total.axes.edges[0][i+1]

                art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                ax.add_artist(art)
                if brokenAxis:
                    art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                    ax1.add_artist(art)

                
            y_top = np.max([np.max(hist_data.values()), np.max(histogram_total.values())])
            if y_top == 0.0:
                y_top = 1.0
                
            ax.set_ylim([0, 2.5*y_top])            
            ax.set_xlim(hist_data.axes.edges[0][0], hist_data.axes.edges[0][-1])

            ax.set_ylabel("Events")            
                        
            if plotStyle == "c":
                
                ax.set_xlabel(variables[variableName]["xaxis"])
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                
                plt.savefig(outDir+"/c_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/c_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_c_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_c_"+cutName+"_"+variableName+".png has been created \n")
                
            elif plotStyle == "diff":                
            
                if brokenAxis:
                    ax.set_xlabel("")
                    ax1.set_xlabel("")
                    handles, labels = ax1.get_legend_handles_labels()
                    ax1.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                else:
                    ax.set_xlabel("")
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                
                #### Ratio Canvas ------
                
                xticks = ax.get_xticks()
                ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
                
                yhax = hep.append_axes(ax=ax, size=1.5, pad=0.3, position="bottom")
                yhax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
                #yhax.set_xticks(xticks)
                yhax.set_xlabel(variables[variableName]["xaxis"])
                yhax.set_ylabel("Signal", loc="center")
                
                ymax = 0.0

                signals = signals + signals_alt ## append alternatives for difference
                for signal in signals:
                    
                    if ymax < np.max(histograms[signal].values()):
                        ymax = np.max(histograms[signal].values())
                    
                    histograms[signal].plot1d(ax=yhax, histtype='step', color=plot_cfg[signal]["colorPlt"], yerr=0.0)

                    nuisances_err2_up = histograms[signal].variances()
                    nuisances_err2_do = histograms[signal].variances()
                
                    for nuisanceName in mynuisances.keys():

                        if "isSignal" in plot_cfg[signal] and plot_cfg[signal]["isSignal"] > 1:
                            up = nuisance_signal_alt_up[signal][nuisanceName].values()
                            do = nuisance_signal_alt_do[signal][nuisanceName].values()
                        else:
                            up = nuisance_signal_up[signal][nuisanceName].values()
                            do = nuisance_signal_do[signal][nuisanceName].values()
                            
                        up_is_up = up > histograms[signal].values()
                        
                        dup2 = np.square(up - histograms[signal].values())
                        ddo2 = np.square(do - histograms[signal].values())
                        nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                        nuisances_err2_do += np.where(up_is_up, ddo2, dup2)
                        
                    nuisances_err_up = np.sqrt(nuisances_err2_up)
                    nuisances_err_do = np.sqrt(nuisances_err2_do)
                
                
                    for i in range(len(histograms[signal].values())):
                        
                        nominal = histograms[signal].values()[i]
                        var_up = nuisances_err_up[i]
                        var_do = nuisances_err_do[i]
                        
                        x_center = histograms[signal].axes.centers[0][i]
                        x_low = histograms[signal].axes.edges[0][i]
                        x_high = histograms[signal].axes.edges[0][i+1]
                        
                        art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), alpha=0.3, facecolor=plot_cfg[signal]["colorPlt"], color=None)
                        yhax.add_artist(art)
                
                yhax.set_ylim([0.0, 1.3*ymax])

                thData_ratio = Hist(hist_data.axes[0])
                ratio_var_up = hist_data.variances() * 0.0
                ratio_var_do = hist_data.variances() * 0.0

                for i in range(len(ratio_var_up)):
                    ratio = hist_data.values()[i] - histogram_totalBkg.values()[i]

                    #var_up = abs(hist_data.values()[i] + data_var_up[i] - histogram_totalBkg.values()[i])
                    #var_do = abs(hist_data.values()[i] - data_var_do[i] - histogram_totalBkg.values()[i])
                        
                    thData_ratio[i] = ratio
                    ratio_var_up[i] = data_var_up[i] #var_up
                    ratio_var_do[i] = data_var_do[i] #var_do
                    
                    #ratio_var_up[i] = var_up
                    #if var_up < 0.0:
                    #    ratio_var_up[i] = 0.0
                    #if var_do < 0.0:
                    #    ratio_var_do[i] = 0.0
                    
                if plot_cfg["DATA"]["isBlind"]==0:
                    thData_ratio.plot1d(ax=yhax, stack=False, histtype='errorbar', xerr=True, yerr=[ratio_var_do, ratio_var_up], color='k', label = "Data", zorder=10)
                        
                plt.savefig(outDir+"/cDiff_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/cDiff_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_cDiff_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_cDiff_"+cutName+"_"+variableName+".png has been created \n")


            elif plotStyle == "sig":

                if brokenAxis:
                    ax.set_xlabel("")
                    ax1.set_xlabel("")
                    handles, labels = ax1.get_legend_handles_labels()
                    ax1.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")                    
                else:
                    ax.set_xlabel("")
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")

                    
		        #### Ratio Canvas ------
                xticks = ax.get_xticks()
                ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
                
                yhax = hep.append_axes(ax=ax, size=1.5, pad=0.3, position="bottom")
                yhax.set_xlim(hist_data.axes.edges[0][0], hist_data.axes.edges[0][-1])

                yhax.set_xlabel(variables[variableName]["xaxis"])
                yhax.set_ylabel("Signal", loc="center")

                nuisances_err2_up = histogram_total.variances() * 0.0
                nuisances_err2_do = histogram_total.variances() * 0.0
                for histo in histogram_bkg:
                    nuisances_err2_up += histo.variances()
                    nuisances_err2_do += histo.variances()

                for nuisanceName in mynuisances.keys():

                    up = nuisanceHistos_up[nuisanceName].values()
                    do = nuisanceHistos_do[nuisanceName].values()

                    up_is_up = up > histogram_total.values()

                    dup2 = np.square(up - histogram_total.values())
                    ddo2 = np.square(do - histogram_total.values())
                    nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                    nuisances_err2_do += np.where(up_is_up, ddo2, dup2)

                for i in range(len(histogram_total.values())):

                    nominal = 0.0
                    if histogram_total.values()[i] != 0.0:
                        var_up = np.sqrt(nuisances_err2_up[i])
                        var_do = np.sqrt(nuisances_err2_do[i])
                    else:
                        var_up = 0.0
                        var_do = 0.0

                    x_center = histogram_total.axes.centers[0][i]
                    x_low = histogram_total.axes.edges[0][i]
                    x_high = histogram_total.axes.edges[0][i+1]

                    art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                    yhax.add_artist(art)

                ymax = 0.0
                past_signals = histogram_total * 0.0
                for signal in histogram_sig.keys():

                    nuisances_err2_up = histogram_total.variances() * 0.0
                    nuisances_err2_do = histogram_total.variances() * 0.0
                    
                    nuisances_err2_up += histograms[signal].variances()
                    nuisances_err2_do += histograms[signal].variances()

                    for nuisanceName in mynuisances.keys():
                        
                        if "type" in nuisances[nuisanceName] and nuisances[nuisanceName]["type"] != "lnN":
                            if signal not in nuisances[nuisanceName]["samples"]:
                                continue
                        else:
                            if "samples" in nuisances[nuisanceName] and signal not in nuisances[nuisanceName]["samples"]:
                                continue
                        
                        if "isSignal" in plot_cfg[signal] and plot_cfg[signal]["isSignal"] > 1:
                            up = nuisance_signal_alt_up[signal][nuisanceName].values()
                            do = nuisance_signal_alt_do[signal][nuisanceName].values()
                        else:
                            up = nuisance_signal_up[signal][nuisanceName].values()
                            do = nuisance_signal_do[signal][nuisanceName].values()
                            
                        up_is_up = up > histograms[signal].values()

                        dup2 = np.square(up - histograms[signal].values())
                        ddo2 = np.square(do - histograms[signal].values())
                        
                        nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                        nuisances_err2_do += np.where(up_is_up, ddo2, dup2)

                    nuisances_err_up = np.sqrt(nuisances_err2_up)
                    nuisances_err_do = np.sqrt(nuisances_err2_do)
                    
                    past_signals = histograms[signal] # +=
                    past_signals.plot1d(ax=yhax, histtype='step', color=plot_cfg[signal]["colorPlt"], yerr=0.0)

                    if ymax < np.max(histograms[signal].values()):
                        ymax = np.max(histograms[signal].values())
                    """
                    for i in range(len(histograms[signal].values())):
                    
                        nominal = past_signals.values()[i]
                        var_up = nuisances_err_up[i]
                        var_do = nuisances_err_do[i]
                    
                        x_center = histograms[signal].axes.centers[0][i]
                        x_low = histograms[signal].axes.edges[0][i]
                        x_high = histograms[signal].axes.edges[0][i+1]
                    
                        art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), alpha=0.3, facecolor=plot_cfg[signal]["colorPlt"], color=None)
                        yhax.add_artist(art)
                    """
                
                yhax.set_ylim([0.0, 1.4*ymax])

                thData_ratio = Hist(hist_data.axes[0])
                ratio_var_up = hist_data.variances() * 0.0
                ratio_var_do = hist_data.variances() * 0.0

                for i in range(len(ratio_var_up)):
                    ratio = hist_data.values()[i] - histogram_totalBkg.values()[i]

                    #var_up = abs(hist_data.values()[i] + data_var_up[i] - histogram_totalBkg.values()[i])
                    #var_do = abs(hist_data.values()[i] - data_var_do[i] - histogram_totalBkg.values()[i])
                        
                    thData_ratio[i] = ratio
                    ratio_var_up[i] = data_var_up[i] #var_up
                    ratio_var_do[i] = data_var_do[i] #var_do
                    
                    #ratio_var_up[i] = var_up
                    #if var_up < 0.0:
                    #    ratio_var_up[i] = 0.0
                    #if var_do < 0.0:
                    #    ratio_var_do[i] = 0.0
                    
                if plot_cfg["DATA"]["isBlind"]==0:
                    thData_ratio.plot1d(ax=yhax, stack=False, histtype='errorbar', xerr=True, yerr=[ratio_var_do, ratio_var_up], color='k', label = "Data", zorder=10)
                
                plt.savefig(outDir+"/cSig_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/cSig_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_cSig_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_cSig_"+cutName+"_"+variableName+".png has been created \n")
                
            elif plotStyle == "ratio":
                
                if brokenAxis:
                    ax.set_xlabel("")
                    ax1.set_xlabel("")
                    handles, labels = ax1.get_legend_handles_labels()
                    ax1.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                else:
                    ax.set_xlabel("")
                    handles, labels = ax.get_legend_handles_labels()
                    ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                
                #### Ratio Canvas ------
                
                xticks = ax.get_xticks()
                ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
                
                yhax = hep.append_axes(ax=ax, size=1.5, pad=0.3, position="bottom")
                yhax.set_xlim(hist_data.axes.edges[0][0], hist_data.axes.edges[0][-1])

                #yhax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
                #yhax.set_xticks(xticks) ### Buggy
                yhax.set_xlabel(variables[variableName]["xaxis"])
                yhax.set_ylabel("Data/Expected", loc="center")

                thData_ratio = Hist(hist_data.axes[0])
                ratio_var_up = hist_data.variances() * 0.0
                ratio_var_do = hist_data.variances() * 0.0

                for i in range(len(ratio_var_up)):
                    if histogram_total.values()[i]>0.0:
                        ratio = hist_data.values()[i] / histogram_total.values()[i]
                        
                        var_up = data_var_up[i] / histogram_total.values()[i]
                        var_do = data_var_do[i] / histogram_total.values()[i]
                    else:
                        ratio = 0.0
                        var_up = 0.0
                        var_do = 0.0
                    
                    thData_ratio[i] = ratio
                    ratio_var_up[i] = var_up
                    ratio_var_do[i] = var_do
                    
                if plot_cfg["DATA"]["isBlind"]==0:
                    thData_ratio.plot1d(ax=yhax, stack=False, histtype='errorbar', xerr=True, yerr=[ratio_var_do, ratio_var_up], color='k', label = "Data", zorder=10)
                                                
                nuisances_err2_up = histogram_total.variances() * 0.0
                nuisances_err2_do = histogram_total.variances() * 0.0
                for histo in histogram_bkg:
                    nuisances_err2_up += histo.variances()
                    nuisances_err2_do += histo.variances()

                for nuisanceName in mynuisances.keys():

                    up = nuisanceHistos_up[nuisanceName].values()
                    do = nuisanceHistos_do[nuisanceName].values()

                    up_is_up = up > histogram_total.values()

                    dup2 = np.square(up - histogram_total.values())
                    ddo2 = np.square(do - histogram_total.values())
                    nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                    nuisances_err2_do += np.where(up_is_up, ddo2, dup2)

                for i in range(len(histogram_total.values())):

                    nominal = 1.0
                    if histogram_total.values()[i] != 0.0:
                        var_up = np.sqrt(nuisances_err2_up[i]) / histogram_total.values()[i]
                        var_do = np.sqrt(nuisances_err2_do[i]) / histogram_total.values()[i]
                    else:
                        var_up = 0.0
                        var_do = 0.0

                    x_center = histogram_total.axes.centers[0][i]
                    x_low = histogram_total.axes.edges[0][i]
                    x_high = histogram_total.axes.edges[0][i+1]

                    art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                    yhax.add_artist(art)
            
                yhax.set_ylim([0.5, 1.5])
                yhax.plot([histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1]], [1, 1], color='k', linewidth=2, linestyle=':')
                        
                plt.savefig(outDir+"/cratio_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/cratio_"+cutName+"_"+variableName+".png has been created \n")

                if not brokenAxis:
                
                    ax.set_ylim([0.1, 100000*y_top])
                    ax.set_yscale("log")
                    
                    plt.savefig(outDir+"/log_cratio_"+cutName+"_"+variableName+".png")
                    print("Info: png file "+ outDir+"/log_cratio_"+cutName+"_"+variableName+".png has been created \n")

                
            #### Close figure
            plt.clf()
            plt.close(fig)
            
            
def GetPoissError(numberEvents, down, up):
        alpha = 1 - 0.6827
        L = 0
        if numberEvents != 0:
            L = ROOT.Math.gamma_quantile(alpha / 2, numberEvents, 1.0)
        U = 0
        if numberEvents == 0:
            #
            # Poisson error agreed in the CMS statistics committee
            # see: https://hypernews.cern.ch/HyperNews/CMS/get/statistics/263.html
            # and https://hypernews.cern.ch/HyperNews/CMS/get/HIG-16-042/32/1/1/1/1/1.html
            # and https://twiki.cern.ch/twiki/bin/viewauth/CMS/PoissonErrorBars
            # to avoid flip-flop.
            # The commented version would have created 1.147 for 0 observed events
            # while now we get 1.84 in the case of 0 observed events
            #
            U = ROOT.Math.gamma_quantile_c(alpha / 2, numberEvents + 1, 1.0)
            # U = ROOT.Math.gamma_quantile_c (alpha,numberEvents+1,1.)
            # print("u = ", U)
        else:
            U = ROOT.Math.gamma_quantile_c(alpha / 2, numberEvents + 1, 1.0)

        # the error
        L = numberEvents - L
        if numberEvents > 0:
            U = U - numberEvents
        # else :
        # U = 1.14 # --> bayesian interval Poisson with 0 events observed
        # 1.14790758039 from 10 lines above

        if up and not down:
            return U
        if down and not up:
            return L
        if up and down:
            return (L, U)
                
                
def main():
    
    parser = defaultParser()
    args = parser.parse_args()

    global cuts, plot
    configsFolder = "configs"
    ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
    print(dir())
    print(globals().keys())
    cuts = cuts["cuts"]
    subsamplesmap = utils.flatten_samples(samples)
    categoriesmap = utils.flatten_cuts(cuts)
    
    onlyCut = args.onlyCut
    onlyVar = args.onlyVar
    onlyPlot = args.onlyPlot
    outDir = args.outDir
    inFile = args.inFile
    brokenAxis = args.brokenAxis>0.5
    brokenValue = args.brokenAxis
    
    if onlyPlot not in ["c", "ratio", "diff", "sig"]:
        print("Error: The only allowed plot styles are 'c', 'ratio', or 'diff' ")
        
    cuts_to_plot = []
    for cutName in cuts:
        if onlyCut in cutName:
            cuts_to_plot.append(cutName)
            
    if inFile == []:
        fileName = outputFolder + "/" + outputFile 
    else:
        inFile = [''.join(ff) for ff in inFile]        
        fileName = inFile
            
    makePlots(samples, variables, nuisances, plot, cuts, lumi, onlyCut=cuts_to_plot, plotStyle=onlyPlot, inFile=fileName, outDir=outDir, onlyVar=onlyVar, brokenAxis=brokenAxis, brokenValue=brokenValue)
    

if __name__ == '__main__':
    main()
    print("DONE!")

