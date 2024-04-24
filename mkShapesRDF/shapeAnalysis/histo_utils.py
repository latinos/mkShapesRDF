import ROOT
import numpy as np
from mkShapesRDF.shapeAnalysis.rnp import rnp_hist2array, rnp_array, rnp_array2hist

ROOT.TH1.SetDefaultSumw2(True)


def fold(h, ifrom, ito):
    """
    Folds a histogram bin content and sumw2

    Parameters
    ----------
    h : ROOT.TH1, ROOT.TH2, ROOT.TH3
        input histogram, will be modified in place
    ifrom : int
        index of bin where to copy from. Will be then set to 0
    ito : int
        index of bin where to copy.

    """
    cont = rnp_hist2array(h, copy=False, include_overflow=True)
    sumw2 = rnp_array(h.GetSumw2(), copy=False)
    if isinstance(h, ROOT.TH3):
        shape = (h.GetNbinsX() + 2, h.GetNbinsY() + 2, h.GetNbinsZ() + 2)
    elif isinstance(h, ROOT.TH2):
        shape = (h.GetNbinsX() + 2, h.GetNbinsY() + 2)
    elif isinstance(h, ROOT.TH1):
        shape = (h.GetNbinsX() + 2,)
    sumw2 = sumw2.reshape(shape)

    if h.GetDimension() == 1:
        cont[ito] += cont[ifrom]
        cont[ifrom] = 0.0
        sumw2[ito] += sumw2[ifrom]
        sumw2[ifrom] = 0.0

    elif h.GetDimension() == 2:
        cont[ito, :] += cont[ifrom, :]
        cont[ifrom, :] = 0.0
        cont[:, ito] += cont[:, ifrom]
        cont[:, ifrom] = 0.0

        # sumw2 is y-major
        nx = h.GetNbinsX()
        ny = h.GetNbinsY()
        sumw2 = np.reshape(sumw2, (ny + 2, nx + 2))
        sumw2[ito, :] += sumw2[ifrom, :]
        sumw2[ifrom, :] = 0.0
        sumw2[:, ito] += sumw2[:, ifrom]
        sumw2[:, ifrom] = 0.0

    elif h.GetDimension() == 3:
        cont[ito, :, :] += cont[ifrom, :, :]
        cont[ifrom, :, :] = 0.0
        cont[:, ito, :] += cont[:, ifrom, :]
        cont[:, ifrom, :] = 0.0
        cont[:, :, ito] += cont[:, :, ifrom]
        cont[:, :, ifrom] = 0.0

        # sumw2 is y-major
        nx = h.GetNbinsX()
        ny = h.GetNbinsY()
        nz = h.GetNbinsZ()
        sumw2 = np.reshape(sumw2, (nz + 2, ny + 2, nx + 2))
        sumw2[ito, :, :] += sumw2[ifrom, :, :]
        sumw2[ifrom, :, :] = 0.0
        sumw2[:, ito, :] += sumw2[:, ifrom, :]
        sumw2[:, ifrom, :] = 0.0
        sumw2[:, :, ito] += sumw2[:, :, ifrom]
        sumw2[:, :, ifrom] = 0.0


