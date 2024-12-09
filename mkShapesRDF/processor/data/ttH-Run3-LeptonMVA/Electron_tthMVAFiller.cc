#include "TMVA/Tools.h"                                                                                                                                                                                                                                                     
#include "TMVA/Reader.h"                                                                                                                                                                                                                                                    
#include "TMVA/MethodCuts.h"                                                                                                                                                                                                                                                

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

class Electron_tthMVAFiller{
public:
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

  int event = 0;
  float Electron_mvaTTH = 0.0;
  float Electron_miniPFRelIso_all = 0.0;
  float Electron_mvaFall17V2noIso_WPL = 0.0;
  int Electron_lostHits = 0;
  int Electron_genPartFlav = 0;
  float Electron_dxy = 0.0;
  float Electron_dz = 0.0;
  
  TMVA::Reader *reader;
  TString weightfile;
  
  Electron_tthMVAFiller(TString infile){

    weightfile = infile;
    
    reader = new TMVA::Reader( "!Color:Silent" );

    reader->AddSpectator("event", &event);
    reader->AddSpectator("Electron_mvaTTH", &Electron_mvaTTH);
    reader->AddSpectator("Electron_miniPFRelIso_all", &Electron_miniPFRelIso_all);
    reader->AddSpectator("Electron_mvaFall17V2noIso_WPL", &Electron_mvaFall17V2noIso_WPL);
    reader->AddSpectator("Electron_lostHits", &Electron_lostHits);
    reader->AddSpectator("Electron_genPartFlav", &Electron_genPartFlav);
    reader->AddSpectator("Electron_dxy", &Electron_dxy);
    reader->AddSpectator("Electron_dz", &Electron_dz);

    reader->AddVariable("Electron_pt",                                                                                &electron_pt);
    reader->AddVariable("Electron_eta",                                                                               &electron_eta);
    reader->AddVariable("Electron_pfRelIso03_all",                                                                    &electron_pfRelIso03_all);
    reader->AddVariable("Electron_miniPFRelIso_chg",                                                                  &electron_miniPFRelIso_chg);
    reader->AddVariable("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg",        &electron_miniRelIsoNeutral);
    reader->AddVariable("Electron_jetNDauCharged",                                                                    &electron_jetNDauCharged);
    reader->AddVariable("Electron_jetPtRelv2",                                                                        &electron_jetPtRelv2);
    reader->AddVariable("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)",                              &electron_jetPtRatio);
    reader->AddVariable("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0", &electron_jetBTagDeepFlavB);
    reader->AddVariable("Electron_sip3d",                                                                             &electron_sip3d);
    reader->AddVariable("Electron_log_dxy := log(abs(Electron_dxy))",                                                 &electron_log_dxy);
    reader->AddVariable("Electron_log_dz  := log(abs(Electron_dz))",                                                  &electron_log_dz);
    reader->AddVariable("Electron_mvaFall17V2noIso",                                                                            &electron_mvaIso);

    reader->BookMVA("BDTG", weightfile);
  }

  RVecF operator()(RVecF Electron_pt, RVecF Electron_eta, RVecF Electron_pfRelIso03_all, RVecF Electron_miniPFRelIso_chg, RVecF Electron_miniRelIsoNeutral, RVecF Electron_jetNDauCharged, RVecF Electron_jetPtRelv2, RVecF Electron_jetBTagDeepFlavB, RVecF Electr\
on_jetPtRatio, RVecF Electron_sip3d, RVecF Electron_log_dxy, RVecF Electron_log_dz, RVecF Electron_mvaIso){

    RVecF results(Electron_pt.size(), -1.0);
    
    float result_electron = -1.0;

    for (long unsigned int i=0; i<Electron_pt.size();i++){

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

    //std::cout << results << std::endl;
    return results;
    
  }
};
