#!/usr/bin/env python

import json
import sys
from sys import exit
argv = sys.argv
sys.argv = argv[:1]
import ROOT
import optparse
# import LatinoAnalysis.Gardener.hwwtools as hwwtools
import os.path
import string
import logging
# import LatinoAnalysis.Gardener.odict as odict
import traceback
from array import array
from collections import OrderedDict
import math
from termcolor import colored

#import os.path

# # Convert TH1F to TH1D, better digested by mkPlot
# def convert_TH1F_to_TH1D(hist_f):
#     """
#     Converts a TH1F histogram to a TH1D histogram.
    
#     Parameters:
#         hist_f (ROOT.TH1F): The input TH1F histogram.
        
#     Returns:
#         ROOT.TH1D: The converted TH1D histogram.
#     """
#     # Create an empty TH1D histogram with the same binning as hist_f
#     hist_d = ROOT.TH1D(hist_f.GetName() + "_d", hist_f.GetTitle(), 
#                        hist_f.GetNbinsX(), hist_f.GetXaxis().GetXmin(), hist_f.GetXaxis().GetXmax())
    
#     # Copy bin contents and errors from TH1F to TH1D
#     for bin in range(1, hist_f.GetNbinsX() + 1):
#         hist_d.SetBinContent(bin, hist_f.GetBinContent(bin))
#         hist_d.SetBinError(bin, hist_f.GetBinError(bin))
    
#     # Optionally, copy the underflow and overflow bin contents and errors
#     hist_d.SetBinContent(0, hist_f.GetBinContent(0))
#     hist_d.SetBinError(0, hist_f.GetBinError(0))
#     hist_d.SetBinContent(hist_d.GetNbinsX() + 1, hist_f.GetBinContent(hist_f.GetNbinsX() + 1))
#     hist_d.SetBinError(hist_d.GetNbinsX() + 1, hist_f.GetBinError(hist_f.GetNbinsX() + 1))
    
#     return hist_d


# ----------------------------------------------------- LawnMower --------------------------------------

