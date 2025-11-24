// This macro contains the function needed to apply scale and smearing correction to electrons and photons
// as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammSFandSSRun3

#include <iostream>
#include "TString.h"
#include "TFile.h"
#include "TRandom3.h"   
#include <string>
#include <vector>
#include "correction.h"

// Obtain the uncertainty on the smearing width using MC original variables
double ele_unc_smear(double Lepton_pt, double Electron_r9, double sc_eta, double random_number, string updn)
{
    double smear = elecset_smear->evaluate({"smear", Lepton_pt, Electron_r9, abs(sc_eta)});
    double unc_smear = elecset_smear->evaluate({"esmear", Lepton_pt, Electron_r9, abs(sc_eta)});
    double mc_unc_smear = Lepton_pt;
    if (updn=="up"){
        mc_unc_smear = Lepton_pt * (1 + (smear + unc_smear) * random_number);
    }
    else if (updn=="dn"){
        mc_unc_smear = Lepton_pt * (1 + (smear - unc_smear) * random_number);
    }
    else {
        cout << "ERROR: updn must be 'up' or 'dn'" << endl;
    }
    return mc_unc_smear;
}

// Scale correction applied to data
double ele_scale(double run, double sc_eta, double Electron_r9, double Lepton_pt, double Electron_seedGain)
{
    double scale = elecset_scale->evaluate({"scale", run, sc_eta, Electron_r9, Lepton_pt, Electron_seedGain});
    double data_scale = scale * Lepton_pt;
    return data_scale;
}

// Calculate the nominal smearing factor for MC
double ele_smear(double Lepton_pt, double Electron_r9, double sc_eta, double random_number)
{
    double smear = elecset_smear->evaluate({"smear", Lepton_pt, Electron_r9, abs(sc_eta)});
    double mc_smear = Lepton_pt * (1 + smear * random_number);
    return mc_smear;
}

// Function that compute the scale uncertainties
// It is evaluated on the original MC variables BUT applied on the smeared pT
// Beware that unlike the documentation (/https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/blob/master/examples/egmScaleAndSmearingExample.py)
// all the inputs are needed for the evaluation
double ele_unc_scale(double run, double sc_eta, double Electron_r9, double Lepton_pt, double Electron_seedGain, double Lepton_newPt, string updn)
{
    double unc_scale = elecset_scale->evaluate({"escale", run, sc_eta, Electron_r9, Lepton_pt, Electron_seedGain});
    double mc_unc_scale = Lepton_newPt;
    if (updn=="up")
    {
        mc_unc_scale = (1 + unc_scale) * Lepton_newPt;
    }
    else if (updn=="dn")
    {
        mc_unc_scale = (1 - unc_scale) * Lepton_newPt;
    }
    else 
    {
        cout << "ERROR: updn must be 'up' or 'dn'" << endl;
    }
    return mc_unc_scale;
}
