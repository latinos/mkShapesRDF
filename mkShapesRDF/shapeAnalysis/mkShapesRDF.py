"""
Main script for the creation of shapes, starting from a configuration folder.

It gives the option to compile the configuration folder and save it as both JSON and pickle file.

It also gives the option to run the analysis in batch mode, or to check for errors in the batch submission.

The analysis can be run in batch mode or locally.

If run in batch mode it gives the ability to merge the output root files.
"""

import sys
from pathlib import Path
import argparse
import os
import glob
import subprocess
import ROOT
from copy import deepcopy
from mkShapesRDF.shapeAnalysis.histo_utils import postProcessNuisances

ROOT.gROOT.SetBatch(True)

headersPath = os.path.dirname(os.path.dirname(__file__)) + "/include/headers.hh"
ROOT.gInterpreter.Declare(f'#include "{headersPath}"')


def defaultParser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--compile",
        type=int,
        choices=[0, 1],
        help="0 compile configuration and save JSON, 1 load compiled configuration",
        required=False,
        default=0,
    )

    parser.add_argument(
        "-o",
        "--operationMode",
        type=int,
        choices=[0, 1, 2],
        help="0 do analysis in batch, 1 check for errors in batch submission, "
        "2 hadd root files",
        required=False,
        default=-1,
    )
    parser.add_argument(
        "-b",
        "--doBatch",
        help="0 (default) runs on local, 1 runs with condor",
        required=False,
        default="0",
    )

    parser.add_argument(
        "-dR",
        "--dryRun",
        choices=[0, 1],
        type=int,
        help="1 do not submit to condor",
        required=False,
        default=0,
    )

    parser.add_argument(
        "-f", "--folder", help="Path to folder", required=False, default="."
    )

    parser.add_argument(
        "-configs",
        "--configsFolder",
        help="Path to configurations folder",
        required=False,
        default="configs",
    )

    parser.add_argument(
        "-config",
        "--configFile",
        help="Path to configuration JSON file to load",
        required=False,
        default="latest",
    )

    parser.add_argument(
        "-l",
        "--limitEvents",
        type=int,
        help="Max number of events",
        required=False,
        default=-1,
    )

    parser.add_argument(
        "-r",
        "--resubmit",
        choices=[0, 1, 2],
        type=int,
        help="Resubmit jobs, 1 resubmit finished jobs with errors, 2 resubmit running jobs",
        required=False,
        default="0",
    )
    parser.add_argument(
        "-q",
        "--queue",
        choices=[
            "espresso",
            "microcentury",
            "longlunch",
            "workday",
            "tomorrow",
            "testmatch",
        ],
        help="Condor queue",
        required=False,
        default="workday",
    )
    return parser