class LawnMower:
    _logger = logging.getLogger('LawnMower')
 
    # _____________________________________________________________________________
    def __init__(self):

        variables = {}
        self._variables = variables

        
 
    # _____________________________________________________________________________
    def makePostFitPlot(self):

        print("=========================")
        print("==== makePostFitPlot ====")
        print("=========================")
        
        
        fileIn = ROOT.TFile(self._inputFileCombine, "READ")


        self._outFile = ROOT.TFile.Open( self._outputFileName, 'update')  # need to append in an existing file if more cuts/variables are wanted

        self._outFile.mkdir ( self._cutNameInOriginal )
        self._outFile.mkdir ( self._cutNameInOriginal + "/" + self._variable)

        self._outFile.cd ( self._cutNameInOriginal + "/" + self._variable )

        
        #post_RooArgSet = ROOT.RooArgSet()
        post_RooArgSet = fileIn.Get("norm_fit_s")      
        normalization = post_RooArgSet
        
        
        if self._kind == 's' :
          folder_fit_name = "shapes_fit_s"   # signal + background
        elif  self._kind == 'b' :
          folder_fit_name = "shapes_fit_b"   # background only fit
        elif  self._kind == 'p' :
          folder_fit_name = "shapes_prefit"   # prefit
        else :
          print(" Seriously? What do you want from me? ")
          return 
       
       
        template_histogram = 0
        
        for sampleName, structureDef in self._structure.items():
           if '/' in sampleName:
             cardName = sampleName.replace('/', '__')
             binName = sampleName[sampleName.find('/') + 1:]
             shapeSource = 'binned/' + binName + '/' + self._cutNameInOriginal + "/" + self._variable
             sampleName = sampleName[:sampleName.find('/')]
           else:
             cardName = sampleName
             shapeSource = self._cutNameInOriginal+"/"+self._variable
           
           # in_samples = False
           # if sampleName in self._samples: in_samples = True
           
           # if not in_samples:
           #   # check if it is in subsamples
           #   in_subsample = False
           #   for _sampleName, _sample in list(self._samples.items()):
           #     if "subsamples" not in _sample: continue
           #     for _subsam in  list(_sample["subsamples"].keys()):
           #       if _sampleName+"_"+ _subsam == sampleName:
           #         in_subsample = True
           #         break
           #   if not in_subsample: continue
           
           if 'removeFromCuts' in structureDef and self._cutNameInOriginal in structureDef['removeFromCuts']:
             continue
           
           
           # 
           # propagate signal from pre-fit if triggered
           # NB: this is needed for exclusion analyses, where the fitted signal is 0
           #     or to show the signal in the background only fit 
           #
           if sampleName == "DATA" :
             
             print("THISFILE:",self._inputFile)
             fileInJustForDATA = ROOT.TFile(self._inputFile, "READ")

             if self._isInputFileFromDatacard:
                 # if sampleName == "DATA": sampleName = "data_obs"
                 self._outFile.cd (self._cutNameInOriginal + "/" + self._variable)
                 print(("Shape source = " + shapeSource + "/" + sampleName))
                 # histo = fileInJustForDATA.Get(self._cutNameInOriginal + "/" + sampleName)
                 histoName = "histo_{}".format(sampleName)
                 if sampleName == "DATA":
                     histoName = "histo_Data"
                 histo = fileInJustForDATA.Get(histoName)
                 print(histo)
                 if not histo:
                    raise RuntimeError("Could not get DATA histogram from input file: {}. File is not from data card.".format(self._inputFile))
                 print("Data integral = {}".format(histo.Integral()))
                 print("Histo:")
                 print(histo)
                 print(("Histo + cardName = histo_" + cardName))
                 histo.SetName  ("histo_" + cardName)
                 histo.SetTitle ("histo_" + cardName)

             else:
                 self._outFile.cd (self._cutNameInOriginal+"/"+self._variable)
                 print(shapeSource + "/histo_" + sampleName)
                 histo = fileInJustForDATA.Get(shapeSource + "/histo_" + sampleName)
                 if not histo:
                    raise RuntimeError("Could not get histogram from input file: {}. File might be from data card.".format(self._inputFile))
                 print(histo)
                 print('histo_' + cardName)
                 histo.SetName  ('histo_' + cardName)
                 histo.SetTitle ('histo_' + cardName)

             histo.Write()              
             
             template_histogram = histo.Clone ("template")


        #print " template_histogram = " , template_histogram
         
        totalFromDatacard = None

        for sampleName, structureDef in self._structure.items():
           if '/' in sampleName:
             cardName = sampleName.replace('/', '__')
             binName = sampleName[sampleName.find('/') + 1:]
             shapeSource = 'binned/' + binName + '/' + self._cutNameInOriginal + "/" + self._variable
             sampleName = sampleName[:sampleName.find('/')]
           else:
             cardName = sampleName
             shapeSource = self._cutNameInOriginal+"/"+self._variable

           # in_samples = False
           # if sampleName in self._samples: in_samples = True
         
           # if not in_samples:
           #  # check if it is in subsamples
           #  in_subsample = False
           #  for _sampleName, _sample in list(self._samples.items()):
           #     if "subsamples" not in _sample: continue
           #     for _subsam in  list(_sample["subsamples"].keys()):
           #        if _sampleName+"_"+ _subsam == sampleName:
           #           in_subsample = True
           #           break
           #  if not in_subsample: continue

           if 'removeFromCuts' in structureDef and self._cutNameInOriginal in structureDef['removeFromCuts']:
             continue

           print(" sampleName = ", sampleName)

           tmp = None

           if sampleName != "DATA":
               if totalFromDatacard is None:
                   if self._isInputFileFromDatacard:
                       # totalFromDatacard = fileInJustForDATA.Get(self._cutNameInOriginal + "/" + sampleName).Clone()
                       try:
                           totalFromDatacard = fileInJustForDATA.Get("histo_"+sampleName).Clone()
                       except:
                           print("")
                           print(colored("WARNING: Could not get histogram for sample ", "yellow", attrs=["bold"]) + colored(sampleName, "yellow", attrs=["bold"]) + colored(" from the input file: ", "yellow", attrs=["bold"]) + self._inputFile)
                           print(colored("Not a big deal, this may be triggered because the sample is not available in the input file or not included in structure.py", "yellow", attrs=["bold"]))
                           print("")
                   else:
                       try:
                           totalFromDatacard = fileInJustForDATA.Get(shapeSource + "/histo_" + sampleName).Clone()
                       except:
                           print("")
                           print(colored("WARNING: Could not get histogram for sample ", "yellow", attrs=["bold"]) + colored(sampleName, "yellow", attrs=["bold"]) + colored(" from the input file: ", "yellow", attrs=["bold"]) + self._inputFile)
                           print(colored("Not a big deal, this may be triggered because the sample is not available in the input file or not included in structure.py", "yellow", attrs=["bold"]))
                           print("")
               else:
                   if self._isInputFileFromDatacard:
                      try:
                          tmp = fileInJustForDATA.Get("histo_"+sampleName).Clone()
                      except:
                          print("")
                          print(colored("WARNING: Could not get histogram for sample ", "yellow", attrs=["bold"]) + colored(sampleName, "yellow", attrs=["bold"]) + colored(" from the input file: ", "yellow", attrs=["bold"]) + self._inputFile)
                          print(colored("Not a big deal, this may be triggered because the sample is not available in the input file and included in structure.py", "yellow", attrs=["bold"]))
                          print("")
                   else:
                      try:
                          tmp = fileInJustForDATA.Get(shapeSource + "/histo_" + sampleName).Clone()
                      except:
                          print("")
                          print(colored("WARNING: Could not get histogram for sample ", "yellow", attrs=["bold"]) + colored(sampleName, "yellow", attrs=["bold"]) + colored(" from the input file: ", "yellow", attrs=["bold"]) + self._inputFile)
                          print(colored("Not a big deal, this may be triggered because the sample is not available in the input file and included in structure.py", "yellow", attrs=["bold"]))
                          print("")
                      
                   if tmp:
                       totalFromDatacard.Add(tmp)

           copied_from_original = False
           
           # if samples_key != "DATA" :
           if sampleName != "DATA":
             if not fileIn.Get(folder_fit_name + "/" + self._cut):
               raise RuntimeError(
                   "Could not get folder " + folder_fit_name +
                   " and cut = " + self._cut + " in file: " + self._inputFileCombine
               )
             if not (fileIn.Get(folder_fit_name + "/" + self._cut).GetListOfKeys().Contains(cardName) ):
               print("")
               print(colored("WARNING: Could not get histogram for sample ", "yellow", attrs=["bold"]) + colored(sampleName, "yellow", attrs=["bold"]) + colored(" from the input file: ", "yellow", attrs=["bold"]) + self._inputFileCombine)
               print(colored("Make sure the sample exists in the input file and matches the key in structure.py", "yellow", attrs=["bold"]))
               print("")
               print(colored("Skipping this sample", "yellow", attrs=["bold"]))
               print("")
               #
               # If for some reason this histogram is not available in the combine output
               # get the histogram from the input root file, the output of mkShape
               # and scale that to 0, so that it is propagated to be used by mkPlot
               # but it will have 0 contribution, as expected (but legends and all the rest will be ok and nice)
               #
               continue
               #
               fileInJustForDATA = ROOT.TFile(self._inputFile, "READ")

               if self._isInputFileFromDatacard:
                 if sampleName == "DATA": sampleName = "data_obs"
                 self._outFile.cd (self._cutNameInOriginal + "/" + self._variable)
                 histo = fileInJustForDATA.Get(self._cutNameInOriginal + "/" + sampleName)
                 histo.SetName  ("histo_" + cardName)
                 histo.SetTitle ("histo_" + cardName)
                 histo.Scale(0.0) # I think this needs to be here, to actually scale the hist to 0?

               else:
                 self._outFile.cd(self._cutNameInOriginal+"/"+self._variable)
                 histo = fileInJustForDATA.Get(shapeSource + "/histo_" + sampleName)
                 histo.SetName  ('histo_' + cardName)
                 histo.SetTitle ('histo_' + cardName)
                 histo.Scale(0.0) # I think this needs to be here, to actually scale the hist to 0?

               histo.Write()
               
               copied_from_original = True

             #
             #
             #
             if not copied_from_original :  
               
               # Ensure that all histograms we save are TH1D  
               histo = fileIn.Get(folder_fit_name + "/" + self._cut + "/" + cardName)
               
               print(folder_fit_name + "/" + self._cut + "/" + cardName)
               
               histo.SetName  ('histo_' + cardName)
               histo.SetTitle ('histo_' + cardName)
               
               # fix the binning copying from "DATA" binning, if available
               if (template_histogram != 0) :
                 histo = self._ChangeBin(histo, template_histogram)
               
               histo.Write()              


        #
        # total signal and total background, and total
        #
        
        #
        # total signal
        if self._getSignalFromPrefit == 0 :
          if not fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total_signal"):
            raise RuntimeError(
                "Could not get histogram total_signal in file: " + self._inputFileCombine +
                " for cut = " + self._cut + " in folder " + folder_fit_name
            )
          histo_total_signal = fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total_signal")
        else:
          if not fileIn.Get("shapes_prefit/" + self._cut + "/" + "total_signal"):
            raise RuntimeError(
                "Could not get histogram total_signal in file: " + self._inputFileCombine +
                " for cut = " + self._cut + " in folder shapes_prefit"
            )
          histo_total_signal = fileIn.Get("shapes_prefit/" + self._cut + "/" + "total_signal")

        if histo_total_signal:
          histo_total_signal.SetName  ('histo_' + 'total_signal')
          histo_total_signal.SetTitle ('histo_' + 'total_signal')
          
          # fix the binning copying from "DATA" binning, if available
          if (template_histogram != 0) :
            histo_total_signal = self._ChangeBin(histo_total_signal, template_histogram)
          
          histo_total_signal.Write()              

        #
        # total background
        if not fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total_background"):
          raise RuntimeError(
              "Could not get histogram total_background in file: " + self._inputFileCombine +
              " for cut = " + self._cut + " in folder " + folder_fit_name
          )
        histo_total_background = fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total_background")
        histo_total_background.SetName  ('histo_' + 'total_background')
        histo_total_background.SetTitle ('histo_' + 'total_background')

        if not fileIn.Get("shapes_prefit/" + self._cut + "/" + "total_background"):
          raise RuntimeError(
              "Could not get histogram total_background in file: " + self._inputFileCombine +
              " for cut = " + self._cut + " in folder shapes_prefit"
          )
        histo_total_background_prefit = fileIn.Get("shapes_prefit/" + self._cut + "/" + "total_background")
        histo_total_background_prefit.SetName  ('histo_total_background_prefit')
        histo_total_background_prefit.SetTitle ('histo_total_background_prefit')

        if not fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total_background"):
          raise RuntimeError(
              "Could not get histogram total_background in file: " + self._inputFileCombine +
              " for cut = " + self._cut + " in folder " + folder_fit_name
          )
        histo_total_background_postfit = fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total_background")
        histo_total_background_postfit.SetName  ('histo_total_background_postfit_' + self._kind)
        histo_total_background_postfit.SetTitle ('histo_total_background_postfit_' + self._kind)

        # fix the binning copying from "DATA" binning, if available
        if (template_histogram != 0) :
          histo_total_background = self._ChangeBin(histo_total_background, template_histogram)
          histo_total_background_prefit = self._ChangeBin(histo_total_background_prefit, template_histogram)
          histo_total_background_postfit = self._ChangeBin(histo_total_background_postfit, template_histogram)
        
        histo_total_background.Write()              
        histo_total_background_prefit.Write()              
        histo_total_background_postfit.Write()              
        
        #
        # total
        if not fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total"):
          raise RuntimeError(
              "Could not get histogram total in file: " + self._inputFileCombine +
              " for cut = " + self._cut + " in folder " + folder_fit_name
          )
        histo_total = fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total")
        
        histo_total.SetName  ('histo_' + 'total')
        histo_total.SetTitle ('histo_' + 'total')

        if not fileIn.Get("shapes_prefit/" + self._cut + "/" + "total"):
          raise RuntimeError(
              "Could not get histogram total in file: " + self._inputFileCombine +
              " for cut = " + self._cut + " in folder shapes_prefit"
          )
        histo_total_prefit = fileIn.Get("shapes_prefit/" + self._cut + "/" + "total")
        histo_total_prefit.SetName  ('histo_total_prefit')
        histo_total_prefit.SetTitle ('histo_total_prefit')

        if not fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total"):
          raise RuntimeError(
              "Could not get histogram total in file: " + self._inputFileCombine +
              " for cut = " + self._cut + " in folder " + folder_fit_name
          )
        histo_total_postfit = fileIn.Get(folder_fit_name + "/" + self._cut + "/" + "total")
        histo_total_postfit.SetName  ('histo_total_postfit_' + self._kind)
        histo_total_postfit.SetTitle ('histo_total_postfit_' + self._kind)

        # fix the binning copying from "DATA" binning, if available
        if (template_histogram != 0) :
          histo_total = self._ChangeBin(histo_total, template_histogram)
          histo_total_prefit = self._ChangeBin(histo_total_prefit, template_histogram)
          histo_total_postfit = self._ChangeBin(histo_total_postfit, template_histogram)

        if self._MCStatFromInput:
            self._AddErrors(histo_total,totalFromDatacard)
            self._AddErrors(histo_total_prefit,totalFromDatacard)
            self._AddErrors(histo_total_postfit,totalFromDatacard)
        
        histo_total.Write()              
        histo_total_prefit.Write()      
        histo_total_postfit.Write()

    # _____________________________________________________________________________
    def _ChangeBin(self, myhisto, templatehisto): 

        nx = templatehisto.GetNbinsX()
        
        binLowEdge = []

        for iBin in range(1, nx+1):
          binLowEdge.append(templatehisto.GetXaxis().GetBinLowEdge(iBin))
        binLowEdge.append(templatehisto.GetXaxis().GetBinLowEdge(nx+1))
        #print " binLowEdge = ", binLowEdge

        new_histo = ROOT.TH1D("temporary","",nx,array('d',binLowEdge))
          
        for iBin in range(1, nx+1):
          new_histo.SetBinContent(iBin, myhisto.GetBinContent(iBin))
          new_histo.SetBinError  (iBin, myhisto.GetBinError(iBin))
          
        new_histo.SetName  (myhisto.GetName())
        new_histo.SetTitle (myhisto.GetTitle())
        
        return new_histo
        
    # _____________________________________________________________________________
    def _AddErrors(self, myhisto, templatehisto): 
        for iBin in range(1, myhisto.GetNbinsX()+1):
            newerror = math.sqrt(pow(myhisto.GetBinError(iBin),2)+pow(templatehisto.GetBinError(iBin),2))
            myhisto.SetBinError(iBin,newerror)


