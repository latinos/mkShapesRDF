from mkShapesRDF.lib.utils import getFrameworkPath
####################### Jet Veto/JEC/JER/JES CFG ##################################

frameworkPath = getFrameworkPath() + "mkShapesRDF"
JetMakerCfg = {
    'Full2022v12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22/jetvetomaps.json.gz",
        "vetokey": "Summer22_23Sep2023_RunCD_V1",
        "JEC": "Summer22_22Sep2023_V2_MC",
        "JER": "Summer22_22Sep2023_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2022EEv12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22EE/jetvetomaps.json.gz",
        "vetokey": "Summer22EE_23Sep2023_RunEFG_V1",
	"JEC": "Summer22EE_22Sep2023_V2_MC",
        "JER": "Summer22EE_22Sep2023_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2022_Summer22EE/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2023v12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23/jetvetomaps.json.gz",
        "vetokey": "Summer23Prompt23_RunC_V1",
	"JEC": "Summer23Prompt23_V1_MC",
        "JER": "Summer23Prompt23_RunCv123_JRV1_MC", ### Why is there another Summer23Prompt23_RunCv4_JR?
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2023BPixv12': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23BPix/jetvetomaps.json.gz",
        "vetokey": "Summer23BPixPrompt23_RunD_V1",
	"JEC": "Summer23BPixPrompt23_V3_MC",
        "JER": "Summer23BPixPrompt23_RunD_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2023_Summer23BPix/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
    },
    'Full2024v15': {
        "vetomap": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2024_Winter24/jetvetomaps.json.gz",
        "vetokey": "Winter24Prompt2024BCDEFGHI_V1",
        "JEC": "Winter24Prompt24_V3_MC",
        "JER": "Summer23BPixPrompt23_RunD_JRV1_MC",
        "jet_jerc" : frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2024_Winter24/jet_jerc.json.gz",
        "jer_smear": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/jer_smear.json.gz",
        "jetId": {
            "json": frameworkPath + "/processor/data/jsonpog-integration/POG/JME/2024_Summer24/jetid.json.gz",
            "key" : "AK4PUPPI_Tight",
        }
    },
}

