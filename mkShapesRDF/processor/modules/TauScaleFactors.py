import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.Tau_cfg import *
import correctionlib
import os
import re

correctionlib.register_pyroot_binding()

class TauScaleFactors(Module):
    def __init__(self, era, recipe):
        super().__init__("TauSF")
        self.era = era
        conf = Taus[era]["TAU"]
        self.file   = conf[0]
        self.recipe = recipe

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

            RVecF doTauScale( RVecF pt, RVecF eta, RVecU dm, RVecU gen ) {{
                RVecF newPt = pt;
                for (unsigned i = 0; i < pt.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 1 && gm != 2 && gm != 5 && gm != 6) continue;

                int decay = (int)dm[i];
                if (decay != 0 && decay != 1 && decay != 10 && decay != 11) continue;

                double scale = tau_tes->evaluate({{ (double)pt[i], (double)eta[i], decay, gm, "DeepTau2018v2p5", "Medium", "Tight", "nom"}});
                newPt[i] = pt[i] * scale;
                std::cout << "Step done" << std::endl;
                }}
                return newPt;
            }}
            std::cout << "doTauScale done" << std::endl;
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

            RVecF doTauSFvse( RVecF eta, RVecU dm, RVecU gen) {{
                RVecF SF(eta.size(), 1.0);
                for (unsigned i = 0; i < eta.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 0 && gm != 1) continue;
                int decay = (int)dm[i];
                if (decay != 0 && decay != 1 && decay != 10 && decay != 11) continue;
                SF[i] = tau_sfvse->evaluate({{(double)eta[i], decay, gm, "VVLoose", "nom"}});
                }}
                return SF;
            }}
            
            RVecF doTauSFvsmu( RVecF eta, RVecU gen) {{
                RVecF SF(eta.size(), 1.0);
                for (unsigned i = 0; i < eta.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 0 && gm != 2) continue;
                if (std::string("{self.era}") == "Full2024v15") {{
                    SF[i] = tau_sfvsmu->evaluate({{(double)eta[i], gm, "Medium", "VVLoose", "Medium", "nom"}});
                }}
                else{{
                    SF[i] = tau_sfvsmu->evaluate({{(double)eta[i], gm, "Medium", "nom"}});
                }}
                }}
                return SF;
            }}

            RVecF doTauSFvsjet( RVecF pt, RVecU dm, RVecU gen ) {{
                RVecF SF(pt.size(), 1.0);
                for (unsigned i = 0; i < pt.size(); i++) {{
                int gm = (int)gen[i];
                if (gm != 0 && gm != 1 && gm != 2 && gm != 3 && gm != 4 && gm != 5 && gm != 6) continue;

                int decay = (int)dm[i];
                if (decay != 0 && decay != 1 && decay != 10 && decay != 11) continue;
                if (std::string("{self.era}") == "Full2024v15") {{
                    SF[i] = tau_sfvsjet->evaluate({{ (double)pt[i], decay, gm, "Medium", "VVLoose", "nom", "dm"}});
                }}
                else{{
                    SF[i] = tau_sfvsjet->evaluate({{ (double)pt[i], decay, gm, "Medium", "VVLoose", "default", "dm"}});
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

        if self.recipe == "Tau Scaler":
            df = df.Define("Tau_Scale", "doTauScale(Tau_pt, Tau_eta, Tau_decayMode, Tau_genPartFlav)")
            df = df.Define("Tau_newPt", "Tau_Scale")
            df = df.Define("Tau_sorting", "sortedIndices(Tau_newPt)")
            df = df.Redefine("Tau_pt", "Take(Tau_newPt, Tau_sorting)")
        elif self.recipe == "Tau SF":
            df = df.Define("Tau_SFe", "doTauSFvse(Tau_eta, Tau_decayMode, Tau_genPartFlav)")
            df = df.Define("Tau_SFmu", "doTauSFvsmu(Tau_eta, Tau_genPartFlav)")
            df = df.Define("Tau_SFjet", "doTauSFvsjet(Tau_pt, Tau_decayMode, Tau_genPartFlav)")
            df = df.Define("Tau_SF", "Tau_SFe * Tau_SFmu * Tau_SFjet")
        return df