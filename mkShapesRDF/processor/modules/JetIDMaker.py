import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import correctionlib
import os
import re
correctionlib.register_pyroot_binding()

class JetIDMaker(Module):
    def __init__(self, year=""):
        super().__init__("JetIDMaker")
        self.doJetId = False
        self.year = year
        self.columnsToDrop = []
        self.runPeriods = None

        if "jetId" in JetMakerCfg[self.year].keys():
            self.doJetId = True
            self.jetIdJson = JetMakerCfg[self.year]["jetId"]["json"]
            self.tight = JetMakerCfg[self.year]["jetId"]["tight"]
            self.tightleptonveto = JetMakerCfg[self.year]["jetId"]["tightleptonveto"]
        elif "1" in JetMakerCfg[self.year].keys() and "jetId" in JetMakerCfg[self.year]["1"].keys(): # Assumes run-periods always starts by 1
            self.doJetId = True
            self.jetIdJson = {}
            self.tight = {}
            self.tightleptonveto = {}
            self.runPeriods = JetMakerCfg[self.year].keys()
            for run in self.runPeriods:
                self.jetIdJson[run] = JetMakerCfg[self.year][run]["jetId"]["json"]
                self.tight[run] = JetMakerCfg[self.year][run]["jetId"]["tight"]
                self.tightleptonveto[run] = JetMakerCfg[self.year][run]["jetId"]["tightleptonveto"]
        
    def runModule(self, df, values):
        
        if "v12" in self.year:
            ROOT.gInterpreter.Declare(
                """
                RVecI Jet_ID(
                    RVecF Jet_eta,
                    RVecF Jet_neHEF,
                    RVecF Jet_neEmEF,
                    RVecF Jet_chEmEF,
                    RVecF Jet_muEF,
                    RVecI Jet_jetId){

                    RVecI Jet_JetId(Jet_eta.size(), 0);

                    for (int i = 0; i < Jet_eta.size(); i++) {

                        float eta = fabs(Jet_eta[i]);
                        int jetid = Jet_jetId[i];

                        bool tight = (jetid & (1 << 1)) && ((eta <= 2.7) || (eta <= 3.0 && Jet_neHEF[i] < 0.99) || (eta >  3.0 && Jet_neEmEF[i] < 0.40));

                        bool tightLepVeto = tight && (eta > 2.7 || (Jet_muEF[i] < 0.80 && Jet_chEmEF[i] < 0.80));

                        Jet_JetId[i] = tightLepVeto ? 6 : (tight ? 2 : 0);

                    }

                    return Jet_JetId;
                }
                """
            )
            df = df.Redefine("Jet_jetId", "Jet_ID(Jet_eta,Jet_neHEF,Jet_neEmEF,Jet_chEmEF,Jet_muEF,Jet_jetId)")
        if self.doJetId:

            jetIdJson = self.jetIdJson
            tight = self.tight
            tightleptonveto = self.tightleptonveto

            print(jetIdJson)
            print(tight)
            print(tightleptonveto)

            text_to_add = ""
            if self.runPeriods:
                text_to_add = """
                correction::Correction::Ref cset_jet_id_tight;
                correction::Correction::Ref cset_jet_id_tightlepveto;
                """
                for run in self.runPeriods:
                    ROOT.gROOT.ProcessLine(f'auto jetIdFile_{run} = correction::CorrectionSet::from_file("{jetIdJson[run]}");')
                    ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tight_{run} = (correction::Correction::Ref) jetIdFile_{run}->at("{tight[run]}");')
                    ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tightlepveto_{run} = (correction::Correction::Ref) jetIdFile_{run}->at("{tightleptonveto[run]}");')

                    text_to_add += f"""
                    if (run_period == {run}) {{
                        cset_jet_id_tight = cset_jet_id_tight_{run};
                        cset_jet_id_tightlepveto = cset_jet_id_tightlepveto_{run};
                    }}
                    """
            else:
                ROOT.gROOT.ProcessLine(f'auto jetIdFile = correction::CorrectionSet::from_file("{jetIdJson}");')
                ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tight = (correction::Correction::Ref) jetIdFile->at("{tight}");')
                ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_jet_id_tightlepveto = (correction::Correction::Ref) jetIdFile->at("{tightleptonveto}");')

            ROOT.gInterpreter.Declare(
                """
                RVecI Jet_ID(
                    RVecF Jet_eta,
                    RVecF Jet_chHEF,
                    RVecF Jet_neHEF,
                    RVecF Jet_chEmEF,
                    RVecF Jet_neEmEF,
                    RVecF Jet_muEF,
                    RVecI Jet_chMultiplicity,
                    RVecI Jet_neMultiplicity,
                    int run_period=-1){

                    RVecI Jet_JetId(Jet_eta.size(), 0);
                    
                    """+text_to_add+"""

                    for (int i=0; i<Jet_eta.size(); i++){

                        int multiplicity = Jet_chMultiplicity[i] + Jet_neMultiplicity[i];

                        int pass_id = cset_jet_id_tight->evaluate({Jet_eta[i], Jet_chHEF[i], Jet_neHEF[i], Jet_chEmEF[i], Jet_neEmEF[i], Jet_muEF[i], Jet_chMultiplicity[i], Jet_neMultiplicity[i], multiplicity});
                        int pass_lepveto = cset_jet_id_tightlepveto->evaluate({Jet_eta[i], Jet_chHEF[i], Jet_neHEF[i], Jet_chEmEF[i], Jet_neEmEF[i], Jet_muEF[i], Jet_chMultiplicity[i], Jet_neMultiplicity[i], multiplicity});

                        if (pass_lepveto) Jet_JetId[i] = 6;
                        else if (pass_id) Jet_JetId[i] = 2;
                        else Jet_JetId[i] = 0;
                    }

                    return Jet_JetId;
                }
                """
            )

            df = df.Define("Jet_jetId", "Jet_ID(Jet_eta,Jet_chHEF,Jet_neHEF,Jet_chEmEF,Jet_neEmEF,Jet_muEF,Jet_chMultiplicity,Jet_neMultiplicity,run_period)")
            
        return df