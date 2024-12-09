#include "TMVA/Tools.h"                                                                                                                                                                                                                                                     
#include "TMVA/Reader.h"                                                                                                                                                                                                                                                    
#include "TMVA/MethodCuts.h"                                                                                                                                                                                                                                                

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

class Muon_tthMVAFiller{
public:
  float muon_pt = 0.0;
  float muon_eta = 0.0;
  float muon_pfRelIso03_all = 0.0;
  float muon_miniPFRelIso_chg = 0.0;
  float muon_miniRelIsoNeutral = 0.0;
  float muon_jetNDauCharged = 0.0;
  float muon_jetPtRelv2 = 0.0;
  float muon_jetPtRatio = 0.0;
  float muon_jetBTagDeepFlavB = 0.0;
  float muon_sip3d = 0.0;
  float muon_log_dxy = 0.0;
  float muon_log_dz = 0.0;
  float muon_segmentComp = 0.0;

  int event = 0;
  float Muon_mvaTTH = 0.0;
  float Muon_miniPFRelIso_all = 0.0;
  int Muon_looseId = 0.0;
  int Muon_genPartFlav = 0;
  int Muon_isGlobal = 0.0;
  int Muon_isTracker = 0.0;
  int Muon_isPFcand = 0.0;
  int Muon_mediumId = 0.0;
  int Muon_looseIdBis = 0.0;
  float Muon_dxy = 0.0;
  float Muon_dz = 0.0;
  
  TMVA::Reader *reader;
  TString weightfile;
  
  Muon_tthMVAFiller(TString infile){
    weightfile = infile;
    
    reader = new TMVA::Reader( "!Color:Silent" );

    reader->AddSpectator("event", &event);
    reader->AddSpectator("Muon_mvaTTH", &Muon_mvaTTH);
    reader->AddSpectator("Muon_miniPFRelIso_all", &Muon_miniPFRelIso_all);
    reader->AddSpectator("Muon_looseId", &Muon_looseId);
    reader->AddSpectator("Muon_genPartFlav", &Muon_genPartFlav);
    reader->AddSpectator("Muon_isGlobal", &Muon_isGlobal);
    reader->AddSpectator("Muon_isTracker", &Muon_isTracker);
    reader->AddSpectator("Muon_isPFcand", &Muon_isPFcand);
    reader->AddSpectator("Muon_mediumId", &Muon_mediumId);
    reader->AddSpectator("Muon_looseId", &Muon_looseIdBis);
    reader->AddSpectator("Muon_dxy", &Muon_dxy);
    reader->AddSpectator("Muon_dz", &Muon_dz);
    
    reader->AddVariable("Muon_pt",                                                                                &muon_pt);
    reader->AddVariable("Muon_eta",                                                                               &muon_eta);
    reader->AddVariable("Muon_pfRelIso03_all",                                                                    &muon_pfRelIso03_all);
    reader->AddVariable("Muon_miniPFRelIso_chg",                                                                  &muon_miniPFRelIso_chg);
    reader->AddVariable("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg",                &muon_miniRelIsoNeutral);
    reader->AddVariable("Muon_jetNDauCharged",                                                                    &muon_jetNDauCharged);
    reader->AddVariable("Muon_jetPtRelv2",                                                                        &muon_jetPtRelv2);
    reader->AddVariable("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)",                                  &muon_jetPtRatio);
    reader->AddVariable("Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0",         &muon_jetBTagDeepFlavB);
    reader->AddVariable("Muon_sip3d",                                                                             &muon_sip3d);
    reader->AddVariable("Muon_log_dxy := log(abs(Muon_dxy))",                                                     &muon_log_dxy);
    reader->AddVariable("Muon_log_dz  := log(abs(Muon_dz))",                                                      &muon_log_dz);
    reader->AddVariable("Muon_segmentComp",                                                                       &muon_segmentComp);

    reader->BookMVA("BDTG", weightfile);
  }

  RVecF operator()(RVecF Muon_pt, RVecF Muon_eta, RVecF Muon_pfRelIso03_all, RVecF Muon_miniPFRelIso_chg, RVecF Muon_miniRelIsoNeutral, RVecF Muon_jetNDauCharged, RVecF Muon_jetPtRelv2, RVecF Muon_jetBTagDeepFlavB, RVecF Muon_jetPtRatio, RVecF Muon_sip3d, RVecF Muon_log_dxy, RVecF Muon_log_dz, RVecF Muon_segmentComp){

    RVecF results(Muon_pt.size(), -1.0);
    
    float result_muon = -1.0;

    for (long unsigned int i=0; i<Muon_pt.size();i++){

        result_muon = -1.0;

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

    //std::cout << results << std::endl;
    return results;
    
  }
};
