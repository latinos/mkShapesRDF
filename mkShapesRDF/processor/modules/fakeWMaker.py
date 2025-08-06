import ROOT
from mkShapesRDF.processor.framework.module import Module
import re
import os

class fakeWMaker(Module):
    def __init__(self, era, framework_path):
        super().__init__("fakeWMaker") 
        self.fake_path = ""
        if framework_path:
            self.fake_path = framework_path.split("framework")[0] + "/processor/data/fakes"
        print(f"Running fakeW computation for {era}")
        self.era = era

    def runModule(self, df, values):
        ROOT.gROOT.ProcessLine(f'#include "{self.fake_path}/fake_rate_reader_class.cc"')
        print('Macro loaded')

        print("Running fakeW computation")
        eleWP_options = ["wp90iso", "mvaWinter22V2Iso_WP90", "cutBased_LooseID_tthMVA_Run3"]
        muWP_options = ["cut_Tight_HWW", "cut_TightID_pfIsoTight_HWW_tthmva_67", "cut_TightID_pfIsoLoose_HWW_tthmva_67"]
        kinds = ['nominal', 'EleUp', 'EleDown', 'MuUp', 'MuDown', 'StatEleUp', 'StatEleDown', 'StatMuUp', 'StatMuDown']
        nLeptons_options = [2, 3]
        electron_tight_charge = "std"
        for eleWP in eleWP_options:
            for muWP in muWP_options:
                for kind in kinds:
                    for nLeptons in nLeptons_options:
                        reader_name = f"fr_reader_{eleWP}_{muWP}_{kind}_{nLeptons}"
                        ROOT.gInterpreter.Declare(
                            f'fake_rate_reader {reader_name}(\"{self.fake_path}/\", '     # fake_path
                            f'\"{self.era}/\", '                                          # era
                            f'\"{eleWP}\", '                                              # ele_WP
                            f'\"{muWP}\", '                                               # muon_WP
                            f'\"{kind}\", '                                               # kind
                            f'{nLeptons}, '                                               # nLeptons
                            f'\"{electron_tight_charge}\");'                              # electron_tight_charge
                        )
                        if kind == 'nominal':
                            df = df.Define(
                                f"fakeW{nLeptons}l_ele_{eleWP}_mu_{muWP}",
                                f"{reader_name}(Lepton_pdgId, Lepton_pt, Lepton_eta, "
                                f"Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, "
                                "Lepton_muonIdx, CleanJet_pt, CleanJet_pt.size())"
                            )
                        else :
                            df = df.Define(
                                f"fakeW{nLeptons}l_ele_{eleWP}_mu_{muWP}_{kind}",
                                f"{reader_name}(Lepton_pdgId, Lepton_pt, Lepton_eta, "
                                f"Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, "
                                "Lepton_muonIdx, CleanJet_pt, CleanJet_pt.size())"
                            )
                        print(f"fakeW{nLeptons}l_ele_{eleWP}_mu_{muWP}_{kind}")
                        print("Done!!!!")

        return df
