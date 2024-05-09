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


def rnp_hist2array(h, include_overflow=False, copy=True, return_errors=False):
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

    if return_errors:
        errors = np.sqrt(rnp_array(h.GetSumw2(), copy=copy))
    else:
        errors = np.zeros_like(arr)

    arr = arr.reshape(shape)
    errors = errors.reshape(shape)
    if not include_overflow:
        slices = []
        for axis, bins in enumerate(shape):
            slices.append(slice(1, -1))
        arr = arr[tuple(slices)]
        errors = errors[tuple(slices)]
    arr = np.transpose(arr)
    errors = np.transpose(errors)
    if return_errors:
        return arr, errors
    return arr


def rnp_array2hist(array, h, errors=None):
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

    if errors is not None:
        if errors.shape != array.shape:
            raise ValueError(
                "Bin contents and Bin errors have different shapes",
                array.shape,
                errors.shape,
            )
        _errors = errors
    else:
        # dummy vector, it won't be set at the end
        _errors = np.zeros_like(array)

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
        errors_overflow = np.zeros(shape, dtype=dtype)
        array_overflow[tuple(slices)] = array
        errors_overflow[tuple(slices)] = _errors
        array = array_overflow
        _errors = errors_overflow

    if array.shape != shape:
        raise ValueError("array2hist: Different shape between array and h")

    array = np.ravel(np.transpose(array))
    _errors = np.ravel(np.transpose(_errors))

    nx = len(array)
    arr = memoryview(array)
    h.Set(nx, arr)
    if errors is not None:
        h.SetError(_errors)
