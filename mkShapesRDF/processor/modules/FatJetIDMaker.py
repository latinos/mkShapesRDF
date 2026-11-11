import ROOT
from mkShapesRDF.processor.framework.module import Module
from mkShapesRDF.processor.data.JetMaker_cfg import JetMakerCfg
import correctionlib

correctionlib.register_pyroot_binding()

class FatJetIDMaker(Module):
    def __init__(self, year=""):
        super().__init__("FatJetIDMaker")
        self.doJetId = False
        self.year = year
        self.runPeriods = None

        cfg = JetMakerCfg[self.year]
        if "fat_jet" in cfg and "fatjetId" in cfg["fat_jet"]:
            self.doJetId = True
            self.jetIdJson = cfg["fat_jet"]["fatjetId"]["json"]
            self.tight = cfg["fat_jet"]["fatjetId"]["tight"]
            self.tightleptonveto = cfg["fat_jet"]["fatjetId"]["tightleptonveto"]
        elif "1" in cfg and "fatjetId" in cfg["1"]["fat_jet"]:
            self.doJetId = True
            self.runPeriods = [run for run in cfg if str(run).isdigit()]
            self.jetIdJson = {}
            self.tight = {}
            self.tightleptonveto = {}
            for run in self.runPeriods:
                self.jetIdJson[run] = cfg[run]["fat_jet"]["fatjetId"]["json"]
                self.tight[run] = cfg[run]["fat_jet"]["fatjetId"]["tight"]
                self.tightleptonveto[run] = cfg[run]["fat_jet"]["fatjetId"]["tightleptonveto"]

    def runModule(self, df, values):
        if "v12" in self.year:
            return df

        if self.doJetId:
            text_to_add = ""
            if self.runPeriods:
                text_to_add = """
                    correction::Correction::Ref cset_fatjet_id_tight;
                    correction::Correction::Ref cset_fatjet_id_tightlepveto;
                """
                for run in self.runPeriods:
                    ROOT.gROOT.ProcessLine(f'auto fatjetIdFile_{run} = correction::CorrectionSet::from_file("{self.jetIdJson[run]}");')
                    ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_fatjet_id_tight_{run} = fatjetIdFile_{run}->at("{self.tight[run]}");')
                    ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_fatjet_id_tightlepveto_{run} = fatjetIdFile_{run}->at("{self.tightleptonveto[run]}");')
                    text_to_add += f"""
                        if (run_period == {run}) {{
                            cset_fatjet_id_tight = cset_fatjet_id_tight_{run};
                            cset_fatjet_id_tightlepveto = cset_fatjet_id_tightlepveto_{run};
                        }}
                    """
            else:
                ROOT.gROOT.ProcessLine(f'auto fatjetIdFile = correction::CorrectionSet::from_file("{self.jetIdJson}");')
                ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_fatjet_id_tight = fatjetIdFile->at("{self.tight}");')
                ROOT.gROOT.ProcessLine(f'correction::Correction::Ref cset_fatjet_id_tightlepveto = fatjetIdFile->at("{self.tightleptonveto}");')

            ROOT.gInterpreter.Declare("""
                ROOT::RVecI FatJet_ID(
                    ROOT::RVecF FatJet_eta,
                    ROOT::RVecF FatJet_chHEF,
                    ROOT::RVecF FatJet_neHEF,
                    ROOT::RVecF FatJet_chEmEF,
                    ROOT::RVecF FatJet_neEmEF,
                    ROOT::RVecF FatJet_muEF,
                    ROOT::RVecI FatJet_chMultiplicity,
                    ROOT::RVecI FatJet_neMultiplicity,
                    int run_period=-1) {

                    ROOT::RVecI FatJet_JetId(FatJet_eta.size(), 0);
                """ + text_to_add + """
                    for (int i = 0; i < FatJet_eta.size(); i++) {
                        int multiplicity = FatJet_chMultiplicity[i] + FatJet_neMultiplicity[i];
                        int pass_id = cset_fatjet_id_tight->evaluate({FatJet_eta[i], FatJet_chHEF[i], FatJet_neHEF[i], FatJet_chEmEF[i], FatJet_neEmEF[i], FatJet_muEF[i], FatJet_chMultiplicity[i], FatJet_neMultiplicity[i], multiplicity});
                        int pass_lepveto = cset_fatjet_id_tightlepveto->evaluate({FatJet_eta[i], FatJet_chHEF[i], FatJet_neHEF[i], FatJet_chEmEF[i], FatJet_muEF[i], FatJet_chMultiplicity[i], FatJet_neMultiplicity[i], multiplicity});
                        FatJet_JetId[i] = tightLepVeto ? 6 : (tight ? 2 : 0);
                    }
                    return FatJet_JetId;
                }
            """
            )
            df = df.Define("FatJet_jetId", "FatJet_ID(FatJet_eta,FatJet_chHEF,FatJet_neHEF,FatJet_chEmEF,FatJet_neEmEF,FatJet_muEF,FatJet_chMultiplicity,FatJet_neMultiplicity,run_period)")

        return df

