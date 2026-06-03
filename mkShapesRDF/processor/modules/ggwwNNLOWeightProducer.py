import ROOT
from mkShapesRDF.processor.framework.module import Module

########
######## ----- ggwwNNLOWeightProducer -----
########
######## Warning: The NNLO weights are computed at 13 TeV
######## (as of 16th of April 2026)
########

class ggwwNNLOWeightProducer(Module):
    def __init__(self,
                 inputFileNLO = "Kfactor_Collected_ggHZZ_2l2l_NLO_NNPDF_NarrowWidth_13TeV.root",
                 inputFileNNLO = "Kfactor_Collected_ggHZZ_2l2l_NNLO_NNPDF_NarrowWidth_13TeV.root",
                 sampleName = "",
                 framework_path=None):

        super().__init__("ggwwNNLOWeightProducer")

        self.inputFileNLO = inputFileNLO
        self.inputFileNNLO = inputFileNNLO
        self.sampleName = sampleName
        if framework_path:
            self.ggww_path = framework_path.split("framework")[0] + "/processor/data/ggww_kfactors"
        else:
            self.ggww_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/ggww_kfactors"
            
        
    def runModule(self, df, values):

        if not self.sampleName.startswith("GluGluto"):
            return df

        if not hasattr(ROOT, "k_reader_GGWW"):
            ROOT.gInterpreter.Declare(
                f"""
                TString fileIn = "{self.ggww_path}/{self.inputFileNLO}";
                TString fileIn_NNLO = "{self.ggww_path}/{self.inputFileNNLO}";    
                #include "{self.ggww_path}/ggww_kfactor.cc"
                ggww_K_producer k_reader_GGWW = ggww_K_producer();
                """
            )
        
        df = df.Define(
            "KFactor_ggWW",
            "k_reader_GGWW(nLHEPart,LHEPart_pt,LHEPart_eta,LHEPart_phi,LHEPart_mass,LHEPart_pdgId,LHEPart_status)"
        )

        df = df.Define(
            "ggww_kfactor_nlo",            
            "KFactor_ggWW[0]"
        )
        df = df.Define(
            "ggww_kfactor_nlo_up",
            "KFactor_ggWW[1]"
        )
        df = df.Define(
            "ggww_kfactor_nlo_do",
            "KFactor_ggWW[2]"
        )
        df = df.Define(
            "ggww_kfactor_nnlo",
            "KFactor_ggWW[3]"
        )
        df = df.Define(
            "ggww_kfactor_nnlo_up",
            "KFactor_ggWW[4]"
        )
        df = df.Define(
            "ggww_kfactor_nnlo_do",
            "KFactor_ggWW[5]"
        )
        df = df.DropColumns("KFactor_ggWW")

        return df
