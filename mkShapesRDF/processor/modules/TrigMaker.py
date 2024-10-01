import ROOT
from mkShapesRDF.processor.framework.module import Module
import correctionlib

import os

ROOT.PyConfig.IgnoreCommandLineOptions = True

from copy import deepcopy

correctionlib.register_pyroot_binding()


class TrigMaker(Module):
    def __init__(
        self,
        era="Full2018v9",
        isData=False,
        keepRunP=False,
        cfg_path="processor/data/TrigMaker_cfg.py",
        seeded=False,
        branch_map="",
        computeSF=True
    ):
        super().__init__("TrigMaker")

        self.era = era
        self.isData = isData
        self.keepRunP = keepRunP
        self.seeded = seeded
        self.firstEvent = True
        self.computeSF = computeSF
        
        self.mu_maxPt = 149.9
        self.mu_minPt = 9.999
        self.mu_maxEta = 2.3999
        self.mu_minEta = -2.3999

        self.el_maxPt = 99.9
        self.el_minPt = 9.999
        self.el_maxEta = 2.4999
        self.el_minEta = -2.4999

        ## Needed?
        if "processor" in os.path.dirname(os.path.dirname(__file__)):
            self.cfg_path = (
                os.path.dirname(os.path.dirname(__file__)).split("processor")[0]
                + cfg_path
            )
        else:
            self.cfg_path = cfg_path

        var = {}
        exec(open(self.cfg_path, "r").read(), var)

        if self.isData:
            self.typeStr = "DATA"
            self.NewVar = var["NewVar_DATA_dict"]
        else:
            self.NewVar = var["NewVar_MC_dict"]
            self.typeStr = "MC"

        self.Trigger = var["Trigger"]

        print(
            "TrigMaker: Era = "
            + self.era
            + ", isData = "
            + str(self.isData)
            + ", keepRunPeriod = "
            + str(self.keepRunP)
        )

        if cfg_path != "processor/data/TrigMaker_cfg.py":
            print("TrigMaker: loaded trigger configuration from " + cfg_path)

        self._branch_map = branch_map

        if self.keepRunP:
            try:
                self.NewVar["I"].remove("run_period")
            except:
                pass

        ##########
        ########## Start file readers  :  Same structure as old Latinos framework
        ##########

        self.TM_trig = {}
        self.TM_LegEffData = {}
        self.TM_LegEffMC = {}
        self.TM_DZEffData = {}
        self.TM_DZEffMC = {}
        self.TM_DRllSF = {}
        self.TM_GlEff = {}
        self.TM_runInt = {}
        self.TM_runPeriods = []

        for RunP in self.Trigger[self.era]:
            self.TM_trig[RunP] = {}
            self.TM_LegEffData[RunP] = {}
            self.TM_LegEffMC[RunP] = {}
            self.TM_DZEffData[RunP] = {}
            self.TM_DZEffMC[RunP] = {}
            self.TM_DRllSF[RunP] = {}
            self.TM_GlEff[RunP] = {}
            self.TM_runPeriods.append(RunP)

            if "runList" in self.Trigger[self.era][RunP].keys():
                self.TM_runInt[RunP] = {
                    "runList": self.Trigger[self.era][RunP]["runList"]
                }
            else:
                self.TM_runInt[RunP] = {
                    "b": self.Trigger[self.era][RunP]["begin"],
                    "e": self.Trigger[self.era][RunP]["end"],
                }

            for Tname in self.Trigger[self.era][RunP][self.typeStr]:
                self.TM_trig[RunP][Tname] = []
                for HLT in self.Trigger[self.era][RunP][self.typeStr][Tname]:
                    if HLT is not None:
                        self.TM_trig[RunP][Tname].append(HLT)
                    else:
                        self.TM_trig[RunP][Tname].append("False")

            for Tname in self.Trigger[self.era][RunP]["LegEffData"]:
                if self.Trigger[self.era][RunP]["LegEffData"][Tname] is not None:
                    temp_file = (
                        self.cfg_path.split("TrigMaker_cfg.py")[0]
                        + "trigger/"
                        + self.Trigger[self.era][RunP]["LegEffData"][Tname]
                    )
                    if ".txt" in temp_file:
                        temp_file = temp_file.split(".txt")[0] + ".json"
                    elif ".json" not in temp_file:
                        print("The following file is not supported")
                        print(temp_file)
                else:
                    temp_file = (
                        cfg_path.split("TrigMaker_cfg.py")[0]
                        + "trigger/dummy_trigger_efficiency.json"
                    )
                self.TM_LegEffData[RunP][Tname] = temp_file

            for Tname in self.Trigger[self.era][RunP]["LegEffMC"]:
                if self.Trigger[self.era][RunP]["LegEffMC"][Tname] is not None:
                    temp_file = (
                        self.cfg_path.split("TrigMaker_cfg.py")[0]
                        + "trigger/"
                        + self.Trigger[self.era][RunP]["LegEffMC"][Tname]
                    )
                    if ".txt" in temp_file:
                        temp_file = temp_file.split(".txt")[0] + ".json"
                    elif ".json" not in temp_file:
                        print("The following file is not supported")
                        print(temp_file)
                else:
                    temp_file = (
                        cfg_path.split("TrigMaker_cfg.py")[0]
                        + "trigger/dummy_trigger_efficiency.json"
                    )
                self.TM_LegEffMC[RunP][Tname] = temp_file

            for Tname in self.Trigger[self.era][RunP]["DZEffData"]:
                Key = list(self.Trigger[self.era][RunP]["DZEffData"][Tname].keys())[0]
                self.TM_DZEffData[RunP][Tname] = {}
                self.TM_DZEffData[RunP][Tname]["type"] = Key
                if Key == "value":
                    self.TM_DZEffData[RunP][Tname]["vals"] = self.Trigger[self.era][
                        RunP
                    ]["DZEffData"][Tname]["value"]
                else:
                    temp_file = (
                        self.cfg_path.split("TrigMaker_cfg.py")[0]
                        + "trigger/"
                        + self.Trigger[self.era][RunP]["DZEffData"][Tname][Key]
                    )
                    if ".txt" in temp_file:
                        temp_file = temp_file.split(".txt")[0] + ".json"
                    elif ".json" not in temp_file:
                        print("The following file is not supported")
                        print(temp_file)
                    self.TM_DZEffData[RunP][Tname]["file"] = temp_file

            for Tname in self.Trigger[self.era][RunP]["DZEffMC"]:
                Key = list(self.Trigger[self.era][RunP]["DZEffMC"][Tname].keys())[0]
                self.TM_DZEffMC[RunP][Tname] = {}
                self.TM_DZEffMC[RunP][Tname]["type"] = Key
                if Key == "value":
                    self.TM_DZEffMC[RunP][Tname]["vals"] = self.Trigger[self.era][RunP][
                        "DZEffMC"
                    ][Tname]["value"]
                else:
                    temp_file = (
                        self.cfg_path.split("TrigMaker_cfg.py")[0]
                        + "trigger/"
                        + self.Trigger[self.era][RunP]["DZEffMC"][Tname][Key]
                    )
                    if ".txt" in temp_file:
                        temp_file = temp_file.split(".txt")[0] + ".json"
                    elif ".json" not in temp_file:
                        print("The following file is not supported")
                        print(temp_file)
                    self.TM_DZEffMC[RunP][Tname]["file"] = temp_file

            for Tname in self.Trigger[self.era][RunP]["GlEff"]:
                self.TM_GlEff[RunP][Tname] = []
                self.TM_GlEff[RunP][Tname].append(
                    self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                )
                self.TM_GlEff[RunP][Tname].append(
                    self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                    - self.Trigger[self.era][RunP]["GlEff"][Tname][1]
                )
                self.TM_GlEff[RunP][Tname].append(
                    min(
                        1.0,
                        self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                        + self.Trigger[self.era][RunP]["GlEff"][Tname][1],
                    )
                )
                # In the following we append the same content of the previous 2 lines, it is just a trick to handle stat and syst components later on
                self.TM_GlEff[RunP][Tname].append(
                    self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                    - self.Trigger[self.era][RunP]["GlEff"][Tname][1]
                )
                self.TM_GlEff[RunP][Tname].append(
                    min(
                        1.0,
                        self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                        + self.Trigger[self.era][RunP]["GlEff"][Tname][1],
                    )
                )
                self.TM_GlEff[RunP][Tname].append(
                    self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                    - self.Trigger[self.era][RunP]["GlEff"][Tname][1]
                )
                self.TM_GlEff[RunP][Tname].append(
                    min(
                        1.0,
                        self.Trigger[self.era][RunP]["GlEff"][Tname][0]
                        + self.Trigger[self.era][RunP]["GlEff"][Tname][1],
                    )
                )

            for Tname in self.Trigger[self.era][RunP]["DRllSF"]:
                self.TM_DRllSF[RunP][Tname] = []
                temp_file = (
                    self.cfg_path.split("TrigMaker_cfg.py")[0]
                    + "trigger/"
                    + self.Trigger[self.era][RunP]["DRllSF"][Tname]
                )
                if ".txt" in temp_file:
                    temp_file = temp_file.split(".txt")[0] + ".json"
                elif ".json" not in temp_file:
                    print("The following file is not supported")
                    print(temp_file)
                self.TM_DRllSF[RunP][Tname] = temp_file

        # Set some run/event specific var
        self.TM_runPeriods.sort()
        self.total_lum = 0.0
        for RunP in self.Trigger[self.era]:
            self.total_lum += self.Trigger[self.era][RunP]["lumi"]

        self.RunFrac = [0.0]
        for RunP in self.Trigger[self.era]:
            self.RunFrac.append(
                self.RunFrac[-1] + self.Trigger[self.era][RunP]["lumi"] / self.total_lum
            )

        if self.keepRunP:
            self.run_p = "run_period"

    def runModule(self, df, values):
        if self.seeded:
            toss_coin = "TRandom3(event).Uniform()"
        else:
            toss_coin = "gRandom->Rndm()"

        ####
        #### Define run_period as implemented in TrigMaker_cfg.py
        ####
        #### For DATA : Check runs
        #### For MC   : Use random numbers and the fraction of the total lumi covered by each run
        ####

        if not self.keepRunP:
            if self.isData:
                run_p_interprate = """"""
                for RunP in self.TM_runInt:
                    begin = str(self.TM_runInt[RunP]["b"])
                    end = str(self.TM_runInt[RunP]["e"])
                    RunP_tmp = str(RunP)

                    run_p_interprate = (
                        run_p_interprate
                        + """
                    if(run>"""
                        + begin
                        + """ && run<="""
                        + end
                        + """){run_period = """
                        + RunP_tmp
                        + """;}
                    """
                    )

                ROOT.gInterpreter.Declare(
                    """
                    int run_p(int run){
                        int run_period = 0;
                        """
                    + run_p_interprate
                    + """
                        return run_period;
                    }
                    """
                )

                df = df.Define("run_p", "run_p(run)")

            else:
                run_p_interprate = """"""
                for iPeriod in range(1, len(self.RunFrac)):
                    begin = str(self.RunFrac[iPeriod - 1])
                    end = str(self.RunFrac[iPeriod])
                    RunP_tmp = str(self.TM_runPeriods[iPeriod - 1])

                    run_p_interprate = (
                        run_p_interprate
                        + """                                                                                                                                             
                    if(toss>="""
                        + begin
                        + """ && toss<"""
                        + end
                        + """){run_period = """
                        + RunP_tmp
                        + """;}                                                                                                                           
                    """
                    )

                ROOT.gInterpreter.Declare(
                    """
                    double run_p(int event){
                        int run_period = 0;
                        double toss;
                        toss = """
                    + toss_coin
                    + """;
                        """
                    + run_p_interprate
                    + """
                        if (toss==1.0){
                                run_period = """
                    + str(self.TM_runPeriods[len(self.RunFrac) - 2])
                    + """;
                        }
                        return run_period;
                    }
                    """
                )
                
                df = df.Define("run_p", "run_p(event)")

        ########################################################################
        #                                                                      #
        #                                                                      #
        #                      DATA LEPTON TRIGGERS                            #
        #                                                                      #
        #                                                                      #
        ########################################################################

        cond = {}
        for RunP in self.TM_trig:
            cond[RunP] = {}
            for Tname in self.TM_trig[RunP]:
                condition = " || ".join(self.TM_trig[RunP][Tname])
                cond[RunP][Tname] = condition

        for name in self.NewVar["I"]:
            tname = None

            if "Trigger_sngEl" in name:
                tname = "SingleEle"
            elif "Trigger_sngMu" in name:
                tname = "SingleMu"
            elif "Trigger_dblEl" in name:
                tname = "DoubleEle"
            elif "Trigger_dblMu" in name:
                tname = "DoubleMu"
            elif "Trigger_ElMu" in name:
                tname = "EleMu"

            if tname != None:
                condition = " || ".join(
                    [
                        "(run_p==" + str(RunP) + " && (" + cond[RunP][tname] + "))"
                        for RunP in cond.keys()
                    ]
                )

                df = df.Define(name, condition)

            else:
                if "run_period" in name and not self.keepRunP:
                    df = df.Define(name, "run_p")
        
        if self.isData or (self.computeSF==False):
            df = df.DropColumns("run_p")
            return df
        
        ########################################################################
        #                                                                      #
        #                                                                      #
        #                      DO 1 LEPTON TRIGGERS                            #
        #                                                                      #
        #                                                                      #
        ########################################################################

        ####
        #### Get Leg efficiencies   :   Load and read json files for each trigger and legs, for MC and Data
        ####
        #### Then, assign correctionlib reference as a function of the run_period and trigger name
        ####
        #### Output  :  1-D array of length 7  [nominal, down, up, down_stat, up_stat, down_syst, up_syst]

        interpret_data = """"""
        for RunP in self.TM_LegEffData:
            for Tname in self.TM_LegEffData[RunP]:
                if not os.path.exists(self.TM_LegEffData[RunP][Tname]):
                    print("Json file not found: " + self.TM_LegEffData[RunP][Tname])

                ROOT.gROOT.ProcessLine(
                    f""" 
                    auto cset_file_leg_Data_{Tname}_{RunP} = correction::CorrectionSet::from_file("{self.TM_LegEffData[RunP][Tname]}"); 
                    """
                )
                ROOT.gROOT.ProcessLine(
                    f"""
                    correction::Correction::Ref cset_eff_leg_Data_{Tname}_{RunP} = (correction::Correction::Ref) cset_file_leg_Data_{Tname}_{RunP}->at("TriggerEff");
                    """
                )
                interpret_data = (
                    interpret_data
                    + """
                if (isData && singleLeg=="%s" && run_period==%s){cset_eff = cset_eff_leg_Data_%s_%s;} 
                """
                    % (Tname, RunP, Tname, RunP)
                )

        interpret_mc = """"""
        for RunP in self.TM_LegEffMC:
            for Tname in self.TM_LegEffMC[RunP]:
                if not os.path.exists(self.TM_LegEffMC[RunP][Tname]):
                    print("Json file not found: " + self.TM_LegEffData[RunP][Tname])

                ROOT.gROOT.ProcessLine(
                    f"""
                    auto cset_file_leg_MC_{Tname}_{RunP} = correction::CorrectionSet::from_file("{self.TM_LegEffMC[RunP][Tname]}");
                """
                )

                ROOT.gROOT.ProcessLine(
                    f"""
                    correction::Correction::Ref cset_eff_leg_MC_{Tname}_{RunP} = (correction::Correction::Ref) cset_file_leg_MC_{Tname}_{RunP}->at("TriggerEff");
                """
                )
                interpret_mc = (
                    interpret_mc
                    + """
                if (!isData && singleLeg=="%s" && run_period==%s){cset_eff = cset_eff_leg_MC_%s_%s;}
                """
                    % (Tname, RunP, Tname, RunP)
                )

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_LegEff(float pt_l1, float eta_l1, int run_period, string singleLeg, bool isData){

                float eff;
                float eff_d;
                float eff_u;

                float eff_d_stat;
                float eff_u_stat;
                float eff_d_syst;
                float eff_u_syst;

                ROOT::RVecF leg_eff(7, 0.0);

                correction::Correction::Ref cset_eff;

                """
            + interpret_data
            + """
                """
            + interpret_mc
            + """
                
                eff = round( 10000 * cset_eff->evaluate({eta_l1, pt_l1, "nominal"})) / 10000.0;
                eff_d_stat = round( 10000 * cset_eff->evaluate({eta_l1, pt_l1, "stat_down"})) / 10000.0;
                eff_u_stat = round( 10000 * cset_eff->evaluate({eta_l1, pt_l1, "stat_up"})) / 10000.0;
                eff_d_syst = round( 10000 * cset_eff->evaluate({eta_l1, pt_l1, "syst_down"})) / 10000.0;
                eff_u_syst = round( 10000 * cset_eff->evaluate({eta_l1, pt_l1, "syst_up"})) / 10000.0;

                leg_eff[0] = eff;
                leg_eff[3] = ROOT::VecOps::Max(ROOT::RVecF{0.0, eff - eff_d_stat});
                leg_eff[4] = ROOT::VecOps::Min(ROOT::RVecF{1.0, eff + eff_u_stat});
                leg_eff[5] = ROOT::VecOps::Max(ROOT::RVecF{0.0, eff - eff_d_syst});
                leg_eff[6] = ROOT::VecOps::Min(ROOT::RVecF{1.0, eff + eff_u_syst});

                leg_eff[1] = ROOT::VecOps::Max(ROOT::RVecF{0.0, eff - eff * sqrt((eff_d_stat/eff)*(eff_d_stat/eff) + (eff_d_syst/eff)*(eff_d_syst/eff))});
                leg_eff[2] = ROOT::VecOps::Min(ROOT::RVecF{1.0, eff + eff * sqrt((eff_u_stat/eff)*(eff_u_stat/eff) + (eff_u_syst/eff)*(eff_u_syst/eff))});  
                
                return leg_eff;
            }
            """
        )

        ###
        ### Define trigger emulator for MC : By default as false
        ###

        df = df.Define(
            "Trig_emu", "ROOT::RVecB{false, false, false, false, false, false}"
        )

        ###
        ### Access global efficiencies for SingleLepton triggers
        ### Output : 1-D array [nom, down, up] with the hardcoded values
        ###

        interpret = """"""
        for leg in ["Mu", "Ele"]:
            for RunP in self.TM_GlEff:
                if leg == "Mu":
                    effgl1 = self.TM_GlEff[RunP]["SingleMu"][0]
                    effgl2 = self.TM_GlEff[RunP]["SingleMu"][1]
                    effgl3 = self.TM_GlEff[RunP]["SingleMu"][2]

                    interpret = (
                        interpret
                        + f"""                                                                                                                                                                                                                             
                    if (singleLeg=="SingleMu" && run_period=="""
                        + str(RunP)
                        + """){
                        gl_eff_1 = """
                        + str(effgl1)
                        + """;
                        gl_eff_2 = """
                        + str(effgl2)
                        + """;
                        gl_eff_3 = """
                        + str(effgl3)
                        + """;
                    }
                    """
                    )

                if leg == "Ele":
                    effgl1 = self.TM_GlEff[RunP]["SingleEle"][0]
                    effgl2 = self.TM_GlEff[RunP]["SingleEle"][1]
                    effgl3 = self.TM_GlEff[RunP]["SingleEle"][2]

                    interpret = (
                        interpret
                        + """                                                                                                                                                                                                                             
                    if (singleLeg=="SingleEle" && run_period=="""
                        + str(RunP)
                        + """){                                                                                                                                                                                            
                        gl_eff_1 = """
                        + str(effgl1)
                        + """;                                                                                                                                                                                                                      
                        gl_eff_2 = """
                        + str(effgl2)
                        + """;                                                                                                                                                                                                                      
                        gl_eff_3 = """
                        + str(effgl3)
                        + """;                                                                                                                                                                                                                      
                    }                                                                                                                                                                                                                                                        
                    """
                    )

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_glEff(int run_period, string singleLeg){

                ROOT::RVecF gl_eff(3, 1.0);
                float gl_eff_1 = 1.0;
                float gl_eff_2 = 1.0;
                float gl_eff_3 = 1.0;

                """
            + interpret
            + """

                gl_eff[0] = gl_eff_1;
                gl_eff[1] = gl_eff_2;
                gl_eff[2] = gl_eff_3;

                return gl_eff;
            }
            """
        )

        ####
        ####  Compute SFs and uncertainties
        ####

        ROOT.gInterpreter.Declare(
            """
            float get_sf(float num, float den){
                if (den==0.0){
                    return 0.0;
                }else{
                    return num / den;
                }
            }
            """
        )

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_sf_unc(ROOT::RVecF eff_data, ROOT::RVecF eff_mc){

                ROOT::RVecF sf_unc(2, 0.0);

                if (eff_data[0]==0.0 || eff_mc[0]==0.0){
                    return sf_unc;
                }
                
                float SF_stat_d = sqrt( (abs(eff_data[3] - eff_data[0])/eff_data[0])*(abs(eff_data[3] - eff_data[0])/eff_data[0]) + (abs(eff_mc[3]-eff_mc[0])/eff_mc[0])*(abs(eff_mc[3]-eff_mc[0])/eff_mc[0]) )*eff_data[0]/eff_mc[0];
                float SF_stat_u = sqrt( (abs(eff_data[4] - eff_data[0])/eff_data[0])*(abs(eff_data[4] - eff_data[0])/eff_data[0]) + (abs(eff_mc[4]-eff_mc[0])/eff_mc[0])*(abs(eff_mc[4]-eff_mc[0])/eff_mc[0]) )*eff_data[0]/eff_mc[0];
                
                float SF_syst_d = 0.0;
                float SF_syst_u = 0.0;

                if (eff_mc[5]!=0.0){
                        SF_syst_d = eff_data[5]/eff_mc[5];
                }

                if (eff_mc[6]!=0.0){
                        SF_syst_u = eff_data[6]/eff_mc[6];
                }

                sf_unc[0] = sqrt(SF_stat_d*SF_stat_d + SF_syst_d*SF_syst_d);
                sf_unc[1] = sqrt(SF_stat_u*SF_stat_u + SF_syst_u*SF_syst_u);
                
                return sf_unc;
            }
            """
        )

        ####
        #### Compute Single Lepton efficiencies
        ####
        #### Output : 1-D array of length 30
        ####
        ####          * eff_data            From [0, 1, 2, 3, 4, 5, 6] : Data efficiencies for Single Lepton triggers [nominal, down, up, down_stat, up_stat, down_syst, up_syst]
        ####          * effData_evt_v       From [7, 8, 9, 10, 11]     : Per trigger data efficiencies ['sinEl', 'sinMu', 'doubleEl', 'doubleMu', 'ElMu']
        ####          * sf_v                From [12, 13, 14]          : Trigger scale factors
        ####          * sf_evt_v            From [15, 16, 17, 18, 19]  : Per trigger scale factors     ['sinEl', 'sinMu', 'doubleEl', 'doubleMu', 'ElMu']
        ####          * sf_evt_v_d          From [20, 21, 22, 23, 24]  : Down scale factor uncertainty
        ####          * sf_evt_v_u          From [25, 26, 27, 28, 29]  : Up scale factor uncertainty

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF getEff_l1(float pt, float eta, int id, int run_period){

                double pt_l1;
                double eta_l1;
                string singleLeg;

                ROOT::RVecF result(30, 0.0);
                ROOT::RVecF eff_data(7, 0.0);
                ROOT::RVecF eff_mc(7, 0.0);

                ROOT::RVecF sf_v(3, 0.0);
                ROOT::RVecF sf_v_unc;

                if (abs(id)==11){
                    singleLeg = "SingleEle";
                    pt_l1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{pt, """
            + str(self.el_maxPt)
            + """}), """
            + str(self.el_minPt)
            + """});
                    eta_l1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{eta, """
            + str(self.el_maxEta)
            + """}), """
            + str(self.el_minEta)
            + """});
                }else if (abs(id)==13){
                    singleLeg = "SingleMu";
                    pt_l1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{pt, """
            + str(self.mu_maxPt)
            + """}), """
            + str(self.mu_minPt)
            + """});
                    eta_l1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{eta, """
            + str(self.mu_maxEta)
            + """}), """
            + str(self.mu_minEta)
            + """});
                }else{
                    return result;
                }

                ROOT::RVecF leg_eff_data = get_LegEff(pt_l1, eta_l1, run_period, singleLeg, true);
                ROOT::RVecF leg_eff_mc = get_LegEff(pt_l1, eta_l1, run_period, singleLeg, false);
                
                ROOT::RVecF gl_eff(3, 0.0);
                gl_eff = get_glEff(run_period, singleLeg);
                
                eff_data[0] = leg_eff_data[0]*gl_eff[0]; // Nominal
                eff_data[1] = leg_eff_data[1]*gl_eff[1]; // down
                eff_data[2] = leg_eff_data[2]*gl_eff[2]; // up
                eff_data[3] = leg_eff_data[3]*gl_eff[1]; // down stat
                eff_data[4] = leg_eff_data[4]*gl_eff[2]; // up stat
                eff_data[5] = leg_eff_data[5]*gl_eff[1]; // down syst
                eff_data[6] = leg_eff_data[6]*gl_eff[2]; // up syst

                eff_mc[0] = leg_eff_mc[0]*gl_eff[0]; // Nominal
                eff_mc[1] = leg_eff_mc[1]*gl_eff[1]; // down
                eff_mc[2] = leg_eff_mc[2]*gl_eff[2]; // up
                eff_mc[3] = leg_eff_mc[3]*gl_eff[1]; // down stat
                eff_mc[4] = leg_eff_mc[4]*gl_eff[2]; // up stat
                eff_mc[5] = leg_eff_mc[5]*gl_eff[1]; // down syst
                eff_mc[6] = leg_eff_mc[6]*gl_eff[2]; // up syst

                sf_v[0] = get_sf(leg_eff_data[0], leg_eff_mc[0]);    
                sf_v_unc = get_sf_unc(eff_data, eff_mc);

                sf_v[1] = sf_v_unc[0];
                sf_v[2] = sf_v_unc[1];
                                
                // compute eff_evt_v 
                // eff_evt_v_map = ['sinEl', 'sinMu', 'doubleEl', 'doubleMu', 'ElMu']
                ROOT::RVecF effData_evt_v(5, 0.0);
                ROOT::RVecF effMC_evt_v(5, 0.0);
                ROOT::RVecF sf_evt_v(5, 0.0);
                ROOT::RVecF sf_evt_v_d(5, 0.0);
                ROOT::RVecF sf_evt_v_u(5, 0.0);
                
                if(abs(id)==11){
                    effData_evt_v[0] = leg_eff_data[0];
                    effMC_evt_v[0] = leg_eff_mc[0];
                    sf_evt_v[0] = get_sf(leg_eff_data[0], leg_eff_mc[0]);
                    ROOT::RVecF sf_evt_v_unc = get_sf_unc(leg_eff_data, leg_eff_mc);
                    sf_evt_v_d[0] = sf_evt_v_unc[0];
                    sf_evt_v_u[0] = sf_evt_v_unc[1];
                }
                if(abs(id)==13){
                    effData_evt_v[1] = leg_eff_data[0];
                    effMC_evt_v[1] = leg_eff_mc[0];
                    sf_evt_v[1] = get_sf(leg_eff_data[0], leg_eff_mc[0]);
                    ROOT::RVecF sf_evt_v_unc = get_sf_unc(leg_eff_data, leg_eff_mc);
                    sf_evt_v_d[1] = sf_evt_v_unc[0];
                    sf_evt_v_u[1] = sf_evt_v_unc[1];
                }


                result[0] = eff_data[0];
                result[1] = eff_data[1];
                result[2] = eff_data[2];
                result[3] = eff_data[3];
                result[4] = eff_data[4];
                result[5] = eff_data[5];
                result[6] = eff_data[6];

                result[7] = effData_evt_v[0];
                result[8] = effData_evt_v[1];
                result[9] = effData_evt_v[2];
                result[10] = effData_evt_v[3];
                result[11] = effData_evt_v[4];

                result[12] = sf_v[0];
                result[13] = sf_v[1];
                result[14] = sf_v[2];

                result[15] = sf_evt_v[0];
                result[16] = sf_evt_v[1];
                result[17] = sf_evt_v[2];
                result[18] = sf_evt_v[3];
                result[19] = sf_evt_v[4];

                result[20] = sf_evt_v_d[0];
                result[21] = sf_evt_v_d[1];
                result[22] = sf_evt_v_d[2];
                result[23] = sf_evt_v_d[3];
                result[24] = sf_evt_v_d[4];

                result[25] = sf_evt_v_u[0];
                result[26] = sf_evt_v_u[1];
                result[27] = sf_evt_v_u[2];
                result[28] = sf_evt_v_u[3];
                result[29] = sf_evt_v_u[4];

                return result;
            }
            """
        )

        df = df.Define("_1lepOk", "Lepton_pt.size() > 0")

        df = df.Define(
            "lep1_eff",
            "_1lepOk ? getEff_l1(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], run_p) : ROOT::RVecF(30, 0.0)",
        )

        ####
        #### Define MC trigger seeds for emulator   :   1-D array of length 8 with random numbers
        ####

        if self.seeded:
            event_seed = "event"
        else:
            event_seed = "-1"

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF getTrndm(int evt_seed){                
                ROOT::RVecF Trndm;
                for (int i=0; i<8; i++){
                        if (evt_seed!=-1){
                                if (i==0){
                                        Trndm.push_back(TRandom3(int(evt_seed*evt_seed)).Uniform());
                                }else{
                                    Trndm.push_back(TRandom3(int(10000*Trndm[i-1])).Uniform());
                                }
                        }else{
                            Trndm.push_back(gRandom->Rndm());
                        }
                    }
                return Trndm;
            }
            """
        )

        df = df.Define("Trndm", "getTrndm(" + event_seed + ")")

        ####
        #### Single Lepton trigger emulator   :   1-D boolean array
        ####
        #### Trig_emu emulator map: 'event' 'sinEl', 'sinMu', 'doubleEl', 'doubleMu', 'ElMu'

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecB Trig_emu_1lep(ROOT::RVecF Trndm, ROOT::RVecF lep1_eff, int lep_id){
                ROOT::RVecB Trig_emu_1lep(6, false);
                if (abs(lep_id)==11){
                        Trig_emu_1lep[1] = lep1_eff[7] > Trndm[0];
                }
                if (abs(lep_id)==13){
                        Trig_emu_1lep[2] = lep1_eff[7] > Trndm[1];
                }                
                Trig_emu_1lep[0] = Trig_emu_1lep[1] || Trig_emu_1lep[2] || Trig_emu_1lep[3] || Trig_emu_1lep[4] || Trig_emu_1lep[5];
                return Trig_emu_1lep;            
            }
            """
        )

        df = df.Redefine(
            "Trig_emu",
            "_1lepOk ? Trig_emu_1lep(Trndm, lep1_eff, Lepton_pdgId[0]) : Trig_emu",
        )

        ####
        #### Define output single lepton trigger variables
        ####

        for name in self.NewVar["F"]:
            if "TriggerEffWeight" in name:
                if "_1l" in name:
                    if "_1l_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[1] : 0.0")
                    elif "_1l_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[2] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[0] : 0.0")
                elif "_sngEl" in name:
                    df = df.Define(name, "_1lepOk ? lep1_eff[7] : 0.0")
                elif "_sngMu" in name:
                    df = df.Define(name, "_1lepOk ? lep1_eff[8] : 0.0")
                elif "_dblEl" in name:
                    df = df.Define(name, "_1lepOk ? lep1_eff[9] : 0.0")
                elif "_dblMu" in name:
                    df = df.Define(name, "_1lepOk ? lep1_eff[10] : 0.0")
                elif "_ElMu" in name:
                    df = df.Define(name, "_1lepOk ? lep1_eff[11] : 0.0")
            elif "TriggerSFWeight" in name:
                if "_1l" in name:
                    if "_1l_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[13] : 0.0")
                    elif "_1l_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[14] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[12] : 0.0")
                elif "_sngEl" in name:
                    if "_sngEl_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[20] : 0.0")
                    elif "_sngEl_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[25] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[15] : 0.0")
                elif "_sngMu" in name:
                    if "_sngMu_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[21] : 0.0")
                    elif "_sngMu_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[26] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[16] : 0.0")
                elif "_dblEl" in name:
                    if "_dblEl_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[22] : 0.0")
                    elif "_dblEl_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[27] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[17] : 0.0")
                elif "_dblMu" in name:
                    if "_dblMu_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[23] : 0.0")
                    elif "_dblMu_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[28] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[18] : 0.0")
                elif "_ElMu" in name:
                    if "_ElMu_d" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[24] : 0.0")
                    elif "_ElMu_u" in name:
                        df = df.Define(name, "_1lepOk ? lep1_eff[29] : 0.0")
                    else:
                        df = df.Define(name, "_1lepOk ? lep1_eff[19] : 0.0")

        ########################################################################
        #                                                                      #
        #                                                                      #
        #                      DO 2 LEPTON TRIGGERS                            #
        #                                                                      #
        #                                                                      #
        ########################################################################

        df = df.Define("_2lepOk", "Lepton_pt.size() > 1")

        ####
        #### Compute drll between 2 leptons
        ####

        ROOT.gInterpreter.Declare(
            """
            float _dRll(float pt1, float eta1, float phi1, float pt2, float eta2, float phi2){

                TLorentzVector L1;
                TLorentzVector L2;
                
                L1.SetPtEtaPhiM(pt1, eta1, phi1, 0.0);
                L2.SetPtEtaPhiM(pt2, eta2, phi2, 0.0);

                return L1.DeltaR(L2);
            }
            """
        )

        df = df.Define(
            "drll",
            "_2lepOk ? _dRll(Lepton_pt[0], Lepton_eta[0], Lepton_phi[0], Lepton_pt[1], Lepton_eta[1], Lepton_phi[1]) : -999.9",
        )

        ####
        #### Compute DZ efficiencies   :   run over run_period and decay mode, then check type and assign results
        ####                               The DZ efficiencies can be hardcoded as list of values, or measured in json files to be read with correctionlib
        ####
        ####                               In case of "nvtx" and "pt" as input type correctionlib is used. Otherwise, the values are directly parsed into c++ function
        ####                               Output : 1-D array with length 6 [nominal-DATA, down-DATA, up-DATA, nominal-MC, down-MC, up-MC]
        ####

        interpreter_DZ = """"""

        for RunP in self.TM_DZEffData:
            for Tname in self.TM_DZEffData[RunP]:
                if Tname == "DoubleMu":
                    code = 1313
                elif Tname == "DoubleEle":
                    code = 1111
                elif Tname == "MuEle":
                    code = 1311
                elif Tname == "EleMu":
                    code = 1113

                if self.TM_DZEffData[RunP][Tname]["type"] == "nvtx":
                    interpreter_DZ = (
                        interpreter_DZ
                        + """
                    if(code=="""
                        + str(code)
                        + """ && run=="""
                        + str(RunP)
                        + """ && isData){
                            if (nvtx>=70){nvtx_dz=69;}
                            float nvtx_tmp = (float)nvtx;
                            auto cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = correction::CorrectionSet::from_file("""
                        + str('"')
                        + self.TM_DZEffData[RunP][Tname]["file"]
                        + str('"')
                        + """);
                            correction::Correction::Ref cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->at("TriggerEff");
                            dz_eff = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({nvtx_tmp, "nominal"});
                            dz_eff_err = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({nvtx_tmp, "error"});
                    }
                    """
                    )
                elif "pt" in self.TM_DZEffData[RunP][Tname]["type"]:
                    interpreter_DZ = (
                        interpreter_DZ
                        + """
                    if(code=="""
                        + str(code)
                        + """ && run=="""
                        + str(RunP)
                        + """ && isData){
                            if (pt1>100){lep_pt1=99.9;}
                            if (pt2>100){lep_pt2=99.9;}
                            auto cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = correction::CorrectionSet::from_file("""
                        + str('"')
                        + self.TM_DZEffData[RunP][Tname]["file"]
                        + str('"')
                        + """);
                            correction::Correction::Ref cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->at("TriggerEff");
                            dz_eff = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({lep_pt1, lep_pt2, "nominal"});
                            dz_eff_err = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({lep_pt1, lep_pt2, "error"});
                    }
                    """
                    )
                elif self.TM_DZEffData[RunP][Tname]["type"] == "value":
                    interpreter_DZ = (
                        interpreter_DZ
                        + """
                    if(code=="""
                        + str(code)
                        + """ && run=="""
                        + str(RunP)
                        + """ && isData){
                            dz_eff = """
                        + str(self.TM_DZEffData[RunP][Tname]["vals"][0])
                        + """;
                            dz_eff_err = """
                        + str(self.TM_DZEffData[RunP][Tname]["vals"][1])
                        + """;
                    }
                    """
                    )

        for RunP in self.TM_DZEffMC:
            for Tname in self.TM_DZEffMC[RunP]:
                if Tname == "DoubleMu":
                    code = 1313
                elif Tname == "DoubleEle":
                    code = 1111
                elif Tname == "MuEle":
                    code = 1311
                elif Tname == "EleMu":
                    code = 1113

                if self.TM_DZEffMC[RunP][Tname]["type"] == "nvtx":
                    interpreter_DZ = (
                        interpreter_DZ
                        + """                                                                                                                                                                                                                    
                    if(code=="""
                        + str(code)
                        + """ && run=="""
                        + str(RunP)
                        + """ && !isData){                                                                                                                                                                                        
                            if (nvtx>=70){nvtx_dz=69;}                                                                                                                                                                                                                       
                            float nvtx_tmp = (float)nvtx;
                            auto cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = correction::CorrectionSet::from_file("""
                        + str('"')
                        + self.TM_DZEffMC[RunP][Tname]["file"]
                        + str('"')
                        + """);                                                                                        
                            correction::Correction::Ref cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->at("TriggerEff");                                                                                                   
                            dz_eff = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({nvtx_tmp, "nominal"});                                                                                                                                                   
                            dz_eff_err = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({nvtx_tmp, "error"});                                                                                                                                                 
                    }                                                                                                                                                                                                                                                        
                    """
                    )
                elif "pt" in self.TM_DZEffMC[RunP][Tname]["type"]:
                    interpreter_DZ = (
                        interpreter_DZ
                        + """                                                                                                                                                                                                                    
                    if(code=="""
                        + str(code)
                        + """ && run=="""
                        + str(RunP)
                        + """ && !isData){                                                                                                                                                                                        
                            if (pt1>100){lep_pt1=99.9;}                                                                                                                                                                                                                      
                            if (pt2>100){lep_pt2=99.9;}                                                                                                                                                                                                                      
                            auto cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = correction::CorrectionSet::from_file("""
                        + str('"')
                        + self.TM_DZEffMC[RunP][Tname]["file"]
                        + str('"')
                        + """);                                                                                       
                            correction::Correction::Ref cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """ = cset_dz_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->at("TriggerEff");                                                                                                   
                            dz_eff = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({lep_pt1, lep_pt2, "nominal"});                                                                                                                                       
                            dz_eff_err = cset_dz_eff_"""
                        + str(Tname)
                        + """_"""
                        + str(RunP)
                        + """->evaluate({lep_pt1, lep_pt2, "error"});                                                                                                                                     
                    }                                                                                                                                                                                                                                                        
                    """
                    )
                elif self.TM_DZEffMC[RunP][Tname]["type"] == "value":
                    interpreter_DZ = (
                        interpreter_DZ
                        + """
                    if(code=="""
                        + str(code)
                        + """ && run=="""
                        + str(RunP)
                        + """ && !isData){                                                                                                                                                                                        
                            dz_eff = """
                        + str(self.TM_DZEffMC[RunP][Tname]["vals"][0])
                        + """;                                                                                                                                                                                  
                            dz_eff_err = """
                        + str(self.TM_DZEffMC[RunP][Tname]["vals"][1])
                        + """;                                                                                                                                                                              
                    }                                                                                                                                                                                                                                                        
                    """
                    )

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_DZ(int run, int nvtx, float pt1, float pt2, int code, bool isData){
                
                ROOT::RVecF DZ_out(3, 0.0);
                float dz_eff = 0.0;
                float dz_eff_err = 0.0;
                int nvtx_dz = nvtx;
                float lep_pt1 = pt1;
                float lep_pt2 = pt2;

                """
            + interpreter_DZ
            + """

                DZ_out[0] = dz_eff;
                DZ_out[1] = dz_eff - dz_eff_err;
                DZ_out[2] = ROOT::VecOps::Min(ROOT::RVecF{1.0, dz_eff+dz_eff_err});
                
                return DZ_out;
            }
            """
        )

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_dz_eff(int id1, float lep_pt1, float lep_eta1, int id2, float lep_pt2, float lep_eta2, int nvtx, int run_period){

                double pt1, eta1;
                double pt2, eta2;

                if (abs(id1)==11){
                    pt1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt1, """
            + str(self.el_maxPt)
            + """}), """
            + str(self.el_minPt)
            + """});
                    eta1 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta1, """
            + str(self.el_maxEta)
            + """}), """
            + str(self.el_minEta)
            + """});
                }else{
                    pt1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt1, """
            + str(self.mu_maxPt)
            + """}), """
            + str(self.mu_minPt)
            + """});
                    eta1 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta1, """
            + str(self.mu_maxEta)
            + """}), """
            + str(self.mu_minEta)
            + """});
                }

                if (abs(id2)==11){
                    pt2 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt2, """
            + str(self.el_maxPt)
            + """}), """
            + str(self.el_minPt)
            + """});
                    eta2 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta2, """
            + str(self.el_maxEta)
            + """}), """
            + str(self.el_minEta)
            + """});
                }else{
                    pt2 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt2, """
            + str(self.mu_maxPt)
            + """}), """
            + str(self.mu_minPt)
            + """});
                    eta2 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta2, """
            + str(self.mu_maxEta)
            + """}), """
            + str(self.mu_minEta)
            + """});
                }

                ROOT::RVecF DZ_results(6, 0.0);                
                ROOT::RVecF dz_eff_mc(3, 0.0);
                ROOT::RVecF dz_eff_data(3, 0.0);
                int code;

                if (abs(id1)==11 && abs(id2)==11){
                    code = 1111;
                    dz_eff_mc = get_DZ(run_period, nvtx, pt1, pt2, code, false);
                    dz_eff_data = get_DZ(run_period, nvtx, pt1, pt2, code, true);
                }else if(abs(id1)==13 && abs(id2)==13){
                    code = 1313;
                    dz_eff_mc = get_DZ(run_period, nvtx, pt1, pt2, code, false);
                    dz_eff_data = get_DZ(run_period, nvtx, pt1, pt2, code, true);
                }else if(abs(id1)==11 && abs(id2)==13){
                    code = 1113;
                    dz_eff_mc = get_DZ(run_period, nvtx, pt1, pt2, code, false);
                    dz_eff_data = get_DZ(run_period, nvtx, pt1, pt2, code, true);
                }else{
                    code = 1311;
                    dz_eff_mc = get_DZ(run_period, nvtx, pt1, pt2, code, false);
                    dz_eff_data = get_DZ(run_period, nvtx, pt1, pt2, code, true);
                }
                    
                DZ_results[0] = dz_eff_data[0];
                DZ_results[1] = dz_eff_data[1];
                DZ_results[2] = dz_eff_data[2];
    
                DZ_results[3] = dz_eff_mc[0];
                DZ_results[4] = dz_eff_mc[1];
                DZ_results[5] = dz_eff_mc[2];

                return DZ_results;
            }
            """
        )

        ####
        #### Global efficiencies    :   The global efficiencies are hardcoded in the Triger dictionary. Then, loop over run_periods and decay modes and parse the values in c++ function
        ####
        #### Output   :   2-D array that contains [SingleLep1Eff, SingleLep2Eff, DoubleEff]
        ####                                       SingleLep1Eff = [eff, down, up, down, up, down, up]   Just a trick to compute later
        ####

        interpret_mumu = """"""
        interpret_eleele = """"""
        interpret_muele = """"""
        interpret_elemu = """"""
        for leg in ["MuMu", "EleEle", "MuEle, EleMu"]:
            for RunP in self.TM_GlEff:
                if leg == "MuMu":
                    effgl1 = self.TM_GlEff[RunP]["SingleMu"][0]
                    effgl2 = self.TM_GlEff[RunP]["SingleMu"][1]
                    effgl3 = self.TM_GlEff[RunP]["SingleMu"][2]
                    effgl4 = self.TM_GlEff[RunP]["SingleMu"][3]
                    effgl5 = self.TM_GlEff[RunP]["SingleMu"][4]
                    effgl6 = self.TM_GlEff[RunP]["SingleMu"][5]
                    effgl7 = self.TM_GlEff[RunP]["SingleMu"][6]

                    effgl1_dbl = self.TM_GlEff[RunP]["DoubleMu"][0]
                    effgl2_dbl = self.TM_GlEff[RunP]["DoubleMu"][1]
                    effgl3_dbl = self.TM_GlEff[RunP]["DoubleMu"][2]
                    effgl4_dbl = self.TM_GlEff[RunP]["DoubleMu"][3]
                    effgl5_dbl = self.TM_GlEff[RunP]["DoubleMu"][4]
                    effgl6_dbl = self.TM_GlEff[RunP]["DoubleMu"][5]
                    effgl7_dbl = self.TM_GlEff[RunP]["DoubleMu"][6]

                    interpret_mumu = (
                        interpret_mumu
                        + """                                                                                                                                                                                                                    
                    if (run_period=="""
                        + str(RunP)
                        + """){                                                                                                                                                                                                        
                        single_eff_gl = {"""
                        + str(effgl1)
                        + """, """
                        + str(effgl2)
                        + """, """
                        + str(effgl3)
                        + """, """
                        + str(effgl4)
                        + """, """
                        + str(effgl5)
                        + """, """
                        + str(effgl6)
                        + """, """
                        + str(effgl7)
                        + """};
                        double_eff_gl = {"""
                        + str(effgl1_dbl)
                        + """, """
                        + str(effgl2_dbl)
                        + """, """
                        + str(effgl3_dbl)
                        + """, """
                        + str(effgl4_dbl)
                        + """, """
                        + str(effgl5_dbl)
                        + """, """
                        + str(effgl6_dbl)
                        + """, """
                        + str(effgl7_dbl)
                        + """};  
                        eff_gl[0] = single_eff_gl;
                        eff_gl[1] = single_eff_gl;    
                        eff_gl[2] = double_eff_gl;    
                    }                                                                                                                                                                                                                                                        
                    """
                    )

                if leg == "EleEle":
                    effgl1 = self.TM_GlEff[RunP]["SingleEle"][0]
                    effgl2 = self.TM_GlEff[RunP]["SingleEle"][1]
                    effgl3 = self.TM_GlEff[RunP]["SingleEle"][2]
                    effgl4 = self.TM_GlEff[RunP]["SingleEle"][3]
                    effgl5 = self.TM_GlEff[RunP]["SingleEle"][4]
                    effgl6 = self.TM_GlEff[RunP]["SingleEle"][5]
                    effgl7 = self.TM_GlEff[RunP]["SingleEle"][6]

                    effgl1_dbl = self.TM_GlEff[RunP]["DoubleEle"][0]
                    effgl2_dbl = self.TM_GlEff[RunP]["DoubleEle"][1]
                    effgl3_dbl = self.TM_GlEff[RunP]["DoubleEle"][2]
                    effgl4_dbl = self.TM_GlEff[RunP]["DoubleEle"][3]
                    effgl5_dbl = self.TM_GlEff[RunP]["DoubleEle"][4]
                    effgl6_dbl = self.TM_GlEff[RunP]["DoubleEle"][5]
                    effgl7_dbl = self.TM_GlEff[RunP]["DoubleEle"][6]

                    interpret_eleele = (
                        interpret_eleele
                        + """
                    if (run_period=="""
                        + str(RunP)
                        + """){
                        single_eff_gl = {"""
                        + str(effgl1)
                        + """, """
                        + str(effgl2)
                        + """, """
                        + str(effgl3)
                        + """, """
                        + str(effgl4)
                        + """, """
                        + str(effgl5)
                        + """, """
                        + str(effgl6)
                        + """, """
                        + str(effgl7)
                        + """};
                        double_eff_gl = {"""
                        + str(effgl1_dbl)
                        + """, """
                        + str(effgl2_dbl)
                        + """, """
                        + str(effgl3_dbl)
                        + """, """
                        + str(effgl4_dbl)
                        + """, """
                        + str(effgl5_dbl)
                        + """, """
                        + str(effgl6_dbl)
                        + """, """
                        + str(effgl7_dbl)
                        + """};
                        eff_gl[0] = single_eff_gl;
                        eff_gl[1] = single_eff_gl;
                        eff_gl[2] = double_eff_gl;
                    }
                    """
                    )

                if leg == "MuEle":
                    effgl1 = self.TM_GlEff[RunP]["SingleMu"][0]
                    effgl2 = self.TM_GlEff[RunP]["SingleMu"][1]
                    effgl3 = self.TM_GlEff[RunP]["SingleMu"][2]
                    effgl4 = self.TM_GlEff[RunP]["SingleMu"][3]
                    effgl5 = self.TM_GlEff[RunP]["SingleMu"][4]
                    effgl6 = self.TM_GlEff[RunP]["SingleMu"][5]
                    effgl7 = self.TM_GlEff[RunP]["SingleMu"][6]

                    effgl1_ele = self.TM_GlEff[RunP]["SingleEle"][0]
                    effgl2_ele = self.TM_GlEff[RunP]["SingleEle"][1]
                    effgl3_ele = self.TM_GlEff[RunP]["SingleEle"][2]
                    effgl4_ele = self.TM_GlEff[RunP]["SingleEle"][3]
                    effgl5_ele = self.TM_GlEff[RunP]["SingleEle"][4]
                    effgl6_ele = self.TM_GlEff[RunP]["SingleEle"][5]
                    effgl7_ele = self.TM_GlEff[RunP]["SingleEle"][6]

                    effgl1_dbl = self.TM_GlEff[RunP]["MuEle"][0]
                    effgl2_dbl = self.TM_GlEff[RunP]["MuEle"][1]
                    effgl3_dbl = self.TM_GlEff[RunP]["MuEle"][2]
                    effgl4_dbl = self.TM_GlEff[RunP]["MuEle"][3]
                    effgl5_dbl = self.TM_GlEff[RunP]["MuEle"][4]
                    effgl6_dbl = self.TM_GlEff[RunP]["MuEle"][5]
                    effgl7_dbl = self.TM_GlEff[RunP]["MuEle"][6]

                    interpret_muele = (
                        interpret_muele
                        + """
                    if (run_period=="""
                        + str(RunP)
                        + """){
                        single_eff_gl = {"""
                        + str(effgl1)
                        + """, """
                        + str(effgl2)
                        + """, """
                        + str(effgl3)
                        + """, """
                        + str(effgl4)
                        + """, """
                        + str(effgl5)
                        + """, """
                        + str(effgl6)
                        + """, """
                        + str(effgl7)
                        + """};
                        single_eff_gl_ele = {"""
                        + str(effgl1_ele)
                        + """, """
                        + str(effgl2_ele)
                        + """, """
                        + str(effgl3_ele)
                        + """, """
                        + str(effgl4_ele)
                        + """, """
                        + str(effgl5_ele)
                        + """, """
                        + str(effgl6_ele)
                        + """, """
                        + str(effgl7_ele)
                        + """};
                        double_eff_gl = {"""
                        + str(effgl1_dbl)
                        + """, """
                        + str(effgl2_dbl)
                        + """, """
                        + str(effgl3_dbl)
                        + """, """
                        + str(effgl4_dbl)
                        + """, """
                        + str(effgl5_dbl)
                        + """, """
                        + str(effgl6_dbl)
                        + """, """
                        + str(effgl7_dbl)
                        + """};
                        eff_gl[0] = single_eff_gl;
                        eff_gl[1] = single_eff_gl_ele;
                        eff_gl[2] = double_eff_gl;
                    }
                    """
                    )

                if leg == "EleMu":
                    effgl1 = self.TM_GlEff[RunP]["SingleMu"][0]
                    effgl2 = self.TM_GlEff[RunP]["SingleMu"][1]
                    effgl3 = self.TM_GlEff[RunP]["SingleMu"][2]
                    effgl4 = self.TM_GlEff[RunP]["SingleMu"][3]
                    effgl5 = self.TM_GlEff[RunP]["SingleMu"][4]
                    effgl6 = self.TM_GlEff[RunP]["SingleMu"][5]
                    effgl7 = self.TM_GlEff[RunP]["SingleMu"][6]

                    effgl1_ele = self.TM_GlEff[RunP]["SingleEle"][0]
                    effgl2_ele = self.TM_GlEff[RunP]["SingleEle"][1]
                    effgl3_ele = self.TM_GlEff[RunP]["SingleEle"][2]
                    effgl4_ele = self.TM_GlEff[RunP]["SingleEle"][3]
                    effgl5_ele = self.TM_GlEff[RunP]["SingleEle"][4]
                    effgl6_ele = self.TM_GlEff[RunP]["SingleEle"][5]
                    effgl7_ele = self.TM_GlEff[RunP]["SingleEle"][6]

                    effgl1_dbl = self.TM_GlEff[RunP]["EleMu"][0]
                    effgl2_dbl = self.TM_GlEff[RunP]["EleMu"][1]
                    effgl3_dbl = self.TM_GlEff[RunP]["EleMu"][2]
                    effgl4_dbl = self.TM_GlEff[RunP]["EleMu"][3]
                    effgl5_dbl = self.TM_GlEff[RunP]["EleMu"][4]
                    effgl6_dbl = self.TM_GlEff[RunP]["EleMu"][5]
                    effgl7_dbl = self.TM_GlEff[RunP]["EleMu"][6]

                    interpret_elemu = (
                        interpret_elemu
                        + """
                    if (run_period=="""
                        + str(RunP)
                        + """){
                        single_eff_gl = {"""
                        + str(effgl1)
                        + """, """
                        + str(effgl2)
                        + """, """
                        + str(effgl3)
                        + """, """
                        + str(effgl4)
                        + """, """
                        + str(effgl5)
                        + """, """
                        + str(effgl6)
                        + """, """
                        + str(effgl7)
                        + """};
                        single_eff_gl_ele = {"""
                        + str(effgl1_ele)
                        + """, """
                        + str(effgl2_ele)
                        + """, """
                        + str(effgl3_ele)
                        + """, """
                        + str(effgl4_ele)
                        + """, """
                        + str(effgl5_ele)
                        + """, """
                        + str(effgl6_ele)
                        + """, """
                        + str(effgl7_ele)
                        + """};
                        double_eff_gl = {"""
                        + str(effgl1_dbl)
                        + """, """
                        + str(effgl2_dbl)
                        + """, """
                        + str(effgl3_dbl)
                        + """, """
                        + str(effgl4_dbl)
                        + """, """
                        + str(effgl5_dbl)
                        + """, """
                        + str(effgl6_dbl)
                        + """, """
                        + str(effgl7_dbl)
                        + """};
                        eff_gl[0] = single_eff_gl_ele;
                        eff_gl[1] = single_eff_gl;
                        eff_gl[2] = double_eff_gl;
                    }
                    """
                    )

        ROOT.gInterpreter.Declare(
            """
            std::vector<ROOT::RVecF> get_gl_eff(int id1, int id2, int run_period){

                std::vector<ROOT::RVecF> eff_gl = {ROOT::RVecF(7, 1.0), ROOT::RVecF(7, 1.0), ROOT::RVecF(7, 1.0)};

                ROOT::RVecF single_eff_gl(7, 1.0);
                ROOT::RVecF single_eff_gl_ele(7, 1.0);
                ROOT::RVecF double_eff_gl(7, 1.0);

                if (abs(id1)==11 && abs(id2)==11){
                    """
            + interpret_eleele
            + """
                }else if(abs(id1)==13 && abs(id2)==13){
                    """
            + interpret_mumu
            + """
                }else if(abs(id1)==11 && abs(id2)==13){
                    """
            + interpret_elemu
            + """
                }else{
                    """
            + interpret_muele
            + """
                }

                return eff_gl;
            }
            """
        )

        ####
        ####  DRll scale factors    :    Evaluate the scale factors from json files with correctionlib
        ####
        ####  Output    :    float
        ####

        interpret_drll = """"""
        for RunP in self.TM_DRllSF:
            for Tname in self.TM_DRllSF[RunP]:
                ROOT.gROOT.ProcessLine(
                    f"""                                                                                                                                                                                                                                                         
                    auto cset_file_drll_{Tname}_{RunP} = correction::CorrectionSet::from_file("{self.TM_DRllSF[RunP][Tname]}");                                                                                                                                              
                """
                )

                ROOT.gROOT.ProcessLine(
                    f"""                                                                                                                                                                                                                                                         
                    correction::Correction::Ref cset_sf_drll_{Tname}_{RunP} = (correction::Correction::Ref) cset_file_drll_{Tname}_{RunP}->at("TriggerEff");                                                                                                            
                """
                )
                interpret_drll = (
                    interpret_drll
                    + """
                if (singleLeg=="%s" && run_period==%s){cset_drll = cset_sf_drll_%s_%s;}
                """
                    % (Tname, RunP, Tname, RunP)
                )

        ROOT.gInterpreter.Declare(
            """
            float drll_sf(int id1, int id2, float drll, int run_period){
                
                float SF_dRll = 1.0;
                string singleLeg;
                correction::Correction::Ref cset_drll;

                if (abs(id1)==11 && abs(id2)==11){  
                    singleLeg = "DoubleEle";
                }else if(abs(id1)==13 && abs(id2)==13){
                    singleLeg = "DoubleMu";
                }else if(abs(id1)==11 && abs(id2)==13){ 
                    singleLeg = "EleMu";
                }else{ 
                    singleLeg = "MuEle";
                }

                """
            + interpret_drll
            + """

                SF_dRll = cset_drll->evaluate({drll, "nominal"});

                return SF_dRll;
            }
            """
        )

        ####
        ####  Leg efficiencies    :    The efficiencies from trigger legs are saved as json files to be read with correctionlib
        ####
        ####  Output   :   2-D array that contains the efficiency mapping [SingleLep1, SingleLep2, DoubleLeg1Lep1, DoubleLeg1Lep2, DoubleLeg2Lep1, DoubleLeg2Lep2]
        ####               Each category contains an array with [nominal, down, up, down_stat, up_stat, down_syst, up_syst]
        ####

        ROOT.gInterpreter.Declare(
            """
            std::vector<ROOT::RVecF> get_eff(int id1, float lep_pt1, float lep_eta1, int id2, float lep_pt2, float lep_eta2, int run_period, bool isData){

                std::vector<ROOT::RVecF> leg_eff;

                float pt1, eta1;
                float pt2, eta2;

                if (abs(id1)==11){
                    pt1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt1, """
            + str(self.el_maxPt)
            + """}), """
            + str(self.el_minPt)
            + """});
                    eta1 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta1, """
            + str(self.el_maxEta)
            + """}), """
            + str(self.el_minEta)
            + """});
                }else{
                    pt1 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt1, """
            + str(self.mu_maxPt)
            + """}), """
            + str(self.mu_minPt)
            + """});
                    eta1 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta1, """
            + str(self.mu_maxEta)
            + """}), """
            + str(self.mu_minEta)
            + """});
                }

                if (abs(id2)==11){
                    pt2 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt2, """
            + str(self.el_maxPt)
            + """}), """
            + str(self.el_minPt)
            + """});
                    eta2 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta2, """
            + str(self.el_maxEta)
            + """}), """
            + str(self.el_minEta)
            + """});
                }else{
                    pt2 = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_pt2, """
            + str(self.mu_maxPt)
            + """}), """
            + str(self.mu_minPt)
            + """});
                    eta2 =ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{lep_eta2, """
            + str(self.mu_maxEta)
            + """}), """
            + str(self.mu_minEta)
            + """});
                }
                
                ROOT::RVecF eff_sng_l1;
                ROOT::RVecF eff_sng_l2;
                ROOT::RVecF eff_dbl1_l1;
                ROOT::RVecF eff_dbl1_l2;
                ROOT::RVecF eff_dbl2_l1;
                ROOT::RVecF eff_dbl2_l2;

                if(abs(id1)==11 && abs(id2)==11){
                    eff_sng_l1 = get_LegEff(pt1, eta1, run_period, "SingleEle", isData);
                    eff_sng_l2 = get_LegEff(pt2, eta2, run_period, "SingleEle", isData);
                    eff_dbl1_l1 = get_LegEff(pt1, eta1, run_period, "DoubleEleLegHigPt", isData);
                    eff_dbl1_l2 = get_LegEff(pt2, eta2, run_period, "DoubleEleLegHigPt", isData);
                    eff_dbl2_l1 = get_LegEff(pt1, eta1, run_period, "DoubleEleLegLowPt", isData);
                    eff_dbl2_l2 = get_LegEff(pt2, eta2, run_period, "DoubleEleLegLowPt", isData);
                }else if(abs(id1)==13 && abs(id2)==13){
                    eff_sng_l1 = get_LegEff(pt1, eta1, run_period, "SingleMu", isData);
                    eff_sng_l2 = get_LegEff(pt2, eta2, run_period, "SingleMu", isData);
                    eff_dbl1_l1 = get_LegEff(pt1, eta1, run_period, "DoubleMuLegHigPt", isData);
                    eff_dbl1_l2 = get_LegEff(pt2, eta2, run_period, "DoubleMuLegHigPt", isData);
                    eff_dbl2_l1 = get_LegEff(pt1, eta1, run_period, "DoubleMuLegLowPt", isData);
                    eff_dbl2_l2 = get_LegEff(pt2, eta2, run_period, "DoubleMuLegLowPt", isData);
                }else if(abs(id1)==11 && abs(id2)==13){
                    eff_sng_l1 = get_LegEff(pt1, eta1, run_period, "SingleEle", isData);
                    eff_sng_l2 = get_LegEff(pt2, eta2, run_period, "SingleMu", isData);
                    eff_dbl1_l1 = get_LegEff(pt1, eta1, run_period, "EleMuLegHigPt", isData);
                    eff_dbl1_l2 = get_LegEff(pt2, eta2, run_period, "MuEleLegHigPt", isData);
                    eff_dbl2_l1 = get_LegEff(pt1, eta1, run_period, "MuEleLegLowPt", isData);
                    eff_dbl2_l2 = get_LegEff(pt2, eta2, run_period, "EleMuLegLowPt", isData);
                }else{
                    eff_sng_l1 = get_LegEff(pt1, eta1, run_period, "SingleMu", isData);
                    eff_sng_l2 = get_LegEff(pt2, eta2, run_period, "SingleEle", isData);
                    eff_dbl1_l1 = get_LegEff(pt1, eta1, run_period, "MuEleLegHigPt", isData);
                    eff_dbl1_l2 = get_LegEff(pt2, eta2, run_period, "EleMuLegHigPt", isData);
                    eff_dbl2_l1 = get_LegEff(pt1, eta1, run_period, "EleMuLegLowPt", isData);
                    eff_dbl2_l2 = get_LegEff(pt2, eta2, run_period, "MuEleLegLowPt", isData);
                }

                leg_eff.push_back(eff_sng_l1);
                leg_eff.push_back(eff_sng_l2);
                leg_eff.push_back(eff_dbl1_l1);
                leg_eff.push_back(eff_dbl1_l2);
                leg_eff.push_back(eff_dbl2_l1);
                leg_eff.push_back(eff_dbl2_l2);

                return leg_eff;
            }
            """
        )

        #### Define temporal efficiencies in dataframe

        df = df.Define(
            "leg_eff_mc",
            "_2lepOk ? get_eff(Lepton_pdgId[0],Lepton_pt[0],Lepton_eta[0],Lepton_pdgId[1],Lepton_pt[1],Lepton_eta[1],run_p,false) : std::vector{ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0)}",
        )

        df = df.Define(
            "leg_eff_data",
            "_2lepOk ? get_eff(Lepton_pdgId[0],Lepton_pt[0],Lepton_eta[0],Lepton_pdgId[1],Lepton_pt[1],Lepton_eta[1],run_p,true) : std::vector{ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0)}",
        )

        df = df.Define(
            "drll_SF",
            "_2lepOk ?  drll_sf(Lepton_pdgId[0], Lepton_pdgId[1], drll, run_p) : 0.0",
        )

        df = df.Define(
            "dz_eff",
            "_2lepOk ? get_dz_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], PV_npvsGood, run) : ROOT::RVecF(6, 0.0)",
        )

        df = df.Define(
            "gl_eff",
            "_2lepOk ? get_gl_eff(Lepton_pdgId[0], Lepton_pdgId[1], run) : std::vector{ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0),ROOT::RVecF(7, 0.0)}",
        )

        ####
        #### Compute event efficiencies : Combine leg, global, DRll and DZ Data and MC efficiencies to obtain per event scale factors
        ####

        #### Output : 1-D array with length 30 and the following structure

        #### From [0, 1, 2, 3, 4, 5, 6]  :  Data efficiencies                              [Nominal, down, up, down_stat, up_stat, down_syst, up_syst]
        #### From [7, 8, 9, 10, 11]      :  Data efficiencies per trigger mode             [SingleEl, SingleMu, DoubleEl, DoubleMu, EleMu]
        #### From [12, 13, 14]           :  Events scale factors
        #### From [15, 16, 17, 18, 19]   :  Scale factors per trigger mode                 [SingleEl, SingleMu, DoubleEl, DoubleMu, EleMu]
        #### From [20, 21, 22, 23, 24]   :  Down unc. for scale factor per trigger mode    [SingleEl, SingleMu, DoubleEl, DoubleMu, EleMu]
        #### From [25, 26, 27, 28, 29]   :  Up unc. for scale factor per trigger mode      [SingleEl, SingleMu, DoubleEl, DoubleMu, EleMu]

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_w(int id1, int id2, std::vector<ROOT::RVecF> effData, std::vector<ROOT::RVecF> effMC, ROOT::RVecF eff_dz, std::vector<ROOT::RVecF> eff_gl, float DRll_SF){

                ROOT::RVecF result(30, 0.0);                

                ROOT::RVecF effData_dz{eff_dz[0], eff_dz[1], eff_dz[2], eff_dz[1], eff_dz[2], eff_dz[0], eff_dz[0]}; // set to nom to avoid double counting when computing the tot SF uncertainty
                ROOT::RVecF effMC_dz{eff_dz[3], eff_dz[4], eff_dz[5], eff_dz[4], eff_dz[5], eff_dz[3], eff_dz[3]};

                // nom, tot_d, tot_u, stat_d, stat_u, syst_d, syst_u
                ROOT::RVecF effData_dbl(7, 0.0);
                ROOT::RVecF effData_sgl(7, 0.0);
                ROOT::RVecF effData_evt(7, 0.0);
                ROOT::RVecF effMC_dbl(7, 0.0);
                ROOT::RVecF effMC_sgl(7, 0.0);
                ROOT::RVecF effMC_evt(7, 0.0);

                // SFnom, SF_d, SF_u
                ROOT::RVecF SF_evt(3, 0.0);

                for (int i=0; i<7; i++){
                    effData_dbl[i] = ROOT::VecOps::Max(ROOT::RVecF{ (effData[4][i]*effData[3][i] + effData[2][i]*effData[5][i] - effData[3][i]*effData[2][i])*eff_gl[2][i]*effData_dz[i], 0.0001 });
                    effData_sgl[i] =  effData[0][i]*eff_gl[0][i]+effData[1][i]*eff_gl[1][i]-effData[0][i]*effData[1][i]*eff_gl[0][i]*eff_gl[1][i];
                    effData_evt[i] = (effData_dbl[i] + effData_sgl[i] - effData[5][i]*eff_gl[2][i]*effData[0][i]*eff_gl[0][i] - effData[4][i]*eff_gl[2][i]*effData[1][i]*eff_gl[1][i]*( 1 - effData[5][i]*eff_gl[2][i]*effData[0][i]*eff_gl[0][i]/effData_dbl[i] ))*DRll_SF;
                        
                    effMC_dbl[i] = ROOT::VecOps::Max(ROOT::RVecF{(effMC[4][i]*effMC[3][i] + effMC[2][i]*effMC[5][i] - effMC[3][i]*effMC[2][i])*eff_gl[2][i]*effMC_dz[i], 0.0001 });
                    effMC_sgl[i] =  effMC[0][i]*eff_gl[0][i]+effMC[1][i]*eff_gl[1][i]-effMC[0][i]*effMC[1][i]*eff_gl[0][i]*eff_gl[1][i];
                    effMC_evt[i] = (effMC_dbl[i] + effMC_sgl[i] - effMC[5][i]*eff_gl[2][i]*effMC[0][i]*eff_gl[0][i] - effMC[4][i]*eff_gl[2][i]*effMC[1][i]*eff_gl[1][i]*( 1 - effMC[5][i]*eff_gl[2][i]*effMC[0][i]*eff_gl[0][i]/effMC_dbl[i] ))*DRll_SF;                 
                }


                SF_evt[0] = get_sf(effData_evt[0], effMC_evt[0]);
                ROOT::RVecF SF_evt_unc = get_sf_unc(effData_evt, effMC_evt);
                SF_evt[1] = SF_evt_unc[0]; 
                SF_evt[2] = SF_evt_unc[1];


                // More specific event efficiencies (stored in a vector hence _v)
                // eff_evt_v_map = ['sinEl', 'sinMu', 'doubleEl', 'doubleMu', 'ElMu']

                ROOT::RVecF effData_evt_v(5, 0.0);
                ROOT::RVecF effMC_evt_v(5, 0.0);
                ROOT::RVecF SF_evt_v(5, 0.0);
                ROOT::RVecF SF_evt_v_d(5, 0.0);
                ROOT::RVecF SF_evt_v_u(5, 0.0);
                ROOT::RVecF effs_data(7, 0.0);
                ROOT::RVecF effs_mc(7, 0.0);


                if (abs(id1)==11 && abs(id2)==11){

                    // Single Lep 1
                    effData_evt_v[0] = (effData[0][0]*eff_gl[0][0] + (1 - effData[0][0]*eff_gl[0][0])*effData[1][0]*eff_gl[1][0])*DRll_SF;
                    effMC_evt_v[0] = (effMC[0][0]*eff_gl[0][0] + (1 - effMC[0][0]*eff_gl[0][0])*effMC[1][0]*eff_gl[1][0])*DRll_SF;
                    SF_evt_v[0] = get_sf(effData_evt_v[0], effMC_evt_v[0]);
                    effs_data[0] = effData_evt_v[0];
                    effs_mc[0] = effMC_evt_v[0];
                    
                    for (int i=1; i<7; i++){
                        effs_data[i] = effData[0][i]*eff_gl[0][i] + (1 - effData[0][i]*eff_gl[0][i])*effData[1][i]*eff_gl[1][i];
                        effs_mc[i] = effMC[0][i]*eff_gl[0][i] + (1 - effMC[0][i]*eff_gl[0][i])*effMC[1][i]*eff_gl[1][i];
                    }

                    SF_evt_v_d[0] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[0] = get_sf_unc(effs_data, effs_mc)[1];

                    // Double Lep
                    effData_evt_v[2] = (effData[4][0]*effData[3][0] + effData[2][0]*effData[5][0] - effData[3][0]*effData[2][0])*eff_gl[2][0]*effData_dz[0]*DRll_SF;
                    effMC_evt_v[2] = (effMC[4][0]*effMC[3][0] + effMC[2][0]*effMC[5][0] - effMC[3][0]*effMC[2][0])*eff_gl[2][0]*effMC_dz[0]*DRll_SF;

                    SF_evt_v[2] = get_sf(effData_evt_v[2], effMC_evt_v[2]);
                    effs_data[0] = effData_evt_v[2];
                    effs_mc[0] = effMC_evt_v[2];
                    for (int i=1; i<7; i++){
                        effs_data[i] = (effData[4][i]*effData[3][i] + effData[2][i]*effData[5][i] - effData[3][i]*effData[2][i])*eff_gl[2][i]*effData_dz[i]*DRll_SF;
                        effs_mc[i] = (effMC[4][i]*effMC[3][i] + effMC[2][i]*effMC[5][i] - effMC[3][i]*effMC[2][i])*eff_gl[2][i]*effMC_dz[i]*DRll_SF;
                    }

                    SF_evt_v_d[2] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[2] = get_sf_unc(effs_data, effs_mc)[1];                        

                }else if(abs(id1)==13 && abs(id2)==13){
                    
                    // Single Lep 1
                    effData_evt_v[1] = (effData[0][0]*eff_gl[0][0] + (1 - effData[0][0]*eff_gl[0][0])*effData[1][0]*eff_gl[1][0])*DRll_SF;
                    effMC_evt_v[1] = (effMC[0][0]*eff_gl[0][0] + (1 - effMC[0][0]*eff_gl[0][0])*effMC[1][0]*eff_gl[1][0])*DRll_SF;

                    SF_evt_v[1] = get_sf(effData_evt_v[1], effMC_evt_v[1]);
                    effs_data[0] = effData_evt_v[1];
                    effs_mc[0] = effMC_evt_v[1];
                    
                    for (int i=1; i<7; i++){
                        effs_data[i] = effData[0][i]*eff_gl[0][i] + (1 - effData[0][i]*eff_gl[0][i])*effData[1][i]*eff_gl[1][i];
                        effs_mc[i] = effMC[0][i]*eff_gl[0][i] + (1 - effMC[0][i]*eff_gl[0][i])*effMC[1][i]*eff_gl[1][i];
                    }

                    SF_evt_v_d[1] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[1] = get_sf_unc(effs_data, effs_mc)[1];

                    // Double Lep
                    effData_evt_v[3] = (effData[4][0]*effData[3][0] + effData[2][0]*effData[5][0] - effData[3][0]*effData[2][0])*eff_gl[2][0]*effData_dz[0]*DRll_SF;
                    effMC_evt_v[3] = (effMC[4][0]*effMC[3][0] + effMC[2][0]*effMC[5][0] - effMC[3][0]*effMC[2][0])*eff_gl[2][0]*effMC_dz[0]*DRll_SF;
                    
                    SF_evt_v[3] = get_sf(effData_evt_v[3], effMC_evt_v[3]);
                    effs_data[0] = effData_evt_v[3];
                    effs_mc[0] = effMC_evt_v[3];

                    for (int i=1; i<7; i++){
                        effs_data[i] = (effData[4][i]*effData[3][i] + effData[2][i]*effData[5][i] - effData[3][i]*effData[2][i])*eff_gl[2][i]*effData_dz[i]*DRll_SF;
                        effs_mc[i] = (effMC[4][i]*effMC[3][i] + effMC[2][i]*effMC[5][i] - effMC[3][i]*effMC[2][i])*eff_gl[2][i]*effMC_dz[i]*DRll_SF;
                    }

                    SF_evt_v_d[3] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[3] = get_sf_unc(effs_data, effs_mc)[1];

                }else if(abs(id1)==11 && abs(id2)==13){


                    // Single Lep 1 : Electron
                    effData_evt_v[0] = effData[0][0]*eff_gl[0][0]*DRll_SF;
                    effMC_evt_v[0] = effMC[0][0]*eff_gl[0][0]*DRll_SF;
                    
                    SF_evt_v[0] = get_sf(effData_evt_v[0], effMC_evt_v[0]);

                    effs_data[0] = effData_evt_v[0];
                    effs_mc[0] = effMC_evt_v[0];

                    for (int i=1; i<7; i++){
                        effs_data[i] = effData[0][i]*eff_gl[0][i];
                        effs_mc[i] = effMC[0][i]*eff_gl[0][i];
                    }
                    
                    SF_evt_v_d[0] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[0] = get_sf_unc(effs_data, effs_mc)[1];


                    // Single Lep 2 : Muon
                    effData_evt_v[1] = effData[1][0]*eff_gl[1][0]*DRll_SF;
                    effMC_evt_v[1] = effMC[1][0]*eff_gl[1][0]*DRll_SF;

                    SF_evt_v[1] = get_sf(effData_evt_v[1], effMC_evt_v[1]);

                    effs_data[0] = effData_evt_v[1];
                    effs_mc[0] = effMC_evt_v[1];

                    for (int i=1; i<7; i++){
                        effs_data[i] = effData[1][i]*eff_gl[1][i];
                        effs_mc[i] = effMC[1][i]*eff_gl[1][i];
                    }

                    SF_evt_v_d[1] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[1] = get_sf_unc(effs_data, effs_mc)[1];
                    

                    // Double lep
                    effData_evt_v[4]  = (effData[4][0]*effData[3][0] + effData[2][0]*effData[5][0] - effData[3][0]*effData[2][0])*eff_gl[2][0]*effData_dz[0]*DRll_SF;
                    effMC_evt_v[4]  = (effMC[4][0]*effMC[3][0] + effMC[2][0]*effMC[5][0] - effMC[3][0]*effMC[2][0])*eff_gl[2][0]*effMC_dz[0]*DRll_SF;
                    
                    SF_evt_v[4] = get_sf(effData_evt_v[4], effMC_evt_v[4]);

                    effs_data[0] = effData_evt_v[4];
                    effs_mc[0] = effMC_evt_v[4];

                    for (int i=1; i<7; i++){
                        effs_data[i] = (effData[4][i]*effData[3][i] + effData[2][i]*effData[5][i] - effData[3][i]*effData[2][i])*eff_gl[2][i]*effData_dz[i]*DRll_SF;
                        effs_data[i] = (effMC[4][i]*effMC[3][i] + effMC[2][i]*effMC[5][i] - effMC[3][i]*effMC[2][i])*eff_gl[2][i]*effMC_dz[i]*DRll_SF;
                    }

                    SF_evt_v_d[4] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[4] = get_sf_unc(effs_data, effs_mc)[1];

                }else{

                    // Single lep 1 : Electron
                    effData_evt_v[0] = effData[1][0]*eff_gl[1][0]*DRll_SF;
                    effMC_evt_v[0] = effMC[1][0]*eff_gl[1][0]*DRll_SF;

                    SF_evt_v[0] = get_sf(effData_evt_v[0], effMC_evt_v[0]);

                    effs_data[0] = effData_evt_v[0];
                    effs_mc[0] = effMC_evt_v[0];

                    for (int i=1; i<7; i++){
                        effs_data[i] = effData[1][i]*eff_gl[1][i];
                        effs_mc[i] = effMC[1][i]*eff_gl[1][i];
                    }

                    SF_evt_v_d[0] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[0] = get_sf_unc(effs_data, effs_mc)[1];
                    
                    
                    // Single lep 2 : Muon
                    effData_evt_v[1] = effData[0][0]*eff_gl[0][0]*DRll_SF;
                    effMC_evt_v[1] = effMC[0][0]*eff_gl[0][0]*DRll_SF;

                    SF_evt_v[1] = get_sf(effData_evt_v[1], effMC_evt_v[1]);
            
                    effs_data[0] = effData_evt_v[1];
                    effs_mc[0] = effMC_evt_v[1];
                    
                    for (int i=1; i<7; i++){
                        effs_data[i] = effData[0][i]*eff_gl[0][i];
                        effs_mc[i] = effMC[0][i]*eff_gl[0][i];                            
                    }

                    SF_evt_v_d[1] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[1] = get_sf_unc(effs_data, effs_mc)[1];

                    
                    // Double lep
                    effData_evt_v[4]  = (effData[4][0]*effData[3][0] + effData[2][0]*effData[5][0] - effData[3][0]*effData[2][0])*eff_gl[2][0]*effData_dz[0]*DRll_SF;
                    effMC_evt_v[4]  = (effMC[4][0]*effMC[3][0] + effMC[2][0]*effMC[5][0] - effMC[3][0]*effMC[2][0])*eff_gl[2][0]*effMC_dz[0]*DRll_SF;

                    SF_evt_v[4] = get_sf(effData_evt_v[4], effMC_evt_v[4]);

                    effs_data[0] = effData_evt_v[4];
                    effs_mc[0] = effMC_evt_v[4];

                    for (int i=1; i<7; i++){
                        effs_data[i] = (effData[4][i]*effData[3][i] + effData[2][i]*effData[5][i] - effData[3][i]*effData[2][i])*eff_gl[2][i]*effData_dz[i]*DRll_SF;
                        effs_mc[i] = (effMC[4][i]*effMC[3][i] + effMC[2][i]*effMC[5][i] - effMC[3][i]*effMC[2][i])*eff_gl[2][i]*effMC_dz[i]*DRll_SF;
                    }

                    SF_evt_v_d[4] = get_sf_unc(effs_data, effs_mc)[0];
                    SF_evt_v_u[4] = get_sf_unc(effs_data, effs_mc)[1];
                }

                result[0] = effData_evt[0];
                result[1] = effData_evt[1];
                result[2] = effData_evt[2];
                result[3] = effData_evt[3];
                result[4] = effData_evt[4];
                result[5] = effData_evt[5];
                result[6] = effData_evt[6];
                
                result[7] = effData_evt_v[0];
                result[8] = effData_evt_v[1];
                result[9] = effData_evt_v[2];
                result[10] = effData_evt_v[3];
                result[11] = effData_evt_v[4];

                result[12] = SF_evt[0];
                result[13] = SF_evt[1];
                result[14] = SF_evt[2];

                result[15] = SF_evt_v[0];
                result[16] = SF_evt_v[1];
                result[17] = SF_evt_v[2];
                result[18] = SF_evt_v[3];
                result[19] = SF_evt_v[4];

                result[20] = SF_evt_v_d[0];
                result[21] = SF_evt_v_d[1];
                result[22] = SF_evt_v_d[2];
                result[23] = SF_evt_v_d[3];
                result[24] = SF_evt_v_d[4];

                result[25] = SF_evt_v_u[0];
                result[26] = SF_evt_v_u[1];
                result[27] = SF_evt_v_u[2];
                result[28] = SF_evt_v_u[3];
                result[29] = SF_evt_v_u[4];

                return result;
            }
            """
        )

        df = df.Define(
            "event_eff_2l",
            "_2lepOk ? get_w(Lepton_pdgId[0], Lepton_pdgId[1], leg_eff_data, leg_eff_mc, dz_eff, gl_eff, drll_SF) : ROOT::RVecF(30, 0.0)",
        )

        ####
        ####  Trigger emulator for 2 leptons   :   Emulate trigger response for MC events. It uses the random seed defined above
        ####
        ####  Output  :  1-D Boolean array. Same as before but updated for 2 leptons
        ####

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecB Trig_emu_2lep(int id1, int id2, ROOT::RVecF Trndm, std::vector<ROOT::RVecF> eff, ROOT::RVecF eff_dz, std::vector<ROOT::RVecF> eff_gl){
                
                ROOT::RVecB Trig_emu_2lep(6, false);

                bool sApass = false;
                bool sBpass = false;
                bool lApass = false;
                bool lBpass = false;
                bool tApass = false;
                bool tBpass = false;
                bool DZpass = false;
                bool dblglpass = false;

                sApass    = eff[0][0]*eff_gl[0][0] > Trndm[0];
                sBpass    = eff[1][0]*eff_gl[1][0] > Trndm[1];
                lApass    = eff[2][0] > Trndm[2];
                lBpass    = eff[3][0] > Trndm[3];
                tApass    = eff[4][0] > Trndm[4];
                tBpass    = eff[5][0] > Trndm[5];
                DZpass    =    eff_dz[0] > Trndm[6];
                dblglpass =    eff_gl[2][0] > Trndm[7];

                if (abs(id1)==11 && abs(id2)==11){ 
                    Trig_emu_2lep[1] = (sApass || sBpass);
                    Trig_emu_2lep[3] = (lApass && tBpass &&  DZpass && dblglpass) || (lBpass && tApass &&  DZpass && dblglpass);
                }else if(abs(id1)==13 && abs(id2)==13){
                    Trig_emu_2lep[2] = (sApass || sBpass);
                    Trig_emu_2lep[4] = (lApass && tBpass &&  DZpass && dblglpass) || (lBpass && tApass &&  DZpass && dblglpass);
                }else if(abs(id1)==11 && abs(id2)==13){ 
                    Trig_emu_2lep[1] = sApass;
                    Trig_emu_2lep[2] = sBpass;
                    Trig_emu_2lep[5] = (lApass && tBpass &&  DZpass && dblglpass) || (lBpass && tApass &&  DZpass && dblglpass);
                }else{
                    Trig_emu_2lep[1] = sBpass;
                    Trig_emu_2lep[2] = sApass;
                    Trig_emu_2lep[5] = (lApass && tBpass &&  DZpass && dblglpass) || (lBpass && tApass &&  DZpass && dblglpass);
                }
                

                Trig_emu_2lep[0] = Trig_emu_2lep[1] || Trig_emu_2lep[2] || Trig_emu_2lep[3] || Trig_emu_2lep[4] || Trig_emu_2lep[5];

                return Trig_emu_2lep;
            }
            """
        )

        df = df.Redefine(
            "Trig_emu",
            "_2lepOk ? Trig_emu_2lep(Lepton_pdgId[0], Lepton_pdgId[1], Trndm, leg_eff_data, dz_eff, gl_eff) : Trig_emu",
        )

        ####
        #### Fill double trigger efficiency branches
        ####

        for name in self.NewVar["F"]:
            if "TriggerEffWeight" in name:
                if "_2l" in name:
                    if "_2l_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[1] : 0.0")
                    elif "_2l_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[2] : 0.0")
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[0] : 0.0")
                elif "_sngEl" in name:
                    df = df.Redefine(name, "_2lepOk ? event_eff_2l[7] : " + name)
                elif "_sngMu" in name:
                    df = df.Redefine(name, "_2lepOk ? event_eff_2l[8] : " + name)
                elif "_dblEl" in name:
                    df = df.Redefine(name, "_2lepOk ? event_eff_2l[9] : " + name)
                elif "_dblMu" in name:
                    df = df.Redefine(name, "_2lepOk ? event_eff_2l[10] : " + name)
                elif "_ElMu" in name:
                    df = df.Redefine(name, "_2lepOk ? event_eff_2l[11] : " + name)
            elif "TriggerSFWeight" in name:
                if "_2l" in name:
                    if "_2l_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[13] : 0.0")
                    elif "_2l_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[14] : 0.0")
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[12] : 0.0")
                elif "_sngEl" in name:
                    if "_sngEl_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[20] : " + name)
                    elif "_sngEl_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[25] : " + name)
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[15] : " + name)
                elif "_sngMu" in name:
                    if "_sngMu_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[21] : " + name)
                    elif "_sngMu_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[26] : " + name)
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[16] : " + name)
                elif "_dblEl" in name:
                    if "_dblEl_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[22] : " + name)
                    elif "_dblEl_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[27] : " + name)
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[17] : " + name)
                elif "_dblMu" in name:
                    if "_dblMu_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[23] : " + name)
                    elif "_dblMu_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[28] : " + name)
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[18] : " + name)
                elif "_ElMu" in name:
                    if "_ElMu_d" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[24] : " + name)
                    elif "_ElMu_u" in name:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[29] : " + name)
                    else:
                        df = df.Define(name, "_2lepOk ? event_eff_2l[19] : " + name)

        ########################################################################
        #                                                                      #
        #                                                                      #
        #                      DO 3 LEPTON TRIGGERS                            #
        #                                                                      #
        #                                                                      #
        ########################################################################

        ####
        #### In case of 3 leptons, first we have to compute again the efficiencies for all the possible combinations as done above
        ####

        df = df.Define("_3lepOk", "Lepton_pt.size() > 2")

        ####
        #### Compute event efficiencies for 3 leptons : Combine leg, global and DZ efficiencies for Data and MC to obtain per event scale factors
        ####
        #### Output : 1-D array with length 10 and the following structure
        ####
        #### [0,1,2,3,4,5,6]   :   event efficiencies  [Nom, down, up, down_stat, up_stat, down_syst, up_syst]
        #### [7, 8, 9]         :   event scale factors

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_l3w(ROOT::RVecF Lepton_pt, ROOT::RVecF Lepton_eta, ROOT::RVecF Lepton_phi, ROOT::RVecI Lepton_pdgId, int PV_npvsGood, int run){

                ROOT::RVecF result(10, 0.0);
                
                std::vector<ROOT::RVecF> eff12Data = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], run, true);
                std::vector<ROOT::RVecF> eff12MC   = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], run, false);
                ROOT::RVecF eff_dz12               = get_dz_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl12  = get_gl_eff(Lepton_pdgId[0], Lepton_pdgId[1], run);
                
                std::vector<ROOT::RVecF> eff13Data = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, true);
                std::vector<ROOT::RVecF> eff13MC   = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, false);
                ROOT::RVecF eff_dz13               = get_dz_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl13  = get_gl_eff(Lepton_pdgId[0], Lepton_pdgId[2], run);
                
                std::vector<ROOT::RVecF> eff23Data = get_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, true);
                std::vector<ROOT::RVecF> eff23MC   = get_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, false);
                ROOT::RVecF eff_dz23               = get_dz_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl23  = get_gl_eff(Lepton_pdgId[1], Lepton_pdgId[2], run);

                ROOT::RVec effData_dz12{eff_dz12[0], eff_dz12[1], eff_dz12[2], eff_dz12[1], eff_dz12[2], eff_dz12[0], eff_dz12[0]}; // set to nom to avoid double counting when computing the tot SF uncertainty
                ROOT::RVec effMC_dz12{eff_dz12[3], eff_dz12[4], eff_dz12[5], eff_dz12[4], eff_dz12[5], eff_dz12[3], eff_dz12[3]};

                ROOT::RVec effData_dz13{eff_dz13[0], eff_dz13[1], eff_dz13[2], eff_dz13[1], eff_dz13[2], eff_dz13[0], eff_dz13[0]};
                ROOT::RVec effMC_dz13{eff_dz13[3], eff_dz13[4], eff_dz13[5], eff_dz13[4], eff_dz13[5], eff_dz13[3], eff_dz13[3]};

                ROOT::RVec effData_dz23{eff_dz23[0], eff_dz23[1], eff_dz23[2], eff_dz23[1], eff_dz23[2], eff_dz23[0], eff_dz23[0]};
                ROOT::RVec effMC_dz23{eff_dz23[3], eff_dz23[4], eff_dz23[5], eff_dz23[4], eff_dz23[5], eff_dz23[3], eff_dz23[3]};

                ROOT::RVecF effData_evt(7, 0.0);
                ROOT::RVecF effMC_evt(7, 0.0);
                
                ROOT::RVecF SF_evt(3, 0.0);

                float s1;
                float s2;
                float s3;
                float e12;
                float e13;
                float e23;
                float eff_dbl;
                float eff_sng;

                for (int i=0; i<7; i++){
                    s1 = eff13Data[0][i]*eff_gl13[0][i];
                    s2 = eff23Data[0][i]*eff_gl12[1][i];
                    s3 = eff13Data[1][i]*eff_gl13[1][i];
                    eff_sng = s1 + (1-s1)*s2 + (1 - s1 - (1 - s1*s2))*s3;
                    e12 = (eff12Data[2][i]*eff12Data[5][i] + (1 - eff12Data[2][i]*eff12Data[5][i])*eff12Data[3][i]*eff12Data[4][i])*effData_dz12[i]*eff_gl12[2][i];
                    e13 = (eff13Data[2][i]*eff13Data[5][i] + (1 - eff13Data[2][i]*eff13Data[5][i])*eff13Data[3][i]*eff13Data[4][i])*effData_dz13[i]*eff_gl13[2][i];
                    e23 = (eff23Data[2][i]*eff23Data[5][i] + (1 - eff23Data[2][i]*eff23Data[5][i])*eff23Data[3][i]*eff23Data[4][i])*effData_dz23[i]*eff_gl23[2][i];
                    eff_dbl = e12 + (1 - e12)*e13 + (1 - e12)*(1 - e13)*e23;
                    //eff_dbl = e12 + (1 - e12)*e13 + (1 - e12 - (1 - e12)*e13)*e23;
                    effData_evt[i] = eff_dbl + (1 - eff_dbl)*eff_sng; 
                    
                    s1 = eff13MC[0][i]*eff_gl13[0][i];
                    s2 = eff23MC[0][i]*eff_gl12[1][i];
                    s3 = eff13MC[1][i]*eff_gl13[1][i];
                    eff_sng = s1 + (1-s1)*s2 + (1 - s1 - (1 - s1*s2))*s3;
                    e12 = (eff12MC[2][i]*eff12MC[5][i] + (1 - eff12MC[2][i]*eff12MC[5][i])*eff12MC[3][i]*eff12MC[4][i])*effMC_dz12[i]*eff_gl12[2][i];
                    e13 = (eff13MC[2][i]*eff13MC[5][i] + (1 - eff13MC[2][i]*eff13MC[5][i])*eff13MC[3][i]*eff13MC[4][i])*effMC_dz13[i]*eff_gl13[2][i];
                    e23 = (eff23MC[2][i]*eff23MC[5][i] + (1 - eff23MC[2][i]*eff23MC[5][i])*eff23MC[3][i]*eff23MC[4][i])*effMC_dz23[i]*eff_gl23[2][i];
                    eff_dbl = e12 + (1 - e12)*e13 + (1 - e12)*(1 - e13)*e23;
                    //eff_dbl = e12 + (1 - e12)*e13 + (1 - e12 - (1 - e12)*e13)*e23
                    effMC_evt[i] = eff_dbl + (1 - eff_dbl)*eff_sng;
                }

                SF_evt[0] = get_sf(effData_evt[0], effMC_evt[0]);
                SF_evt[1] = get_sf_unc(effData_evt, effMC_evt)[0];
                SF_evt[2] = get_sf_unc(effData_evt, effMC_evt)[1];

                result[0] = effData_evt[0];
                result[1] = effData_evt[1];
                result[2] = effData_evt[2];
                result[3] = effData_evt[3];
                result[4] = effData_evt[4];
                result[5] = effData_evt[5];
                result[6] = effData_evt[6];
                
                result[7] = SF_evt[0];
                result[8] = SF_evt[1];
                result[9] = SF_evt[2];

                return result;
            }
            """
        )

        #### Compute event efficiencies

        df = df.Define(
            "event_eff_3l",
            "_3lepOk ? get_l3w(Lepton_pt, Lepton_eta, Lepton_phi, Lepton_pdgId, PV_npvsGood, run_p) : ROOT::RVecF(10, 0.0)",
        )

        ####
        #### Fill 3 lepton trigger efficiencies
        ####

        for name in self.NewVar["F"]:
            if "TriggerEffWeight" in name:
                if "_3l" in name:
                    if "_3l_d" in name:
                        df = df.Define(name, "_3lepOk ? event_eff_3l[1] : 0.0")
                    elif "_3l_u" in name:
                        df = df.Define(name, "_3lepOk ? event_eff_3l[2] : 0.0")
                    else:
                        df = df.Define(name, "_3lepOk ? event_eff_3l[0] : 0.0")
            elif "TriggerSFWeight" in name:
                if "_3l" in name:
                    if "_3l_d" in name:
                        df = df.Define(name, "_3lepOk ? event_eff_3l[8] : 0.0")
                    elif "_3l_u" in name:
                        df = df.Define(name, "_3lepOk ? event_eff_3l[9] : 0.0")
                    else:
                        df = df.Define(name, "_3lepOk ? event_eff_3l[7] : 0.0")

        ########################################################################
        #                                                                      #
        #                                                                      #
        #                      DO 4 LEPTON TRIGGERS                            #
        #                                                                      #
        #                                                                      #
        ########################################################################

        #### As done with 3 leptons, compute efficiencies for all the possible combinations

        df = df.Define("_4lepOk", "Lepton_pt.size() > 3")

        ####
        #### Compute event efficiencies for 4 leptons : Combine leg, global and DZ efficiencies for Data and MC to obtain per event scale factors
        ####
        #### Output : 1-D array with length 10 and the following structure
        ####
        #### [0,1,2,3,4,5,6]   :   event efficiencies  [Nom, down, up, down_stat, up_stat, down_syst, up_syst]
        #### [7, 8, 9]         :   event scale factors

        ROOT.gInterpreter.Declare(
            """
            ROOT::RVecF get_nlw(ROOT::RVecF Lepton_pt, ROOT::RVecF Lepton_eta, ROOT::RVecF Lepton_phi, ROOT::RVecI Lepton_pdgId, int PV_npvsGood, int run){

                ROOT::RVecF result(10, 0.0);

                std::vector<ROOT::RVecF> eff12Data = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], run, true);
                std::vector<ROOT::RVecF> eff12MC   = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], run, false);
                ROOT::RVecF eff_dz12               = get_dz_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl12  = get_gl_eff(Lepton_pdgId[0], Lepton_pdgId[1], run);

                std::vector<ROOT::RVecF> eff13Data = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, true);
                std::vector<ROOT::RVecF> eff13MC   = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, false);
                ROOT::RVecF eff_dz13               = get_dz_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl13  = get_gl_eff(Lepton_pdgId[0], Lepton_pdgId[2], run);

                std::vector<ROOT::RVecF> eff14Data = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], run, true);
                std::vector<ROOT::RVecF> eff14MC   = get_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], run, false);
                ROOT::RVecF eff_dz14               = get_dz_eff(Lepton_pdgId[0], Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl14  = get_gl_eff(Lepton_pdgId[0], Lepton_pdgId[3], run);

                std::vector<ROOT::RVecF> eff23Data = get_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, true);
                std::vector<ROOT::RVecF> eff23MC   = get_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], run, false);
                ROOT::RVecF eff_dz23               = get_dz_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl23  = get_gl_eff(Lepton_pdgId[1], Lepton_pdgId[2], run);

                std::vector<ROOT::RVecF> eff24Data = get_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], run, true);
                std::vector<ROOT::RVecF> eff24MC   = get_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], run, false);
                ROOT::RVecF eff_dz24               = get_dz_eff(Lepton_pdgId[1], Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl24  = get_gl_eff(Lepton_pdgId[1], Lepton_pdgId[3], run);
                
                std::vector<ROOT::RVecF> eff34Data = get_eff(Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], run, true);
                std::vector<ROOT::RVecF> eff34MC   = get_eff(Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], run, false);
                ROOT::RVecF eff_dz34               = get_dz_eff(Lepton_pdgId[2], Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[3], Lepton_pt[3], Lepton_eta[3], PV_npvsGood, run);
                std::vector<ROOT::RVecF> eff_gl34  = get_gl_eff(Lepton_pdgId[2], Lepton_pdgId[3], run);
                
                ROOT::RVecF effData_dbl_inv(7, 1.0);
                ROOT::RVecF effData_sng_inv(7, 1.0);

                ROOT::RVecF effMC_dbl_inv(7, 1.0);
                ROOT::RVecF effMC_sng_inv(7, 1.0);

                ROOT::RVecF effData_evt(7, 0.0);
                ROOT::RVecF effMC_evt(7, 0.0);

                ROOT::RVecF SF_evt(3, 0.0);

                ROOT::RVec effData_dz12{eff_dz12[0], eff_dz12[1], eff_dz12[2], eff_dz12[1], eff_dz12[2], eff_dz12[0], eff_dz12[0]};
                ROOT::RVec effMC_dz12{eff_dz12[3], eff_dz12[4], eff_dz12[5], eff_dz12[4], eff_dz12[5], eff_dz12[3], eff_dz12[3]};

                ROOT::RVec effData_dz13{eff_dz13[0], eff_dz13[1], eff_dz13[2], eff_dz13[1], eff_dz13[2], eff_dz13[0], eff_dz13[0]}; 
                ROOT::RVec effMC_dz13{eff_dz13[3], eff_dz13[4], eff_dz13[5], eff_dz13[4], eff_dz13[5], eff_dz13[3], eff_dz13[3]}; 

                ROOT::RVec effData_dz14{eff_dz14[0], eff_dz14[1], eff_dz14[2], eff_dz14[1], eff_dz14[2], eff_dz14[0], eff_dz14[0]};
                ROOT::RVec effMC_dz14{eff_dz14[3], eff_dz14[4], eff_dz14[5], eff_dz14[4], eff_dz14[5], eff_dz14[3], eff_dz14[3]};

                ROOT::RVec effData_dz23{eff_dz23[0], eff_dz23[1], eff_dz23[2], eff_dz23[1], eff_dz23[2], eff_dz23[0], eff_dz23[0]};
                ROOT::RVec effMC_dz23{eff_dz23[3], eff_dz23[4], eff_dz23[5], eff_dz23[4], eff_dz23[5], eff_dz23[3], eff_dz23[3]}; 
                
                ROOT::RVec effData_dz24{eff_dz24[0], eff_dz24[1], eff_dz24[2], eff_dz24[1], eff_dz24[2], eff_dz24[0], eff_dz24[0]};
                ROOT::RVec effMC_dz24{eff_dz24[3], eff_dz24[4], eff_dz24[5], eff_dz24[4], eff_dz24[5], eff_dz24[3], eff_dz24[3]};

                ROOT::RVec effData_dz34{eff_dz34[0], eff_dz34[1], eff_dz34[2], eff_dz34[1], eff_dz34[2], eff_dz34[0], eff_dz34[0]};
                ROOT::RVec effMC_dz34{eff_dz34[3], eff_dz34[4], eff_dz34[5], eff_dz34[4], eff_dz34[5], eff_dz34[3], eff_dz34[3]};

                float temp_var;

                for (int i=0; i<7; i++){                        
                    // 1 - 2
                    temp_var = (eff12Data[2][i]*eff12Data[5][i] + (1 - eff12Data[2][i]*eff12Data[5][i])*eff12Data[3][i]*eff12Data[4][i])*effData_dz12[i]*eff_gl12[2][i];
                    effData_dbl_inv[i] = effData_dbl_inv[i] * (1 - temp_var);
                    
                    // 1 - 3
                    temp_var = (eff13Data[2][i]*eff13Data[5][i] + (1 - eff13Data[2][i]*eff13Data[5][i])*eff13Data[3][i]*eff13Data[4][i])*effData_dz13[i]*eff_gl13[2][i];
                    effData_dbl_inv[i] = effData_dbl_inv[i] * (1 - temp_var);
                    
                    // 1 - 4
                    temp_var = (eff14Data[2][i]*eff14Data[5][i] + (1 - eff14Data[2][i]*eff14Data[5][i])*eff14Data[3][i]*eff14Data[4][i])*effData_dz14[i]*eff_gl14[2][i];
                    effData_dbl_inv[i] = effData_dbl_inv[i] * (1 - temp_var);
                    
                    // 2 - 3
                    temp_var = (eff23Data[2][i]*eff23Data[5][i] + (1 - eff23Data[2][i]*eff23Data[5][i])*eff23Data[3][i]*eff23Data[4][i])*effData_dz23[i]*eff_gl23[2][i];
                    effData_dbl_inv[i] = effData_dbl_inv[i] * (1 - temp_var);
                    
                    // 2 - 4
                    temp_var = (eff24Data[2][i]*eff24Data[5][i] + (1 - eff24Data[2][i]*eff24Data[5][i])*eff24Data[3][i]*eff24Data[4][i])*effData_dz24[i]*eff_gl24[2][i];
                    effData_dbl_inv[i] = effData_dbl_inv[i] * (1 - temp_var);
                    
                    // 3 - 4
                    temp_var = (eff34Data[2][i]*eff34Data[5][i] + (1 - eff34Data[2][i]*eff34Data[5][i])*eff34Data[3][i]*eff34Data[4][i])*effData_dz34[i]*eff_gl34[2][i];
                    effData_dbl_inv[i] = effData_dbl_inv[i] * (1 - temp_var);
                    
                    
                    // 1 - 2
                    temp_var = (eff12MC[2][i]*eff12MC[5][i] + (1 - eff12MC[2][i]*eff12MC[5][i])*eff12MC[3][i]*eff12MC[4][i])*effMC_dz12[i]*eff_gl12[2][i];
                    effMC_dbl_inv[i] = effMC_dbl_inv[i] * (1 - temp_var);
                    
                    // 1 - 3
                    temp_var = (eff13MC[2][i]*eff13MC[5][i] + (1 - eff13MC[2][i]*eff13MC[5][i])*eff13MC[3][i]*eff13MC[4][i])*effMC_dz13[i]*eff_gl13[2][i];
                    effMC_dbl_inv[i] = effMC_dbl_inv[i] * (1 - temp_var);
                    
                    // 1 - 4
                    temp_var = (eff14MC[2][i]*eff14MC[5][i] + (1 - eff14MC[2][i]*eff14MC[5][i])*eff14MC[3][i]*eff14MC[4][i])*effMC_dz14[i]*eff_gl14[2][i];
                    effMC_dbl_inv[i] = effMC_dbl_inv[i] * (1 - temp_var);
                    
                    // 2 - 3
                    temp_var = (eff23MC[2][i]*eff23MC[5][i] + (1 - eff23MC[2][i]*eff23MC[5][i])*eff23MC[3][i]*eff23MC[4][i])*effMC_dz23[i]*eff_gl23[2][i];
                    effMC_dbl_inv[i] = effMC_dbl_inv[i] * (1 - temp_var);
                    
                    // 2 - 4
                    temp_var = (eff24MC[2][i]*eff24MC[5][i] + (1 - eff24MC[2][i]*eff24MC[5][i])*eff24MC[3][i]*eff24MC[4][i])*effMC_dz24[i]*eff_gl24[2][i];
                    effMC_dbl_inv[i] = effMC_dbl_inv[i] * (1 - temp_var);
                    
                    // 3 - 4
                    temp_var = (eff34MC[2][i]*eff34MC[5][i] + (1 - eff34MC[2][i]*eff34MC[5][i])*eff34MC[3][i]*eff34MC[4][i])*effMC_dz34[i]*eff_gl34[2][i];
                    effMC_dbl_inv[i] = effMC_dbl_inv[i] * (1 - temp_var);
                    
                    
                    
                    // Single Lepton efficiencies
                    effData_sng_inv[i] = effData_sng_inv[i] * (1 - eff14Data[0][i]*eff_gl14[0][i]);
                    effData_sng_inv[i] = effData_sng_inv[i] * (1 - eff24Data[0][i]*eff_gl24[0][i]);
                    effData_sng_inv[i] = effData_sng_inv[i] * (1 - eff34Data[0][i]*eff_gl34[0][i]);
                    effData_sng_inv[i] = effData_sng_inv[i] * (1 - eff14Data[1][i]*eff_gl14[1][i]);
                    
                    effMC_sng_inv[i] = effMC_sng_inv[i] * (1 - eff14MC[0][i]*eff_gl14[0][i]);
                    effMC_sng_inv[i] = effMC_sng_inv[i] * (1 - eff24MC[0][i]*eff_gl24[0][i]);
                    effMC_sng_inv[i] = effMC_sng_inv[i] * (1 - eff34MC[0][i]*eff_gl34[0][i]);
                    effMC_sng_inv[i] = effMC_sng_inv[i] * (1 - eff14MC[1][i]*eff_gl14[1][i]);
                    
                    effData_evt[i] = 1.0 - effData_dbl_inv[i]*effData_sng_inv[i];
                    effMC_evt[i] = 1.0 - effMC_dbl_inv[i]*effMC_sng_inv[i];
                }

                SF_evt[0] = get_sf(effData_evt[0], effMC_evt[0]);
                SF_evt[1] = get_sf_unc(effData_evt, effMC_evt)[0];
                SF_evt[2] = get_sf_unc(effData_evt, effMC_evt)[1];

                result[0] = effData_evt[0];
                result[1] = effData_evt[1];
                result[2] = effData_evt[2];
                result[3] = effData_evt[3];
                result[4] = effData_evt[4];
                result[5] = effData_evt[5];
                result[6] = effData_evt[6];
                
                result[7] = SF_evt[0];     
                result[8] = SF_evt[1];     
                result[9] = SF_evt[2];     

                return result;
            }
            """
        )

        #### Compute event efficiencies

        df = df.Define(
            "event_eff_4l",
            "_4lepOk ? get_nlw(Lepton_pt, Lepton_eta, Lepton_phi, Lepton_pdgId, PV_npvsGood, run_p) : ROOT::RVecF(10, 0.0)",
        )

        ####
        #### Fill 4 lepton trigger efficiencies
        ####

        for name in self.NewVar["F"]:
            if "TriggerEffWeight" in name:
                if "_4l" in name:
                    if "_4l_d" in name:
                        df = df.Define(name, "_4lepOk ? event_eff_4l[1] : 0.0")
                    elif "_4l_u" in name:
                        df = df.Define(name, "_4lepOk ? event_eff_4l[2] : 0.0")
                    else:
                        df = df.Define(name, "_4lepOk ? event_eff_4l[0] : 0.0")
            elif "TriggerSFWeight" in name:
                if "_4l" in name:
                    if "_4l_d" in name:
                        df = df.Define(name, "_4lepOk ? event_eff_4l[8] : 0.0")
                    elif "_4l_u" in name:
                        df = df.Define(name, "_4lepOk ? event_eff_4l[9] : 0.0")
                    else:
                        df = df.Define(name, "_4lepOk ? event_eff_4l[7] : 0.0")

        if "TriggerEmulator" in self.NewVar["I"]:
            df = df.Define("TriggerEmulator", "Trig_emu")

        df = df.DropColumns("Trig_emu")
        df = df.DropColumns("_1lepOk")
        df = df.DropColumns("Trndm")
        df = df.DropColumns("lep1_eff")
        df = df.DropColumns("run_p")
        df = df.DropColumns("event_eff_2l")
        df = df.DropColumns("leg_eff_data")
        df = df.DropColumns("leg_eff_mc")
        df = df.DropColumns("drll_SF")
        df = df.DropColumns("dz_eff")
        df = df.DropColumns("gl_eff")
        df = df.DropColumns("_2lepOk")
        df = df.DropColumns("event_eff_3l")
        df = df.DropColumns("_3lepOk")
        df = df.DropColumns("event_eff_4l")
        df = df.DropColumns("_4lepOk")

        return df
