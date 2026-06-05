#!/usr/bin/env python
import sys

import ROOT

import argparse
import collections
import os
import os.path
import re

import shutil
from textwrap import dedent


ROOT.gROOT.SetBatch(True)

argv = sys.argv
sys.argv = argv[:1]


# ----------------------------------------------------- Merge Years: e.g. Run 2, Run 3, ... --------------------------------------


class MergerFactory:
    # _logger = logging.getLogger('MergerFactory')

    # _____________________________________________________________________________
    def __init__(self):
        self._fileIn = None

    # _____________________________________________________________________________

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

       # print ("merge:: variables = ", variables)

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
       # print ("cuts = ", cuts)
       # print ("new_cuts = ", new_cuts)
       cuts = new_cuts

       new_list_of_nuisances = nuisances


       #
       # Get all the samples from all the years. This is needed for the definition of the nuisances
       #
       foldersToMergeSamplesFiles = {
           k : os.path.join(p["folder"], 'samples.py') for k, p in foldersToMerge.items()
           }
       # print ("foldersToMergeSamplesFiles   = ", foldersToMergeSamplesFiles)


       #
       # get all the niusances from all the years
       #
       all_nuisances = {}

       for folderHR, year_nuisances in foldersToMergeNuisancesFiles.items() :
         year_samples = foldersToMergeSamplesFiles[folderHR]
         # print ("year_samples = ", year_samples)
         temp_samples = self.extract_dict(year_samples, "samples")
         # print ("temp_samples = ", temp_samples)

         # print ("year_nuisances = ", year_nuisances)
         nuisances = self.extract_dict(year_nuisances, "nuisances", temp_samples)
         all_nuisances[folderHR] = nuisances

       # print ("all_nuisances = ", all_nuisances)



       #
       # get all the root files with the histograms from the different years
       #
       new_root_file_name = "histos_"     + tag + ".root"
       # print (" new_root_file_name = ", new_root_file_name)
       rootFileNew = ROOT.TFile.Open( new_root_file_name, "RECREATE")

       histograms = {}

       for folderHR, folder in foldersToMerge.items():
         # copy the default root file for bookkeeping
         old_root_file_name = folder["folder"] + "/" + "rootFiles" + "/mkShapes__" + folder["tag"] + ".root"
         new_root_file_name = "year_" + folderHR + "_histos_" + folder["tag"] + ".root"
         # print (" Partial: old_root_file_name = ", old_root_file_name)
         os.system ("cp " + old_root_file_name + "   " + new_root_file_name )
         rootFile    = ROOT.TFile.Open( new_root_file_name, "READ")


         #
         # the following instruction is essential, because in ROOT the TH1F is owned by the root file
         # and in python here for some reason the root file is closed (but why why why ...),
         # thus all histograms deleted (None pointer) during the loop ...
         # By doing "cd" the histograms are owned by the output file, thus surviving
         #
         rootFileNew.cd()
         # get the histograms
         histograms[folderHR] = {}

         # loop over cuts
         for cutName in cuts :
           # print ("cut = ", cutName ) #, " :: ", cuts[cutName]
           # loop over variables
           for variableName, variable in variables.items():
             # print ("   variable = ", variableName )  #, " :: ", variable
             folder_name = cutName + "/" + variableName
             # print ("folder_name = ", folder_name)
             histograms[folderHR][folder_name] = {}
             folder_in_file = rootFile.Get(folder_name)
             # print ("type = ", type(folder_in_file))

             for k in folder_in_file.GetListOfKeys():
               h = k.ReadObj()
               # only 1d histograms supported
               histoName = h.GetName()
               match = re.search("histo_", histoName)
               if not match:
                 continue
               # print ("        histoName = ", histoName, "  h = ", h, "   --> match =", match, " --> cloning it ")
               # print ("        histoName = ", histoName, "  --> match =", match, " --> cloning it ")
               histograms[folderHR][folder_name][histoName] = h.Clone()  # clone is needed, otherwise None in the dictionary

         # print (" histograms[", folderHR, "] = ", histograms)

       #
       # print for debug
       #

       # print (" histograms = ", histograms)


       #
       # add the nominals for all the years
       #

       rootFileNew.cd()


       # loop over cuts
       for cutName in cuts :
         # print ("cut = ", cutName ) #, " :: ", cuts[cutName]

         # loop over variables
         for variableName, variable in variables.items():
           # print ("   variable = ", variableName )  #, " :: ", variable
           folder_name = cutName + "/" + variableName
           # print (" while adding nominals folder_name = ", folder_name)
           rootFileNew.cd()
           rootFileNew.mkdir(folder_name)
           rootFileNew.cd(folder_name)

           # loop over samples
           for sampleName, sample in samples.items():

             histos_to_be_summed = []

             for folderHR, folder in foldersToMerge.items():
               histoName = "histo_" + sampleName
               # print (" type of histo, folderHR = ", folderHR, " --> histoName = ", histoName ," --> ", type(histograms[folderHR][folder_name][histoName]))
               histos_to_be_summed.append(histograms[folderHR][folder_name][histoName])

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

       # print ("merge:: new_list_of_nuisances = ", new_list_of_nuisances)

       rootFileNew.cd()

       # loop over cuts
       for cutName in cuts :
         # loop over variables
         for variableName, variable in variables.items():
           folder_name = cutName + "/" + variableName
           rootFileNew.cd()
           rootFileNew.cd(folder_name)
           # print (" merge nuisances: ", folder_name)

           # loop over nuisances
           for nuisanceName, nuisance in new_list_of_nuisances.items():

             #
             # if the combined nuisance type is lnN, don't touch anything, nothing to be done on histograms level
             #
             if nuisance['type'] == 'lnN' :
               continue

             elif 'name' in nuisance.keys() :

               # print ("nuisanceName = ", nuisanceName)
               # print ("   --> nuisance = ", nuisance)

               # loop over samples
               for sampleName, sample in samples.items():

                 # nameTempUp   = 'histo_' + str(sampleName) + '_CMS_' + (nuisance['name']) + 'Up'
                 # nameTempDown = 'histo_' + str(sampleName) + '_CMS_' + (nuisance['name']) + 'Down'
                 nameTempUp   = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Up'
                 nameTempDown = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Down'
                 nameTemp     = 'histo_' + str(sampleName)

                 histos_up_to_be_summed = []
                 histos_down_to_be_summed = []

                 histos_up_to_be_summed_weights = []
                 histos_down_to_be_summed_weights = []

                 for folderHR, folder in foldersToMerge.items():
                   #
                   # If the histogram up and down are present in the input root files, add the histograms up/down
                   # No matter if then the nuisance is not a shape nuisance but lnN ... still, you add the histograms!
                   # eh perbacco, the histogram exists, then you add it, you might change idea later on
                   #
                   # print ("All the histograms names is [histograms[", folderHR, "][", folder_name, "]]: ", histograms[folderHR][folder_name].keys())
                   # print ("I'm looking for: ", nameTempUp, " and ", nameTempDown)
                   if nameTempUp in histograms[folderHR][folder_name].keys() and nameTempDown in histograms[folderHR][folder_name].keys() :
                     # print (" I found: ", nameTempUp, " and ", nameTempDown)
                     histos_up_to_be_summed.append  ( histograms[folderHR][folder_name][nameTempUp] )
                     histos_down_to_be_summed.append( histograms[folderHR][folder_name][nameTempDown] )
                     histos_up_to_be_summed_weights.append ( 1.0 )
                     histos_down_to_be_summed_weights.append ( 1.0 )

                   else :
                     #
                     # it might be that for that particular sample
                     # or for a specific year in the combination
                     # the nuisance is not defined or missing.
                     # In this case, ok, nothing to be done: the up/down variation should be taken as the nominal
                     #
                     # The nuisance might have been a lnN ... this has to be handled properly
                     #

                     if nuisanceName in all_nuisances[folderHR].keys() :
                       if all_nuisances[folderHR][nuisanceName]['type'] == 'lnN' and  sampleName in all_nuisances[folderHR][nuisanceName]['samples'].keys() :
                         #
                         #    lnN nuisances:
                         #    the up/down could be given separately:   '1.03/0.99'
                         #    or unique :                              '1.02'
                         #
                         histos_up_to_be_summed.append  ( histograms[folderHR][folder_name][nameTemp] )
                         histos_down_to_be_summed.append( histograms[folderHR][folder_name][nameTemp] )
                         if "/" not in all_nuisances[folderHR][nuisanceName]['samples'][sampleName]:
                           # print (" I'm using the weight [", folderHR, "][", nuisanceName, "] =  ", float(all_nuisances[folderHR][nuisanceName]['samples'][sampleName]))
                           histos_up_to_be_summed_weights.append ( float(all_nuisances[folderHR][nuisanceName]['samples'][sampleName]) )
                           histos_down_to_be_summed_weights.append ( 1. / float(all_nuisances[folderHR][nuisanceName]['samples'][sampleName]) )
                         else :
                           # print ("all_nuisances[", folderHR, "][", nuisanceName, "]['samples'][", sampleName, "] = ", all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                           val_up, val_down = all_nuisances[folderHR][nuisanceName]['samples'][sampleName].split("/")
                           histos_up_to_be_summed_weights.append ( val_up )
                           histos_down_to_be_summed_weights.append ( val_down )

                     else:
                       histos_up_to_be_summed.append  ( histograms[folderHR][folder_name][nameTemp] )
                       histos_down_to_be_summed.append( histograms[folderHR][folder_name][nameTemp] )
                       histos_up_to_be_summed_weights.append   ( 1.0 )
                       histos_down_to_be_summed_weights.append ( 1.0 )


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


       return True

    # _____________________________________________________________________________
    def _saveNuisanceHistos(
        self,
        cutName,
        variableName,
        sampleName,
        suffixIn,
        suffixOut=None,
        symmetrize=False,
    ):

        histoUp = self._getHisto(cutName, variableName, sampleName, suffixIn + "Up")
        histoDown = self._getHisto(cutName, variableName, sampleName, suffixIn + "Down")

        return True

    # _____________________________________________________________________________
    def _getHisto(self, cutName, variableName, sampleName, suffix=None):
        shapeName = "%s/%s/histo_%s" % (cutName, variableName, sampleName)
        if suffix:
            shapeName += suffix

        if type(self._fileIn) is dict:
            # by-sample ROOT file
            histo = self._fileIn[sampleName].Get(shapeName)
        else:
            # Merged single ROOT file
            histo = self._fileIn.Get(shapeName)

        if not histo:
            print(shapeName, "not found")
            #             if 'met' in variableName.lower() and 'met' in suffix.lower():
            #                 print(variableName, 'does not contain', suffix)
            #                 sys.exit()
            if suffix:
                print("Getting the nominal instead of varied")
                histo = self._getHisto(cutName, variableName, sampleName)
                histo.SetName(shapeName)
                return histo

        return histo

    # _____________________________________________________________________________
    def _removeStatUncertainty(self, histo):
        for iBin in range(0, histo.GetNbinsX() + 2):
            histo.SetBinError(iBin, 0.0)


