import sys
import subprocess
from mkShapesRDF.processor.framework.Steps_cfg import Steps
from mkShapesRDF.processor.framework.Sites_cfg import Sites
from mkShapesRDF.processor.framework.Productions_cfg import Productions
from mkShapesRDF.lib.search_files import SearchFiles
import os
from pathlib import Path
from math import ceil
from textwrap import dedent
from mkShapesRDF.lib.utils import getFrameworkPath


class Processor:
    """
    The ``Processor`` class is used to create the folder structure for batch submission and the scripts to run the processing.
    """

    def __init__(
        self,
        condorDir,
        eosDir,
        prodName,
        step,
        selTree=[],
        excTree=[],
        isLatino=True,
        inputFolder="",
        redirector="",
        maxFilesPerJob=1,
        limitFiles=-1,
        dryRun=0,
        MT=False,
    ):
        """
        Initialize the processor object

        Parameters
        ----------

        condorDir : str
            Path to the directory to use for condor jobs

        eosDir : str
            Path to the directory to use for eos (output files)

        prodName : str
            Production name (must be in ``Productions_cfg.py``)

        step : str
            Step name (must be in ``Steps_cfg.py``)

        selTree : `list of str`
            List of sample names to process (must be in the sample file associated to the production)

        excTree : `list of str`
            List of sample names to exclude (must be in the sample file associated to the production)

        isLatino : bool
            If True, use the latino naming convention (e.g. ``nanoLatino_DYJetsToLL_M-50__part*.root``)

        inputFolder : str, optional, default: ""
            Path to the input folder (where input files are searched, if empty, DAS is used)

        redirector : str, optional, default: ""
            Redirector to use (if empty, use direct access)

        maxFilesPerJob : int, optional, default: 1
            Maximum number of files per job (If 20 files and maxFilesPerJob=10, 2 jobs will be created)

        limitFiles : int, optional, default: -1
            Limit the number of input files to consider (if -1, all files are considered)

        dryRun : int, optional, default: 0
            If 1, do not submit jobs, just create the folder structure and the scripts

        MT : bool, optional, default: False
            If True, use multi-threading in the runner (``ROOT.EnableImplicitMT()``)
            Be careful since the events order is not preserved!

        """
        self.condorDir = condorDir
        self.eosDir = eosDir
        self.searchFiles = SearchFiles()
        self.prodName = prodName
        self.selTree = selTree
        self.excTree = excTree
        self.isLatino = isLatino
        self.step = step
        self.inputFolder = inputFolder
        self.redirector = redirector
        self.maxFilesPerJob = maxFilesPerJob
        self.limitFiles = limitFiles
        self.dryRun = dryRun
        self.path = getFrameworkPath() + "mkShapesRDF/processor/framework/"
        self.MT = MT

    def getFiles_cfg(self, sampleName):
        """
        Utility function to get a dictionary to be passed to the proper function of ``SearchFiles``

        Parameters
        ----------
        sampleName : str
            Sample name (must be in the sample file associated to the production)

        Returns
        -------
        dict
            Dictionary to be passed to the proper function of ``SearchFiles``
        """
        if self.inputFolder == "":
            # if no inputFolder is given -> DAS
            d = {
                "process": self.Samples[sampleName]["nanoAOD"],
                "instance": self.Samples[sampleName].get("instance", ""),
            }
            if self.redirector != "":
                d["redirector"] = self.redirector
        else:
            d = {
                "folder": self.inputFolder,
                "process": sampleName,
                "isLatino": self.isLatino,
                "redirector": self.redirector,
            }
        return d

    def addDeclareLines(self, step):
        """
        Add the declare lines to the python script file

        Parameters
        ----------
        step : str
            the step name to consider. Must be in ``Steps_cfg.py``. If the step is a chain, the declare lines of the substeps are added recursively.
            The imports, the declaration and the module call are added to the python script file.
        """
        if step not in Steps.keys():
            print(f"Error, step {step} not found in Steps")
            sys.exit()
        if "selection" in Steps[step].keys():
            self.fPy += "df = df.Filter(" + Steps[step]["selection"] + ")\n"
        if Steps[step]["isChain"]:
            for subtarget in Steps[step]["subTargets"]:
                self.addDeclareLines(subtarget)
        elif "declare" in Steps[step].keys():
            self.fPy += "from " + Steps[step]["import"] + " import *\n"
            self.fPy += Steps[step]["declare"] + "\n"
            self.fPy += "module = " + Steps[step]["module"] + "\n"
            self.fPy += "df = module.run(df, values) \n"

    def run(self):
        """Create the folder structure and the scripts to run the processing. Submit if dryRun==0"""
        global fPy
        self.fPy = dedent(
            """
        import sys
        sys.path.insert(0, list(filter(lambda k: 'myenv' in k, sys.path))[0])
        import ROOT
        import os
        ROOT.gROOT.SetBatch(True)
        """
        )

        if self.MT:
            self.fPy += "ROOT.EnableImplicitMT()\n"

        self.fPy += "from mkShapesRDF.processor.framework.mRDF import mRDF\n"
        self.fPy += "import subprocess\n"
        self.fPy += "import sys\n"

        if Productions[self.prodName]["isData"]:
            self.fPy += (
                'lumiFile = "'
                + os.path.abspath(self.path + Productions[self.prodName]["jsonFile"])
                + '"\n'
            )
        else:
            xsFile = Productions[self.prodName]["xsFile"]
            with open(self.path + xsFile) as file:
                exec(file.read(), globals())
            self.fPy += "xs_db = " + str(xs_db) + "\n"  # noqa F821

        with open(self.path + Productions[self.prodName]["samples"]) as file:
            exec(file.read(), globals())

        self.Samples = Samples  # noqa F821

        fSh = ""
        with open(self.path + "../../../start.sh") as file:
            fSh += file.read()

        if self.inputFolder == "":
            cmd = "voms-proxy-info"
            proc = subprocess.Popen(
                cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
            )
            out, err = proc.communicate()

            if "Proxy not found" in err.decode("utf-8"):
                print("WARNING: No GRID proxy -> Get one first with:")
                print("voms-proxy-init -voms cms -rfc --valid 168:0")
                sys.exit()

            proxypath = " xxx "
            for line in out.decode("utf-8").split("\n"):
                if "path" in line:
                    proxypath = line.split(":")[1].strip()
            print(proxypath)

            os.system("cp " + proxypath + " " + os.environ["HOME"] + "/.proxy")

            fSh += f"export X509_USER_PROXY={os.environ['HOME']}/.proxy\n"

        fSh += "time python script.py\n"

        jobDir = self.condorDir + "/" + self.prodName + "/" + self.step + "/"
        Path(jobDir).mkdir(parents=True, exist_ok=True)

        with open(jobDir + "run.sh", "w") as file:
            file.write(fSh)

        os.system("chmod +x " + jobDir + "run.sh")

        eosTmpPath = Sites["eosTmpWorkDir"]
        
        frameworkPath = getFrameworkPath() + "mkShapesRDF"

        self.fPy += "sampleName = 'RPLME_SAMPLENAME'\n"

        self.fPy += "_files = RPLME_FILES\n"
        self.fPy += dedent(
            """
        files = []
        eosTmpPath = '"""+eosTmpPath+"""'
        for f in _files:
            filename = f.split('/')[-1]
            if eosTmpPath=="USEDAS":
                filename = os.environ['TMPDIR'] + '/input__' + filename
            else:
                filename = eosTmpPath + 'input__' + filename
            files.append(filename)
            proc = 0
            if "root://" in f:
                proc = subprocess.Popen(f"xrdcp {f} {filename}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                proc = subprocess.Popen(f"cp {f} {filename}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out, err = proc.communicate()
            print(out.decode('utf-8'))
            print(err.decode('utf-8'), file=sys.stderr)
            if proc.returncode != 0:
                print(f"Error copying file {f}", file=sys.stderr)
                sys.exit(1)\n
        """
        )
        
        self.fPy += f"ROOT.gInterpreter.Declare('#include \"{frameworkPath}/include/headers.hh\"')\n"

        self.fPy += "df = mRDF()\n"
        self.fPy += 'df = df.readRDF("Events", files)\n'

        self.fPy += "values = []\n"

        self.addDeclareLines(self.step)

        self.fPy += dedent(
            """
        snapshots = []
        snapshot_destinations = []
        for val in values:
            if "snapshot" == val[0]:
                snapshots.append(val[1][0])
                snapshot_destinations.append(val[2])

        import uproot
        import awkward
        for snapshot in snapshots:
            snapshot(df.df)

        finalFiles = []
        for destination in snapshot_destinations:
            copyFromInputFiles = destination[1]
            outputFilename = destination[0]

            if copyFromInputFiles:
                Snapshot.CopyFromInputFiles(outputFilename, files)

            outputFolderPath = destination[2]
            outputFilenameEOS = destination[3]

            # Create output folder
            proc = subprocess.Popen(f"mkdir -p {outputFolderPath}", shell=True)
            proc.wait()

            # Copy output file in output folder
            proc = subprocess.Popen(f"cp {outputFilename} {outputFolderPath}/{outputFilenameEOS}", shell=True)
            proc.wait()
            finalFiles.append(f'{outputFolderPath}/{outputFilenameEOS}')

            # Remove the output file from local
            proc = subprocess.Popen(f"rm {outputFilename}", shell=True)
            proc.wait()
            
        def sciNot(value):
            # scientific notation
            return "{:.3e}".format(value)
        
        data = []
        reservedValuesNames = ["snapshot", "variables"]
        for val in values:
            if val[0] in reservedValuesNames:
                continue
            if "list" in str(type(val)):
                if str(type(val[0])) == "<class 'function'>":
                    data.append(val[0](*val[1:]))
                else:
                    data.append([val[1], sciNot(val[0].GetValue())])
            else:
                data.append("", sciNot(val.GetValue()))

        from tabulate import tabulate

        print(tabulate(data, headers=["desc.", "value"]))
            """)

        if self.inputFolder != "" and eosTmpPath!="USEDAS":
            self.fPy += dedent("""
        for f in files:
            print('Removing input file', f)
            proc = subprocess.Popen(f"rm {f}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            print(out.decode('utf-8'))
            print(err.decode('utf-8'), file=sys.stderr)
            """)

        self.fPy += dedent("""
        # check final file integrity
        for finalFile in finalFiles:
            f = uproot.open(finalFile)
            branches = [k.name for k in f['Events'].branches]
            print(f['Events'][branches[0]].array(entry_stop=10))
            f.close()
        """)
        
        self.fPy = self.fPy.replace("RPLME_FW", frameworkPath)

        #: folderPathEos is the output folder path (not ending with ``/`` so that is possible to add suffix to the folder)
        if self.inputFolder == "":
            folderPathEos = self.eosDir + "/" + self.prodName + "/"  # + self.step
            folderPathEos += Steps[self.step].get("outputFolder", self.step)
        else:
            folderPathEos = self.inputFolder + "__"
            folderPathEos += Steps[self.step].get("outputFolder", self.step)
            
        self.fPy = self.fPy.replace("RPLME_EOSPATH", folderPathEos)
        
        allSamples = []

        samplesToProcess = self.Samples.keys()
        samplesNotToProcess = []

        if len(self.selTree) != 0:
            for i, sampleName in enumerate(samplesToProcess):
                if sampleName not in self.selTree:
                    samplesNotToProcess.append(i)
        if len(self.excTree) != 0:
            for i, sampleName in enumerate(samplesToProcess):
                if sampleName in self.excTree:
                    samplesNotToProcess.append(i)

        samplesToProcess = [
            sampleName
            for i, sampleName in enumerate(samplesToProcess)
            if i not in samplesNotToProcess
        ]
        if len(samplesToProcess) == 0:
            print("No samples to process", file=sys.stderr)
            sys.exit(1)

        for sampleName in samplesToProcess:
            files_cfg = self.getFiles_cfg(sampleName)
            files = []
            if self.inputFolder == "":
                files = self.searchFiles.searchFilesDAS(**files_cfg)
            else:
                files = self.searchFiles.searchFiles(**files_cfg)

            if self.limitFiles!=-1:
                files = files[: self.limitFiles]

            if len(files) == 0:
                print("No files found for", sampleName, "and configuration", files_cfg)
                sys.exit()

            print(files[0])

            nParts = ceil(len(files) / self.maxFilesPerJob)

            sample_fPy = self.fPy.replace("RPLME_SAMPLENAME", sampleName)

            if "RPLME_genEventSumw" in self.fPy:
                import ROOT

                ROOT.gROOT.SetBatch(True)
                ROOT.EnableImplicitMT()
                df = ROOT.RDataFrame("Runs", files)
                genEventSumw = df.Sum("genEventSumw").GetValue()
                sample_fPy = sample_fPy.replace("RPLME_genEventSumw", str(genEventSumw))

            for part in range(nParts):
                _files = files[
                    part * self.maxFilesPerJob : (part + 1) * self.maxFilesPerJob
                ]
                _fPy = sample_fPy.replace("RPLME_FILES", str(_files))
                outputFilename = (
                    "nanoLatino_" + sampleName + "__part" + str(part) + ".root"
                )

                if self.inputFolder != "":
                    outputFilename = _files[0].split("/")[-1]

                if eosTmpPath=="USEDAS":
                    #if not os.path.exists(os.environ['TMPDIR']):
                    #    os.mkdir(os.environ['TMPDIR'])
                    _fPy = _fPy.replace("RPLME_OUTPUTFILENAMETMP", "os.environ['TMPDIR']")
                else:
                    _fPy = _fPy.replace("RPLME_OUTPUTFILENAMETMP", eosTmpPath)
                _fPy = _fPy.replace("RPLME_OUTPUTFILENAME", outputFilename)

                jobDirPart = jobDir + sampleName + "__part" + str(part) + "/"
                Path(jobDirPart).mkdir(parents=True, exist_ok=True)

                with open(jobDirPart + "/script.py", "w") as f:
                    f.write(_fPy)
                allSamples.append(sampleName + "__part" + str(part))

        fJdl = dedent(
            """
universe = vanilla
executable = run.sh
arguments = $(Folder)

should_transfer_files = YES
transfer_input_files = $(Folder)/script.py

output = $(Folder)/out.txt
error  = $(Folder)/err.txt
log    = $(Folder)/log.txt

request_cpus   = 1
request_memory = 12GB
request_disk   = 10GB
requirements = (OpSysAndVer =?= "AlmaLinux9")
+JobFlavour = "testmatch"

queue 1 Folder in RPLME_ALLSAMPLES
"""
        )

        fJdl = fJdl.replace("RPLME_ALLSAMPLES", " ".join(allSamples))
        with open(jobDir + "/submit.jdl", "w") as f:
            f.write(fJdl)

        if self.dryRun == 0:
            proc = subprocess.Popen(
                f"cd {jobDir}; condor_submit submit.jdl;", shell=True
            )
            proc.wait()