def main():
    parser = defaultParser()
    args = parser.parse_args()

    compileFolder = args.compile
    operationMode = args.operationMode
    doBatch = int(args.doBatch)
    dryRun = int(args.dryRun)
    queue = args.queue

    global folder
    global batchFolder
    global outputFolder

    folder = os.path.abspath(args.folder)
    configsFolder = os.path.abspath(args.folder + "/" + args.configsFolder)
    configFile = args.configFile
    resubmit = int(args.resubmit)

    if compileFolder == 1:
        print(os.getcwd())
        print(os.path.abspath(f"{folder}/configuration.py"))
        if not os.path.exists(folder) or not os.path.exists(
            f"{folder}/configuration.py"
        ):
            print("Error, configuration folder does not exists!")
            sys.exit()

        from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib

        # variables before execution of files
        configVars1 = dict(list(globals().items()) + list(locals().items()))

        ConfigLib.loadConfig(["configuration.py"], globals())
        ConfigLib.loadConfig(filesToExec, globals(), imports)

        globals()["varsToKeep"].insert(0, "folder")

        d = ConfigLib.createConfigDict(
            varsToKeep, dict(list(globals().items()) + list(locals().items()))
        )

        # variables after execution of files
        configVars2 = dict(list(globals().items()) + list(locals().items()))

        import datetime

        dt = datetime.datetime.now()
        Path(configsFolder).mkdir(parents=True, exist_ok=True)

        fileName = configsFolder + "/config_" + dt.strftime("%y-%m-%d_%H_%M_%S")
        fileNameJson = configsFolder + "/config"

        ConfigLib.dumpConfigDict(d, fileName)
        ConfigLib.dumpConfigDict(d, fileNameJson, doJson=True)

        ConfigLib.loadDict(d, globals())

    else:
        from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib

        if configFile != "latest":
            p = os.path.abspath(configFile)
            if not os.path.exists(p):
                print("Config file", configFile, "doest not exists at path", p)
                sys.exit()
            else:
                d = ConfigLib.loadPickle(p, globals())
        else:
            d = ConfigLib.loadLatestPickle(configsFolder, globals())

    samples = globals()["samples"]
    aliases = globals()["aliases"]
    variables = globals()["variables"]
    cuts = globals()["cuts"]
    nuisances = globals()["nuisances"]
    lumi = globals()["lumi"]
    print(samples.keys())
    print(d.keys())

    print("\n\n", batchVars, "\n\n")

    batchFolder = f"{folder}/{batchFolder}"

    if "/eos/user" in outputFolder or "/ceph/" in outputFolder:
        Path(f"{outputFolder}").mkdir(parents=True, exist_ok=True)
        outputPath = os.path.abspath(f"{outputFolder}")
        outputFileMap = f"{outputPath}/{outputFile}"
    else: 
        Path(f"{folder}/{outputFolder}").mkdir(parents=True, exist_ok=True)
        outputPath = os.path.abspath(f"{folder}/{outputFolder}")
        outputFileMap = f"{outputPath}/{outputFile}"

    if operationMode == 2 and os.path.exists(outputFileMap):
        print("Can't merge files, output already exists")
        print(f"You can run: \nrm {outputFileMap}")
        sys.exit()

    limit = int(args.limitEvents)

    # PROCESSING
    runnerFile = globals()["runnerFile"]
    if runnerFile == "default":
        runnerPath = os.path.realpath(os.path.dirname(__file__)) + "/runner.py"
        runnerFile = "runner.py"
    else:
        runnerPath = f"{folder}/{runnerFile}"
    print("\n\nRunner path: ", runnerPath, "\n\n")
    if not os.path.exists(runnerPath):
        print("Runner file / path does not exist!")
        sys.exit()

    _results = {}
    sys.path.insert(0, os.path.dirname(runnerPath))
    runnerModule = __import__(runnerFile.strip(".py"))
    if not hasattr(runnerModule, "RunAnalysis"):
        raise AttributeError(
            f"Runner module {runnerFile} from {runnerPath} has no attribute RunAnalysis"
        )
    RunAnalysis = runnerModule.RunAnalysis

    if operationMode == 0:
        print("#" * 20, "\n\n", "   Doing analysis", "\n\n", "#" * 20)

        if doBatch == 1:
            print("#" * 20, "\n\n", " Running on condor  ", "\n\n", "#" * 20)

            _samples = RunAnalysis.splitSamples(samples)

            from mkShapesRDF.shapeAnalysis.BatchSubmission import BatchSubmission

            batch = BatchSubmission(
                folder,
                outputPath,
                batchFolder,
                headersPath,
                runnerPath,
                tag,
                _samples,
                d,
                batchVars,
                globals().get("jdlconfigfile", ""),
            )
            batch.createBatches()
            batch.submit(dryRun, queue)

        else:
            print("#" * 20, "\n\n", " Running on local machine  ", "\n\n", "#" * 20)

            _samples = RunAnalysis.splitSamples(samples, False)

            runner = RunAnalysis(
                _samples,
                aliases,
                deepcopy(variables),
                deepcopy(cuts),
                nuisances,
                lumi,
                limit,
                outputFileMap,
            )
            runner.run()
            cuts = cuts["cuts"]
            postProcessNuisances(
                outputFileMap, samples, aliases, variables, cuts, nuisances
            )

    elif operationMode == 1:
        errs = glob.glob("{}/{}/*/err.txt".format(batchFolder, tag))
        files = glob.glob("{}/{}/*/script.py".format(batchFolder, tag))

        errsD = list(map(lambda k: "/".join(k.split("/")[:-1]), errs))
        filesD = list(map(lambda k: "/".join(k.split("/")[:-1]), files))
        # print(files)
        notFinished = list(set(filesD).difference(set(errsD)))
        sort_key = lambda k: (k.split("_")[0], int(k.split("_")[-1]))
        notFinishedShort = sorted(
            list(map(lambda k: k.split("/")[-1], notFinished)), key=sort_key
        )
        finishedShort = sorted(
            list(map(lambda k: k.split("/")[-2], errs)), key=sort_key
        )
        allSamples = {}
        for file in finishedShort:
            sample = "_".join(file.split("_")[:-1])
            if sample not in allSamples:
                allSamples[sample] = {"done": 1, "running": 0}
            else:
                allSamples[sample]["done"] += 1
        for file in notFinishedShort:
            sample = "_".join(file.split("_")[:-1])
            if sample not in allSamples:
                allSamples[sample] = {"done": 0, "running": 1}
            else:
                allSamples[sample]["running"] += 1


        import tabulate

        tabulated = [["Sample", "Total", "Finished", "Running"]]
        for sample in allSamples:
            tot = allSamples[sample]["done"] + allSamples[sample]["running"]
            tabulated.append(
                [
                    sample,
                    str(tot),
                    "\033[92m " + str(allSamples[sample]["done"]) + "\033[00m",
                    "\033[93m " + str(allSamples[sample]["running"]) + "\033[00m",
                ]
            )
        print(tabulate.tabulate(tabulated, headers="firstrow", tablefmt="fancy_grid"))

        tabulated = []
        tabulated.append(["Total jobs", "Finished jobs", "Running jobs"])
        tabulated.append(
            [
                len(files),
                "\033[92m " + str(len(errs)) + "\033[00m",
                "\033[93m " + str(len(notFinished)) + "\033[00m",
            ]
        )

        print(tabulate.tabulate(tabulated, headers="firstrow", tablefmt="fancy_grid"))
        # print('queue 1 Folder in ' + ' '.join(list(map(lambda k: k.split('/')[-1], notFinished))))
        normalErrs = """Warning in <TClass::Init>: no dictionary for class edm::ProcessHistory is available
        Warning in <TClass::Init>: no dictionary for class edm::ProcessConfiguration is available
        Warning in <TClass::Init>: no dictionary for class edm::ParameterSetBlob is available
        Warning in <TClass::Init>: no dictionary for class edm::Hash<1> is available
        Warning in <TClass::Init>: no dictionary for class pair<edm::Hash<1>,edm::ParameterSetBlob> is available
        Warning in <TInterpreter::ReadRootmapFile>: class  podio::
        real
        user
        sys
        run locally
        No TTree was created for
        Warning in <Snapshot>: A lazy Snapshot action was booked but never triggered.
        cling::DynamicLibraryManager::loadLibrary(): libOpenGL.so.0: cannot open shared object file: No such file or directory
        Error in <AutoloadLibraryMU>: Failed to load library /cvmfs/sft.cern.ch/lcg/releases/ROOT/6.28.00
        TClass::Init:0: RuntimeWarning: no dictionary for class edm::Hash<1> is available
        TClass::Init:0: RuntimeWarning: no dictionary for class edm::ParameterSetBlob is available
        TClass::Init:0: RuntimeWarning: no dictionary for class edm::ProcessHistory is available
        TClass::Init:0: RuntimeWarning: no dictionary for class edm::ProcessConfiguration is available
        TClass::Init:0: RuntimeWarning: no dictionary for class pair<edm::Hash<1>,edm::ParameterSetBlob> is available
        During startup - Warning message:
        Setting LC_CTYPE failed, using "C" 
        """
        normalErrs = normalErrs.split("\n")
        normalErrs = list(map(lambda k: k.strip(" ").strip("\t"), normalErrs))
        normalErrs = list(filter(lambda k: k != "", normalErrs))

        toResubmit = []

        def normalErrsF(k):
            for s in normalErrs:
                if s in k:
                    return True
                elif k.startswith(s):
                    return True
            return False

        for err in errs:
            with open(err) as file:
                lines = file.read()
            txt = lines.split("\n")
            # txt = list(filter(lambda k: k not in normalErrs, txt))
            txt = list(filter(lambda k: not normalErrsF(k), txt))
            txt = list(filter(lambda k: k.strip() != "", txt))
            if len(txt) > 0:
                print("Found unusual error in")
                print(err)
                print("\n")
                print("\n".join(txt))
                print("\n\n")
                toResubmit.append(err)
        toResubmit = list(map(lambda k: "".join(k.split("/")[-2]), toResubmit))
        print(toResubmit)
        if len(toResubmit) > 0:
            print("\n\nShould resubmit the following files\n")
            print(
                "queue 1 Folder in "
                + " ".join(list(map(lambda k: k.split("/")[-1], toResubmit)))
            )
            if resubmit == 1:
                from mkShapesRDF.shapeAnalysis.BatchSubmission import BatchSubmission

                BatchSubmission.resubmitJobs(
                    batchFolder, tag, toResubmit, dryRun, queue
                )

        if resubmit == 2:
            # resubmit all the jobs that are not finished
            toResubmit = list(map(lambda k: "".join(k.split("/")[-1]), notFinished))
            print(toResubmit)
            from mkShapesRDF.shapeAnalysis.BatchSubmission import BatchSubmission

            BatchSubmission.resubmitJobs(batchFolder, tag, toResubmit, dryRun, queue)

    elif operationMode == 2:
        print(
            "",
            "".join(["#" for _ in range(20)]),
            "\n\n",
            "Merging root files",
            "\n\n",
            "".join(["#" for _ in range(20)]),
        )

        _samples = RunAnalysis.splitSamples(samples)
        print(len(_samples))
        outputFileTrunc = ".".join(outputFile.split(".")[:-1])
        if "/eos/user" in outputFolder or "/ceph/" in outputFolder:
            filesToMerge = list(
                map(
                    lambda k: f"{outputFolder}/{outputFileTrunc}__ALL__{k[0]}_{str(k[3])}.root",
                    _samples,
                )
            )
            print("\n\nMerging files\n\n")
            print("\n\n", filesToMerge, "\n\n")
        
            print(f"Hadding files into {outputFolder}/{outputFile}")
        else:
            filesToMerge = list(
                map(
                    lambda k: f"{folder}/{outputFolder}/{outputFileTrunc}__ALL__{k[0]}_{str(k[3])}.root",
                    _samples,
                )
            )
            print("\n\nMerging files\n\n")
            print("\n\n", filesToMerge, "\n\n")
            
            print(f"Hadding files into {folder}/{outputFolder}/{outputFile}")
        #filesToMerge = list(
        #    map(
        #        lambda k: f"{folder}/{outputFolder}/{outputFileTrunc}__ALL__{k[0]}_{str(k[3])}.root",
        #        _samples,
        #    )
        #)
        #print("\n\nMerging files\n\n")
        #print("\n\n", filesToMerge, "\n\n")

        #print(f"Hadding files into {outputFileMap}")
        for fileToMerge in filesToMerge:
            os.system(f"echo {fileToMerge} >> filesToMerge_{outputFile}.txt")
        #process = subprocess.Popen(
        #    f"hadd2 -j 10 {outputFileMap} @filesToMerge_{outputFile}.txt; \
        #    rm filesToMerge_{outputFile}.txt",
        #    shell=True,
        #)
        if "/eos/user" in outputFolder or "/ceph/" in outputFolder:
            process = subprocess.Popen(
                f'hadd2 -j 10 {outputFolder}/{outputFile} @filesToMerge_{outputFile}.txt; \
                rm filesToMerge_{outputFile}.txt',
                shell=True,
            )
        else:
            process = subprocess.Popen(
                f'hadd2 -j 10 {folder}/{outputFolder}/{outputFile} @filesToMerge_{outputFile}.txt; \
                rm filesToMerge_{outputFile}.txt',
                shell=True,
            )

        process.communicate()

        if process.returncode == 0:
            print("Hadd was successful")
            cuts = cuts["cuts"]
            print(f"outputFileMap = {outputFileMap}")
            postProcessNuisances(
                outputFileMap, samples, aliases, variables, cuts, nuisances
            )
        else:
            print("mkShapesRDF: Hadd failed!", file=sys.stderr)
            sys.exit(1)

    else:
        print("Operating mode was set to -1, nothing was done")


if __name__ == "__main__":
    main()