def defaultParser():
    sys.argv = argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
    opt = parser.parse_args()
    print ("opt.pycfg    = ", opt.pycfg)
    loadDefaultOptions(parser, opt.pycfg)
    opt = parser.parse_args()

    print ("opt.tag              = ", opt.tag)
    print ("opt.variablesFile    = ", opt.variablesFile)
    print ("opt.cutsFile         = ", opt.cutsFile)
    print ("opt.samplesFile      = ", opt.samplesFile)
    print ("opt.structureFile    = ", opt.structureFile)
    print ("opt.nuisancesFile    = ", opt.nuisancesFile)
    print ("opt.foldersToMerge   = ", opt.foldersToMerge)

    #
    # since the tricky part is the handling of the nuisances
    # there is the need to read the nuisances.py of each single "folder to merge"
    #
    # for the time being it assumes that the different files are named "nuisances.py"
    # alternatively it will need to read the configuration.py file for each folder
    # and extract the correct name of the "nuisances.py" file
    #

    foldersToMergeNuisancesFiles = {
        k : os.path.join(p["folder"], 'nuisances.py') for k, p in opt.foldersToMerge.items()
        }
    print ("foldersToMergeNuisancesFiles   = ", foldersToMergeNuisancesFiles)

    factory = MergerFactory()

    # ~~~~
    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle.read())
      handle.close()
      # clean the dictionary to remove globals due to "exec" funcionality
      samples = {k: v for k, v in samples.items() if not (k.startswith('__') and k.endswith('__'))}

    variables = {}
    if os.path.exists(opt.variablesFile) :
      handle = open(opt.variablesFile,'r')
      exec(handle.read())
      handle.close()
      # print ("variables extended = ", variables)
      # clean the dictionary to remove globals due to "exec" funcionality
      variables = {k: v for k, v in variables.items() if not (k.startswith('__') and k.endswith('__'))}

    cuts = {}
    if os.path.exists(opt.cutsFile) :
      handle = open(opt.cutsFile,'r')
      exec(handle.read())
      handle.close()

      # print (" did I read it ? -->", opt.cutsFile)
      # print (" did I read it ? -->extended cuts = ", cuts)

      # clean the dictionary to remove globals due to "exec" funcionality
      cuts = {k: v for k, v in cuts.items() if not (k.startswith('__') and k.endswith('__'))}

    # print ("cuts = ", cuts)

    nuisances = {}
    if os.path.exists(opt.nuisancesFile) :
      handle = open(opt.nuisancesFile,'r')
      exec(handle.read())
      handle.close()
      # clean the dictionary to remove globals due to "exec" funcionality
      nuisances = {k: v for k, v in nuisances.items() if not (k.startswith('__') and k.endswith('__'))}


    factory.merge(
       opt.tag,
       variables,
       cuts,
       samples,
       nuisances,
       opt.foldersToMerge,
       foldersToMergeNuisancesFiles
       )


    # print ("opt.cutsFile = ", opt.cutsFile)

    # unpacking of variables
    # cuts = cuts["cuts"]
    # inputFile = outputFolder + "/" + outputFile

    # ROOT.TH1.SetDefaultSumw2(True)

    # subsamplesmap = utils.flatten_samples(samples)
    # categoriesmap = utils.flatten_cuts(cuts)
    #
    # utils.update_variables_with_categories(variables, categoriesmap)
    # utils.update_nuisances_with_subsamples(nuisances, subsamplesmap)
    # utils.update_nuisances_with_categories(nuisances, categoriesmap)

    # factory.makeDatacards(
        # inputFile, opt.outputDirDatacard, variables, cuts, samples, structure, nuisances
    # )


    exit()

if __name__ == "__main__":
    main()
