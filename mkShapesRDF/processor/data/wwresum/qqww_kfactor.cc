#ifndef QQWW_KFACTOR
#define QQWW_KFACTOR

#include "TSystem.h"

#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <iterator>

#include "TLorentzVector.h"
#include "TMath.h"

#include "TH2D.h"
#include "TGraph.h"
#include "TFile.h"
#include <map>

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

using namespace std;

class qqww_K_producer{
public:

  qqww_K_producer(std::string central,
		  std::string resum_up,
		  std::string resum_down,
		  std::string scale_up,
		  std::string scale_down);

  void SetPTWW( float ptl1 , float phil1,   float ptl2 , float phil2,   float ptv1 , float phiv1 ,   float ptv2 , float phiv2);
  void SetPTWW( float ptV1 , float phiV1,   float ptV2 , float phiV2);
  void SetPTWW( float ptV1 , float phiV1, float etaV1,   float ptV2 , float phiV2, float etaV2);

  float GetPTWW();
  float GetMWW();

  TFile* fileInput;
  TLorentzVector L1,L2,V1,V2;
  TLorentzVector W1, W2;
  
  float ptww;
  float mww;
  
  TGraph* _resum_central;
  TGraph* _resum_Rup;
  TGraph* _resum_Rdown;
  TGraph* _resum_Qup;
  TGraph* _resum_Qdown;
  TGraph* _resum_nnlonnll_central;
  
  TGraph* _mc_central;
  TGraph* _mc_Rup;
  TGraph* _mc_Rdown;
  TGraph* _mc_Qup;
  TGraph* _mc_Qdown;
  TGraph* _mc_nnlonnll_central;
  
  bool _useOnlyRatio;

  float operator()(RVecF GenPart_pt, RVecF GenPart_eta, RVecF GenPart_phi, RVecF GenPart_mass, RVecI GenPart_pdgId, RVecI GenPart_status, RVecI GenPart_statusFlags, int variation, int kind = 0){

    float weight = -1;
    
    float w_pt1 = -1;
    float w_eta1;
    float w_phi1;

    float w_pt2 = -1;
    float w_eta2;
    float w_phi2;

    for (unsigned int i=0; i<GenPart_pt.size(); i++){
      if (fabs(GenPart_pdgId[i]) == 24 && (GenPart_statusFlags[i] >> 13 & 1)){
	if (w_pt1 == -1){
	  w_pt1 = GenPart_pt[i];
	  w_eta1 = GenPart_eta[i];
	  w_phi1 = GenPart_phi[i];
	}else{
	  w_pt2 = GenPart_pt[i];
          w_eta2 = GenPart_eta[i];
          w_phi2 = GenPart_phi[i];
	}
      }
    }

    if (w_pt1 != -1 && w_pt2 != -1){

      SetPTWW(w_pt1, w_phi1, w_eta1, w_pt2, w_phi2, w_eta2);
      
      if (_useOnlyRatio == false) {
  
	if (variation == 0) {
	  weight =  ptww < 500. ? _resum_central->Eval(ptww)/_mc_central->Eval(ptww) : 1;
	}
	else if (variation == -1) {
	  if (kind == 0) {
	    weight =  ptww < 500. ? _resum_Qdown->Eval(ptww)/_mc_Qdown->Eval(ptww) : 1;
	    //    weight = _reweightingFactors_Qdown[bin];   
	  }
	  if (kind == 1) {
	    weight =  ptww < 500. ? _resum_Rdown->Eval(ptww)/_mc_Rdown->Eval(ptww) : 1;
	    //    weight = _reweightingFactors_Rdown[bin];   
	  }
	}
	else if (variation == 1) {
	  if (kind == 0) {
	    weight =  ptww < 500. ? _resum_Qup->Eval(ptww)/_mc_Qup->Eval(ptww) : 1;
	    //    weight = _reweightingFactors_Qup[bin];   
	  }
	  if (kind == 1) {
	    weight =  ptww < 500. ? _resum_Rup->Eval(ptww)/_mc_Rup->Eval(ptww) : 1;
	    //    weight = _reweightingFactors_Rup[bin];   
	  }
	}
      }else{
	if (variation == 0) {
	  weight =  ptww < 500. ? _resum_central->Eval(ptww) : 1;
	}
	else if (variation == -1) {
	  if (kind == 0) {
	    weight =  ptww < 500. ? (_resum_Qdown->Eval(ptww)*_resum_central->Eval(ptww)) : 1;
	  }
	  if (kind == 1) {
	    if (ptww < 500.) {
	      if (ptww < 50.) {
		weight =  _resum_Rdown->Eval(ptww) * _resum_central->Eval(ptww);
	      }
	      else {
		weight =  _resum_central->Eval(ptww);      
	      }
	    }
	    else {
	      weight = 1.0;
	    }
	  }
	}else if (variation == 1) {
	  if (kind == 0) {
	    weight =  ptww < 500. ? (_resum_Qup->Eval(ptww)*_resum_central->Eval(ptww)) : 1;
	    //    weight = _reweightingFactors_Qup[bin];   
	  }
	  if (kind == 1) {
	    if (ptww < 500.) {
	      if (ptww < 50.) {
		weight =  _resum_Rup->Eval(ptww) * _resum_central->Eval(ptww);
	      }
	      else {
		weight =  _resum_central->Eval(ptww);      
	      }
	    }
	    else {
	      weight = 1.0;
	    }
	  }
	}
      }
    }
    return weight;
  }  
};

float qqww_K_producer::GetPTWW(){
 return ptww;
}

float qqww_K_producer::GetMWW(){
 return mww;
}

void qqww_K_producer::SetPTWW( float ptV1 , float phiV1, float etaV1,   float ptV2 , float phiV2, float etaV2) {
 W1.SetPtEtaPhiM(ptV1, etaV1, phiV1, 80.385);
 W2.SetPtEtaPhiM(ptV2, etaV2, phiV2, 80.385);
 ptww = (W1+W2).Pt();
 mww  = (W1+W2).M();
}

void qqww_K_producer::SetPTWW( float ptV1 , float phiV1,   float ptV2 , float phiV2) {
 W1.SetPtEtaPhiM(ptV1, 0., phiV1, 0.);
 W2.SetPtEtaPhiM(ptV2, 0., phiV2, 0.);
 ptww = (W1+W2).Pt();
}

void qqww_K_producer::SetPTWW( float ptl1 , float phil1,   float ptl2 , float phil2,   float ptv1 , float phiv1 ,   float ptv2 , float phiv2) {
 L1.SetPtEtaPhiM(ptl1, 0., phil1, 0.);
 L2.SetPtEtaPhiM(ptl2, 0., phil2, 0.);
 V1.SetPtEtaPhiM(ptv1, 0., phiv1, 0.);
 V2.SetPtEtaPhiM(ptv2, 0., phiv2, 0.);
 ptww = (L1+L2+V1+V2).Pt();
}

// Read NLO/LO weights and fill histograms
qqww_K_producer::qqww_K_producer(std::string central,
				 std::string resum_up,
				 std::string resum_down,
				 std::string scale_up,
				 std::string scale_down){

  _resum_central = new TGraph(central.c_str());
  _resum_Rup = new TGraph(resum_up.c_str());
  _resum_Rdown = new TGraph(resum_down.c_str());
  _resum_Qup = new TGraph(scale_up.c_str());
  _resum_Qdown = new TGraph(scale_down.c_str());
  _resum_nnlonnll_central = 0x0;

  ptww = -1;
  mww = -1;
  
  _useOnlyRatio = true;

}
  

#endif
