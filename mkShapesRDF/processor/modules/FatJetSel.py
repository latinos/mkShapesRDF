import ROOT
from mkShapesRDF.processor.framework.module import Module
#from mkShapesRDF.processor.modules.LeptonMaker import LeptonMaker 


# Dictionary for FatJet cuts  
FatJetFilter_dict = {
   'default' : { 'pt_min': 0 , 'pt_max' : 5000, 'max_eta' : 2.4, 'max_tau21': 1000, 'mass_range' : [0 , 10000],
               'DeltaRlep' : 0.4, 'DeltaRjet' : 0.4, 'jet_id' : 0},
}

class FatJetSel(Module):

    def __init__(self, Mask=True, dict=FatJetFilter_dict, Era = "default"):
        super().__init__("FatJetSel")   
        cuts = dict[Era]
        self.max_pt = cuts['pt_max']
        self.min_pt = cuts['pt_min']
        self.max_eta = cuts['max_eta']
        self.max_tau21 = cuts['max_tau21']
        self.mass_range = cuts['mass_range']
        self.DeltaRjet = cuts['DeltaRjet']
        self.DeltaRlep = cuts['DeltaRlep']
        self.jet_id = cuts['jet_id']



    def CheckCuts(self, df): 
        goodFatJet =( f"CleanFatJet_pt >= {self.min_pt} && CleanFatJet_pt <= {self.max_pt} && " +
                     f"abs(CleanFatJet_eta) <= {self.max_eta} && " + 
                     f"(CleanFatJet_tau21 <= {self.max_tau21} && CleanFatJet_tau1 > 0) && " +
                     f"CleanFatJet_msoftdrop >= {self.mass_range[0]} && CleanFatJet_msoftdrop <= {self.mass_range[1]} && " +
                     f"CleanFatJet_jetId > {self.jet_id} && " +
                     f"CheckDeltaR(CleanFatJet_phi, CleanJet_phi, CleanFatJet_eta, CleanJet_eta, {self.DeltaRjet})"
                    )
        return goodFatJet


    # *********************************************************** #
    # ******************** RUN MODULE ************************* #
    # *********************************************************** #
    def runModule(self, df, values):
        columnsToDrop = []

        # // Define CLeanJet, CleanFatJet, Lepton columns
        # df = self.lepMake.runModule(df, values)

        # //////////////////////////////////////// #
        # // apply cuts 
        CheckDeltaR = (""" 
            ROOT::RVec<Bool_t> CheckDeltaR(ROOT::RVec<double> phi1, ROOT::RVec<double> phi2, ROOT::RVec<double> eta1, ROOT::RVec<double> eta2, double DeltaRcuts) {
             ROOT::RVec<Bool_t> result(phi1.size(), false);
              for (size_t i = 0; i < phi1.size(); ++i) {
                result[i] = false;  
                 for (size_t j = 0; j < phi2.size(); ++j) {
                  double dphi = phi1[i] - phi2[j];
                  if (dphi > ROOT::Math::Pi()) dphi -= 2 * ROOT::Math::Pi();
                  if (dphi < -ROOT::Math::Pi()) dphi += 2 * ROOT::Math::Pi();
                  double deta = eta1[i] - eta2[j];
                  double deltaR = sqrt(deta * deta + dphi * dphi);
                  if (deltaR < DeltaRcuts) {
                    result[i] = true;  
                    break;
                  }
                 }
              }
            return result;
            }
        """)
        ROOT.gInterpreter.Declare(CheckDeltaR)   
        

        cut_FatJets  = self.CheckCuts(df)
        df = df.Define("CleanFatJetMask", cut_FatJets)  

        
        columnsToDrop.append("CleanFatJet_Mask") 
        vars_ToDrop = ["Mask", "tau1", "tau2", "tau21", "jetId", "msoftdrop"]
        for i in vars_ToDrop:
            columnsToDrop.append(f"CleanFatJet_{i}")
        # //////////////////////////////////////// #

        # //////////////////////////////////////// #

        # store jets that are not fatjets
        df = df.Define("isCleanJetNotFat", f" ! CheckDeltaR(CleanJet_phi, CleanFatJet_phi, CleanJet_eta, CleanFatJet_eta, {self.DeltaRjet})")
        df = df.Define("isLeptonNotFat", f" ! CheckDeltaR(Lepton_phi, CleanFatJet_phi, Lepton_eta, CleanFatJet_eta, {self.DeltaRlep})")
        df = df.Define("MuonNotFat_Idx", "Lepton_electronIdx[isLeptonNotFat]")
        df = df.Define("ElectronNotFat_Idx", "Lepton_muonIdx[isLeptonNotFat]")
    


        # apply mask
        CleanFatJet_variables = ["jetId",  "pt", "eta", "mass", "phi" , "msoftdrop", "tau1", "tau2", "tau21"]
        for var in CleanFatJet_variables:
            df = df.Redefine(
                f"CleanFatJet_{var}", f"CleanFatJet_{var}[CleanFatJetMask]"
            )
                
        columnsToDrop.append("isCleanJetNotFat")
        columnsToDrop.append("isLeptonNotFat")
  
    
        # remove columns
        ''' 
        columnsToDrop.extend(DroppedColumns)
        for col in columnsToDrop:
            df = df.DropColumns(col)
        '''
        return df
    # ******************** END RUN MODULE ********************** #
    # ********************************************************** #