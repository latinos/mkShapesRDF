import fnmatch
import subprocess
import glob
import sys


class SearchFiles:
    """
    Class to search for files in a folder or DAS
    """

    def __init__(self):
        # cache result of `glob.glob(folder)` and `xrdfs redirector ls folder`
        self.cached_list_of_files = {}

    def searchFiles(
        self, folder, process, redirector="root://eoscms.cern.ch/", isLatino=True
    ):
        r"""Search for files in a folder. If redirector is specified, it will use xrdfs to query the redirector.

        Parameters
        ----------

            folder : str
                the folder to search in

            process : str
                the name of the process to search for

            redirector : str, optional, default: ``"root://eoscms.cern.ch/"``
                redirector to use.

            isLatino : bool, optional
                if the process is a latino process. Defaults to True. The process to search for will be ``"nanoLatino_" + process + "__part*.root"``.

        Returns
        -------

            `list of str`
                list of files found including the redirector
        """
        if not folder.endswith("/"):
            folder += "/"

        listOfFiles = []
        if len(self.cached_list_of_files.get(folder, [])) == 0:
            print("Need to query for files for folder", folder)
            if redirector != "":
                print("with redirector", redirector)
                proc = subprocess.Popen(
                    f"xrdfs {redirector} ls {folder}",
                    shell=True,
                    stdout=subprocess.PIPE,
                )
                listOfFiles = proc.communicate()[0].decode("utf-8").split("\n")
            else:
                listOfFiles = glob.glob(folder + "*")
            self.cached_list_of_files[folder] = listOfFiles
        else:
            listOfFiles = self.cached_list_of_files[folder]

        if isLatino:
            process = "nanoLatino_" + process + "__part*.root"
        else:
            process = process + "*.root"

        files = list(
            filter(lambda k: fnmatch.fnmatch(k, folder + process), listOfFiles)
        )

        if isLatino:
            files = sorted(
                files,
                key=lambda k: int(k.split("/")[-1].split(".")[0].split("__part")[-1]),
            )
        else:
            files = sorted(files)

        if redirector != "":
            files = list(map(lambda k: redirector + k, files))

        return files

    def searchFilesDAS(
        self, process, redirector="root://cms-xrd-global.cern.ch/", instance=""
    ):
        r"""Search for files given a DAS query. If instance is specified, it will search for files with the provided instance.

        Parameters
        ----------

            process : str
                the name of the process to search for

            redirector : str, optional, default:  ``"root://cms-xrd-global.cern.ch/"``.
                redirector to use.

            instance : str, optional
                instance to use. Defaults to "". instance="prod/phys03" will search for files generated with crab.


        Returns
        -------

            `list of str`
                list of files found including the redirector

        """

        files = []
        if (len(self.cached_list_of_files.get(process, []))) == 0:
            procString = f'dasgoclient --query="file dataset={process}'
            if instance != "":
                procString += " instance=" + instance
            procString += '"'

            proc = subprocess.Popen(
                procString,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = proc.communicate()
            out = out.decode("utf-8")
            out = out.split("\n")
            files = list(filter(lambda k: k.strip() != "", out))
            print(files, len(files))
            err = err.decode("utf-8")
            if len(err) != 0:
                print("There were some errors in retrieving file:")
                print(err)
                sys.exit()
        else:
            files = self.cached_list_of_files[process]

        files = list(map(lambda k: redirector + k, files))
        return files
