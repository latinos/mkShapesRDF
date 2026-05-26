#!/usr/bin/env python
import os
import sys
import ROOT
import uproot
import numpy as np
from sys import argv
import argparse
import copy
import shutil
from textwrap import dedent
from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)


def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-o",
        "--outDir",
        type=str,
        help="Output directory",
        required=False,
        default=f"rootFiles/",
    )

    parser.add_argument(
        "-i",
        "--inDir",
        type=str,
        help="Input directory",
        required=False,
        default=f"rootFiles/",
    )

    parser.add_argument(
        "--configurationFile",
        dest="pycfg",
        help="input configuration file",
        default="merge_configuration.py",
    )
    
    return parser

#
# load configurations into the parser, according to configuration.py
#
def loadDefaultOptions(parser, pycfg=None, quiet=False):

    if pycfg != None and os.path.exists(pycfg):
        # print ("loadDefaultOptions: pycfg = ", pycfg)
        handle = open(pycfg,'r')
        variables = {}
        exec(handle.read(),variables)
        handle.close()
        # clean the dictionary to remove globals due to "exec" funcionality
        variables = {k: v for k, v in variables.items() if not (k.startswith('__') and k.endswith('__'))}

        # print ("loadDefaultOptions: variables = ", variables.items())
        for opt_name, opt_value in variables.items():
          parser.add_argument('--' + opt_name, default=opt_value)
        return
    else:
        return


