#!/usr/bin/env python

import numpy as np
import pandas as pd

import sys

import itertools

from correctionlib.schemav2 import Binning, Category, Correction, CorrectionSet


def convert_to_json(textfile, mode=None):
    tmp_file = open(textfile, "r")

    tmp_df = [line.rstrip().split() for line in tmp_file if "#" not in line]
    tmp_df = [[float(each) for each in line] for line in tmp_df]

    tmp_file.close()

    df = pd.DataFrame()

    do_int_edges = False

    all_systematics = []
    if mode == "drll":
        df = pd.DataFrame(tmp_df, columns=["dRllBin_low", "dRllBin_high", "value"])
        variableLabels = ["dRll"]
        systematics = None
    elif mode == "DZ":
        if len(tmp_df[0]) == 5:
            df = pd.DataFrame(
                tmp_df,
                columns=["keyBin_low", "keyBin_high", "value", "error", "error2"],
            )
            variableLabels = ["key"]
            systematics = ["error", "error2"]
        else:
            df = pd.DataFrame(
                tmp_df,
                columns=[
                    "pt1Bin_low",
                    "pt1Bin_high",
                    "pt2Bin_low",
                    "pt2Bin_high",
                    "value",
                    "error",
                    "error2",
                ],
            )
            variableLabels = ["pt1", "pt2"]
            systematics = ["error", "error2"]
    elif mode == "Leg":
        df = pd.DataFrame(
            tmp_df,
            columns=[
                "etaBin_low",
                "etaBin_high",
                "ptBin_low",
                "ptBin_high",
                "value",
                "stat_down",
                "stat_up",
                "syst_down",
                "syst_up",
            ],
        )
        systematics = ["stat_down", "stat_up", "syst_down", "syst_up"]
        variableLabels = ["eta", "pt"]

        df = (
            df.drop_duplicates()
        )  ## Just in case. There are several files with a duplicated row at the end

    binning = {}

    for var in variableLabels:
        binning[var] = np.unique(
            list(df[var + "Bin_low"].values) + list(df[var + "Bin_high"].values)
        )

    outname = textfile.split(".txt")[0] + ".json"

    indices = [
        list(range(1, len(binning[variableLabel]))) for variableLabel in variableLabels
    ]

    output = {}

    all_systematics = {}
    for index in itertools.product(*indices):
        subVarKeys = [
            "{}:[{},{}]".format(
                variableLabels[i],
                binning[variableLabels[i]][ind - 1],
                binning[variableLabels[i]][ind],
            )
            for i, ind in enumerate(index)
        ]

        _out = output

        _out["binning"] = [
            {
                "variable": vl,
                "binning": binning[vl].tolist(),
            }
            for vl in variableLabels
        ]

        for subVarKey in subVarKeys:
            if subVarKey not in _out:
                _out[subVarKey] = {}
            _out = _out[subVarKey]

        eff_bin = df

        for var in variableLabels:
            eff_bin = eff_bin.loc[
                eff_bin[var + "Bin_high"]
                == binning[var][list(index)[variableLabels.index(var)]]
            ]

        ## Only needed in DZ Eff. pt1:pt2 don't cover the full phase space
        if eff_bin.empty and mode=="DZ":
            eff_bin = pd.DataFrame({"pt1Bin_low": binning[variableLabels[0]][index[0]-1], 
                                    "pt1Bin_high": binning[variableLabels[0]][index[0]],
                                    "pt2Bin_low": binning[variableLabels[1]][index[1]-1],
                                    "pt2Bin_high": binning[variableLabels[1]][index[1]],
                                    "value" : [1.0],
                                    "error" : [0.0],
                                    "error2": [0.0]
                                })

        _out["value"] = eff_bin["value"]

        if systematics != None:
            for sys in systematics:
                _out[sys] = eff_bin[sys]

        all_systematics[index] = _out.copy()

    print("The new json file will be stored at: \n")
    print(outname)

    bin_vars = list(binning.keys())
    dimensions = len(binning)

    inputs = [
        {"name": bin_var, "type": "real", "description": bin_var}
        for bin_var in bin_vars
    ]
    inputs += [
        {
            "name": "systematic",
            "type": "string",
            "description": "Choose nominal efficiency or one of the uncertainties",
        }
    ]

    def build_schema_recursively(dim, index):
        # If we reach recursion bottom, build and return the systematics node

        if dim == dimensions + 1:
            keys, content = [], []
            for syst, value in all_systematics[index].items():
                keys.append(syst)
                syst = syst if syst != "value" else "nominal"
                content.append({"key": syst, "value": value})
            return Category.parse_obj(
                {"nodetype": "category", "input": "systematic", "content": content}
            )

        # If not, build a binning node
        edges = list(map(float, binning[bin_vars[dim - 1]]))
        content = [
            build_schema_recursively(
                dim + 1, tuple(list(index)[0 : dim - 1] + [i] + list(index)[dim:])
            )
            for i in indices[dim - 1]
        ]
        return Binning.parse_obj(
            {
                "nodetype": "binning",
                "input": bin_vars[dim - 1],
                "edges": edges,
                "flow": "error",
                "content": content,
            }
        )

    content = build_schema_recursively(1, tuple([1] * dimensions))

    corr = Correction.parse_obj(
        {
            "version": 1,
            "name": "TriggerEff",
            "description": "Trigger efficiencies from txt files",
            "inputs": inputs,
            "output": {
                "name": "weight",
                "type": "real",
                "description": "Output efficiency (nominal) or uncertainty",
            },
            "data": content,
        }
    )

    cset = CorrectionSet.parse_obj({"schema_version": 2, "corrections": [corr]})

    # Write out converted json
    with open(outname, "w") as fout:
        fout.write(cset.json(exclude_unset=True, indent=4))


if __name__ == "__main__":
    if len(sys.argv) == 0 or len(sys.argv) > 3:
        print("Error: Please introduce trigger text file name")
        sys.exit(1)

    textfile = sys.argv[1]
    if len(sys.argv) > 2:
        mode = sys.argv[2]
    else:
        mode = None

    convert_to_json(textfile, mode)
