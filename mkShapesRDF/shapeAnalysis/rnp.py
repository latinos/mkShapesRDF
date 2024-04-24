import ROOT
import numpy as np

ROOT.TH1.SetDefaultSumw2(True)


def rnp_array(array, copy=True):
    """
    Convert TArray into numpy.array

    Parameters
    ----------
    array : ROOT.TArray
        a ROOT TArrayD
    copy : bool, optional
        if True returns a copy, by default True

    Returns
    -------
    np.array
        converted numpy array
    """
    if not isinstance(array, ROOT.TArrayD):
        raise ValueError("Cannot convert ", array, "to TArrayD")
    dtype = np.double
    nx = len(array)
    arr = np.ndarray((nx,), dtype=dtype, buffer=array.GetArray())
    if copy:
        arr = arr.copy()
    return arr


def rnp_hist2array(h, include_overflow=False, copy=True):
    """
    Converts histogram into a numpy array

    Parameters
    ----------
    h : ROOT.TH1, ROOT.TH2, ROOT.TH3
        histogram, 1, 2 or 3D
    include_overflow : bool, optional
        Includes underflow and overflow bins, by default False
    copy : bool, optional
        if true returns a copy of the array, its modification won't affect the histogram, by default True

    Returns
    -------
    np.array
        converted numpy array
    """
    arr = rnp_array(h, copy=copy)
    if isinstance(h, ROOT.TH3):
        shape = (h.GetNbinsZ() + 2, h.GetNbinsY() + 2, h.GetNbinsX() + 2)
    elif isinstance(h, ROOT.TH2):
        shape = (h.GetNbinsY() + 2, h.GetNbinsX() + 2)
    elif isinstance(h, ROOT.TH1):
        shape = (h.GetNbinsX() + 2,)
    arr = arr.reshape(shape)
    if not include_overflow:
        slices = []
        for axis, bins in enumerate(shape):
            slices.append(slice(1, -1))
        arr = arr[tuple(slices)]
    return arr


def rnp_array2hist(array, h):
    """
    Sets bin contents with a numpy array, modifying it in place

    Parameters
    ----------
    array : np.array
        numpy array with counts
    h : ROOT.TH1, ROOT.TH2, ROOT.TH3
        histogram
    """
    dtype = np.double
    if isinstance(h, ROOT.TH3):
        shape = (h.GetNbinsX() + 2, h.GetNbinsY() + 2, h.GetNbinsZ() + 2)
    elif isinstance(h, ROOT.TH2):
        shape = (h.GetNbinsX() + 2, h.GetNbinsY() + 2)
    elif isinstance(h, ROOT.TH1):
        shape = (h.GetNbinsX() + 2,)
    if array.shape != shape:
        slices = []
        for axis, bins in enumerate(shape):
            if array.shape[axis] == bins - 2:
                slices.append(slice(1, -1))
            elif array.shape[axis] == bins:
                slices.append(slice(None))
            else:
                raise ValueError("array and histogram are not compatible")
        array_overflow = np.zeros(shape, dtype=dtype)
        array_overflow[tuple(slices)] = array
        array = array_overflow
    if array.shape != shape:
        raise "array2hist: Different shape between array and h"
    array = np.ravel(np.transpose(array))
    nx = len(array)
    arr = memoryview(array)
    h.Set(nx, arr)
