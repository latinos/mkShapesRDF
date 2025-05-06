from mkShapesRDF.lib.utils import getFrameworkPath
####################### Jet Veto/JEC/JER/JES CFG ##################################

frameworkPath = getFrameworkPath() + "mkShapesRDF"
JetMakerCfg = {
    'Full2022v12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22/jetvetomaps.json.gz",
        "vetokey": "Summer22_23Sep2023_RunCD_V1",
        "JEC": "Summer22_22Sep2023_V2_MC",
        "JEC_data" : "Summer22_22Sep2023_RunCD_V2_DATA",
        "JER": "Summer22_22Sep2023_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2022EEv12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22EE/jetvetomaps.json.gz",
        "vetokey": "Summer22EE_23Sep2023_RunEFG_V1",
	    "JEC": "Summer22EE_22Sep2023_V2_MC",
        "JEC_data" : ["Summer22EE_22Sep2023_RunE_V2_DATA", 'Summer22EE_22Sep2023_RunF_V2_DATA', 'Summer22EE_22Sep2023_RunG_V2_DATA'],
        "JER": "Summer22EE_22Sep2023_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22EE/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2023v12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23/jetvetomaps.json.gz",
        "vetokey": "Summer23Prompt23_RunC_V1",
	    "JEC": "Summer23Prompt23_V1_MC",
        "JEC_data" : ["Summer23Prompt23_RunCv123_V1_DATA", "Summer23Prompt23_RunCv4_V1_DATA"],
        "JER": "Summer23Prompt23_RunCv1234_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2023BPixv12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23BPix/jetvetomaps.json.gz",
        "vetokey": "Summer23BPixPrompt23_RunD_V1",
	    "JEC": "Summer23BPixPrompt23_V1_MC",
        "JEC_data" : "Summer23BPixPrompt23_RunD_V1_DATA",
        "JER": "Summer23BPixPrompt23_RunD_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23BPix/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
}