def postPlot(hTotal, doFold, unroll=True):
    """
    Takes TH1, TH2 or TH3, folds if necessary and unrolls

    Parameters
    ----------
    hTotal : ROOT.TH1, ROOT.TH2, ROOT.TH3
        input histogram
    doFold : bool
        0 do not fold, 1 fold underflow, 2 fold overflow, 3 fold everything
    unroll : bool, optional
        if dimension >= 2 unrolls to 1D, by default True

    Returns
    -------
    ROOT.TH1
        folded and unrolled histogram
    """
    if doFold == 1 or doFold == 3:
        fold(hTotal, 0, 1)
    if doFold == 2 or doFold == 3:
        fold(hTotal, -1, -2)

    # if unroll and hTotal.InheritsFrom(ROOT.TH2.Class()):
    if unroll and isinstance(hTotal, ROOT.TH2) and hTotal.GetDimension() == 2:
        # --- transform 2D into 1D
        #
        #      3    6    9
        #      2    5    8
        #      1    4    7
        #
        # over/underflow are discarded
        hTotal_rolled = hTotal

        nx = hTotal_rolled.GetNbinsX()
        ny = hTotal_rolled.GetNbinsY()
        name = hTotal.GetName()
        hTotal = ROOT.TH1D(
            name + "_tmp", hTotal.GetTitle(), nx * ny, 0.0, float(nx * ny)
        )
        hTotal.GetXaxis().SetTitle(hTotal_rolled.GetXaxis().GetTitle())

        # contents
        cont = rnp_hist2array(hTotal_rolled, copy=False).reshape(-1)
        # hist2array for TH2 returns [x, y] arrays -> reshape -1 achieves the desired bin numbering
        rnp_array2hist(cont, hTotal)

        # sumw2
        # Sumw2 array follows the ROOT bin numbering (y-major)
        sumw22d = rnp_array(hTotal_rolled.GetSumw2(), copy=False).reshape(
            (ny + 2, nx + 2)
        )
        # chop off overflow and underflow bins
        sumw22d = sumw22d[1:-1, 1:-1]
        sumw2 = rnp_array(hTotal.GetSumw2(), copy=False)
        # transpose to change the bin numbering
        sumw2[1:-1] = sumw22d.T.flat

        # stats
        stats2d = ROOT.TArrayD(7)
        hTotal_rolled.GetStats(stats2d.GetArray())
        stats1d = ROOT.TArrayD(4)
        stats1d[0] = stats2d[0]
        stats1d[1] = stats2d[1]
        stats1d[2] = stats2d[2] + stats2d[4]
        stats1d[3] = stats2d[3] + stats2d[5]
        hTotal.PutStats(stats1d.GetArray())

        hTotal_rolled.Delete()

    if unroll and isinstance(hTotal, ROOT.TH3) and hTotal.GetDimension() == 3:
        # --- transform 2D into 1D
        #
        #      3    6    9
        #      2    5    8
        #      1    4    7
        #
        # over/underflow are discarded
        hTotal_rolled = hTotal

        nx = hTotal_rolled.GetNbinsX()
        ny = hTotal_rolled.GetNbinsY()
        nz = hTotal_rolled.GetNbinsZ()
        name = hTotal.GetName()
        hTotal = ROOT.TH1D(
            name + "_tmp", hTotal.GetTitle(), nx * ny * nz, 0.0, float(nx * ny * nz)
        )
        hTotal.GetXaxis().SetTitle(hTotal_rolled.GetXaxis().GetTitle())

        # contents
        cont = rnp_hist2array(hTotal_rolled, copy=False).reshape(-1)
        # hist2array for TH3 returns [x, y, z] arrays -> reshape -1 achieves the desired bin numbering
        rnp_array2hist(cont, hTotal)

        # sumw2
        # Sumw2 array follows the ROOT bin numbering (z-major)
        sumw22d = rnp_array(hTotal_rolled.GetSumw2(), copy=False).reshape(
            (nz + 2, ny + 2, nx + 2)
        )
        # chop off overflow and underflow bins
        sumw22d = sumw22d[1:-1, 1:-1, 1:-1]
        sumw2 = rnp_array(hTotal.GetSumw2(), copy=False)
        # transpose to change the bin numbering
        sumw2[1:-1] = sumw22d.T.flat

        # stats in 3D
        # stats[0] = sumw
        # stats[1] = sumw2
        # stats[2] = sumwx
        # stats[3] = sumwx2
        # stats[4] = sumwy
        # stats[5] = sumwy2
        # stats[6] = sumwxy
        # stats[7] = sumwz
        # stats[8] = sumwz2
        # stats[9] = sumwxz
        # stats[10]= sumwyz

        stats3d = ROOT.TArrayD(11)
        hTotal_rolled.GetStats(stats3d.GetArray())
        stats1d = ROOT.TArrayD(4)
        stats1d[0] = stats3d[0]
        stats1d[1] = stats3d[1]
        stats1d[2] = stats3d[2] + stats3d[4] + stats3d[7]
        stats1d[3] = stats3d[3] + stats3d[5] + stats3d[8]
        hTotal.PutStats(stats1d.GetArray())

        hTotal_rolled.Delete()

    return hTotal


