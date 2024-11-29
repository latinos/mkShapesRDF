"""
Defines the samples and the list of files together with the weights to use for them.

Examples
--------

>>> from mkShapesRDF.lib.search_files import SearchFiles
>>> searchFiles = SearchFiles()
>>> redirector = ""


>>> mcProduction = "Summer16_102X_nAODv7_Full2016v7"
>>> dataReco = "Run2016_102X_nAODv7_Full2016v7"
>>> mcSteps = "MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7"
>>> fakeSteps = "DATAl1loose2016v7__l2loose__fakeW"
>>> dataSteps = "DATAl1loose2016v7__l2loose__l2tightOR2016v7"
>>> ##############################################
>>> ###### Tree base directory for the site ######
>>> ##############################################
>>> treeBaseDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano"
>>> limitFiles = -1
>>> def makeMCDirectory(var=""):
>>>     _treeBaseDir = treeBaseDir + ""
>>>     if redirector != "":
>>>         _treeBaseDir = redirector + treeBaseDir
>>>     if var == "":
>>>         return "/".join([_treeBaseDir, mcProduction, mcSteps])
>>>     else:
>>>         return "/".join([_treeBaseDir, mcProduction, mcSteps + "__" + var])
>>>
>>>
>>> mcDirectory = makeMCDirectory()
>>> fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
>>> dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)



>>> samples = {}
>>> DataRun = [
>>>     ["B", "Run2016B-02Apr2020_ver2-v1"],
>>>     ["C", "Run2016C-02Apr2020-v1"],
>>>     ["D", "Run2016D-02Apr2020-v1"],
>>>     ["E", "Run2016E-02Apr2020-v1"],
>>>     ["F", "Run2016F-02Apr2020-v1"],
>>>     ["G", "Run2016G-02Apr2020-v1"],
>>>     ["H", "Run2016H-02Apr2020-v1"],
>>> ]
>>> DataSets = ["MuonEG", "SingleMuon", "SingleElectron", "DoubleMuon", "DoubleEG"]
>>> DataTrig = {
>>>     "MuonEG": " Trigger_ElMu",
>>>     "SingleMuon": "!Trigger_ElMu && Trigger_sngMu",
>>>     "SingleElectron": "!Trigger_ElMu && !Trigger_sngMu && Trigger_sngEl",
>>>     "DoubleMuon": "!Trigger_ElMu && !Trigger_sngMu && !Trigger_sngEl && Trigger_dblMu",
>>>     "DoubleEG": "!Trigger_ElMu && !Trigger_sngMu && !Trigger_sngEl && !Trigger_dblMu && Trigger_dblEl",
>>> }


>>> mcCommonWeightNoMatch = "XSWeight*SFweight*METFilter_MC"
>>> mcCommonWeight = "XSWeight*SFweight*PromptGenLepMatch2l*METFilter_MC"
>>> 
>>> 
>>> ###### Zjj EWK #######
>>> 
>>> files = nanoGetSampleFiles(mcDirectory, "EWK_LLJJ_MLL-50_MJJ-120")
>>> 
>>> samples["Zjj"] = {
>>>     "name": files,
>>>     "weight": mcCommonWeight,
>>>     "FilesPerJob": 1,
>>> }


>>> 
>>> ###### DY MC ######
>>> # example of subsamples
>>> dys = {
>>>     "DY_hardJets": "hardJets",
>>>     "DY_PUJets": "PUJets",
>>>     "DY_inclusive_rwgt": ("true", "0.8"), 
>>>     # passing as a value a tuple/list of len 2 one can 
>>>     # assign a custom multiplicative weight to this subsample
>>>     # aliases can be used inside subsampleCut or subsampleWeight
>>> }
>>> 
>>> files = nanoGetSampleFiles(mcDirectory, "DYJetsToLL_M-50_ext2")
>>> 
>>> samples["DY"] = {
>>>     "name": files,
>>>     "weight": mcCommonWeight
>>>     + "*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0)) * ewknloW",
>>>     "FilesPerJob": 5,
>>>     "subsamples": dys,
>>>     "flatten_samples_map": 1 
>>>     # By default (flatten_samples_map=0), subsamples will carry the sample
>>>     # name as prefix (e.g. DY_DY_hardJets, DY_DY_PUJets, ...). By specifying 
>>>     # flatten_samples_map=1 the sample prefix will be dropped and subsamples
>>>     # names will be the one appearing in the subsamples dictionary keys 
>>>     # (for this example subsample shape names will be DY_hardJets, DY_PUJets)
>>> }



>>> ###########################################
>>> ################## DATA ###################
>>> ###########################################
>>> 
>>> samples["DATA"] = {
>>>     "name": [],
>>>     "weight": "METFilter_DATA*LepWPCut",
>>>     "weights": [],
>>>     "isData": ["all"],
>>>     "FilesPerJob": 50,
>>> }
>>> 
>>> for _, sd in DataRun:
>>>     for pd in DataSets:
>>>         files = nanoGetSampleFiles(dataDirectory, pd + "_" + sd)
>>> 
>>>         samples["DATA"]["name"].extend(files)
>>>         addSampleWeight(samples, "DATA", pd + "_" + sd, DataTrig[pd])
>>>         # samples['DATA']['weights'].extend([DataTrig[pd]] * len(files))
"""
# flake8: noqa E266
from mkShapesRDF.lib.search_files import SearchFiles
import os



