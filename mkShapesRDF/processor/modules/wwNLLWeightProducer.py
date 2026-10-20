import ROOT
from mkShapesRDF.processor.framework.module import Module

########
######## ----- wwNLLWeightProducer -----
########
######## Warning: The NLL weights are computed at 13 TeV
######## (as of 16th of April 2026)
########

class wwNLLWeightProducer(Module):
    def __init__(self,
                 sampleName = "",
                 subFolder = "13TeV",
                 framework_path=None):

        super().__init__("wwNLLWeightProducer")

        self.sampleName = sampleName
        self.subFolder = subFolder
        if framework_path:
            self.wwresum_path = framework_path.split("framework")[0] + "/processor/data/wwresum"
        else:
            self.wwresum_path = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/wwresum"

            
        
    def runModule(self, df, values):

        if not self.sampleName.startswith("WWTo"):
            return df


        if not hasattr(ROOT, "k_reader_QQWW"):
            ROOT.gInterpreter.Declare(
                f"""
                #include "{self.wwresum_path}/qqww_kfactor.cc"
                qqww_K_producer k_reader_QQWW = qqww_K_producer(
                    "{self.wwresum_path}/{self.subFolder}/central.dat",
                    "{self.wwresum_path}/{self.subFolder}/resum_up.dat",
                    "{self.wwresum_path}/{self.subFolder}/resum_down.dat",
                    "{self.wwresum_path}/{self.subFolder}/scale_up.dat",
                    "{self.wwresum_path}/{self.subFolder}/scale_down.dat"
                );
                """
            )
        
        df = df.Define(
            "wwNLL",
            "k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,0)"
        )
        df = df.Define(
            "nllW_Rup",
            "k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,1,1)"
        )
        df = df.Define(
            "nllW_Rdown",
            "k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,-1,1)"
        )
        df = df.Define(
            "nllW_Qup",
            "k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,1,0)"
        )
        df = df.Define(
            "nllW_Qdown",
            "k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,-1,0)"
        )

        return df
