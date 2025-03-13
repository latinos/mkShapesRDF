import json
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *
import ROOT
#import sys
#sys.path.insert(0, list(filter(lambda k: 'myenv/lib' in k, sys.path))[0])
import os
import uproot
import awkward as ak
import pandas as pd
import numpy as np
from math import ceil

class addTnPTree(Module):
    def __init__(self, era, flavor, saveParquet=True, eosPath="", outputFilename=""):
        super().__init__("addTnPTree")

        self.era = era
        self.flavor = flavor
        
        self.saveParquet = saveParquet
        self.eosPath = eosPath
        self.outputFilename = outputFilename
        
        if ("2022" in self.era) or ("2023" in self.era):
            if self.flavor == "Electron": 
                self.tagSel   = "Electron_pt>34 && Electron_cutBased>3 && abs(Electron_eta)<2.5 && (Electron_filterBits & 1)"
                self.probeSel = "Electron_pt>7.0 && abs(Electron_eta)<2.5"
                self.passTrig = "HLT_Ele35_WPTight_Gsf"
            elif self.flavor == "Muon":
                self.tagSel   = "Muon_pt>26.0 && Muon_tightId && abs(Muon_eta)<2.4 && (Muon_filterBits & 3)"
                self.probeSel = "Muon_pt>5.0 && Muon_isTracker && abs(Muon_eta)<2.4"
                self.passTrig = "HLT_IsoMu24"

            self.mass_range = [60, 140]
        else:
            if self.flavor == "Electron":
                self.tagSel   = "Electron_pt>34 && Electron_cutBased>3 && abs(Electron_eta)<2.5 && (Electron_filterBits & 1)"                
                self.probeSel = "Electron_pt>7.0 && abs(Electron_eta)<2.5"
                self.passTrig = "HLT_Ele35_WPTight_Gsf"
            elif self.flavor == "Muon":
                self.tagSel   = "Muon_pt>26.0 && Muon_tightId && abs(Muon_eta)<2.4 && (Muon_filterBits & 3)"
                self.probeSel = "Muon_pt>5.0 && Muon_isTracker && abs(Muon_eta)<2.4"
                self.passTrig = "HLT_IsoMu24"

            self.mass_range = [60, 140]
            
        self.era = era
        
    def runModule(self, df, values):

        if not hasattr(ROOT, "sortedIndices"):
            ROOT.gInterpreter.Declare(
                """
                #include "ROOT/RDataFrame.hxx"
                #include "ROOT/RVec.hxx"
                #include "Math/Vector4D.h"

                using namespace ROOT;
                using namespace ROOT::VecOps;

                RVecI sortedIndices(RVecF variable){
                    // return sortedIndices based on variable
                    return Reverse(Argsort(variable));
                }
                """
            )
        
        ROOT.gInterpreter.Declare(
            """
            #include "ROOT/RDataFrame.hxx"
            #include "ROOT/RVec.hxx"
            #include "Math/Vector4D.h"

            using namespace ROOT;
            using namespace ROOT::VecOps;
            
            RVecI CreateTrigIndex(const RVecF Lepton_eta,
		                  const RVecF Lepton_phi,
                                  const RVecI Lepton_pdgId,
		                  const RVecF TrigObj_eta,
		                  const RVecF TrigObj_phi,
                                  const RVecI TrigObj_id,
		                  const float minDR=0.1)
            {
                RVecI Lepton_TrigIdx(Lepton_eta.size(), 999);
                float dR = 999.9;

                for (int iLep=0; iLep < Lepton_eta.size(); iLep++){
                        float tmpDR = minDR;
                        for (int iTr=0; iTr < TrigObj_eta.size(); iTr++){
                            if (Lepton_pdgId[iLep] == TrigObj_id[iTr]){
                                dR = DeltaR(Lepton_eta[iLep], TrigObj_eta[iTr], Lepton_phi[iLep], TrigObj_phi[iTr]);
                                if (dR<tmpDR){
	                            tmpDR = dR;
	                            Lepton_TrigIdx[iLep] = iTr;
                                }
                            }
                        }
                }
                return Lepton_TrigIdx;
            }

            RVec<std::pair<int,int>> CreateTPPair(const RVec<Int_t> &Tag_leptons,
                                                  const RVec<Int_t> &Probe_Candidates,
                                                  const int doOppositeCharge,
                                                  const RVec<Int_t> &Tag_Charge,
                                                  const RVec<Int_t> &Probe_charge,
                                                  const int isSameCollection = true)
            {
                RVec<std::pair<int,int>> TP_pairs;

                for (int iLep1 = 0; iLep1 < Tag_leptons.size(); iLep1++) {
                        
                    if (!Tag_leptons[iLep1]) continue;
                    for(int iLep2 = 0; iLep2 < Probe_Candidates.size(); iLep2++){
                            
                        if (isSameCollection && (iLep1 == iLep2)) continue;
                        if (!Probe_Candidates[iLep2]) continue;
                        if (doOppositeCharge && (Tag_Charge[iLep1] == Probe_charge[iLep2])) continue;
                        std::pair<int,int> TP_pair = std::make_pair(iLep1, iLep2);
                        TP_pairs.push_back(TP_pair);
                    }          
                }              
                return TP_pairs;
            }


            RVec<Float_t> getTPVariables(RVec<std::pair<int,int>> TPPairs,
                                         RVec<Float_t> &Lepton_pt, RVec<Float_t> &Lepton_eta, RVec<Float_t> &Lepton_phi,
                                         RVec<Float_t> &Cand_pt, RVec<Float_t> &Cand_eta, RVec<Float_t> &Cand_phi,
                                         int option = 4 /* 1 = pt, 2 = eta, 3 = phi, 4 = mass*/ )
            {
                RVec<Float_t> TPVariables;
                for (int i=0;i<TPPairs.size();i++){
                    std::pair<int,int> TPPair = TPPairs.at(i);
                    int tag_index = TPPair.first;
                    int probe_index = TPPair.second;
                    ROOT::Math::PtEtaPhiMVector tag(  Lepton_pt[tag_index],   Lepton_eta[tag_index],   Lepton_phi[tag_index],   0.0);
                    ROOT::Math::PtEtaPhiMVector probe(Cand_pt[probe_index], Cand_eta[probe_index], Cand_phi[probe_index], 0.0);
                    if (option == 1) TPVariables.push_back( (tag + probe).pt() );
                    else if (option == 2 ) TPVariables.push_back( (tag + probe).eta() );
                    else if (option == 3) TPVariables.push_back( (tag + probe).phi() );
                    else if (option == 4) TPVariables.push_back( (tag + probe).mass() );
                }
                return TPVariables;   
            }

            RVecB getDuplicatedProbes(RVec<std::pair<int,int>> TPPairs, RVec<Float_t> &Cand_pt)
            {
                RVecB Cand_duplicated(Cand_pt.size(), false);
                RVecI Cand_index;
                for (int i=0;i<TPPairs.size();i++){
                    Cand_index.push_back(TPPairs.at(i).second);
                }
                for (int i=0;i<Cand_index.size();i++){
                    if (Sum(Cand_index==Cand_index[i])>1) Cand_duplicated[Cand_index[i]] = true;
                }
                return Cand_duplicated;  
            }
            
            template <typename T>
            RVec<T> getVariables(RVec<std::pair<int,int>> TPPairs,
                                 RVec<T>  &Cand_variable,
                                 int option /*1 for tag, 2 for probe*/)
            {
                RVec<T>  Variables(TPPairs.size(), 0);    
                for (int i = 0; i < TPPairs.size(); i++){
                    std::pair<int, int> TPPair = TPPairs.at(i);
                    T variable;
                    if (option==1)      variable = Cand_variable.at(TPPair.first);
                    else if (option==2) variable = Cand_variable.at(TPPair.second);
                    Variables[i] = variable;
                }
                return Variables;
            }
            """
        )

        collection = "Electron" if self.flavor=="Electron" else "Muon"
        
        df = df.Define(f"{collection}_trigIdx",    f"CreateTrigIndex({collection}_eta, {collection}_phi, {collection}_pdgId, TrigObj_eta, TrigObj_phi, TrigObj_id, 0.1)")
        df = df.Define(f"{collection}_isTrig",     f"{collection}_trigIdx < 950")
        df = df.Define(f"{collection}_filterBits", f"Take(TrigObj_filterBits, {collection}_trigIdx, 0)")

        df = df.Alias("Tag_pt",     f"{collection}_pt")
        df = df.Alias("Tag_eta",    f"{collection}_eta")
        df = df.Alias("Tag_phi",    f"{collection}_phi")
        df = df.Alias("Tag_charge", f"{collection}_charge")
        
        df = df.Define(f"Tag_{collection}",   self.tagSel)
        df = df.Define(f"Probe_{collection}", self.probeSel)

        df = df.Alias("Tag_trigIdx",    f"{collection}_trigIdx")
        df = df.Alias("Tag_isTrig",     f"{collection}_isTrig")

        df = df.Define("All_TPPairs", f"CreateTPPair(Tag_{collection}, Probe_{collection}, 1, Tag_charge, {collection}_charge, 1)")
        df = df.Define("All_TPmass",  f"getTPVariables(All_TPPairs, Tag_pt, Tag_eta, Tag_phi, {collection}_pt, {collection}_eta, {collection}_phi, 4)")
        
        df = df.Define("TPPairs", f"All_TPPairs[All_TPmass>{self.mass_range[0]} && All_TPmass<{self.mass_range[1]}]")

        df = df.Filter("TPPairs.size() > 0")

        df = df.Define("pair_pt",    f"getTPVariables(TPPairs, Tag_pt, Tag_eta, Tag_phi, {collection}_pt, {collection}_eta, {collection}_phi, 1)")
        df = df.Define("pair_eta",   f"getTPVariables(TPPairs, Tag_pt, Tag_eta, Tag_phi, {collection}_pt, {collection}_eta, {collection}_phi, 2)")
        df = df.Define("pair_phi",   f"getTPVariables(TPPairs, Tag_pt, Tag_eta, Tag_phi, {collection}_pt, {collection}_eta, {collection}_phi, 3)")
        df = df.Define("pair_mass",  f"getTPVariables(TPPairs, Tag_pt, Tag_eta, Tag_phi, {collection}_pt, {collection}_eta, {collection}_phi, 4)")

        df = df.Define("npairs",              "TPPairs.size()")
        df = df.Define("nTag",                f"Sum(Tag_{collection}==true)")
        df = df.Define("nVertices",           "PV_npvs")
        df = df.Define(f"{collection}_isDuplicated",  f"getDuplicatedProbes(TPPairs, {collection}_pt)")
        df = df.Define(f"probe_isDuplicated", f"getVariables(TPPairs, {collection}_isDuplicated, 2)")

        ### Create new branches
        variables_to_save = []
        variables_to_skip = ["vidNestedWPBitmap", "seediEtaOriX"]
        for var in df.GetColumnNames():
            if str(var).startswith(f"{collection}_"):
                label = var.split(f"{collection}_")[1]

                if label in variables_to_skip: continue
                df = df.Define(f"probe_{label}", f"getVariables(TPPairs, {var}, 2)")
                variables_to_save.append(f"probe_{label}")
                
                df = df.Define(f"tag_{label}", f"getVariables(TPPairs, {var}, 1)")
                variables_to_save.append(f"tag_{label}")
                
        variables_to_save.append("npairs")
        variables_to_save.append("pair_mass")
        variables_to_save.append("pair_pt")
        variables_to_save.append("pair_eta")
        variables_to_save.append("pair_phi")
        variables_to_save.append("probe_isDuplicated")
        variables_to_save.append("nTag")
        variables_to_save.append("event")
        variables_to_save.append("nVertices")
        variables_to_save.append("run")
        variables_to_save.append("luminosityBlock")
        if "genWeight" in df.GetColumnNames():
            variables_to_save.append("genWeight")
            variables_to_save.append("puWeight")
            variables_to_save.append("Pileup_nTrueInt")
            variables_to_save.append("Pileup_nPU")
            
        variables_to_save.append(self.passTrig)

        ### Expand additional variables
        for var in variables_to_save:
            if var.startswith("pair") or var.startswith("probe") or var.startswith("tag"):
                continue
            df = df.Redefine(var, f"RVecD(pair_mass.size(), {var})")

        if not self.saveParquet:
            return df
            
        chunksize = 10_000
        nIterations = max(ceil(df.Count().GetValue() / chunksize), 1)
        branches = variables_to_save
        outName = self.eosPath + "/" + self.outputFilename.split(".root")[0] + ".parquet"

        if not os.path.isdir(os.path.dirname(outName)):
            os.makedirs(os.path.dirname(outName))

        writeROOT = False
        if self.flavor=="Electron":
            writeROOT = True
            outName = outName.replace(".parquet", ".root")
            
        first = True

        print("Total number of iterations -> " + str(nIterations))
        print("Total number of events     -> " + str(df.Count().GetValue()))
        print("Output branches:")
        print("----------------")
        print(branches)

        for i in range(nIterations):
            print("Iteration: " + str(i))
            _df = df.df.Range(i * chunksize, (i+1) * chunksize)
            events = ak.from_rdataframe(_df, branches)            
        
            def getBranchFlatten(events, branch):
                ak_array = [ak.Array(v) for v in events[branch]]
                np_array = ak.to_numpy(ak.flatten(ak_array))
                return np_array
            
            df_np = {}
            for key in branches:
                df_np[key] = getBranchFlatten(events, key)

            if writeROOT:
                if first:
                    outFile = uproot.recreate(outName)
                    outFile["Events"] = df_np
                    outFile.close()
                else:
                    outFile = uproot.update(outName)
                    outFile["Events"].extend(df_np)
                    outFile.close()
            else:
                df_ak = pd.DataFrame(df_np)        
                if first:
                    df_ak.to_parquet(outName, engine='fastparquet', append=False)
                    first=False
                else:
                    df_ak.to_parquet(outName, engine='fastparquet', append=True)            

        return df
