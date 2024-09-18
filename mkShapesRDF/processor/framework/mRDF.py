import ROOT
from fnmatch import fnmatch
from mkShapesRDF.lib.parse_cpp import ParseCpp


class mRDF:
    r"""Private version of RDataFrame that allows to define new columns, drop columns, and use Vary together with Snapshot."""

    def __init__(self):
        r"""Initialize the mRDF object."""
        self.df = 0  #: df stores the RDataFrame object
        self.cols = []  #: cols stores the list of columns
        self.cols_d = []  #: cols_d stores the list of columns that were dropped
        self.variations = {}  #: variations stores the list of variations

    @staticmethod
    def variationNaming(variationName, variationTag, col=""):
        """
        Naming convention for variations.

        Given a variation name and a tag it will return ``{variationName}{variationTag}``.
        If a column name is provided, it will return ``col_{variationName}{variationTag}``.

        Parameters
        ----------
        variationName : str
            Variation name
        variationTag : str
            Variation tag
        col : str, optional, default: ""
            column name that has the variation

        Returns
        -------
        str
            formatted string
        """
        if col == "":
            return variationName + variationTag
        else:
            return col + "_" + variationName + variationTag

    def setNode(self, dfNode, cols, cols_d, variations):
        r"""Set internal variables of an ``mRDF`` object to the provided ones

        Parameters
        ----------
        dfNode : ROOT.RDataFrame
            The RDataFrame object

        cols : `list of str`
            The list of columns of the RDataFrame

        cols_d : `list of str`
            The list of columns that were dropped

        variations : dict
            The `dict` of variations

        Returns
        -------
        mRDF
            The ``mRDF`` object with the internal variables set to the provided ones

        """
        self.df = dfNode
        self.cols = cols
        self.cols_d = cols_d
        self.variations = variations
        return self

    def Copy(self):
        r"""Copy the ``mRDF`` object

        Returns
        -------
        mRDF
            The copy of the ``mRDF`` object
        """

        c = mRDF()
        c.setNode(self.df, self.cols.copy(), self.cols_d.copy(), self.variations.copy())
        return c

    def readRDF(self, *ar, **kw):
        r"""Read the RDataFrame object and create the special column ``CUT`` used to hold the different Filters

        Parameters
        ----------
        ar : list
            The list of arguments to be passed to the RDataFrame constructor

        kw : dict
            The dictionary of keyword arguments to be passed to the RDataFrame constructor

        Returns
        -------
        mRDF
            The ``mRDF`` object with the new RDataFrame object stored

        """
        try:
            self.df = ROOT.RDataFrame(*ar, **kw).Define("CUT", "true")
        except:
            self.df = ROOT.RDataFrame(*ar, **kw).Redefine("CUT", "true")
        self.cols = list(map(lambda k: str(k), self.df.GetColumnNames()))
        return self

    def Define(self, a, b, excludeVariations=[]):
        r"""Define a new column, if the column already exists redefine it.

        Parameters
        ----------
        a : str
            The name of the new column

        b : str
            The expression to be evaluated to define the new column

        excludeVariations : `list of str`, optional, default: []
            List of pattern of variations to exlude. If ``*`` is used, all variations will
            be excluded and the defined column will be nominal only.

        Returns
        -------
        mRDF
            The ``mRDF`` object with the new column defined

        Notes
        -----
        If ``excludeVariations`` is ``[]``, the define expression (``b``) will be checked for all possible variations.
        If variations of the define expression are found, they will be defined for the new column as well
        (i.e. varied ``b`` will be defined as variations of ``a``).
        """

        c = self.Copy()

        if a not in (c.cols + c.cols_d):
            c.df = c.df.Define(a, b)
        else:
            c.df = c.df.Redefine(a, b)
        c.cols = list(set(c.cols + [a]))

        # check variations
        depVars = ParseCpp.listOfVariables(ParseCpp.parse(b))
        variations = {}
        for variationName in c.variations.keys():
            if len([1 for x in excludeVariations if fnmatch(variationName, x)]) > 0:
                # if variationName matches a pattern of excludeVariations, skip it
                continue

            s = list(
                filter(lambda k: k in depVars, c.variations[variationName]["variables"])
            )
            if len(s) > 0:
                # only register variations if they have an impact on "a" variable
                variations[variationName] = {
                    "tags": c.variations[variationName]["tags"],
                    "variables": s,
                }

        for variationName in variations.keys():
            varied_bs = []
            for tag in variations[variationName]["tags"]:
                varied_b = ParseCpp.parse(b)
                for variable in variations[variationName]["variables"]:
                    varied_b = ParseCpp.replace(
                        varied_b,
                        variable,
                        mRDF.variationNaming(variationName, tag, variable),
                    )
                varied_bs.append(ParseCpp.format(varied_b))
            _type = c.df.GetColumnType(a)
            expression = (
                ParseCpp.RVecExpression(_type) + " {" + ", ".join(varied_bs) + "}"
            )
            c = c.Vary(a, expression, variations[variationName]["tags"], variationName)

        return c

    def Redefine(self, a, b):
        """ """
        return self.Define(a, b)

    def Vary(self, colName, expression, variationTags=["down", "up"], variationName=""):
        """
        Define variations for an existing column, given an expression

        Parameters
        ----------
        colName : str
            nominal column name
        expression : str
            a valid C++ expression that defines the variations
        variationTags : list, optional, default: ``["down", "up"]``
            list of tags to be used for the variations (len must be 2)
        variationName : str, optional, default: ""
            name of the variation

        Returns
        -------
        mRDF
            The ``mRDF`` object with the variations defined

        Notes
        -----
        ``Vary`` will call ``Define`` internally to define a temporary variable that contains the varied expression.
        Since also ``Define`` will call ``Vary`` internally, the user should be careful to not end up in an infinite loop!

        Examples
        --------
        When defining the same variation twice for different nominal variables, the tags must be the same (order does not matter)

        >>> df = df.Vary("var", "var + 1", ["down", "up"], "var_JER_0")
        >>> df = df.Vary("var2", "var2 + 2", [ "up", "down"], "var_JER_0")

        References
        ----------
        See the official ``RDataFrame::Vary()`` `documentation <https://root.cern/doc/master/classROOT_1_1RDF_1_1RInterface.html#a84d15369c945e4fe85e919224a0fc99f>`_
        even if not used here (not compatible with ``Snapshot``).

        """
        
        c = self.Copy()
        if variationName not in c.variations.keys():
            c.variations[variationName] = {"tags": variationTags, "variables": []}
        else:
            if not (
                variationTags[0] in c.variations[variationName]["tags"]
                and variationTags[1] in c.variations[variationName]["tags"]
            ):
                print("Using different tags for same variation is not allowed")
                print("You should use tags", c.variations[variationName]["tags"])

        c.variations[variationName]["variables"] = list(
            set(c.variations[variationName]["variables"] + [colName])
        )
        
        for i, variationTag in enumerate(variationTags):
            
            c = c.Define(
                mRDF.variationNaming(variationName, variationTag, colName),
                expression + "[" + str(i) + "]",
                excludeVariations=["*"],
            )

        return c

    def Filter(self, string):
        """
        Filter the mRDF, the filter is sensitive to Variations through the use of ``CUT``, see the notes.

        Parameters
        ----------
        string : str
            the filter expression

        Returns
        -------
        mRDF
            The ``mRDF`` object with the filter applied

        Notes
        -----
        If the filter expression contains a variable for which variation are already defined,
        the ``CUT`` will be varied accordingly. Only events that pass at least one of the varied ``CUT`` (or the nominal)
        will be considered.
        """
        c = self.Copy()
        c = c.Define("CUT", "CUT && (" + string + ")")

        # consider only events that pass at least one of the varied CUT
        variationNames = c.GetVariationsForCol("CUT")
        varied_bs = []
        for variationName in variationNames:
            for tag in c.variations[variationName]["tags"]:
                varied_bs.append(mRDF.variationNaming(variationName, tag, "CUT"))

        nom_and_variations = ["CUT"] + varied_bs
        filterExpr = " || ".join(nom_and_variations)
        c.df = c.df.Filter(filterExpr)
        return c

    def GetColumnNames(self):
        """ """
        return self.cols

    def GetVariations(self):
        """ """
        return self.variations

    def GetVariationsForCol(self, column):
        """
        Get the list of variations for a given column

        Parameters
        ----------
        column : str
            the nominal column name

        Returns
        -------
        list
            list of all variations defined for the given column
        """
        variations = []
        for variationName in self.variations.keys():
            if column in self.variations[variationName]["variables"]:
                variations.append(variationName)
        return variations

    def GetVariedColumns_oneVariation(self, columns, variationName, tag):
        """
        Given a list of columns, return the varied columns for a given variation and tag

        Parameters
        ----------
        columns : `list of str`
            list of columns to search variations for
        variationName : str
            the variation name
        tag : str
            the variation tag

        Returns
        -------
        `list of str`
            List of varied columns for the given variation and tag
        """

        tmp_varied_cols = list(
            set(columns).intersection(set(self.variations[variationName]["variables"]))
        )

        tmp_varied_cols = list(
            map(
                lambda k: mRDF.variationNaming(variationName, tag, k),
                tmp_varied_cols,
            )
        )
        return tmp_varied_cols

    def GetVariedColumns(self, columns):
        """
        Given a list of columns, return the varied columns for all variations and tags

        Parameters
        ----------
        columns : `list of str`
            list of columns to search variations for

        Returns
        -------
        `list of str`
            List of varied columns for all variations and tags
        """

        tmp_varied_cols = []
        for variationName in self.variations:
            for tag in self.variations[variationName]["tags"]:
                tmp_varied_cols += self.GetVariedColumns_oneVariation(
                    columns, variationName, tag
                )
        return tmp_varied_cols

    def DropColumns(self, pattern, includeVariations=True):
        """
        Drop columns that match the given pattern

        Parameters
        ----------
        pattern : str
            the pattern to be matched
        includeVariations : bool, optional, default: True
            whether to include variations or not

        Returns
        -------
        mRDF
            The ``mRDF`` object with the columns dropped

        Notes
        -----
        The columns from ``self.cols`` matching the pattern will be dropped and added to ``self.cols_d``.
        If ``includeVariations`` is ``True``, the variations of the dropped columns will be dropped as well.
        """
        c = self.Copy()
        tmp_cols_d = list(set(filter(lambda k: fnmatch(k, pattern), c.cols)))
        if len(tmp_cols_d) == 0:
            print("Warning: no columns found to drop with pattern", pattern)

        tmp_varied_cols_d = c.GetVariedColumns(columns=tmp_cols_d)

        if includeVariations:
            tmp_cols_d = list(set(tmp_cols_d).union(set(tmp_varied_cols_d)))
        else:
            tmp_cols_d = list(set(tmp_cols_d).difference(set(tmp_varied_cols_d)))

        # print('Deleting columns', tmp_cols_d)
        c.cols_d = list(set(c.cols_d + tmp_cols_d))
        c.cols = list(set(c.cols).difference(tmp_cols_d))
        return c

    def Count(self):
        r"""Count the number of events

        Returns
        -------
        `Proxy<Long64_t>`
            The number of events (need to apply ``GetValue()`` to get the actual value)
        """
        return self.df.Count()

    def Sum(self, string):
        r"""Sum the values of a column

        Parameters
        ----------
        string : str
            the column name

        Returns
        -------
        `Proxy<Float_t>`
            The sum of the values of the column (need to apply ``GetValue()`` to get the actual value)

        """
        return self.df.Sum(string)

    # def Snapshot(self, *args, **kwargs):
    #     """
    #     Produce a Snapshot of the mRDF and return it
    #
    #     Parameters
    #     ----------
    #     *args : list
    #         list of arguments to be passed to the ``RDataFrame::Snapshot`` method
    #
    #     **kwargs : dict
    #         dictionary of keyword arguments to be passed to the ``RDataFrame::Snapshot`` method
    #
    #
    #     Returns
    #     -------
    #     `Snapshot` or `Proxy<Snapshot>`
    #         The ``Snapshot`` object, or a ``Proxy<Snapshot>`` if ``lazy=True`` is passed as a keyword argument
    #     """
    #     return self.df.Snapshot(*args, **kwargs)
    #
    def Snapshot(self, treeName, fileName, columns, isNominal=True, *args, **kwargs):
        """
        Produce a Snapshot of the mRDF and return it

        Parameters
        ----------
        *args : list
            list of arguments to be passed to the ``RDataFrame::Snapshot`` method

        **kwargs : dict
            dictionary of keyword arguments to be passed to the ``RDataFrame::Snapshot`` method


        Returns
        -------
        `Snapshot` or `Proxy<Snapshot>`
            The ``Snapshot`` object, or a ``Proxy<Snapshot>`` if ``lazy=True`` is passed as a keyword argument
        """
        # events = ak.from_rdataframe(self.df, columns)
        # def function(columns, ):
        import uproot
        import awkward as ak
        import numpy as np
        from math import ceil

        def call(df):
            chunksize = 10_000
            nIterations = max(ceil(df.Count().GetValue() / chunksize), 1)
            outFile = uproot.recreate(fileName, compression=uproot.LZMA(9))
            branches = columns.copy()
            print(branches)
            #####
            ##### Temporal fix / remove branches with type: string -> incompatbility with awkward/uproot
            if "BeamSpot_type" in branches:
                branches.remove("BeamSpot_type")
            if "Photon_seediEtaOriX" in branches:
                branches.remove("Photon_seediEtaOriX")
            if "Electron_seediEtaOriX" in branches:
                branches.remove("Electron_seediEtaOriX")
            _branches = branches.copy()
            CollectionsToZip = ['CleanJet','WH3l_dphilmet','WH3l_mtlmet','MET','Jet','PuppiMET','Lepton_tightMuon','Lepton_tightElectron','Lepton_isTightElectron','Lepton_isTightMuon','Lepton',
                                'Muon','Electron','Photon','Gen','LHE','HLT','L1','Tau','IsoTrack','GenPart','LHEPart','TrigObj','LepCut2l','LepCut3l','LepCut4l','NeutrinoGen','SubJet',
                                'ChsMET','LeptonGen','FatJet','LepSF2l','LepSF3l','LepSF4l','PhotonGen','DressedLepton','GenDressedLepton','SubGenJetAK8','LowPtElectron','VetoLepton',
                                'BeamSpot','LHEWeight','GenIsolatedPhoton','RawMET','TkMET','CorrT1METJet','boostedTau','newJet','GenJet','TriggerEffWeight','TriggerSFWeight',
                                'GenJetAK8','Flag','puWeight','Pileup','GenProton','HTXS', 'GenVtx','Generator','Trigger','GenVisTau','RawPuppiMET','SoftActivityJet',
                                'CaloMET','Rho','FsrPhoton','DeepMETResponseTune','PV','SV','GenMET','DeepMETResolutionTune','gen','OtherPV']

            zips = {}            
            for zipName in CollectionsToZip:
                zipBranches = list(filter(lambda k: k.startswith(zipName + '_'), branches))
                zips[zipName] = zipBranches
                branches = list(set(branches).difference(zipBranches))

            for i in range(nIterations):
                _df = df.Range( i * chunksize, (i+1) * chunksize)
                events = ak.from_rdataframe(_df, _branches)
                def getBranch(events, branch):
                    if 'float64' in str(events[branch].type):
                        return ak.values_astype(events[branch],'float32')
                    return events[branch]
                
                d = {}
                for zipName in zips:
                    z = {}
                    for branch in zips[zipName]:
                        z[branch[len(zipName)+1:]] = getBranch(events, branch)

                    if len(list(z.keys())) == 0:
                        # print('No columns found to zip for collection', zipName)
                        continue

                    d[zipName] = ak.zip(z)

                for branch in branches:
                    d[branch] = getBranch(events, branch).to_list()

                _events = ak.Array(d)                
                if treeName not in outFile:
                    if len(_events) == 0:
                        print("Not needed!!!")
                        dtypes = {}
                        for branch in _events.fields:
                            dtypes[branch] = _events[branch].type
                        # print(dtypes)
                        # print('Creating ttree')
                        outFile.mktree(treeName, dtypes)
                        continue
                    else:
                        outFile[treeName] = d
                        continue

                outFile[treeName].extend(d)

            outFile.close()

        return (call, columns)
        
    def Histo1D(self, *args):
        """
        Produce a TH1D of the mRDF and return it 
        Parameters 
        ----------
        *args : list 
            list of arguments to be passed to the ``RDataFrame::Histo1D`` method  
        Returns
        -------   
        `Proxy<TH1D>` 
        """
        return self.df.Histo1D(*args)

    def Range(self, nEvents):
        """
        Filter the dataframe to get a subset of events
        Parameters
        ----------
        *args : list
        list of arguments to be passed to the ``RDataFrame::Range`` method
        Returns
        -------
        The mRDF objects with a new range of events
        """
        c = self.Copy()
        c.df = c.df.Range(nEvents)
        return c
