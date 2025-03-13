import ROOT
from mkShapesRDF.processor.framework.module import Module
import re
import correctionlib

correctionlib.register_pyroot_binding()


def makeCPPString(string):
    s = str(string)
    return s.replace(".", "_").replace("-", "m").replace("+", "p")

class btagSFProducerLatinos(Module):
    def __init__(
        self,
        era,
        algo="deepJet",
        selectedWPs=["shape"],
        mode="shape",
        framework_path=None,
        jesSystsForShape=[],
    ):
        super().__init__("btagSFProducerLatinos")
        self.era = era
        self.algo = algo
        self.selectedWPs = selectedWPs
        self.jesSystsForShape = jesSystsForShape
        self.mode = mode

        self.max_abs_eta = """2.49999"""
        self.min_pt = """20.0001"""

        if "2022" or "2023" in era:
            self.prodTime = "Summer"
        else:
            print("btagSFProducerLatinos")
            print("-------------------")
            print("Warning: Production season unknown for " + era)
            print("Please check!!")

        year = re.findall(r'\d+', era)[0]
        key = era.split("Full20")[1].split("v")[0]
        
        if framework_path:
            pathToJson = framework_path.split("framework")[0] + "/processor/data/jsonpog-integration/POG/BTV/" + year + "_" + self.prodTime + key + "/btagging.json.gz"
        else:
            pathToJson = os.path.dirname(os.path.dirname(__file__)).split("processor")[0] + "/processor/data/jsonpog-integration/POG/BTV/" + year + "_" + self.prodTime + key + "/btagging.json.gz"
        
        self.inputFileName = pathToJson
        self.measurement_types = None
        self.supported_wp = None

        self.systs = []
        self.central_and_systs = []

        self.systs_shape_corr = []
        self.central_and_systs_shape_corr = []

    def runModule(self, df, values):
        ### Correctionlib JSON structure and allowed chains  # noqa: E266
        supported_algos = {
            "deepJet": {
                "light": {
                    "inputs": ["systematic", "working_point", "flavor", "abseta", "pt"],
                    "systematic": [
                        "central",
                        "down",
                        "down_correlated",
                        "down_uncorrelated",
                        "up",
                        "up_correlated",
                        "up_uncorrelated",
                    ],
                    "working_point": ["L", "M", "T"],
                    "flavor": {"b": 5, "c": 4, "udsg": 0},
                    "abseta": "abs(Jet_eta)",
                    "pt": "Jet_pt",
                },
                "shape": {
                    "inputs": ["systematic", "flavor", "abseta", "pt"],
                    "systematic": [
                        "hf",
                        "lf",
                        "hfstats1",
                        "hfstats2",
                        "lfstats1",
                        "lfstats2",
                        "cferr1",
                        "cferr2",
                    ],
                    "flavor": {"b": 5, "c": 4, "udsg": 0},
                    "abseta": "abs(Jet_eta)",
                    "pt": "Jet_pt",
                    "Discriminant": "Jet_btagDeepFlavB",
                },
            },
            "particleNet": {
                "light": {
                    "inputs": ["systematic", "working_point", "flavor", "abseta", "pt"],
                    "systematic": [
                        "central",
                        "down",
                        "down_correlated",
                        "down_uncorrelated",
                        "up",
                        "up_correlated",
                        "up_uncorrelated",
                    ],
                    "working_point": ["L", "M", "T"],
                    "flavor": {"b": 5, "c": 4, "udsg": 0},
                    "abseta": "abs(Jet_eta)",
                    "pt": "Jet_pt",
                },
                "shape": {
                    "inputs": ["systematic", "flavor", "abseta", "pt", "discriminant"],
                    "systematic": [
                        "hf",
                        "lf",
                        "hfstats1",
                        "hfstats2",
                        "lfstats1",
                        "lfstats2",
                        "cferr1",
                        "cferr2",
                    ],
                    "flavor": {"b": 5, "c": 4, "udsg": 0},
                    "abseta": "abs(Jet_eta)",
                    "pt": "Jet_pt",
                    "Discriminant": "Jet_btagPNetB",
                },
            },
            "robustParticleTransformer": {
                "light": {
                    "inputs": ["systematic", "working_point", "flavor", "abseta", "pt"],
                    "systematic": [
                        "central",
                        "down",
                        "down_correlated",
                        "down_uncorrelated",
                        "up",
                        "up_correlated",
                        "up_uncorrelated",
                    ],
                    "working_point": ["L", "M", "T"],
                    "flavor": {"b": 5, "c": 4, "udsg": 0},
                    "abseta": "abs(Jet_eta)",
                    "pt": "Jet_pt",
                },
                "shape": {
                    "inputs": ["systematic", "flavor", "abseta", "pt", "discriminant"],
                    "systematic": [
                        "hf",
                        "lf",
                        "hfstats1",
                        "hfstats2",
                        "lfstats1",
                        "lfstats2",
                        "cferr1",
                        "cferr2",
                    ],
                    "flavor": {"b": 5, "c": 4, "udsg": 0},
                    "abseta": "abs(Jet_eta)",
                    "pt": "Jet_pt",
                    "Discriminant": "Jet_btagRobustParTAK4B",
                },
	    },
        }

        if self.algo not in supported_algos.keys():
            raise ValueError(
                "ERROR: Algorithm '%s' not supported for era = '%s'! Please choose among { %s }."
                % (self.algo, self.era, supported_algos)
            )

        if self.mode not in supported_algos[self.algo].keys():
            raise ValueError(
                "ERROR: Algorithm '%s' not supported for mode = '%s'! Please choose among { %s }."
                % (self.algo, self.mode, supported_algos)
            )

        if self.mode == "incl":
            for wp in self.selectedWPs:
                if wp not in supported_algos[self.algo][self.mode]["working_point"]:
                    raise ValueError(
                        "ERROR: Working point '%s' not supported for algo = '%s' and mode = '%s'! Please choose among { %s }."
                        % (wp, self.algo, self.mode, self.supported_wp)
                    )

        print("Compute b-tag scale factors for -> Algorithm: " + self.algo + "   Mode: " + self.mode)

        branch_algo = {"deepJet": "Jet_btagDeepFlavB", "particleNet": "Jet_btagPNetB", "robustParticleTransformer": "Jet_btagRobustParTAK4B"}
        branch_sfalgo = {"deepJet": "deepjet", "particleNet": "partNet", "robustParticleTransformer": "partTransformer"}

        branch_name = branch_algo[self.algo]
        branch_sfname = branch_sfalgo[self.algo]
        
        # define systematic uncertainties
        self.systs = []
        self.systs.append("up")
        self.systs.append("down")
        self.central_and_systs = ["central"]
        self.central_and_systs.extend(self.systs)

        # define systs for shape SF
        self.systs_shape_corr = []
        for syst in [
            "lf",
            "hf",
            "hfstats1",
            "hfstats2",
            "lfstats1",
            "lfstats2",
            "cferr1",
            "cferr2",
        ] + self.jesSystsForShape:
            self.systs_shape_corr.append("up_%s" % syst)
            self.systs_shape_corr.append("down_%s" % syst)
        self.central_and_systs_shape_corr = ["central"]
        self.central_and_systs_shape_corr.extend(self.systs_shape_corr)

        shape_syst = [
            "lf",
            "hf",
            "hfstats1",
            "hfstats2",
            "lfstats1",
            "lfstats2",
            "cferr1",
            "cferr2",
        ] + self.jesSystsForShape
        
        ### Open Json  # noqa: E266
        cset_btag_name = f"cset_btag_{self.era}_{self.mode}_{self.algo}"
        cset_btag_sf_name = f"cset_btag_sf_{self.era}_{self.mode}_{self.algo}"
        if not hasattr(ROOT, cset_btag_name):
            # check if cset_btag is already defined

            ROOT.gROOT.ProcessLine(
                f"""
                auto {cset_btag_name} = correction::CorrectionSet::from_file("{self.inputFileName}");
                """
            )

        ### Load the correction given algo and mode  # noqa: E266
        if not hasattr(ROOT, cset_btag_sf_name):
            # check if cset_btag_sf is already defined
            s = f"""
            correction::Correction::Ref {cset_btag_sf_name} = (correction::Correction::Ref) {cset_btag_name}->at("{self.algo}_{self.mode}");
            """
        else:
            # if already defined store the new cset_btag_sf
            s = f"""
            {cset_btag_sf_name} = (correction::Correction::Ref) {cset_btag_name}->at("{self.algo}_{self.mode}");
            """

        ROOT.gROOT.ProcessLine(s)

        suffix = f"{self.mode}_{self.algo}"
        getbtagSF_shape_name = f"getbtagSF_shape_{suffix}"
        getbtagSF_wp_name = f"getbtagSF_wp_name_{suffix}"

        if self.mode == "shape":
            if not hasattr(ROOT, getbtagSF_shape_name):
                ROOT.gInterpreter.Declare(
                    "ROOT::RVecF "
                    + getbtagSF_shape_name
                    + """
                    (std::string syst, ROOT::RVecI flav, ROOT::RVecF eta, ROOT::RVecF pt, ROOT::RVecF btag){
                        ROOT::RVecF sf(pt.size(), 1.0);

                        for (unsigned int i = 0, n = pt.size(); i < n; ++i) {
                                if (pt[i]<"""
                    + self.min_pt
                    + """ || abs(eta[i])>"""
                    + self.max_abs_eta
                    + """ || btag[i]<0.0 || isnan(btag[i]) || btag[i]>19.999){continue;}
                                if (syst.find("jes") != std::string::npos && flav[i]!=0){continue;}
                                if (syst.find("cferr") != std::string::npos){
                                        if (flav[i]==4){
                                                auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, abs(flav[i]), abs(eta[i]), pt[i], btag[i]});
                                                sf[i] = float(sf_tmp);
                                        }else{
                                            continue;
                                        }
                                }else if (syst.find("hf") != std::string::npos || syst.find("lf") != std::string::npos){
                                    if (flav[i]==4){
                                            continue;
                                    }else{
                                        auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, abs(flav[i]), abs(eta[i]), pt[i], btag[i]});
                                        sf[i] = float(sf_tmp);
                                    }
                                }else{
                                    auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, abs(flav[i]), abs(eta[i]), pt[i], btag[i]});
                                    sf[i] = float(sf_tmp);
                                }
                        }
                        return sf;
                    }
                    """
                )

            for central_or_syst in self.central_and_systs_shape_corr:
                if central_or_syst == "central":
                    df = df.Define(
                        f"Jet_btagSF_{branch_sfname}_shape",
                        f'{getbtagSF_shape_name}("{central_or_syst}", Jet_hadronFlavour, Jet_eta, Jet_pt, {branch_name})',
                    )
                else:
                    df = df.Define(
                        f"Jet_btagSF_{branch_sfname}_shape_{central_or_syst}",
                        f'{getbtagSF_shape_name}("{central_or_syst}", Jet_hadronFlavour, Jet_eta, Jet_pt, {branch_name})',
                    )

            ### Do we want a separated variation for b-tagging? For this moment save the variation in the nominal file -------
            #for syst in shape_syst:
            #    df = df.Vary(
            #        f"Jet_btagSF_{branch_sfname}_shape",
            #        "ROOT::RVec<ROOT::RVecF>{Jet_btagSF_"
            #        + branch_sfname
            #        + "_shape_up_"
            #        + syst
            #        + ", Jet_btagSF_"
            #        + branch_sfname
            #        + "_shape_down_"
            #        + syst
            #        + "}",
            #        ["up", "down"],
            #        syst,
            #    )
            #    df = df.DropColumns("Jet_btagSF_" + branch_sfname + "_shape_up_" + syst)
            #    df = df.DropColumns(
            #        "Jet_btagSF_" + branch_sfname + "_shape_down_" + syst
            #    )
        
        else:

            print("Fixed working point scale factors not fully supported!!! Check the code <--------")

            
            ##### ADVICE: The fixed SF computation is temporary removed -----------------------------
            ###
            ### If we want to add fixed WP to the postprocessor we need to fine tune the workfow. Needed:
            ###
            ###   - Add MC efficiencies to properly compute the SF
            ###   - Compute the SF separately for light and heavy flavour
            ###
            ###
            ###

            '''
            ROOT.gInterpreter.Declare(
                "ROOT::RVecF "
                + getbtagSF_wp_name
                + """
                (std::string syst, std::string wp, ROOT::RVecI flav, ROOT::RVecF eta, ROOT::RVecF pt){
                    ROOT::RVecF sf(pt.size(), 1.0);
                    for (unsigned int i = 0, n = pt.size(); i < n; ++i) {
                            if (pt[i]<"""
                + self.min_pt
                + """ || abs(eta[i])>"""
                + self.max_abs_eta
                + """ || btag[i]<0.0){continue;}
                        auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, wp, abs(flav[i]), abs(eta[i]), pt[i]});
                        sf[i] = float(sf_tmp);
                    }
                    return sf;
                }
                """
            )

            for wp in self.selectedWPs:
                for central_or_syst in self.central_and_systs:
                    if central_or_syst == "central":
                        df = df.Define(
                            f"Jet_btagSF_{branch_sfname}_{self.mode}_{wp}",
                            f'{getbtagSF_wp_name}("{central_or_syst}", "{wp}", Jet_hadronFlavour, Jet_eta, Jet_pt)',
                        )
                    else:
                        df = df.Define(
                            f"Jet_btagSF_{branch_sfname}_{self.mode}_{wp}_{central_or_syst}",
                            f'{getbtagSF_wp_name}("{central_or_syst}", "{wp}", Jet_hadronFlavour, Jet_eta, Jet_pt)',
                        )

            ### Do we want a separated variation for b-tagging? For this moment save the variation in the nominal file ------------
            #for wp in self.selectedWPs:
            #    df = df.Vary(
            #        f"Jet_btagSF_{branch_sfname}_{self.mode}_{wp}",
            #        "ROOT::RVec<ROOT::RVecF>{Jet_btagSF_"
            #        + branch_sfname
            #        + "_"
            #        + self.mode
            #        + "_"
            #        + wp
            #        + "_up, Jet_btagSF_"
            #        + branch_sfname
            #        + "_"
            #        + self.mode
            #        + "_"
            #        + wp
            #        + "_down}",
            #        ["up", "down"],
            #        f"Jet_btagSF_{branch_sfname}_{self.mode}_{wp}_variation",
            #    )
            #    df = df.DropColumns("Jet_btagSF_" + branch_sfname + "_" + self.mode + "_" + wp + "_up")
            #    df = df.DropColumns("Jet_btagSF_" + branch_sfname + "_" + self.mode + "_" + wp + "_down")
            '''

        return df
