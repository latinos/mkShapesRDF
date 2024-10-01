import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.PUWeight_cfg import PUCfg
import correctionlib

import os

ROOT.PyConfig.IgnoreCommandLineOptions = True

from copy import deepcopy

correctionlib.register_pyroot_binding()


class runDependentPuW(Module):
    def __init__(
            self,
            era="Full2022EEv11",
            files = []
    ):
        super().__init__("runDependentPuW")

        self.era = era
        self.PUWeightCfg = PUCfg[era]
        self.files = files

        self.base_path = ""
        if "processor" in os.path.dirname(os.path.dirname(__file__)):
            self.base_path = (
                os.path.dirname(os.path.dirname(__file__)).split("processor")[0]
            )
            

    def runModule(self, df, values):


        targeth = {}
        targeth['beginRP']    = []
        targeth['endRP']      = []
        targeth['hist']       = []
        targeth['name']       = []

        which_runP = """"""

        for rpr in self.PUWeightCfg['targetfiles'] : 

            targeth['beginRP'] = int(rpr.split('-')[0])
            targeth['endRP']  = int(rpr.split('-')[1])

            inputFile = self.base_path + self.PUWeightCfg['targetfiles'][rpr]

            s = f"""
            TFile* PUFile_{targeth['beginRP']} = TFile::Open("{inputFile}");
            TH1D* PUProfile_{targeth['beginRP']} = PUFile_{targeth['beginRP']}->Get<TH1D>("{self.PUWeightCfg['targethist']}");
            """
            
            ROOT.gROOT.ProcessLine(s)

            if self.PUWeightCfg['doSysVar']:                
                s = f"""
                TH1D* PUProfile_{targeth['beginRP']}_plus =  PUFile_{targeth['beginRP']}->Get<TH1D>("{self.PUWeightCfg['targethist']}_plus");
                TH1D* PUProfile_{targeth['beginRP']}_minus =  PUFile_{targeth['beginRP']}->Get<TH1D>("{self.PUWeightCfg['targethist']}_minus");
                """            
                ROOT.gROOT.ProcessLine(s)
                
                which_runP = which_runP + """
                if (runP>="""+str(targeth['beginRP'])+""" && runP<="""+str(targeth['endRP'])+"""){
                    targethist       = PUProfile_"""+str(targeth['beginRP'])+""";
                    targethist_plus  = PUProfile_"""+str(targeth['beginRP'])+"""_plus;
                    targethist_minus = PUProfile_"""+str(targeth['beginRP'])+"""_minus;
                }
                """
            else:
                which_runP = which_runP + """                                                                                                                                                              
                if (runP>="""+str(targeth['beginRP'])+""" && runP<="""+str(targeth['endRP'])+"""){                                                                                               
                    targethist       = PUProfile_"""+str(targeth['beginRP'])+""";                                                                                                                          
                }                                                                                                                                                                                          
                """


        name = self.PUWeightCfg['name']
        norm = self.PUWeightCfg['norm']
        nvtxVar = self.PUWeightCfg['nvtx_var']
        doSysVar = self.PUWeightCfg['doSysVar']
        verbose = self.PUWeightCfg['verbose']
        #verbose = True

        fixLargeWeights = True
        if self.PUWeightCfg['srcfile'] != "auto" :
            inputFile = self.base_path + self.PUWeightCfg['srcfile']
            s = f"""                                                                                                                                                                                       
            TFile* SRCFile = TFile::Open("{inputFile}");                                                                                                                                                   
            TH1* hist = SRCFile->Get<TH1*>("{self.PUWeightCfg['srchist']}");                                                                                                                                     
            """
        else:
            fixLargeWeights = False

            myFile = ROOT.TFile.Open(inputFile, "READ")
            myHist = myFile.Get(self.PUWeightCfg['targethist'])
            myModel = ROOT.RDF.TH1DModel(myHist)
            hist = df.Histo1D(myModel, nvtxVar)

            s = """
            float xmin = """ + str(myHist.GetXaxis().GetXmin()) + """;
            float xmax = """ + str(myHist.GetXaxis().GetXmax()) + """;
            ROOT::RVecF hist_values = {"""
            for i in range(hist.GetNbinsX()-1):
                s = s + str(hist.GetBinContent(i)) + ""","""
            s = s + str(hist.GetBinContent(hist.GetNbinsX()-1)) + """};
            TH1D hist = TH1D("HistPU", "HistPU", hist_values.size(), xmin, xmax);
            for (int i=0; i<hist_values.size(); i++){
                hist.SetBinContent(i, hist_values[i]);
            }
            """

            ### Why this is not working? Cling error!
            #inFiles = """{"""
            #for iF in self.files[:len(self.files)-1]:
            #    inFiles = inFiles + iF + ""","""
            #inFiles = inFiles + self.files[len(self.files)-1] + """};"""

            #s = """
            #std::vector<string> inputFiles = """+inFiles+f"""
            #ROOT::RDataFrame tmp_df = ROOT::RDataFrame("Events", inFiles);      
            #TH1D* myHist =  (TH1D*)PUProfile_1->Clone("autoPU");
            #myHist->Reset();
            #ROOT::RDF::TH1DModel myModel = ROOT::RDF::TH1DModel(*myHist);
            #TH1D* hist = tmp_df.Histo1D(myModel, "{nvtxVar}").GetPtr();
            #"""

        
        ROOT.gROOT.ProcessLine(s)
        
        ROOT.gInterpreter.Declare(
            """
            float computeWeights(int nvertex, TH1D* targethist, bool norm, bool verbose_, bool fixLargeWgts, std::vector<float> refvals_, std::vector<float> targetvals_){
  
                float result = 0.0;
                TH1* histogram_;
                float maxshift=0.0025;
                float hardmax=3;

                TH1 *ret = (TH1*)hist.Clone("hweights");
                ret->SetDirectory(0);
                
                int nbins=hist.GetNcells();
                std::vector<float> vals;
                for(int i=0; i<nbins; ++i) {
                        double bc=hist.GetBinContent(i);
                        vals.push_back(std::max(bc,0.));
                }
                if(verbose_) std::cout << "Normalization of " << hist.GetName() << ": " << hist.Integral() << std::endl;
                if(norm) {
                        float scale = 1.0/hist.Integral();
                        for(int i=0; i<nbins; ++i) vals[i] *= scale;
                }
                
                nbins=targethist->GetNcells();
                std::vector<float> targetvals;
                for(int i=0; i<nbins; ++i) {
                        double bc=targethist->GetBinContent(i);
                        targetvals.push_back(std::max(bc,0.));
                }
                if(verbose_) std::cout << "Normalization of " << targethist->GetName() << ": " << targethist->Integral() << std::endl;
                if(norm) {
                        float scale = 1.0/targethist->Integral();
                        for(int i=0; i<nbins; ++i) targetvals[i] *= scale;
                }
                
                std::vector<float> weights;
                nbins = vals.size();
                if(verbose_) std::cout << "Weights for variable " << hist.GetName() << " with a number of bins equal to " << nbins << ":" << std::endl;
                for(int i=0; i<nbins; ++i) {
                        float weight = vals[i] !=0 ? targetvals[i]/vals[i] : 1.;
                        if(verbose_) std::cout <<  std::setprecision(3) << weight << " ";
                        weights.push_back(weight);
                }
                if(verbose_) std::cout << "." << std::endl;
                
                if(fixLargeWgts){

                    float maxw = std::min(*(std::max_element(weights.begin(),weights.end())),float(5.));
                    std::vector<float> cropped;
                    while (maxw > hardmax) {
                        cropped.clear();
                        for(int i=0; i<(int)weights.size(); ++i) cropped.push_back(std::min(maxw,weights[i]));
                        // Check integral
                        float myint=0;
                        float refint=0;
                        for(int i=0; i<(int)cropped.size(); ++i) {
                            myint += cropped[i]*refvals_[i];
                            refint += weights[i]*refvals_[i];
                        }
                        float shift = (myint-refint)/refint;
                        if(verbose_) std::cout << "For maximum weight " << maxw << ": integral relative change: " << shift << std::endl;
                        if(fabs(shift) > maxshift) break;
                        maxw *= 0.95;
                    }
                    maxw /= 0.95;
                    if (cropped.size()>0) {
                        for(int i=0; i<(int)weights.size(); ++i) cropped[i] = std::min(maxw,weights[i]);
                        float myint=0;
                        float refint=0;
                        for(int i=0; i<(int)cropped.size(); ++i) {
                            myint += cropped[i]*refvals_[i];
                            refint += weights[i]*refvals_[i];
                        }
                        float normshift = (myint-refint)/refint;
                        for(int i=0; i<(int)weights.size(); ++i) weights[i] = cropped[i]*(1-normshift);
                    }

                }

                if(verbose_) std::cout << "Final weights: " << std::endl;
                for(int i=0; i<(int)weights.size(); ++i) {
                    ret->SetBinContent(i,weights[i]);
                    if(verbose_) std::cout << std::setprecision(3) << weights[i] << " ";
                }
                if(verbose_) std::cout << "." << std::endl;
                histogram_ = ret;

                int bin = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(nvertex)));
                result = histogram_->GetBinContent(bin);
                return result;
            }

            ROOT::RVecF puWeights(int nvertex, int runP, bool doSyst, bool fixLargeWeights, bool norm, bool verbose){
                
                TH1D* targethist;
                TH1D* targethist_plus;
                TH1D* targethist_minus;

                float results = 0.0;
                float results_plus = 0.0;
                float results_minus = 0.0;

                std::vector<float> refvals_,targetvals_,targetvals_plus,targetvals_minus;

                """+which_runP+"""

                if (hist.GetNcells()!=targethist->GetNcells()){
                    cout << "ERROR! Numerator and denominator histograms have different number of bins!" << endl;
                    results = 0.0;
                    results_plus = 0.0;
                    results_minus = 0.0;
                }else{
                    for(int i=0; i<(int)hist.GetNcells(); ++i) {
                        refvals_.push_back(hist.GetBinContent(i));
                        targetvals_.push_back(targethist->GetBinContent(i));
                        if (doSyst){
                            targetvals_plus.push_back(targethist_plus->GetBinContent(i));
                            targetvals_minus.push_back(targethist_minus->GetBinContent(i));
                        }
                    }
                    results = computeWeights(nvertex, targethist, norm, verbose, fixLargeWeights, refvals_, targetvals_);
                    if (doSyst){
                        results_plus = computeWeights(nvertex, targethist, norm, verbose, fixLargeWeights, refvals_, targetvals_plus);
                        results_minus = computeWeights(nvertex, targethist, norm, verbose, fixLargeWeights, refvals_, targetvals_minus);
                    }
                }
                if (!doSyst){
                    ROOT::RVecF all_results(3, 0.0); 
                    all_results[0] = results;
                    all_results[1] = results;
                    all_results[2] = results;
                    return all_results;
                }else{
                    ROOT::RVecF all_results(3, 0.0);
                    all_results[0] = results;
                    all_results[1] = results_plus;
                    all_results[2] = results_minus;
                    return all_results;
                }
            }
            """
        )
        
        df = df.Define(
            name,
            "puWeights("+nvtxVar+", run_period, "+str(doSysVar).lower()+", "+str(fixLargeWeights).lower()+", "+str(norm).lower()+", "+str(verbose).lower()+")[0]"
        )

        df = df.Define(
            name+"Up",
            "puWeights("+nvtxVar+", run_period, "+str(doSysVar).lower()+", "+str(fixLargeWeights).lower()+", "+str(norm).lower()+", "+str(verbose).lower()+")[1]"
        )
              
        df = df.Define(
            name+"Down",
            "puWeights("+nvtxVar+", run_period, "+str(doSysVar).lower()+", "+str(fixLargeWeights).lower()+", "+str(norm).lower()+", "+str(verbose).lower()+")[2]"
        )  
        

        return df