# ----------------------------------------------------- Merge Years: e.g. Run 2, Run 3, ... --------------------------------------
class MergerFactory:
    # _logger = logging.getLogger('MergerFactory')

    # _____________________________________________________________________________
    def __init__(self, tag, inDir, outDir, foldersToMerge):

        ### Prepare the output keys, output file, and inputs        
        self._fileOut = outDir + '/histos_' + tag + '.root'
        self._filesIn = {}
        self.all_nuisances = {}
        self.all_years = ["2016", "2017", "2018", "2022EE", "2022", "2023BPix", "2023", "2024", "2025", "2026"] # The order is important

        for folderHR, folder in foldersToMerge.items():
            # copy the default root file for bookkeeping
            old_root_file_name = outDir + "/mkShapes__" + folder["tag"] + ".root"
            new_root_file_name = outDir + "/year_" + folderHR + "_histos_" + folder["tag"] + ".root"
            print (" Partial: old_root_file_name = ", old_root_file_name)
            os.system ("cp " + old_root_file_name + "   " + new_root_file_name )

            self._filesIn[folderHR] = new_root_file_name

        print("Safe-copied the root files for bookkeeping: ", self._filesIn)

    def extract_dict(self, filename, var_name, samples_input = {}):
        # namespace = {}

        namespace = {
          'samples': samples_input
        }

        # print ("I'm looking at ", filename)
        try:
            with open(filename, 'r') as f:
                # We use an empty dict for globals to isolate the output
                # exec(f.read(), {}, namespace)
                exec(f.read(), namespace, namespace)
            # print ("   namespace = ", namespace)
            return namespace.get(var_name)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return None
        
    def getVariedHistos(self, folderHR, folder_name, rootFileIn, sampleName, nuisanceName, nuisance, yearKeys, extra="CMS_"):
        
        nameTemp     = 'histo_' + str(sampleName)
        nameTempUp   = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Up'
        nameTempDown = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Down'

        usedExtra = False
        nameExtraTempUp   = 'histo_' + str(sampleName) + '_' + extra + (nuisance['name']) + 'Up'
        nameExtraTempDown = 'histo_' + str(sampleName) + '_' + extra + (nuisance['name']) + 'Down'

        #
        # If the histogram up and down are present in the input root files, add the histograms up/down
        # No matter if then the nuisance is not a shape nuisance but lnN ... still, you add the histograms!
        # eh perbacco, the histogram exists, then you add it, you might change idea later on
        #
        # print ("All the histograms names is [histograms[", folderHR, "][", folder_name, "]]: ", histograms[folderHR][folder_name].keys())
        # print ("I'm looking for: ", nameTempUp, " and ", nameTempDown)
        if nameTempUp in yearKeys and nameTempDown in yearKeys :
            
            # print (" I found: ", nameTempUp, " and ", nameTempDown)
            histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTempUp)
            histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTempDown)
            histo_up_to_be_summed_weights = 1.0
            histo_down_to_be_summed_weights = 1.0

        elif nameExtraTempUp in yearKeys and nameExtraTempDown in yearKeys :
            
            # In some cases, the histograms might be named with the "CMS_" prefix, e.g. "histo_sample_CMS_nuisanceUp" instead of "histo_sample_nuisanceUp". 
            # In this case, we should look for the histograms with the "CMS_" prefix and add them if they are present.

            # print (" I found extra-named: ", nameExtraTempUp, " and ", nameExtraTempDown)
            histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameExtraTempUp)
            histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameExtraTempDown)
            histo_up_to_be_summed_weights = 1.0
            histo_down_to_be_summed_weights = 1.0

            usedExtra = True

        else :

            #
            # it might be that for that particular sample
            # or for a specific year in the combination
            # the nuisance is not defined or missing.
            # In this case, ok, nothing to be done: the up/down variation should be taken as the nominal
            #
            # The nuisance might have been a lnN ... this has to be handled properly
            #

            if nuisanceName in self.all_nuisances[folderHR].keys() :
                if self.all_nuisances[folderHR][nuisanceName]['type'] == 'lnN' and  sampleName in self.all_nuisances[folderHR][nuisanceName]['samples'].keys() :
                    #
                    #    lnN nuisances:
                    #    the up/down could be given separately:   '1.03/0.99'
                    #    or unique :                              '1.02'
                    #
                    histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )

                    if "/" not in self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName]:
                      # print (" I'm using the weight [", folderHR, "][", nuisanceName, "] =  ", float(all_nuisances[folderHR][nuisanceName]['samples'][sampleName]))
                      histo_up_to_be_summed_weights =  float(self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                      histo_down_to_be_summed_weights = 1. / float(self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                    else :
                        # print ("all_nuisances[", folderHR, "][", nuisanceName, "]['samples'][", sampleName, "] = ", all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                        val_up, val_down = self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName].split("/")
                        histo_up_to_be_summed_weights = val_up
                        histo_down_to_be_summed_weights = val_down

                else:
                    # Take nominal value if the nuisance is not defined for that sample, or if the nuisance is not a lnN nor shape
                    histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_up_to_be_summed_weights = 1.0
                    histo_down_to_be_summed_weights = 1.0

            else:
                ### To keep the (un)correlation of nuisances, one need to define new nuisances. For example:
                # lumi_Uncorrelated exists in all the nuisances.py, but it needs to be uncorrelated across years
                # therefore, in the global nuisances.py is defined a new nuisance, e.g. lumi_Uncorrelated_2018, lumi_Uncorrelated_2017, etc.
                matched = False
                for year in self.all_years :
                    if year in nuisanceName and year in folderHR :
                        oldNuisanceName = nuisanceName.split("_"+year)[0]
                        if oldNuisanceName in self.all_nuisances[folderHR].keys() :
                            matched = True
                            histo_up_to_be_summed, histo_down_to_be_summed, histo_up_to_be_summed_weights, histo_down_to_be_summed_weights, nameTempUp, nameTempDown = self.getVariedHistos(folderHR, folder_name, rootFileIn, sampleName, oldNuisanceName, nuisance, yearKeys, extra="CMS_")

                if not matched :
                    # print(f"Taking nominal value for {nuisanceName} in {folderHR}!")
                    histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_up_to_be_summed_weights = 1.0
                    histo_down_to_be_summed_weights = 1.0

        if usedExtra :
            return histo_up_to_be_summed, histo_down_to_be_summed, histo_up_to_be_summed_weights, histo_down_to_be_summed_weights, nameExtraTempUp, nameExtraTempDown
        else :
            return histo_up_to_be_summed, histo_down_to_be_summed, histo_up_to_be_summed_weights, histo_down_to_be_summed_weights, nameTempUp, nameTempDown



    # _____________________________________________________________________________
    def merge(
        self,
        tag,
        variables,
        cuts,
        samples,
        nuisances,
        foldersToMerge,
        foldersToMergeNuisancesFiles,
    ):
        
        print ("merge:: variables = ", variables)

        #
        # expand cuts, unrolling the categories
        #
        new_cuts = {}
        for k, j in cuts.items():
          if isinstance(cuts[k], dict) and "categories" in cuts[k].keys():
              for cat in cuts[k]['categories']:
                # cuts.append(k+'_'+cat)
                new_cuts[k+'_'+cat] = {}
          else :
            new_cuts[k] = {}
        print ("cuts = ", cuts)
        print ("new_cuts = ", new_cuts)
        cuts = new_cuts     
        new_list_of_nuisances = nuisances

        #
        # Get all the samples from all the years. This is needed for the definition of the nuisances
        #
        foldersToMergeSamplesFiles = {
           k : os.path.join(p["folder"], 'samples.py') for k, p in foldersToMerge.items()
        }
        print ("foldersToMergeSamplesFiles   = ", foldersToMergeSamplesFiles)

        #
        # get all the niusances from all the years
        #

        for folderHR, year_nuisances in foldersToMergeNuisancesFiles.items() :
            year_samples = foldersToMergeSamplesFiles[folderHR]
            # print ("year_samples = ", year_samples)
            temp_samples = self.extract_dict(year_samples, "samples")
            # print ("temp_samples = ", temp_samples)
            # print ("year_nuisances = ", year_nuisances)
            nuisances = self.extract_dict(year_nuisances, "nuisances", temp_samples)
            self.all_nuisances[folderHR] = nuisances

        # print ("all_nuisances = ", self.all_nuisances)


        #### Be memory efficient to work with large number of samples and nuisances
        # 
        # Avoid copying everything in memory, and instead read the histograms from the root files on the fly, and merge them directly into the output file.
        # Do it per cut, per sample and per variable, and store the output in each iteration. Open and close the output file at each iteration to avoid keeping everything in memory.
        #

        # loop over cuts
        for cutName in cuts :
            print ("cut = ", cutName )

            # loop over variables
            for variableName, variable in variables.items():
                print ("   variable = ", variableName )  #, " :: ", variable
                folder_name = cutName + "/" + variableName
                # print (" while adding nominals folder_name = ", folder_name)

                ## Store all keys using uproot
                allKeys = {}
                for folderHR in self._filesIn.keys() :
                    fileIn = self._filesIn[folderHR]
                    with uproot.open(fileIn) as f:
                        allKeys[folderHR] = np.unique([ key.split(";")[0] for key in f[folder_name].keys() ])
                        # print(f"Number of keys for {folderHR} in {folder_name}: {len(allKeys[folderHR])}")   

                rootIn = {}
                # loop over years and copy nominals
                for folderHR in self._filesIn.keys():
                    fileIn = self._filesIn[folderHR]
                    # print("Openning file: ", fileIn)
                    rootIn[folderHR] = ROOT.TFile.Open(fileIn, "READ")
                
                # Open output file
                outFile = ROOT.TFile(self._fileOut, "UPDATE")
                # create the folder if it does not exist
                outFile.mkdir(folder_name)
                outFile.cd(folder_name)

                # loop over samples
                for sampleName, sample in samples.items():

                    print("        sample: ", sampleName)                 

                    histos_to_be_summed = []
                    ## loop over years and copy nominals
                    for folderHR in self._filesIn.keys():
                        histos_to_be_summed.append( rootIn[folderHR].Get(folder_name + "/histo_" + sampleName) )

                    # print (" start adding ... ")
                    summed_histo = histos_to_be_summed[0].Clone()

                    # print ("type = ", type(summed_histo))
                    # print (" the [0] is : ", summed_histo.GetName())

                    for hh in histos_to_be_summed[1:] :  # skip first one
                        summed_histo.Add(hh)

                    # print (" now write: ", summed_histo.GetName())
                    summed_histo.Write()

                    #
                    # Now let's handle the nuisances
                    #

                    # loop over nuisances
                    for nuisanceName, nuisance in new_list_of_nuisances.items():

                        histos_up_to_be_summed = []
                        histos_down_to_be_summed = []

                        histos_up_to_be_summed_weights = []
                        histos_down_to_be_summed_weights = []

                        #
                        # if the combined nuisance type is lnN, don't touch anything, nothing to be done on histograms level
                        #
                        if nuisance['type'] == 'lnN' :
                            continue

                        if "stat" in nuisanceName:
                            continue
            
                        if "type" in nuisance.keys() and (nuisance["type"] == "rateParam" or nuisance["type"] == "lnU"):
                            continue

                        if 'name' in nuisance.keys() :

                            if "samples" in nuisance.keys() and sampleName not in nuisance["samples"].keys() :
                                continue

                            nameTemp     = 'histo_' + str(sampleName)
                            nameTempUp   = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Up'
                            nameTempDown = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Down'

                            # print ("nuisanceName = ", nuisanceName)
                            # print ("   --> nuisance = ", nuisance)

                            for folderHR in self._filesIn.keys():
                                
                                histo_up, histo_do, histoW_up, histoW_do, nameTempUp, nameTempDown = self.getVariedHistos(folderHR, folder_name, rootIn[folderHR], sampleName, nuisanceName, nuisance, allKeys[folderHR], extra="CMS_")
                                histos_up_to_be_summed.append(histo_up)
                                histos_down_to_be_summed.append(histo_do)
                                histos_up_to_be_summed_weights.append(histoW_up)
                                histos_down_to_be_summed_weights.append(histoW_do)
                        else:
                            # print("nuisance ", nuisanceName, " has no name key, skipping it for histograms merging")
                            continue

                        #
                        # if the nuisance has NO effect on a sample, the histograms are not even created, thus it's not possible to merge them
                        #
                        if len(histos_up_to_be_summed) >= 1:
                            summed_up_histo = histos_up_to_be_summed[0].Clone()
                            # print ("histos_up_to_be_summed_weights[ 0 ] = ", histos_up_to_be_summed_weights[0])
                            summed_up_histo.Scale(histos_up_to_be_summed_weights[0])
                            ihh = 0
                            for hh in histos_up_to_be_summed[1:] :  # skip first one
                                ihh += 1
                                summed_up_histo.Add(hh, histos_up_to_be_summed_weights[ihh])
                                # print ("histos_up_to_be_summed_weights[", ihh, "] = ", histos_up_to_be_summed_weights[ihh])
                            # set the name properly, mentioning the nuisance
                            summed_up_histo.SetName (nameTempUp)
                            summed_up_histo.Write()

                            summed_down_histo = histos_down_to_be_summed[0].Clone()
                            summed_down_histo.Scale(histos_down_to_be_summed_weights[0])
                            # print ("histos_down_to_be_summed_weights[ 0 ] = ", histos_down_to_be_summed_weights[0])
                            ihh = 0
                            for hh in histos_down_to_be_summed[1:] :  # skip first one
                                ihh += 1
                                summed_down_histo.Add(hh, histos_down_to_be_summed_weights[ihh])
                                # print ("histos_down_to_be_summed_weights[", ihh, "] = ", histos_down_to_be_summed_weights[ihh])
                            summed_down_histo.SetName (nameTempDown)
                            summed_down_histo.Write()

                outFile.Close()
                for key in rootIn.keys() :
                    rootIn[key].Close()

        return True


def main():
    
    header = """
    ----------------------------------------------------------------------------------------
                                                                                           .
           __  __                      __   __                                             .
          |  \/  | ___ _ __ __ _  ___  \ \ / /__  __ _ _ __ ___                            .
          | |\/| |/ _ \ '__/ _` |/ _ \  \ V / _ \/ _` | '__/ __|                           .
          | |  | |  __/ | | (_| |  __/   | |  __/ (_| | |  \__ \                           .
          |_|  |_|\___|_|  \__, |\___|   |_|\___|\__,_|_|  |___/                           .
                           |___/                                                           .
                                                                                           .
    ----------------------------------------------------------------------------------------
    """
    header = dedent(header)
    print(header)

    parser = defaultParser()
    args = parser.parse_args()
    print ("opt.pycfg    = ", args.pycfg)
    loadDefaultOptions(parser, args.pycfg)
    opt = parser.parse_args()

    global cuts, plot
    configsFolder = "configs"
    ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
    print(dir())
    print(globals().keys())
    cuts = cuts["cuts"]
    subsamplesmap = utils.flatten_samples(samples)
    categoriesmap = utils.flatten_cuts(cuts)
    outDir = args.outDir
    inDir = args.inDir
    
    print ("args.tag              = ", tag)
    print ("args.foldersToMerge   = ", opt.foldersToMerge)     

    foldersToMergeNuisancesFiles = {
        k : os.path.join(p["folder"], 'nuisances_ALL.py') for k, p in opt.foldersToMerge.items()
    }
    print ("foldersToMergeNuisancesFiles   = ", foldersToMergeNuisancesFiles)

    factory = MergerFactory(tag, inDir, outDir, opt.foldersToMerge)
    factory.merge(
       tag,
       variables,
       cuts,
       samples,
       nuisances,
       opt.foldersToMerge,
       foldersToMergeNuisancesFiles
    )       

    exit()

if __name__ == "__main__":
    main()