def postProcessNuisances(filename, samples, aliases, variables, cuts, nuisances):
    """
    Post process nuisances of type weight_[envelope/rms/square].
    For each nuisance/cut/variable/sample will take many histograms in input and only save Up and Down histograms

    Parameters
    ----------
    filename : str
        path to input root file
    samples : dict
        configuration samples
    aliases : dict
        configuration aliases
    variables : dict
        configuration variables
    cuts : dict
        configuration cuts
    nuisances : dict
        configuration nuisances
    """
    import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils

    f = ROOT.TFile.Open(filename, "update")
    # post process -> nuisance envelops and RMS

    categoriesmap = utils.flatten_cuts(cuts)
    for nuisance in nuisances.keys():
        if not (
            nuisances[nuisance].get("kind", "").endswith("envelope")
            or nuisances[nuisance].get("kind", "").endswith("rms")
            or nuisances[nuisance].get("kind", "").endswith("square")
        ):
            continue
        
        nuisanceKind = nuisances[nuisance]["kind"].split("_")[1]
        print("work for ", nuisance)
        subsamplesmap = utils.flatten_samples(samples)
        utils.update_variables_with_categories(variables, categoriesmap)
        utils.update_nuisances_with_subsamples(nuisances, subsamplesmap)
        utils.update_nuisances_with_categories(nuisances, categoriesmap)
        _cuts = list(cuts.keys())
        _samples = list(samples.keys())
        for cut in _cuts:
            for variable in variables.keys():
                f.cd(f"/{cut}/{variable}")
                print("work in ", cut, variable)
                for sampleName in _samples:
                    limitSamples = nuisances[nuisance].get("samples", {})
                    if not (
                        len(limitSamples.keys()) == 0
                        or sampleName in limitSamples.keys()
                    ):
                        continue
                    weights = nuisances[nuisance]["samples"][sampleName]
                    histoNameToProcess = [f"histo_{sampleName}_{nuisances[nuisance]['name']}_SPECIAL_NUIS_{nuisanceKind}" + str(i) for i in range(0, len(weights))]
                    hNominal = ROOT.gDirectory.Get(f"histo_{sampleName}")
                    hName = f"histo_{sampleName}_{nuisances[nuisance]['name']}"
                    vnominal = rnp_hist2array(hNominal, include_overflow=True, copy=False)
                    variations = np.empty((len(weights), vnominal.size), dtype=vnominal.dtype)
                    arrup = 0
                    arrdo = 0
                    for ivar in range(len(weights)):
                        hVar = ROOT.gDirectory.Get(histoNameToProcess[ivar])
                        variations[ivar, :] = rnp_hist2array(hVar, include_overflow=True, copy=True)
                    if nuisanceKind == "envelope":
                        arrup = np.max(variations, axis=0)
                        arrdo = np.min(variations, axis=0)
                    elif nuisanceKind == "rms":
                        arrnom = np.tile(vnominal.flat, (variations.shape[0], 1))
                        arrv = np.sqrt(np.mean(np.square(variations - arrnom), axis=0))
                        arrup = vnominal + arrv
                        arrdo = vnominal - arrv
                    elif nuisanceKind == 'square':
                        vnominal = rnp_hist2array(
                            hNominal, include_overflow=True, copy=True
                        )
                        arrnom = np.tile(vnominal, (variations.shape[0], 1))
                        arrv = np.sqrt(np.sum(np.square(variations - arrnom), axis=0))
                        arrup = vnominal + arrv
                        arrdo = vnominal - arrv
                    else:
                        continue
                    print(arrup)
                    print(arrdo)
                    histoNameUp     = hName + "Up"
                    histoNameDown   = hName + "Down"
                    outputHistoUp   = hNominal.Clone(histoNameUp)
                    outputHistoDown = hNominal.Clone(histoNameDown)
                    rnp_array2hist(arrup, outputHistoUp)
                    rnp_array2hist(arrdo, outputHistoDown)
                    outputHistoUp.Write()
                    outputHistoDown.Write()
    f.Close()
