import ROOT
from fnmatch import fnmatch
from mkShapesRDF.processor.framework.module import Module
import sys
import subprocess


class Snapshot(Module):
    """
    The Snapshot module handles the creation of the final output files.
    There are 4 possible scenarios:

    - snapshot nominals only
    - snapshot variations only in separate files (one file per variation)
    - snapshot nominals and variation in separate files (one file per variation and one file for nominal)
    - snapshot both nominals and variations in the same file

    The module does not run the snapshotting itself, but it creates the Snapshot objects with lazy evaluation.
    The snapshots to be run are added to the ``values`` variable:

    .. code-block:: python

        values.append(
            [
                "snapshot",
                SnapshotObject,
                [tmpOutputFilename, copyFromInputFiles , outputFolderPath, outputFilenameEOS]
            ])

    Where

    - ``tmpOutputFilename`` is the name of the temporary output file,
    - ``copyFromInputFiles`` is a boolean that indicates if the  auxiliary keys of the input files should be copied in the output (only done for nominals),
    - ``outputFolderPath`` is the path of the output folder
    - ``outputFilenameEOS`` is the name of the output file in the EOS folder (final output file name)

    """

    def __init__(
        self,
        tmpOutputFilename,
        columns,
        eosPath,
        outputFilename,
        includeVariations=True,
        splitVariations=True,
        storeNominals=True,
        outputMap={}
    ):
        super().__init__("Snapshot")
        self.tmpOutputFilename = tmpOutputFilename
        self.columns = columns

        self.eosPath = eosPath
        self.outputFilename = outputFilename

        self.includeVariations = includeVariations
        self.splitVariations = splitVariations
        self.storeNominals = storeNominals
        self.outputMap = outputMap

    @staticmethod
    def CopyFromInputFiles(outputFilename, inputFiles):
        """
        Copy the auxiliary keys from the input files into the output file.

        It ``hadd``s the input files into a temporary file, then it copies the keys from the temporary file into the output file.

        Parameters
        ----------
        outputFilename : str
            The name of the output file where to copy the keys (should be equal to ``tmpOutputFilename``)
        inputFiles : `list of str`
            The list of input files from which to copy the keys

        """
        # copy other information from inputFiles into the outputfile
        file_name = outputFilename.split('/')[-1]
        if outputFilename.split(file_name)[0] != "":
            mergedOutput = outputFilename.split(file_name)[0]+f"merged_{file_name}"
        else:
            mergedOutput = f"merged_{file_name}"
            
        proc = subprocess.Popen(
            f'hadd -fk {mergedOutput} {" ".join(inputFiles)}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        print(out.decode("utf-8"))
        print(err.decode("utf-8"), file=sys.stderr)

        f = ROOT.TFile.Open(mergedOutput)
        f2 = ROOT.TFile(outputFilename, "UPDATE")

        trees = [k.GetName() for k in f.GetListOfKeys()]
        trees = list(set(trees).difference(set(["Events"])))
        f2.cd()
        for key in trees:
            if 'tag' in key:
                f.Get(key).Clone().Write()
            else:
                f.Get(key).CloneTree().Write()
        f2.Close()
        f.Close()

        proc = subprocess.Popen(
            f"rm {mergedOutput}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        print(out.decode("utf-8"))
        print(err.decode("utf-8"), file=sys.stderr)

    def SplitVariations(self, df):
        """
        Create a Snapshot object for each variation and tag.

        Parameters
        ----------
        df : mRDF
            The ``mRDF`` object to use for snapshot

        """

        # create separate files for each variation and tag
        if self.outputMap != {}:
            for variationName in self.outputMap.keys():
                for tag in df.variations[self.outputMap[variationName][0]]["tags"]:
                    tmp_varied_cols = []

                    for variationNameSpecific in self.outputMap[variationName]:

                        tmp_varied_cols.extend(
                            df.GetVariedColumns_oneVariation(
                                self.saveColumns, variationNameSpecific, tag
                            )
                        )

                    outputFilename = self.tmpOutputFilename.split(".")
                    outputFilename[-2] += "__" + variationName + "_" + tag
                    outputFilename = ".".join(outputFilename)
                    self.snapshots.append(
                        [
                            variationName + "_" + tag,
                            tmp_varied_cols,
                            outputFilename,
                            False,
                            self.eosPath + "__" + variationName + tag + "_suffix",
                            self.outputFilename,
                        ]
                    )
        else:
            for variationName in df.variations:
                for tag in df.variations[variationName]["tags"]:
                    tmp_varied_cols = df.GetVariedColumns_oneVariation(
                        self.saveColumns, variationName, tag
                    )
                    outputFilename = self.tmpOutputFilename.split(".")
                    outputFilename[-2] += "__" + variationName + "_" + tag
                    outputFilename = ".".join(outputFilename)
                    self.snapshots.append(
                        [
                            variationName + "_" + tag,
                            tmp_varied_cols,
                            outputFilename,
                            False,
                            self.eosPath + "__" + variationName + tag + "_suffix",
                            self.outputFilename,
                        ]
                    )

    def StoreNominals(self, df):
        """
        Create a Snapshot object for the nominal columns.

        Parameters
        ----------
        df : mRDF
            The ``mRDF`` object to use for snapshot
        """
        # store only nominals and remove variations from the list
        tmp_varied_cols = df.GetVariedColumns(self.saveColumns)
        saveColumns = list(set(self.saveColumns).difference(set(tmp_varied_cols)))
        self.snapshots.append(
            [
                "nominal",
                saveColumns,
                self.tmpOutputFilename,
                True,
                self.eosPath,
                self.outputFilename,
            ]
        )

    def StoreNominalsAndVariations(self, df):
        """
        Create a Snapshot object containing both nominals and variations.

        Parameters
        ----------
        df : mRDF
            The ``mRDF`` object to use for snapshot

        """
        # store variation in the same file as nominal
        tmp_varied_cols = df.GetVariedColumns(self.saveColumns)
        self.snapshots.append(
            [
                "nominal and varied",
                self.saveColumns + tmp_varied_cols,
                self.tmpOutputFilename,
                True,
                self.eosPath,
                self.outputFilename,
            ]
        )

    def runModule(self, df, values):
        print("Snapshotting to", self.outputFilename, "columns:\n", self.columns)

        cols = df.GetColumnNames()
        saveColumns = []
        for pattern in self.columns:
            tmp_cols = list(set(filter(lambda k: fnmatch(k, pattern), cols)))
            if len(tmp_cols) == 0:
                print("Warning: no columns found to snapshot with pattern", pattern)
            saveColumns = list(set(saveColumns).union(set(tmp_cols)))

        self.saveColumns = list(set(saveColumns))

        self.snapshots = []

        if self.includeVariations and self.splitVariations and self.storeNominals:
            self.SplitVariations(df)
            self.StoreNominals(df)

        if self.includeVariations and self.splitVariations and not self.storeNominals:
            self.SplitVariations(df)

        if (
            self.includeVariations
            and not self.splitVariations
            and not self.storeNominals
        ):
            print(
                "Cannot snapshot variations all together without storing nominal\nEither set storeNominals=True or splitVariations=True",
                file=sys.stderr,
            )
            sys.exit(1)

        if (
            not self.includeVariations
            and not self.splitVariations
            and not self.storeNominals
        ):
            print(
                "Snapshot without variations and without storing nominal is not supported",
                file=sys.stderr,
            )
            sys.exit(1)

        if (
            not self.includeVariations
            and self.splitVariations
            and not self.storeNominals
        ):
            print(
                "Snapshot without variations and with split variations is not supported\nTurn on includeVariations",
                file=sys.stderr,
            )
            sys.exit(1)

        if not self.includeVariations and self.splitVariations and self.storeNominals:
            print(
                "Snapshot without variations and with split variations is not supported\nTurn on includeVariations",
                file=sys.stderr,
            )
            sys.exit(1)

        if (
            not self.includeVariations
            and not self.splitVariations
            and self.storeNominals
        ):
            self.StoreNominals(df)

        if self.includeVariations and not self.splitVariations and self.storeNominals:
            self.StoreNominalsAndVariations(df)

        for snapshot in self.snapshots:
            if "nominal" in snapshot[0]:
                isNominal = True
            else:
                isNominal = False
            _cols = sorted(list(set(snapshot[1])))
            opts = ROOT.RDF.RSnapshotOptions()
            opts.fLazy = True
            opts.fMode = "UPDATE"
            opts.fOverwriteIfExists = True
            opts.fCompressionAlgorithm = ROOT.RCompressionSetting.EAlgorithm.kLZMA
            opts.fCompressionLevel = 9
            values.append(
                [
                    "snapshot",
                    df.Snapshot("Events", snapshot[2], _cols, isNominal, opts),
                    snapshot[2:],
                ]
            )

        return df
