from mkShapesRDF.lib.utils import getFrameworkPath
####################### Jet Veto/JEC/JER/JES CFG ##################################

frameworkPath = getFrameworkPath() + "mkShapesRDF"
JetMakerCfg = {
    'Full2022v12': {
        "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/latest/jetvetomaps.json.gz",
        "vetokey": "Summer22_23Sep2023_RunCD_V1",
        "JEC": "Summer22_22Sep2023_V3_MC",
        "JEC_data" : "Summer22_22Sep2023_RunCD_V3_DATA",
        "JER": "Summer22_22Sep2023_JRV1_MC",
        "jet_jerc" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/latest/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "met_xy_json" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/latest/met_xyCorrections_2022_2022EE.json.gz",
        "met_xy_era" : "2022"
    },
    'Full2022EEv12': {
        "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/latest/jetvetomaps.json.gz",
        "vetokey": "Summer22EE_23Sep2023_RunEFG_V1",
	"JEC": "Summer22EE_22Sep2023_V3_MC",
        "JEC_data" : ["Summer22EE_22Sep2023_RunE_V3_DATA", 'Summer22EE_22Sep2023_RunF_V3_DATA', 'Summer22EE_22Sep2023_RunG_V3_DATA'],
        "JER": "Summer22EE_22Sep2023_JRV1_MC",
        "jet_jerc" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/latest/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "met_xy_json" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/latest/met_xyCorrections_2022_2022EE.json.gz",
        "met_xy_era" : "2022EE"
    },
    'Full2023v12': {
        "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/latest/jetvetomaps.json.gz",
        "vetokey": "Summer23Prompt23_RunC_V1",
	"JEC": "Summer23Prompt23_V2_MC",
        #"JEC_data" : ["Summer23Prompt23_RunCv123_V1_DATA", "Summer23Prompt23_RunCv4_V1_DATA"],
        "JEC_data" : ["Summer23Prompt23_V2_DATA", "Summer23Prompt23_V2_DATA"],
        "JER": "Summer23Prompt23_RunCv1234_JRV1_MC",
        "jet_jerc" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/latest/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "met_xy_json" :	"/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/latest/met_xyCorrections_2023_2023BPix.json.gz",
        "met_xy_era" : "2023"
    },
    'Full2023BPixv12': {
        "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/latest/jetvetomaps.json.gz",
        "vetokey": "Summer23BPixPrompt23_RunD_V1",
        "JEC": "Summer23BPixPrompt23_V3_MC",
        "JEC_data" : "Summer23BPixPrompt23_V3_DATA",        
        "JER": "Summer23BPixPrompt23_RunD_JRV1_MC",
        "jet_jerc" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/latest/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "met_xy_json" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/latest/met_xyCorrections_2023_2023BPix.json.gz",
        "met_xy_era" : "2023BPix"
    },
    'Full2024v15': {
        "vetomap": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/jetvetomaps.json.gz",
        "vetokey": "Summer24Prompt24_RunBCDEFGHI_V1",
        "JEC": "Summer24Prompt24_V2_MC",
        "JEC_data" : "Summer24Prompt24_V2_DATA",
        "JER": "Summer23BPixPrompt23_RunD_JRV1_MC",        
        "jet_jerc" : "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jer_smear/jer_smear_run3.json.gz",
        "jetId": {
            "json": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/jetid.json.gz",
            "key" : "AK4PUPPI_Tight",
        }
    },
}

