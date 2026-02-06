import ROOT
import numpy as np
from mkShapesRDF.shapeAnalysis import rnp
from mkShapesRDF.shapeAnalysis import histo_utils

ROOT.gROOT.SetBatch(True)

rng = np.random.Generator(np.random.PCG64(1281))


def test_array2hist():
    nbins_x = 10
    nbins_y = 15

    nbins_x_with_fold = nbins_x + 2
    nbins_y_with_fold = nbins_y + 2

    bin_content = rng.normal(120, 8, size=(nbins_x_with_fold, nbins_y_with_fold))
    bin_error = rng.normal(48, 2, size=(nbins_x_with_fold, nbins_y_with_fold))

    h = ROOT.TH2D("", "", nbins_x, 0, 1, nbins_y, 0, 1)

    # just for test
    rnp.rnp_array2hist(bin_content, h)
    _ = rnp.rnp_hist2array(
        h, include_overflow=True, copy=True
    )

    # now the actual set and get method
    rnp.rnp_array2hist(bin_content, h, bin_error)

    bin_content2, bin_error2 = rnp.rnp_hist2array(
        h, include_overflow=True, copy=True, return_errors=True
    )

    assert bin_content.shape == bin_content2.shape
    assert np.all(bin_content == bin_content2)
    assert bin_error.shape == bin_error2.shape
    assert np.all(bin_error == bin_error2)

    # No fold
    h_unroll = histo_utils.postPlot(h, doFold=0, unroll=True, delete_oldHisto=False)

    # We are good people -> we work x-major
    bin_content3, bin_error3 = rnp.rnp_hist2array(
        h, include_overflow=False, copy=True, return_errors=True
    )
    bin_content3 = bin_content3.flatten()
    bin_error3 = bin_error3.flatten()
    bin_content4, bin_error4 = rnp.rnp_hist2array(
        h_unroll, include_overflow=False, copy=True, return_errors=True
    )

    assert bin_content3.shape == bin_content4.shape
    assert np.all(bin_content3 == bin_content4)
    assert bin_error3.shape == bin_error4.shape
    assert np.all(bin_error3 == bin_error4)

    # Do fold
    h_for_unroll = h.Clone()
    h_for_unroll.SetName("tmp2") # just to suppress warning of memoryleak
    h_unroll = histo_utils.postPlot(h_for_unroll, doFold=3, unroll=True, delete_oldHisto=False)

    # We're passing below h which has 2 dimension -> bin_content3 will be 2D
    # We are good people -> we work x-major
    bin_content3, bin_error3 = rnp.rnp_hist2array(
        h, include_overflow=True, copy=True, return_errors=True
    )


    bin_content3 = bin_content3[1:-1, 1:-1]
    bin_error3 = bin_error3[1:-1, 1:-1]

    edges = np.zeros_like(bin_content3) != 0.0
    edges[0, :] = True
    edges[-1, :] = True
    edges[:, 0] = True
    edges[:, -1] = True

    bin_content3 = bin_content3.flatten()
    bin_error3 = bin_error3.flatten()
    edges = edges.flatten()
    bin_content4, bin_error4 = rnp.rnp_hist2array(
        h_unroll, include_overflow=False, copy=True, return_errors=True
    )

    # Here we know that the bin content of under and overflow was folded
    # we therefore expect the bin content to be different in the edges

    assert bin_content3.shape == bin_content4.shape
    assert np.all(bin_content3[~edges] == bin_content4[~edges])
    assert np.all(bin_content3[edges] != bin_content4[edges])
    assert bin_error3.shape == bin_error4.shape
    assert np.all(bin_error3[~edges] == bin_error4[~edges])
    assert np.all(bin_error3[edges] != bin_error4[edges])


test_array2hist()
print('Good, no errors for now ;)')