def nanoGetSampleFiles(path, name):
    """
    Retrieve files given path and name

    Parameters
    ----------
    path : str
        path to folder where to look for files
    name : str
        name of the file to look for

    Returns
    -------
    `list of tuple`
        list of tuples in the form of ``(name, list of files)``

    Notes
    -----
    This function uses SearchFiles (the object ``searchFile``) to retrieve the files and the Latino naming convention is assumed.
    The ``redirector`` defined above is also used.

    """
    _files = searchFiles.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]


def CombineBaseW(samples, proc, samplelist):
    """
    Combine baseW for a given process. 
    
    If two samples (different names) enter the same phase space the new baseW will consider 
    the XS and the sum of all ``genEventSumw`` across all the files.

    Parameters
    ----------
    samples : dict
        dictionary of samples
    proc : str
        the samples key for the process
    samplelist : `list of str`
        list of sample name inside ``samples[proc]`` to combine

    Notes
    -----
    Will call ``addSampleWeight`` for each sample in ``samplelist``.

    """
    _filtFiles = list(filter(lambda k: k[0] in samplelist, samples[proc]["name"]))
    _files = list(map(lambda k: k[1], _filtFiles))
    _l = list(map(lambda k: len(k), _files))
    leastFiles = _files[_l.index(min(_l))]
    dfSmall = ROOT.RDataFrame("Runs", leastFiles)
    s = dfSmall.Sum("genEventSumw").GetValue()
    f = ROOT.TFile(leastFiles[0])
    t = f.Get("Events")
    t.GetEntry(1)
    xs = t.baseW * s

    __files = []
    for f in _files:
        __files += f
    df = ROOT.RDataFrame("Runs", __files)
    s = df.Sum("genEventSumw").GetValue()
    newbaseW = str(xs / s)
    weight = newbaseW + "/baseW"

    for iSample in samplelist:
        addSampleWeight(samples, proc, iSample, weight)


def addSampleWeight(samples, sampleName, sampleNameType, weight):
    """ 
    Add weight to a sample

    Parameters
    ----------
    samples : dict
        dictionary of samples
    sampleName : str
        the samples key for the process
    sampleNameType : str
        the sample name inside ``samples[proc]`` to add the weight to
    weight : str
        the weight to add


    """
    obj = list(filter(lambda k: k[0] == sampleNameType, samples[sampleName]["name"]))[0]
    samples[sampleName]["name"] = list(
        filter(lambda k: k[0] != sampleNameType, samples[sampleName]["name"])
    )
    if len(obj) > 2:
        samples[sampleName]["name"].append(
            (obj[0], obj[1], obj[2] + "*(" + weight + ")")
        )
    else:
        samples[sampleName]["name"].append((obj[0], obj[1], "(" + weight + ")"))

