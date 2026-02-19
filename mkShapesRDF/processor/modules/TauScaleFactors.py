import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.Tau_cfg import *
import correctionlib
import os
import re

correctionlib.register_pyroot_binding()

class TauScaleFactors(Module):
    def __init__(self, era):
        super().__init__("TauSF")
        self.era = era
        conf = Taus[era]["TAU"]
        self.file   = conf[0]

    def runModule(self, df, values):

        if not hasattr(ROOT, "doTauScale"):
            ROOT.gInterpreter.Declare(f"""
            #include <iostream>
            #include <vector>
            #include <string>
            #include "correction.h"
            #include "ROOT/RVec.hxx"

            using namespace ROOT::VecOps;

            auto tau_corr_set = correction::CorrectionSet::from_file("{self.file}");
            auto tau_tes = tau_corr_set->at("tau_energy_scale");

            std::vector<RVecF> doTauScale( RVecF pt, RVecF mass, RVecF eta, RVecU dm, RVecU gen) {{
                RVecF newPt = pt;
                RVecF newmass = mass;
                std::vector<RVecF> results = {{newPt, newmass}};
                for (unsigned i = 0; i < pt.size(); i++) {{
                int gm = (int)gen[i];
                int decay = (int)dm[i];
                if (decay != 0 && decay != 1 && decay != 10 && decay != 11) continue;

                double scale = tau_tes->evaluate({{ (double)pt[i], (double)eta[i], decay, gm, "DeepTau2018v2p5", "Medium", "Tight", "nom"}});
                newPt[i] = pt[i] * scale;
                newmass[i] = mass[i] * scale;
                }}
                results[0] = newPt;
                results[1] = newmass;
                return results;
            }}
            std::cout << "doTauScale done" << std::endl;
            """)

        if not hasattr(ROOT, "doTauMET"):
            ROOT.gInterpreter.Declare(f"""
            #include <iostream>
            #include <vector>
            #include <string>
            #include "correction.h"
            #include "ROOT/RVec.hxx"

            using namespace ROOT::VecOps;

            std::vector<double> doTauMET(RVecF orig_pt, RVecF new_pt, RVecF tau_phi, double met_pt, double met_phi) {{
                double metx = met_pt * cos(met_phi);
                double mety = met_pt * sin(met_phi);
                for (unsigned i = 0; i < new_pt.size(); i++) {{
                double dpt = new_pt[i] - orig_pt[i];
                metx -= dpt * cos(tau_phi[i]);
                mety -= dpt * sin(tau_phi[i]);
                }}
                double new_met_pt = sqrt(metx*metx + mety*mety);
                double new_met_phi = atan2(mety, metx);
                return {{new_met_pt, new_met_phi}};
            }}
            std::cout << "doTauMET done" << std::endl;
            """)

        if not hasattr(ROOT, "doTauSF"):
            ROOT.gInterpreter.Declare(f"""
            #include <iostream>
            #include <vector>
            #include <string>
            #include "correction.h"
            #include "ROOT/RVec.hxx"

            using namespace ROOT::VecOps;

            auto tau_corr_set_sf = correction::CorrectionSet::from_file("{self.file}");
            auto tau_sfvse = tau_corr_set_sf->at("DeepTau2018v2p5VSe");
            auto tau_sfvsmu = tau_corr_set_sf->at("DeepTau2018v2p5VSmu");
            auto tau_sfvsjet = tau_corr_set_sf ->at("DeepTau2018v2p5VSjet");

            RVecF doTauSFvse(RVecF pt, RVecF eta, RVecF dz, RVecU dm, RVecU gen) {{
                RVecF SF(eta.size(), 1.0);
                for (unsigned i = 0; i < eta.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 0 && gm != 1 && gm != 3) continue;
                int decay = (int)dm[i];
                if (decay != 0 && decay != 1 && decay != 10 && decay != 11) continue;
                if (pt[i] <= 20 || fabs(eta[i]) >= 2.5 || fabs(dz[i]) >= 0.2 || decay == 5 || decay == 6) continue;
                SF[i] = tau_sfvse->evaluate({{(double)eta[i], decay, gm, "VVLoose", "nom"}});
                }}
                return SF;
            }}
            
            RVecF doTauSFvsmu(RVecF pt, RVecF eta, RVecF dz, RVecU dm, RVecU gen) {{
                RVecF SF(eta.size(), 1.0);
                for (unsigned i = 0; i < eta.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 0 && gm != 2 && gm != 4) continue;
                int decay = (int)dm[i];
                if (pt[i] <= 20 || fabs(eta[i]) >= 2.5 || fabs(dz[i]) >= 0.2 || decay == 5 || decay == 6) continue;
                if (std::string("{self.era}") == "Full2024v15") {{
                    SF[i] = tau_sfvsmu->evaluate({{(double)eta[i], gm, "Medium", "VVLoose", "Medium", "nom"}});
                }}
                else{{
                    SF[i] = tau_sfvsmu->evaluate({{(double)eta[i], gm, "Medium", "nom"}});
                }}
                }}
                return SF;
            }}

            RVecF doTauSFvsjet(RVecF pt, RVecF eta, RVecF dz, RVecU dm, RVecU gen ) {{
                RVecF SF(pt.size(), 1.0);
                for (unsigned i = 0; i < pt.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 0 && gm != 1 && gm != 2 && gm != 3 && gm != 4 && gm != 5 && gm != 6) continue;
                int decay = (int)dm[i];
                if (pt[i] <= 20 || fabs(eta[i]) >= 2.5 || fabs(dz[i]) >= 0.2 || decay == 5 || decay == 6) continue;
                if (std::string("{self.era}") == "Full2024v15") {{
                    if (decay != 0 && decay != 1 && decay != 10 && decay != 11) continue;
                    SF[i] = tau_sfvsjet->evaluate({{ (double)pt[i], decay, gm, "Medium", "VVLoose", "nom", "dm"}});
                }}
                else{{
                    if (decay != 0 && decay != 1 && decay != 2 && decay != 10 && decay != 11) continue;
                    SF[i] = tau_sfvsjet->evaluate({{ (double)pt[i], decay, gm, "Medium", "VVLoose", "nom", "dm"}});
                }}
                }}
                return SF;
            }}

            std::cout << "doTauSF done" << std::endl;
            """)

        if not hasattr(ROOT, "sortedIndices"):
            ROOT.gInterpreter.Declare("""
                #include "ROOT/RVec.hxx"
                ROOT::RVecI sortedIndices(ROOT::RVecF variable) {
                    return ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(variable));
                }
            """)

        df = df.Define("Tau_Scale", "doTauScale(Tau_pt, Tau_mass, Tau_eta, Tau_decayMode, Tau_genPartFlav)")
        df = df.Define("Tau_Scale_pt", "Tau_Scale[0]")
        df = df.Define("Tau_Scale_mass", "Tau_Scale[1]")
        df = df.Redefine("TES_MET_pt", "doTauMET(Tau_pt, Tau_Scale_pt, Tau_phi, PuppiMET_pt, PuppiMET_phi)[0]")
        df = df.Redefine("TES_MET_phi", "doTauMET(Tau_pt, Tau_Scale_pt, Tau_phi, PuppiMET_pt, PuppiMET_phi)[1]")
        df = df.Define("Tau_SFe", "doTauSFvse(Tau_pt, Tau_eta, Tau_dz, Tau_decayMode, Tau_genPartFlav)")
        df = df.Define("Tau_SFmu", "doTauSFvsmu(Tau_pt, Tau_eta, Tau_dz, Tau_decayMode,  Tau_genPartFlav)")
        df = df.Define("Tau_SFjet", "doTauSFvsjet(Tau_pt, Tau_eta, Tau_dz, Tau_decayMode,  Tau_genPartFlav)")
        df = df.Define("Tau_SF", "Tau_SFe * Tau_SFmu * Tau_SFjet")
        df = df.DropColumns("Tau_Scale")
        return df
