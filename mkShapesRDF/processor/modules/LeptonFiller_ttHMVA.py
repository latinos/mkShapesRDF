from mkShapesRDF.processor.framework.module import Module
import os
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()

class LeptonFiller_ttHMVA(Module):
    def __init__(self, script_path="processor/data/ttH-Run3-LeptonMVA/"):
        super().__init__("LeptonFiller_ttHMVA")

        if "processor" in os.path.dirname(os.path.dirname(__file__)):
            self.script_path = (
                os.path.dirname(os.path.dirname(__file__)).split("processor")[0]
                + script_path
            )
        else:
            self.script_path = script_path

        
    def runModule(self, df, values):

        if not hasattr(ROOT, "getJetPtRatio"):
            ROOT.gInterpreter.Declare(
                """
		ROOT::RVecF getJetPtRatio(ROOT::RVecF Muon_jetRelIso){
                    ROOT::RVecF result(Muon_jetRelIso.size(), 1.5);
                    float tmp_value = 0.0;
                    for (int i=0; i<Muon_jetRelIso.size(); i++){
                        tmp_value = 1.0 / (1.0 + Muon_jetRelIso[i]);
                        if (tmp_value<1.5){
                            result[i] = tmp_value;
                        }
                    }
                    return result;
                }
		"""
            )
        
        ### Use TMVA ----
        ROOT.gInterpreter.Declare(
            """
            #include "TMVA/Tools.h"
            #include "TMVA/Reader.h"
            #include "TMVA/MethodCuts.h"

            using namespace ROOT;
            using namespace ROOT::VecOps;

            RVecF evaluateTTH_muon(RVecF Muon_pt,RVecF Muon_eta,RVecF Muon_pfRelIso03_all,RVecF Muon_miniPFRelIso_chg,RVecF Muon_miniRelIsoNeutral,RVecF Muon_jetNDauCharged,RVecF Muon_jetPtRelv2,RVecF Muon_jetBTagDeepFlavB,RVecF Muon_jetPtRatio,RVecF Muon_sip3d,RVecF Muon_log_dxy,RVecF Muon_log_dz,RVecF Muon_segmentComp){

                TMVA::Reader *reader = new TMVA::Reader( "!Color:Silent" );"""+f"""
                TString weightfile = "{self.script_path}/Muon-mvaTTH.2022EE.weights.xml";"""+"""

                float muon_pt = 0.0;
                float muon_eta = 0.0;
                float muon_pfRelIso03_all = 0.0;
                float muon_miniPFRelIso_chg = 0.0;
                float muon_miniRelIsoNeutral = 0.0;
                float muon_jetNDauCharged = 0.0;
                float muon_jetPtRelv2 = 0.0;
                float muon_jetBTagDeepFlavB = 0.0;
                float muon_jetPtRatio = 0.0;
                float muon_sip3d = 0.0;
                float muon_log_dxy = 0.0;
                float muon_log_dz = 0.0;
                float muon_segmentComp = 0.0;

                reader->AddVariable("Muon_pt",                        &muon_pt);
                reader->AddVariable("Muon_eta",                       &muon_eta);
                reader->AddVariable("Muon_pfRelIso03_all",            &muon_pfRelIso03_all);
                reader->AddVariable("Muon_miniPFRelIso_chg",          &muon_miniPFRelIso_chg);
                reader->AddVariable("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg", &muon_miniRelIsoNeutral);
                reader->AddVariable("Muon_jetNDauCharged",            &muon_jetNDauCharged);
                reader->AddVariable("Muon_jetPtRelv2",                &muon_jetPtRelv2);
                reader->AddVariable("Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0", &muon_jetBTagDeepFlavB);
                reader->AddVariable("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)", &muon_jetPtRatio);
                reader->AddVariable("Muon_sip3d",                         &muon_sip3d);
                reader->AddVariable("Muon_log_dxy := log(abs(Muon_dxy))", &muon_log_dxy);
                reader->AddVariable("Muon_log_dz  := log(abs(Muon_dz))",  &muon_log_dz);
                reader->AddVariable("Muon_segmentComp",                   &muon_segmentComp);

                RVecF results(Muon_pt.size(), -1.0);

                reader->BookMVA("BDTG", weightfile);

                float result_muon = -1.0;

                for (int i=0; i<Muon_pt.size();i++){

                    result_muon =   -1.0;

                    muon_pt = Muon_pt[i];
                    muon_eta = Muon_eta[i];
                    muon_pfRelIso03_all = Muon_pfRelIso03_all[i];
                    muon_miniPFRelIso_chg = Muon_miniPFRelIso_chg[i];
                    muon_miniRelIsoNeutral = Muon_miniRelIsoNeutral[i];
                    muon_jetNDauCharged = Muon_jetNDauCharged[i];
                    muon_jetPtRelv2 = Muon_jetPtRelv2[i];
                    muon_jetBTagDeepFlavB = Muon_jetBTagDeepFlavB[i];
                    muon_jetPtRatio = Muon_jetPtRatio[i];
                    muon_sip3d = Muon_sip3d[i];
                    muon_log_dxy = Muon_log_dxy[i];
                    muon_log_dz = Muon_log_dz[i];
                    muon_segmentComp = Muon_segmentComp[i];
                    
                    result_muon = reader->EvaluateMVA("BDTG");
                    results[i] = (float)result_muon;
                }
                delete reader;
                return results;    
            } 
            """
        )


        ROOT.gInterpreter.Declare(
            """
            using namespace ROOT;
            using namespace ROOT::VecOps;

            RVecF evaluateTTH_electron(RVecF Electron_pt, RVecF Electron_eta, RVecF Electron_pfRelIso03_all, RVecF Electron_miniPFRelIso_chg, RVecF Electron_miniRelIsoNeutral, RVecF Electron_jetNDauCharged, RVecF Electron_jetPtRelv2, RVecF Electron_jetBTagDeepFlavB, RVecF Electron_jetPtRatio, RVecF Electron_sip3d, RVecF Electron_log_dxy, RVecF Electron_log_dz, RVecF Electron_mvaIso){

                TMVA::Reader *reader = new TMVA::Reader( "!Color:Silent" );"""+f"""                
                TString weightfile = "{self.script_path}/Electron-mvaTTH.2022EE.weights_mvaISO.xml";"""+"""                                                                                                    
                
                float electron_pt = 0.0;
                float electron_eta = 0.0;
                float electron_pfRelIso03_all = 0.0;
                float electron_miniPFRelIso_chg = 0.0;
                float electron_miniRelIsoNeutral = 0.0;
                float electron_jetNDauCharged = 0.0;
                float electron_jetPtRelv2 = 0.0;
                float electron_jetBTagDeepFlavB = 0.0;
                float electron_jetPtRatio = 0.0;
                float electron_sip3d = 0.0;
                float electron_log_dxy = 0.0;
                float electron_log_dz = 0.0;
                float electron_mvaIso = 0.0;   
                
                reader->AddVariable("Electron_pt",                                                                                &electron_pt);
                reader->AddVariable("Electron_eta",                                                                               &electron_eta);
                reader->AddVariable("Electron_pfRelIso03_all",                                                                    &electron_pfRelIso03_all);
                reader->AddVariable("Electron_miniPFRelIso_chg",                                                                  &electron_miniPFRelIso_chg);
                reader->AddVariable("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg",        &electron_miniRelIsoNeutral);
                reader->AddVariable("Electron_jetNDauCharged",                                                                    &electron_jetNDauCharged);
                reader->AddVariable("Electron_jetPtRelv2",                                                                        &electron_jetPtRelv2);
                reader->AddVariable("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0", &electron_jetBTagDeepFlavB);
                reader->AddVariable("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)",                              &electron_jetPtRatio);
                reader->AddVariable("Electron_sip3d",                                                                             &electron_sip3d);
                reader->AddVariable("Electron_log_dxy := log(abs(Electron_dxy))",                                                 &electron_log_dxy);
                reader->AddVariable("Electron_log_dz  := log(abs(Electron_dz))",                                                  &electron_log_dz);
                reader->AddVariable("Electron_mvaIso",                                                                            &electron_mvaIso);
                
                RVecF results(Electron_pt.size(), -1.0);
                reader->BookMVA("BDTG", weightfile);
                float result_electron = -1.0;
                
                for (int i=0; i<Electron_pt.size();i++){
                        
                    result_electron = -1.0;

                    electron_pt = Electron_pt[i];
                    electron_eta = Electron_eta[i];
                    electron_pfRelIso03_all = Electron_pfRelIso03_all[i];
                    electron_miniPFRelIso_chg = Electron_miniPFRelIso_chg[i];
                    electron_miniRelIsoNeutral = Electron_miniRelIsoNeutral[i];
                    electron_jetNDauCharged = Electron_jetNDauCharged[i];
                    electron_jetPtRelv2 = Electron_jetPtRelv2[i];
                    electron_jetBTagDeepFlavB = Electron_jetBTagDeepFlavB[i];
                    electron_jetPtRatio = Electron_jetPtRatio[i];
                    electron_sip3d = Electron_sip3d[i];
                    electron_log_dxy = Electron_log_dxy[i];
                    electron_log_dz = Electron_log_dz[i];
                    electron_mvaIso = Electron_mvaIso[i];
                    result_electron = reader->EvaluateMVA("BDTG");        
                    
                    results[i] = (float)result_electron;
                }         
                delete reader;
                return results;
            }  
            """
        )

        if "Muon_log_dxy" not in df.GetColumnNames():
            df = df.Define("Muon_miniRelIsoNeutral", "Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg")
            df = df.Define("Muon_jetPtRatio", "getJetPtRatio(Muon_jetRelIso)")
            df = df.Define("Muon_jetBTagDeepFlavB", "ROOT::VecOps::Take(Jet_btagDeepFlavB,Muon_jetIdx,float(0.0))")
            df = df.Define("Muon_log_dxy", "ROOT::VecOps::log(abs(Muon_dxy))")
            df = df.Define("Muon_log_dz", "ROOT::VecOps::log(abs(Muon_dz))")
        
            df = df.Define("Electron_miniRelIsoNeutral", "Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg")
            df = df.Define("Electron_jetPtRatio", "getJetPtRatio(Electron_jetRelIso)")
            df = df.Define("Electron_jetBTagDeepFlavB", "ROOT::VecOps::Take(Jet_btagDeepFlavB,Electron_jetIdx,float(0.0))")
            df = df.Define("Electron_log_dxy", "ROOT::VecOps::log(abs(Electron_dxy))")
            df = df.Define("Electron_log_dz", "ROOT::VecOps::log(abs(Electron_dz))")

        df = df.Define(
            "Muon_tthMVA",
            "evaluateTTH_muon(Muon_pt, Muon_eta, Muon_pfRelIso03_all, Muon_miniPFRelIso_chg, Muon_miniRelIsoNeutral, Muon_jetNDauCharged, Muon_jetPtRelv2, Muon_jetBTagDeepFlavB, Muon_jetPtRatio, Muon_sip3d, Muon_log_dxy, Muon_log_dz, Muon_segmentComp)"
        )
        df = df.Define(
            "Electron_tthMVA",
            "evaluateTTH_electron(Electron_pt,Electron_eta,Electron_pfRelIso03_all,Electron_miniPFRelIso_chg,Electron_miniRelIsoNeutral,Electron_jetNDauCharged,Electron_jetPtRelv2,Electron_jetBTagDeepFlavB,Electron_jetPtRatio,Electron_sip3d,Electron_log_dxy,Electron_log_dz,Electron_mvaIso)"
        )
        
        return df
