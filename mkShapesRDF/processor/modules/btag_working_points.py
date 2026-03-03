B_TAG_BRANCHES = {
    "DeepFlavB": "Jet_btagDeepFlavB",
    "RobustParTAK4B": "Jet_btagRobustParTAK4B",
    "PNetB": "Jet_btagPNetB",
    "UParTAK4B": "Jet_btagUParTAK4B",
}

B_TAG_WORKING_POINTS = {
    "Full2022v12": {
        "DeepFlavB": {
            "loose": 0.0583,
            "medium": 0.3086,
            "tight": 0.7183,
            "xtight": 0.8111,
            "xxtight": 0.9512,
        },
        "RobustParTAK4B": {
            "loose": 0.0849,
            "medium": 0.4319,
            "tight": 0.8482,
            "xtight": 0.9151,
            "xxtight": 0.9874,
        },
        "PNetB": {
            "loose": 0.0470,
            "medium": 0.2450,
            "tight": 0.6734,
            "xtight": 0.7862,
            "xxtight": 0.9610,
        },
    },
    "Full2022EEv12": {
        "DeepFlavB": {
            "loose": 0.0614,
            "medium": 0.3196,
            "tight": 0.7300,
            "xtight": 0.8184,
            "xxtight": 0.9542,
        },
        "RobustParTAK4B": {
            "loose": 0.0897,
            "medium": 0.4510,
            "tight": 0.8604,
            "xtight": 0.9234,
            "xxtight": 0.9893,
        },
        "PNetB": {
            "loose": 0.0499,
            "medium": 0.2605,
            "tight": 0.6915,
            "xtight": 0.8033,
            "xxtight": 0.9664,
        },
    },
    "Full2023v12": {
        "DeepFlavB": {
            "loose": 0.0479,
            "medium": 0.2435,
        },
        "RobustParTAK4B": {
            "loose": 0.0681,
            "medium": 0.3494,
        },
        "PNetB": {
            "loose": 0.0358,
            "medium": 0.1919,
        },
    },
    "Full2023BPixv12": {
        "DeepFlavB": {
            "loose": 0.0480,
            "medium": 0.2435,
        },
        "RobustParTAK4B": {
            "loose": 0.0683,
            "medium": 0.3494,
        },
        "PNetB": {
            "loose": 0.0359,
            "medium": 0.1919,
        },
    },
    "Full2024v15": {
        "DeepFlavB": {
            "loose": 0.0480,
            "medium": 0.2435,
            "tight": 0.6563,
            "xtight": 0.7671,
            "xxtight": 0.9483,
        },
        "UParTAK4B": {
            "loose": 0.0246,
            "medium": 0.1272,
            "tight": 0.4648,
            "xtight": 0.6298,
            "xxtight": 0.9739,
        },
        "PNetB": {
            "loose": 0.0359,
            "medium": 0.1919,
            "tight": 0.6133,
            "xtight": 0.7544,
            "xxtight": 0.9688,
        },
    },
}


def resolve_btag_configuration(era, btagger, working_point):
    if era not in B_TAG_WORKING_POINTS:
        raise ValueError(
            f"Unsupported era '{era}'. Available eras: {sorted(B_TAG_WORKING_POINTS.keys())}"
        )

    era_wps = B_TAG_WORKING_POINTS[era]
    if btagger not in era_wps:
        raise ValueError(
            f"Unsupported btagger '{btagger}' for era '{era}'. "
            f"Available taggers: {sorted(era_wps.keys())}"
        )

    tagger_wps = era_wps[btagger]
    if working_point not in tagger_wps:
        raise ValueError(
            f"Unsupported working point '{working_point}' for era '{era}' and btagger '{btagger}'. "
            f"Available working points: {sorted(tagger_wps.keys())}"
        )

    if btagger not in B_TAG_BRANCHES:
        raise ValueError(
            f"No branch mapping configured for btagger '{btagger}'. "
            f"Available mappings: {sorted(B_TAG_BRANCHES.keys())}"
        )

    return B_TAG_BRANCHES[btagger], float(tagger_wps[working_point])