if __name__ == '__main__':
    sys.argv = argv
    
    print(colored(r'''
----------------------------------------------------------------------------------------------------------------------------------


    _ \                                            _ \               |         ____| _)  |               |         |         
  |   |   __|  _ \  __ \    _` |   __|  _ \      |   |  _ \    __|  __|       |      |  __|      __ \   |   _ \   __|   __| 
  ___/   |     __/  |   |  (   |  |     __/      ___/  (   | \__ \  | _____|  __|    |  |        |   |  |  (   |  |   \__ \ 
 _|     _|   \___|  .__/  \__,_| _|   \___|     _|    \___/  ____/ \__|      _|     _| \__|      .__/  _| \___/  \__| ____/ 
                   _|                                                                           _|                          
 

----------------------------------------------------------------------------------------------------------------------------------
''', "green", attrs=["bold"]))
    
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--inputFileCombine'       , dest='inputFileCombine'       , help='file with Combine post-fit results. Typically FitDiagnostics output.'                          , default='input.root')
    parser.add_option('--outputFile'             , dest='outputFile'             , help='output file with histograms, same format as mkShape.py output'  , default='output.root')
    parser.add_option('--variable'               , dest='variable'               , help='variable name', default='mll')
    parser.add_option('--cut'                    , dest='cut'                    , help='cut name as appears in inputFileCombine'  , default='ch1')
    parser.add_option('--cutNameInOriginal'      , dest='cutNameInOriginal'      , help='cut name as appears in cuts.py with "_<category>" appended'  , default='hww2l2v_13TeV_0j')
    parser.add_option('--inputFile'              , dest='inputFile'              , help='input file with histograms (only to get the DATA distribution)' , default='input.root')
    parser.add_option('--isInputFileFromDatacard', dest='isInputFileFromDatacard', help='Use this option to specify if inpuFile is from datacard shapes. Set to 1 to trigger this.', type=int, default=0)
    parser.add_option('--kind'                   , dest='kind'                   , help='which kind of post-fit distribution: s = signal + background, b = background only, p = prefit'  , default='s')
    parser.add_option('--structureDir'           , dest='structureDir'           , help='structure.py directory', default=None )
    parser.add_option('--getSignalFromPrefit'    , dest='getSignalFromPrefit'    , help='get the signal shape and normalization from pre-fit. Needed for exclusion analyses. Set to 1 to trigger this.', default=0,    type=int)
    parser.add_option('--MCStatFromInput'        , dest='MCStatFromInput'        , help='add prefit MC stat. unc. to posterior total unc. (for bystander fits)', type=int, default=0)
          
    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print(" inputFileCombine        =          ", opt.inputFileCombine)
    print(" inputFile (for DATA)    =          ", opt.inputFile)
    print(" isInputFileFromDatacard =          ", opt.isInputFileFromDatacard)
    print(" outputFile              =          ", opt.outputFile)
    print(" variable                =          ", opt.variable)
    print(" cut                     =          ", opt.cut)
    print(" kind                    =          ", opt.kind)
    print(" getSignalFromPrefit     =          ", opt.getSignalFromPrefit)
    print(" structureDir            =          ", opt.structureDir)
    print(" cutNameInOriginal       =          ", opt.cutNameInOriginal)


    if opt.cutNameInOriginal == '' :
      opt.cutNameInOriginal = opt.cut

    if os.path.exists(opt.outputFile):
        print("")
        print(colored("Output file: '" + opt.outputFile + "' already exists and will be overwritten.", "yellow", attrs=["bold"]))
        print("")
        import time
        time.sleep(5)
        os.remove(opt.outputFile)
    # if not opt.debug:
    #     pass
    # elif opt.debug == 2:
    #     print('Logging level set to DEBUG (%d)' % opt.debug)
    #     logging.basicConfig( level=logging.DEBUG )
    # elif opt.debug == 1:
    #     print('Logging level set to INFO (%d)' % opt.debug)
    #     logging.basicConfig( level=logging.INFO )

    factory = LawnMower()
    factory._inputFileCombine    = opt.inputFileCombine
    factory._outputFileName      = opt.outputFile
    factory._variable            = opt.variable
    factory._cut                 = opt.cut
    factory._cutNameInOriginal   = opt.cutNameInOriginal
    factory._kind                = opt.kind
    factory._getSignalFromPrefit = opt.getSignalFromPrefit
    factory._MCStatFromInput     = opt.MCStatFromInput



    # # ~~~~
    # samples = OrderedDict()
    # if os.path.exists(opt.samplesFile) :
    #   handle = open(opt.samplesFile,'r')
    #   exec(handle)
    #   handle.close()

    # factory._samples = samples

    # ~~~~
    if opt.structureDir == None :
       print(" Please provide the structure directory ")
       #exit ()

    elif os.path.exists(opt.structureDir) :
      # handle = open(opt.structureDir,'r')
      # exec(handle)
      # handle.close()
      sys.path.append('{}'.format(opt.structureDir))
      # import structure
      from structure import structure
      print(structure)

    factory._structure = structure
    
    factory._inputFile = opt.inputFile
    factory._isInputFileFromDatacard = opt.isInputFileFromDatacard
    
    factory.makePostFitPlot()
    
    print('... and now closing ...')
        
       
       
       
