import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.LeptonSel_cfg import *
import correctionlib
import os

correctionlib.register_pyroot_binding()


class LeptonSF(Module):
    # def __init__(self, LepFilter, nLF):
    def __init__(self, era):
        super().__init__("LeptonSF")
        self.era = era
        if ("Full2022EEv11" in era) or ("Full2022EEv12" in era):
            self.egamma_era = "2022FG"
        elif ("Full2022v12" in era):
            self.egamma_era = "2022Re-recoBCD"
        
        self.mu_maxPt = 199.9
        self.mu_minPt = 15.001
        self.mu_maxEta = 2.3999
        self.mu_minEta = -2.3999

        self.el_maxPt = 499.99
        self.el_minPt = 10.001
        self.el_maxEta = 2.4999
        self.el_minEta = -2.4999

        self.LepFilter = LepFilter_dict
        self.ElectronWP = ElectronWP
        self.MuonWP = MuonWP

        self.cfg_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0]

        self.SF_dict = {}

        # electron setup
        self.SF_dict["electron"] = {}
        for wp in self.ElectronWP[self.era]["TightObjWP"]:
            self.SF_dict["electron"][wp] = {}
            self.SF_dict["electron"][wp]["tkSF"] = {}
            self.SF_dict["electron"][wp]["wpSF"] = {}
            self.SF_dict["electron"][wp]["hasTrk"] = False
            for SFkey in self.ElectronWP[self.era]["TightObjWP"][wp]:
                if SFkey == "tkSF":
                    self.SF_dict["electron"][wp]["hasTrk"] = True
                    self.SF_dict["electron"][wp]["tkSF"]["data"] = []
                    self.SF_dict["electron"][wp]["tkSF"]["key"] = []
                    self.SF_dict["electron"][wp]["tkSF"]["beginRP"] = []
                    self.SF_dict["electron"][wp]["tkSF"]["endRP"] = []
                    for rpr in self.ElectronWP[self.era]["TightObjWP"][wp]["tkSF"]:
                        self.SF_dict["electron"][wp]["tkSF"]["beginRP"].append(
                            int(rpr.split("-")[0])
                        )
                        self.SF_dict["electron"][wp]["tkSF"]["endRP"].append(
                            int(rpr.split("-")[1])
                        )
                        temp_file = (
                            self.cfg_path
                            + "/processor/"
                            + self.ElectronWP[self.era]["TightObjWP"][wp]["tkSF"][rpr][1]
                        )
                        self.SF_dict["electron"][wp]["tkSF"]["data"].append(temp_file)
                        self.SF_dict["electron"][wp]["tkSF"]["key"].append(
                            self.ElectronWP[self.era]["TightObjWP"][wp]["tkSF"][rpr][0]
                        )
                if SFkey == "wpSF":
                    self.SF_dict["electron"][wp]["wpSF"]["data"] = []
                    self.SF_dict["electron"][wp]["wpSF"]["key"] = []
                    self.SF_dict["electron"][wp]["wpSF"]["beginRP"] = []
                    self.SF_dict["electron"][wp]["wpSF"]["endRP"] = []
                    for rpr in self.ElectronWP[self.era]["TightObjWP"][wp]["wpSF"]:
                        self.SF_dict["electron"][wp]["wpSF"]["beginRP"].append(
                            int(rpr.split("-")[0])
                        )
                        self.SF_dict["electron"][wp]["wpSF"]["endRP"].append(
                            int(rpr.split("-")[1])
                        )
                        temp_file = (
                            self.cfg_path
                            + "/processor/"
                            + self.ElectronWP[self.era]["TightObjWP"][wp]["wpSF"][rpr][
                                1
                            ]
                        )
                        self.SF_dict["electron"][wp]["wpSF"]["data"].append(temp_file)
                        self.SF_dict["electron"][wp]["wpSF"]["key"].append(
                            self.ElectronWP[self.era]["TightObjWP"][wp]["wpSF"][rpr][0]
                        )

        # muon setup
        self.SF_dict["muon"] = {}
        for wp in self.MuonWP[self.era]["TightObjWP"]:
            self.SF_dict["muon"][wp] = {}
            self.SF_dict["muon"][wp]["tkSF"] = {}
            self.SF_dict["muon"][wp]["idSF"] = {}
            self.SF_dict["muon"][wp]["isoSF"] = {}
            self.SF_dict["muon"][wp]["tthMvaSF"] = {}
            self.SF_dict["muon"][wp]["hastthMvaSF"] = False
            for SFkey in self.MuonWP[self.era]["TightObjWP"][wp]:
                if SFkey == "idSF":
                    self.SF_dict["muon"][wp]["idSF"]["data"] = []
                    self.SF_dict["muon"][wp]["idSF"]["key"] = []
                    self.SF_dict["muon"][wp]["idSF"]["beginRP"] = []
                    self.SF_dict["muon"][wp]["idSF"]["endRP"] = []
                    for rpr in self.MuonWP[self.era]["TightObjWP"][wp]["idSF"]:
                        self.SF_dict["muon"][wp]["idSF"]["beginRP"].append(
                            int(rpr.split("-")[0])
                        )
                        self.SF_dict["muon"][wp]["idSF"]["endRP"].append(
                            int(rpr.split("-")[1])
                        )
                        temp_file = (
                            self.cfg_path
                            + "/processor/"
                            + self.MuonWP[self.era]["TightObjWP"][wp]["idSF"][rpr][1]
                        )
                        self.SF_dict["muon"][wp]["idSF"]["data"].append(temp_file)
                        self.SF_dict["muon"][wp]["idSF"]["key"].append(
                            self.MuonWP[self.era]["TightObjWP"][wp]["idSF"][rpr][0]
                        )

                if SFkey == "isoSF":
                    self.SF_dict["muon"][wp]["isoSF"]["data"] = []
                    self.SF_dict["muon"][wp]["isoSF"]["key"] = []
                    self.SF_dict["muon"][wp]["isoSF"]["beginRP"] = []
                    self.SF_dict["muon"][wp]["isoSF"]["endRP"] = []
                    for rpr in self.MuonWP[self.era]["TightObjWP"][wp]["isoSF"]:
                        self.SF_dict["muon"][wp]["isoSF"]["beginRP"].append(
                            int(rpr.split("-")[0])
                        )
                        self.SF_dict["muon"][wp]["isoSF"]["endRP"].append(
                            int(rpr.split("-")[1])
                        )
                        temp_file = (
                            self.cfg_path
                            + "/processor/"
                            + self.MuonWP[self.era]["TightObjWP"][wp]["isoSF"][rpr][1]
                        )
                        self.SF_dict["muon"][wp]["isoSF"]["data"].append(temp_file)
                        self.SF_dict["muon"][wp]["isoSF"]["key"].append(
                            self.MuonWP[self.era]["TightObjWP"][wp]["isoSF"][rpr][0]
                        )

                if SFkey == "tthMvaSF":
                    self.SF_dict["muon"][wp]["hastthMvaSF"] = True
                    self.SF_dict["muon"][wp]["tthMvaSF"]["beginRP"] = []
                    self.SF_dict["muon"][wp]["tthMvaSF"]["endRP"] = []
                    self.SF_dict["muon"][wp]["tthMvaSF"]["data"] = []
                    self.SF_dict["muon"][wp]["tthMvaSF"]["key"] = []
                    for rpr in self.MuonWP[self.era]["TightObjWP"][wp]["tthMvaSF"]:
                        self.SF_dict["muon"][wp]["tthMvaSF"]["beginRP"].append(
                            int(rpr.split("-")[0])
                        )
                        self.SF_dict["muon"][wp]["tthMvaSF"]["endRP"].append(
                            int(rpr.split("-")[1])
                        )
                        temp_file = (
                            self.cfg_path
                            + "/processor/"
                            + self.MuonWP[self.era]["TightObjWP"][wp]["tthMvaSF"][rpr][
                                1
                            ]
                        )
                        self.SF_dict["muon"][wp]["tthMvaSF"]["data"].append(temp_file)
                        self.SF_dict["muon"][wp]["tthMvaSF"]["key"].append(
                            self.MuonWP[self.era]["TightObjWP"][wp]["tthMvaSF"][rpr][0]
                        )

        print("LeptonSFMaker: making scale factors for analysis of " + self.era)

    def runModule(self, df, values):
        columnsToDrop = []
        did_reco = False

        df = df.Define("Lepton_RecoSF", "ROOT::RVecF(Lepton_pt.size(), 1.0)")

        df = df.Define("Lepton_RecoSF_Up", "ROOT::RVecF(Lepton_pt.size(), 1.0)")

        df = df.Define("Lepton_RecoSF_Down", "ROOT::RVecF(Lepton_pt.size(), 1.0)")

        ### Electrons
        for wp in self.SF_dict["electron"]:
            if self.SF_dict["electron"][wp]["hasTrk"] and not did_reco:
                interpret_runP = """"""

                for i in range(len(self.SF_dict["electron"][wp]["tkSF"]["data"])):
                    if os.path.exists(self.SF_dict["electron"][wp]["tkSF"]["data"][i]):
                        
                        pathToJson = self.SF_dict["electron"][wp]["tkSF"]["data"][i]

                        beginRP = self.SF_dict["electron"][wp]["tkSF"]["beginRP"][i]
                        endRP = self.SF_dict["electron"][wp]["tkSF"]["endRP"][i]

                        key = self.SF_dict["electron"][wp]["tkSF"]["key"][i]

                        ROOT.gROOT.ProcessLine(
                            f'auto csetEl_Reco_{beginRP}_{endRP} = correction::CorrectionSet::from_file("{pathToJson}");'
                        )
                        ROOT.gROOT.ProcessLine(
                            f'correction::Correction::Ref cset_electron_Reco_{beginRP}_{endRP} = (correction::Correction::Ref) csetEl_Reco_{beginRP}_{endRP}->at("{key}");'
                        )

                        interpret_runP = (
                            interpret_runP
                            + """
                        if (runP>="""
                            + str(beginRP)
                            + """ && runP<="""
                            + str(endRP)
                            + """){
                            cset_electron_Reco = cset_electron_Reco_%s_%s;
                        }
                        """ % (beginRP, endRP)
                        )

                    else:
                        print("Path does not exist for " + wp + " at:")
                        print(self.SF_dict["electron"][wp]["tkSF"]["data"][i])
                
                ROOT.gInterpreter.Declare(
                    """
                    std::vector<ROOT::RVecF> getSF_Reco(ROOT::RVecF ele_pt, ROOT::RVecF ele_eta, ROOT::RVecI ele_pdgId, int runP){

                        std::vector<ROOT::RVecF> SFTot;
                        ROOT::RVecF SF;
                        ROOT::RVecF SFup;
                        ROOT::RVecF SFdown;
                        float sf,sfup,sfdown;
                        float pt,eta;

                        correction::Correction::Ref cset_electron_Reco;

                        """
                        + interpret_runP
                        + """

                        for (int i=0; i<ele_pt.size(); i++){
                            if (abs(ele_pdgId[i])==11){

                                pt = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{ele_pt[i], """
                                + str(self.el_maxPt)
                                + """}), """
                                + str(self.el_minPt)
                                + """});
                                eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{ele_eta[i], """
                                + str(self.el_maxEta)
                                + """}), """
                                + str(self.el_minEta)
                                + """});
                                    
                                if (pt< 20){
                                    pt = ROOT::VecOps::Min(ROOT::RVecF{pt, 19.99});
                                    sf     = cset_electron_Reco->evaluate({"%s", "sf", "RecoBelow20", eta, pt});
                                    sfup   = cset_electron_Reco->evaluate({"%s", "sfup", "RecoBelow20", eta, pt});
                                    sfdown = cset_electron_Reco->evaluate({"%s", "sfdown", "RecoBelow20", eta, pt});
                                }else if (pt>=20.0 && pt<=75.0){
                                    pt = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{pt, 74.99}), 20.0001});
                                    sf = cset_electron_Reco->evaluate({"%s", "sf", "Reco20to75", eta, pt});
                                    sfup = cset_electron_Reco->evaluate({"%s", "sfup", "Reco20to75", eta, pt});
                                    sfdown = cset_electron_Reco->evaluate({"%s", "sfdown", "Reco20to75", eta, pt});
                                }else{
                                    sf     = cset_electron_Reco->evaluate({"%s", "sf", "RecoAbove75", eta, pt});
                                    sfup   = cset_electron_Reco->evaluate({"%s", "sfup", "RecoAbove75", eta, pt});
                                    sfdown = cset_electron_Reco->evaluate({"%s", "sfdown", "RecoAbove75", eta, pt});
                                }
                                    
                                SF.push_back(sf);
                                SFup.push_back(sfup-sf);
                                SFdown.push_back(sf-sfdown);
                            }else{
                                SF.push_back(1.0);
                                SFup.push_back(1.0);
                                SFdown.push_back(1.0);
                            }
                        }

                        SFTot.push_back(SF);
                        SFTot.push_back(SFup);
                        SFTot.push_back(SFdown);
                        return SFTot;
                    }
                    """
                    % (self.egamma_era, self.egamma_era, self.egamma_era, self.egamma_era, self.egamma_era, self.egamma_era, self.egamma_era, self.egamma_era, self.egamma_era)
                )

                df = df.Define(
                    "EleRecoSF_tmp",
                    f"getSF_Reco(Lepton_pt, Lepton_eta, Lepton_pdgId, run_period)",
                )

                columnsToDrop.append("EleRecoSF_tmp")

                df = df.Redefine("Lepton_RecoSF", "EleRecoSF_tmp[0]")

                df = df.Redefine(
                    "Lepton_RecoSF_Up", "EleRecoSF_tmp[0] + EleRecoSF_tmp[1]"
                )

                df = df.Redefine(
                    "Lepton_RecoSF_Down", "EleRecoSF_tmp[0] - EleRecoSF_tmp[2]"
                )

                did_reco = True

            interpret_runP = """"""
            isPOGFormat = False
            for i in range(len(self.SF_dict["electron"][wp]["wpSF"]["data"])):
                if os.path.exists(self.SF_dict["electron"][wp]["wpSF"]["data"][i]):
                    
                    pathToJson = self.SF_dict["electron"][wp]["wpSF"]["data"][i]
                    key = self.SF_dict["electron"][wp]["wpSF"]["key"][i]

                    beginRP = self.SF_dict["electron"][wp]["wpSF"]["beginRP"][i]
                    endRP = self.SF_dict["electron"][wp]["wpSF"]["endRP"][i]

                    ROOT.gROOT.ProcessLine(
                        f'auto csetEl{wp}_wpSF_{beginRP}_{endRP} = correction::CorrectionSet::from_file("{pathToJson}");'
                    )
                    ROOT.gROOT.ProcessLine(
                        f'correction::Correction::Ref cset_electron_{wp}_wpSF_{beginRP}_{endRP} = (correction::Correction::Ref) csetEl{wp}_wpSF_{beginRP}_{endRP}->at("{key}");'
                    )

                    evaluator = """"""
                    if "POG" in pathToJson:
                        isPOGFormat = True
                        evaluator = """
                        pt = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{ele_pt[i], """ + str(self.el_maxPt) + """}), """ + str(self.el_minPt) + """});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{ele_eta[i], """ + str(self.el_maxEta) + """}), """ + str(self.el_minEta) + """});  

                        sf     = cset_electron_""" + wp + """_wpSF->evaluate({"%s", "sf", "%s", eta, pt});
                        sfstat = cset_electron_""" % (self.egamma_era, wp) + wp + """_wpSF->evaluate({"%s", "sfup", "%s", eta, pt}); 
                        sfsyst = cset_electron_""" % (self.egamma_era, wp) + wp + """_wpSF->evaluate({"%s", "sfdown", "%s", eta, pt}); """ % (self.egamma_era, wp)
                        
                    else:
                        evaluator = """
                        pt = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{ele_pt[i], """ + str(self.mu_maxPt) + """}), """ + str(self.mu_minPt) + """});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{ele_eta[i], """ + str(self.mu_maxEta) + """}), """ + str(self.mu_minEta) + """});  

                        sf     = cset_electron_""" + wp + """_wpSF->evaluate({eta, pt, "nominal"});
                        sfstat = cset_electron_""" + wp + """_wpSF->evaluate({eta, pt, "stat"});
                        sfsyst = cset_electron_""" + wp + """_wpSF->evaluate({eta, pt, "syst"});
                        """
                        
                    interpret_runP = (
                        interpret_runP
                        + """ 
                    if (runP>="""
                        + str(beginRP)
                        + """ && runP<="""
                        + str(endRP)
                        + """){  
                        cset_electron_"""
                        + wp
                        + """_wpSF = cset_electron_%s_wpSF_%s_%s;
                    } 
                    """
                        % (wp, beginRP, endRP)
                    )

                else:
                    print("Path does not exist for " + wp + " at:")
                    print(self.SF_dict["electron"][wp]["wpSF"]["data"][i])
                    
            ROOT.gInterpreter.Declare(
                """
                    std::vector<ROOT::RVecF> getSF_"""
                    + wp
                    + """_wpSF(ROOT::RVecF ele_pt, ROOT::RVecF ele_eta, ROOT::RVecI ele_pdgId, int runP){

                        std::vector<ROOT::RVecF> SFTot;
                        ROOT::RVecF SF;
                        ROOT::RVecF SFstat;
                        ROOT::RVecF SFsyst;
                        float sf,sfstat,sfsyst;
                        float pt,eta;

                        correction::Correction::Ref cset_electron_"""
                        + wp
                        + """_wpSF;

                        """
                        + interpret_runP
                        + """

                        for (int i=0; i<ele_pt.size(); i++){
                            if (abs(ele_pdgId[i])==11){
                                
                                """
                                + evaluator
                                + """
                                
                                SF.push_back(sf);
                                SFstat.push_back(sfstat);
                                SFsyst.push_back(sfsyst);
                            }else{
                                SF.push_back(1.0);
                                SFstat.push_back(0.0);
                                SFsyst.push_back(0.0);
                            }
                        }
                        SFTot.push_back(SF);
                        SFTot.push_back(SFstat);
                        SFTot.push_back(SFsyst);
                        return SFTot;
                    }
                """
            )

            df = df.Define(
                f"ElewpSF_{wp}",
                f"getSF_{wp}_wpSF(Lepton_pt, Lepton_eta, Lepton_pdgId, run_period)",
            )

            columnsToDrop.append(f"ElewpSF_{wp}")
            
            df = df.Define(f"Lepton_tightElectron_{wp}_IdIsoSF", f"ElewpSF_{wp}[0]")
            
            if isPOGFormat:
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_IdIsoSF_Up",
                    f"ElewpSF_{wp}[1]",
                )
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_IdIsoSF_Down",
                    f"ElewpSF_{wp}[2]",
                )
            else:
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_IdIsoSF_Up",
                    f"ElewpSF_{wp}[0] + ElewpSF_{wp}[1]",
                )
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_IdIsoSF_Down",
                    f"ElewpSF_{wp}[0] - ElewpSF_{wp}[1]",
                )
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_IdIsoSF_Syst",
                    f"ElewpSF_{wp}[0] + ElewpSF_{wp}[2]",
                )

            if self.SF_dict["electron"][wp]["hasTrk"]:
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_TotSF",
                    f"Lepton_tightElectron_{wp}_IdIsoSF * Lepton_RecoSF",
                )
                if isPOGFormat:
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Up",
                        f"Lepton_tightElectron_{wp}_IdIsoSF * Lepton_RecoSF + sqrt((ElewpSF_{wp}[1]-ElewpSF_{wp}[0])*(ElewpSF_{wp}[1]-ElewpSF_{wp}[0]) + EleRecoSF_tmp[1]*EleRecoSF_tmp[1])",
                    )
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Down",
                        f"Lepton_tightElectron_{wp}_IdIsoSF * Lepton_RecoSF + sqrt((ElewpSF_{wp}[0]-ElewpSF_{wp}[2])*(ElewpSF_{wp}[0]-ElewpSF_{wp}[2]) + EleRecoSF_tmp[1]*EleRecoSF_tmp[1])",
                    )
                else:
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Up",
                        f"Lepton_tightElectron_{wp}_IdIsoSF * Lepton_RecoSF + sqrt(ElewpSF_{wp}[1]*ElewpSF_{wp}[1] + ElewpSF_{wp}[2]*ElewpSF_{wp}[2] + EleRecoSF_tmp[1]*EleRecoSF_tmp[1])",
                    )
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Down",
                        f"Lepton_tightElectron_{wp}_IdIsoSF * Lepton_RecoSF - sqrt(ElewpSF_{wp}[1]*ElewpSF_{wp}[1] + ElewpSF_{wp}[2]*ElewpSF_{wp}[2] + EleRecoSF_tmp[2]*EleRecoSF_tmp[2])",
                    )
            else:
                df = df.Define(
                    f"Lepton_tightElectron_{wp}_TotSF",
                    f"Lepton_tightElectron_{wp}_IdIsoSF",
                )
                if isPOGFormat:
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Up",
                        f"Lepton_tightElectron_{wp}_IdIsoSF_Up",
                    )
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Down",
			f"Lepton_tightElectron_{wp}_IdIsoSF_Down",
		    )
                else:
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Up",
                        f"Lepton_tightElectron_{wp}_IdIsoSF + sqrt(ElewpSF_{wp}[1]*ElewpSF_{wp}[1] + ElewpSF_{wp}[2]*ElewpSF_{wp}[2])",
                    )
                    df = df.Define(
                        f"Lepton_tightElectron_{wp}_TotSF_Down",
                        f"Lepton_tightElectron_{wp}_IdIsoSF - sqrt(ElewpSF_{wp}[1]*ElewpSF_{wp}[1] + ElewpSF_{wp}[2]*ElewpSF_{wp}[2])",
                    )

        ### Muons
        for wp in self.SF_dict["muon"]:
            hasTTHmva = str(self.SF_dict["muon"][wp]["hastthMvaSF"]).lower()

            ### ID SF
            interpret_idSF = """"""
            for i in range(len(self.SF_dict["muon"][wp]["idSF"]["data"])):
                if os.path.exists(self.SF_dict["muon"][wp]["idSF"]["data"][i]):
                    pathToJson = self.SF_dict["muon"][wp]["idSF"]["data"][i]
                    key = self.SF_dict["muon"][wp]["idSF"]["key"][i]

                    beginRP = self.SF_dict["muon"][wp]["idSF"]["beginRP"][i]
                    endRP = self.SF_dict["muon"][wp]["idSF"]["endRP"][i]

                    ROOT.gROOT.ProcessLine(
                        f'auto csetMu{wp}_idSF_{beginRP}_{endRP} = correction::CorrectionSet::from_file("{pathToJson}");'
                    )
                    ROOT.gROOT.ProcessLine(
                        f'correction::Correction::Ref cset_muon_{wp}_idSF_{beginRP}_{endRP} = (correction::Correction::Ref) csetMu{wp}_idSF_{beginRP}_{endRP}->at("{key}");'
                    )

                    interpret_idSF = (
                        interpret_idSF
                        + """
                    if (runP>="""
                        + str(beginRP)
                        + """ && runP<="""
                        + str(endRP)
                        + """){ 
                        cset_muon_"""
                        + wp
                        + """_idSF = cset_muon_%s_idSF_%s_%s;
                    }
                    """
                        % (wp, beginRP, endRP)
                    )

                else:
                    print("Path does not exist for " + wp + " at:")
                    print(self.SF_dict["muon"][wp]["idSF"]["data"][i])
                    
            ### Iso SF
            interpret_isoSF = """"""
            for i in range(len(self.SF_dict["muon"][wp]["isoSF"]["data"])):
                if os.path.exists(self.SF_dict["muon"][wp]["isoSF"]["data"][i]):
                    pathToJson = self.SF_dict["muon"][wp]["isoSF"]["data"][i]
                    key = self.SF_dict["muon"][wp]["isoSF"]["key"][i]

                    beginRP = self.SF_dict["muon"][wp]["isoSF"]["beginRP"][i]
                    endRP = self.SF_dict["muon"][wp]["isoSF"]["endRP"][i]

                    ROOT.gROOT.ProcessLine(
                        f'auto csetMu{wp}_isoSF_{beginRP}_{endRP} = correction::CorrectionSet::from_file("{pathToJson}");'
                    )
                    ROOT.gROOT.ProcessLine(
                        f'correction::Correction::Ref cset_muon_{wp}_isoSF_{beginRP}_{endRP} = (correction::Correction::Ref) csetMu{wp}_isoSF_{beginRP}_{endRP}->at("{key}");'
                    )

                    interpret_isoSF = (
                        interpret_isoSF
                        + """
                    if (runP>="""
                        + str(beginRP)
                        + """ && runP<="""
                        + str(endRP)
                        + """){    
                        cset_muon_"""
                        + wp
                        + """_isoSF = cset_muon_%s_isoSF_%s_%s;
                    }
                    """
                        % (wp, beginRP, endRP)
                    )
                else:
                    print("Path does not exist for " + wp + " at:")
                    print(self.SF_dict["muon"][wp]["isoSF"]["data"][i])
                    
            ### TTH mva
            interpret_tthSF = """"""
            if self.SF_dict["muon"][wp]["hastthMvaSF"]:
                for i in range(len(self.SF_dict["muon"][wp]["tthMvaSF"]["data"])):
                    if os.path.exists(self.SF_dict["muon"][wp]["tthMvaSF"]["data"][i]):
                        pathToJson = self.SF_dict["muon"][wp]["tthMvaSF"]["data"][i]
                        key = self.SF_dict["muon"][wp]["tthMvaSF"]["key"][i]

                        beginRP = self.SF_dict["muon"][wp]["tthMvaSF"]["beginRP"][i]
                        endRP = self.SF_dict["muon"][wp]["tthMvaSF"]["endRP"][i]

                        ROOT.gROOT.ProcessLine(
                            f'auto csetMu{wp}_tthMvaSF_{beginRP}_{endRP} = correction::CorrectionSet::from_file("{pathToJson}");'
                        )
                        ROOT.gROOT.ProcessLine(
                            f'correction::Correction::Ref cset_muon_{wp}_tthMvaSF_{beginRP}_{endRP} = (correction::Correction::Ref) csetMu{wp}_tthMvaSF_{beginRP}_{endRP}->at("{key}");'
                        )

                        interpret_tthSF = (
                            interpret_tthSF
                            + """
                        if (runP>="""
                            + str(beginRP)
                            + """ && runP<="""
                            + str(endRP)
                            + """){
                            cset_muon_"""
                            + wp
                            + """_tthSF = cset_muon_%s_tthMvaSF_%s_%s; 
                        }
                        """
                            % (wp, beginRP, endRP)
                        )
                    else:
                        print("Path does not exist for " + wp + " at:")
                        print(self.SF_dict["muon"][wp]["tthMvaSF"]["data"][i])
            else:
                interpret_tthSF = (
                    interpret_tthSF
                    + """
                bool dummy = false;
                """
                )

            ROOT.gInterpreter.Declare(
                """
                    std::vector<ROOT::RVecF> getSF_"""
                    + wp
                    + """_Muon(ROOT::RVecF mu_pt, ROOT::RVecF mu_eta, ROOT::RVecI mu_pdgId, int runP, bool hasTTHMVA){
                        
                        std::vector<ROOT::RVecF> SFTot;
                        ROOT::RVecF SF;
                        ROOT::RVecF SFstat;
                        ROOT::RVecF SFsyst;
                        
                        float sf,sfstat,sfsyst,sf_id,sf_idstat,sf_idsyst,sf_iso,sf_isostat,sf_isosyst,sf_tth,sf_tthstat,sf_tthsyst;
                        float pt,eta;

                        correction::Correction::Ref cset_muon_"""
                        + wp
                        + """_idSF;
                        correction::Correction::Ref cset_muon_"""
                        + wp
                        + """_isoSF;
                        correction::Correction::Ref cset_muon_"""
                        + wp
                        + """_tthSF;

                        """
                        + interpret_idSF
                        + """
                        """
                        + interpret_isoSF
                        + """

                        if (hasTTHMVA){
                            """
                            + interpret_tthSF
                            + """
                        }
                        
                        for (int i=0; i<mu_pt.size(); i++){
                            if (abs(mu_pdgId[i])==13){

                                pt = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{mu_pt[i], """
                                + str(self.mu_maxPt)
                                + """}), """
                                + str(self.mu_minPt)
                                + """}); 
                                                                                                                                                                    
                                eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{mu_eta[i], """
                                + str(self.mu_maxEta)
                                + """}), """
                                + str(self.mu_minEta)
                                + """});

                                sf_id     = cset_muon_"""
                                + wp
                                + """_idSF->evaluate({abs(eta), pt, "nominal"});
                                sf_idstat = cset_muon_"""
                                + wp
                                + """_idSF->evaluate({abs(eta), pt, "stat"});
                                sf_idsyst = cset_muon_"""
                                + wp
                                + """_idSF->evaluate({abs(eta), pt, "syst"});

                                sf_iso     = cset_muon_"""
                                + wp
                                + """_isoSF->evaluate({abs(eta), pt, "nominal"});
                                sf_isostat = cset_muon_"""
                                + wp
                                + """_isoSF->evaluate({abs(eta), pt, "stat"});
                                sf_isosyst = cset_muon_"""
                                + wp
                                + """_isoSF->evaluate({abs(eta), pt, "syst"});

                                if (hasTTHMVA){
                                    sf_tth     = cset_muon_"""
                                    + wp
                                    + """_tthSF->evaluate({abs(eta), pt, "nominal"});
                                    sf_tthstat = cset_muon_"""
                                    + wp
                                    + """_tthSF->evaluate({abs(eta), pt, "stat"});
                                    sf_tthsyst = cset_muon_"""
                                    + wp
                                    + """_tthSF->evaluate({abs(eta), pt, "syst"});
                                }else{
                                    sf_tth     = 1.0;
                                    sf_tthstat = 0.0;
                                    sf_tthsyst = 0.0;
                                }

                                sf = sf_id * sf_iso * sf_tth;
                                sfstat = sqrt(sf_idstat*sf_idstat + sf_isostat*sf_isostat + sf_tthstat*sf_tthstat);
                                sfsyst = sqrt(sf_idsyst*sf_idsyst + sf_isosyst*sf_isosyst + sf_tthsyst*sf_tthsyst);

                                SF.push_back(sf);
                                SFstat.push_back(sfstat);
                                SFsyst.push_back(sfsyst);

                            }else{
                                SF.push_back(1.0);
                                SFstat.push_back(0.0);
                                SFsyst.push_back(0.0);
                            }
                        }
                        SFTot.push_back(SF);
                        SFTot.push_back(SFstat);
                        SFTot.push_back(SFsyst);
                        return SFTot;
                    }
                """
            )

            df = df.Define(
                f"MuonSF_{wp}_tmp",
                f"getSF_{wp}_Muon(Lepton_pt, Lepton_eta, Lepton_pdgId, run_period, {hasTTHmva})",
            )

            columnsToDrop.append(f"MuonSF_{wp}_tmp")

            df = df.Define(f"Lepton_tightMuon_{wp}_IdIsoSF", f"MuonSF_{wp}_tmp[0]")

            df = df.Define(
                f"Lepton_tightMuon_{wp}_IdIsoSF_Up",
                f"MuonSF_{wp}_tmp[0] + MuonSF_{wp}_tmp[1]",
            )

            df = df.Define(
                f"Lepton_tightMuon_{wp}_IdIsoSF_Down",
                f"MuonSF_{wp}_tmp[0] - MuonSF_{wp}_tmp[1]",
            )

            df = df.Define(
                f"Lepton_tightMuon_{wp}_IdIsoSF_Syst",
                f"MuonSF_{wp}_tmp[0] + MuonSF_{wp}_tmp[2]",
            )

            df = df.Define(f"Lepton_tightMuon_{wp}_TotSF", f"MuonSF_{wp}_tmp[0]")

            df = df.Define(
                f"Lepton_tightMuon_{wp}_TotSF_Up",
                f"MuonSF_{wp}_tmp[0] + sqrt(MuonSF_{wp}_tmp[1]*MuonSF_{wp}_tmp[1] + MuonSF_{wp}_tmp[2]*MuonSF_{wp}_tmp[2])",
            )

            df = df.Define(
                f"Lepton_tightMuon_{wp}_TotSF_Down",
                f"MuonSF_{wp}_tmp[0] - sqrt(MuonSF_{wp}_tmp[1]*MuonSF_{wp}_tmp[1] + MuonSF_{wp}_tmp[2]*MuonSF_{wp}_tmp[2])",
            )

        for col in columnsToDrop:
            df = df.DropColumns(col)

        return df
