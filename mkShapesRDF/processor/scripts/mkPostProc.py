from mkShapesRDF.processor.framework.processor import Processor
from mkShapesRDF.processor.framework.Sites_cfg import Sites
import argparse
import os
from sys import argv
import glob
import subprocess
import tabulate

#: condorDir is the path to use for condor submission, user might want to change it -> edit ``mkPostProc.py``
condorDir = (
    "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1]) + "/condor"
)

#: eosDir and defaultRedirector are defined in Sites_cfg.py, user might want to modify them
eosDir = Sites["eosDir"]
defaultRedirector = Sites["rediretor"]


def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-o",
        "--operationMode",
        type=int,
        choices=[0, 1],
        help="0 do analysis in batch, 1 check for errors in batch submission",
        required=True,
    )

    parser.add_argument(
        "-p",
        "--prod",
        type=str,
        help="Production name to run",
        required=True,
    )

    parser.add_argument(
        "-s",
        "--step",
        type=str,
        help="Step name to run",
        required=True,
    )

    return parser


def operationMode0Parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(add_help=False)
    parser0 = argparse.ArgumentParser(parents=[parser])

    parser0.add_argument(
        "-T",
        "--selTree",
        type=str,
        help="List of samples to select, comma separated",
        required=False,
        default="",
    )

    parser0.add_argument(
        "-E",
        "--excTree",
        type=str,
        help="List of samples to exclude, comma separated",
        required=False,
        default="",
    )

    parser0.add_argument(
        "-iL",
        "--isLatino",
        type=bool,
        help="If the files in input follow the latino naming convention",
        required=False,
        default=True,
    )

    parser0.add_argument(
        "-i",
        "--inputFolder",
        help="Input folder to search for files",
        required=False,
        default="",
    )

    parser0.add_argument(
        "--maxFilesPerJob",
        type=int,
        help="Max number of input files per job (will merge input files)",
        required=False,
        default=1,
    )

    parser0.add_argument(
        "-l",
        "--limitFiles",
        type=int,
        help="Limit number of files to process",
        required=False,
        default=-1,
    )

    parser0.add_argument(
        "-dR",
        "--dryRun",
        choices=[0, 1],
        type=int,
        help="1 do not submit to condor",
        required=False,
        default=0,
    )

    parser0.add_argument(
        "--useRedirector",
        choices=[0, 1],
        type=int,
        help="0 do not use redirector, 1 use it",
        required=False,
        default=0,
    )
    return parser0


def operationMode1Parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(add_help=False)
    parser1 = argparse.ArgumentParser(parents=[parser])

    parser1.add_argument(
        "-r",
        "--resubmit",
        type=int,
        choices=[0, 1],
        help="0 do not resubmit, 1 resubmit",
        required=False,
        default=0,
    )

    return parser1


def main():
    parser = defaultParser()
    if len(argv) < (1 + 2 * 3):
        # just give the parser error
        args = parser.parse_args()
    else:
        real_args = argv[1 : 1 + 2 * 3]
        args = parser.parse_args(real_args)

    opMode = args.operationMode
    prodName = args.prod
    step = args.step

    if opMode == 0:
        parser0 = operationMode0Parser(parser)
        args = parser0.parse_args()

        selTree = args.selTree
        excTree = args.excTree

        if selTree == "":
            selTree = []
        else:
            selTree = [s.strip() for s in selTree.split(",")]

        if excTree == "":
            excTree = []
        else:
            excTree = [s.strip() for s in excTree.split(",")]

        isLatino = args.isLatino
        inputFolder = args.inputFolder
        maxFilesPerJob = args.maxFilesPerJob
        limitFiles = args.limitFiles
        dryRun = args.dryRun
        useRedirector = args.useRedirector

        redirector = ""
        if useRedirector == 1:
            redirector = defaultRedirector

        a = Processor(
            condorDir=condorDir,
            eosDir=eosDir,
            prodName=prodName,
            step=step,
            selTree=selTree,
            excTree=excTree,
            isLatino=isLatino,
            inputFolder=inputFolder,
            redirector=redirector,
            maxFilesPerJob=maxFilesPerJob,
            limitFiles=limitFiles,
            dryRun=dryRun,
        )

        a.run()
    elif opMode == 1:
        parser1 = operationMode1Parser(parser)
        args = parser1.parse_args()
        resubmit = args.resubmit
        print("Should check for errors")

        folder = condorDir + "/" + prodName + "/" + step + "/"

        folder = os.path.abspath(folder)

        errs = glob.glob(f"{folder}/*/err.txt")
        files = glob.glob(f"{folder}/*/script.py")

        errsD = list(map(lambda k: "/".join(k.split("/")[:-1]), errs))
        filesD = list(map(lambda k: "/".join(k.split("/")[:-1]), files))
        # print(files)
        notFinished = list(set(filesD).difference(set(errsD)))
        print(notFinished)
        tabulated = []
        tabulated.append(["Total jobs", "Finished jobs", "Running jobs"])
        tabulated.append([len(files), len(errs), len(notFinished)])

        print(tabulate.tabulate(tabulated))
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
                # print("\n".join(txt))
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
                with open(f"{folder}/submit.jdl") as file:
                    txt = file.read()

                lines = txt.split("\n")
                line = list(filter(lambda k: k.startswith("queue"), lines))[0]
                lines[lines.index(line)] = (
                    f'queue 1 Folder in {", ".join(toResubmit)}\n '
                )
                with open(f"{folder}/submit.jdl", "w") as file:
                    file.write("\n".join(lines))
                proc = subprocess.Popen(
                    f"cd {folder}; condor_submit submit.jdl", shell=True
                )
                proc.wait()

    else:
        print("Invalid operation mode")


if __name__ == "__main__":
    main()
