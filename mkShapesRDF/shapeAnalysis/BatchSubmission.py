import subprocess
from pathlib import Path
import os
import shutil


class BatchSubmission:
    @staticmethod
    def resubmitJobs(batchFolder, tag, samples, dryRun, queue):
        """
        Resubmit failed jobs and rename the old error file to err-1.txt
        Args:
            batchFolder (string): path to the batch folder
            tag (string): string used to tag the configuration
            samples (list of strings): samples to be resubmitted in the form of ['DY_0', ...]
        """

        # Path(f'{self.batchFolder}/{self.tag}/{sampleName}_{str(i)}').mkdir(parents=True, exist_ok=False)
        for sample in samples:
            if os.path.exists(f"{batchFolder}/{tag}/{sample}/err.txt"):
                os.rename(
                    f"{batchFolder}/{tag}/{sample}/err.txt",
                    f"{batchFolder}/{tag}/{sample}/err-1.txt",
                )
        with open(f"{batchFolder}/{tag}/submit.jdl") as file:
            txt = file.read()
        lines = txt.split("\n")
        line = list(filter(lambda k: k.startswith("queue"), lines))[0]
        jobflavour = list(filter(lambda k: k.startswith("+JobFlavour"), lines))[0]
        lines[lines.index(line)] = f'queue 1 Folder in {", ".join(samples)}\n '
        lines[lines.index(jobflavour)] = f'+JobFlavour = "{queue}"\n '
        with open(f"{batchFolder}/{tag}/submit.jdl", "w") as file:
            file.write("\n".join(lines))

        if dryRun != 1:
            process = subprocess.Popen(
                f"cd {batchFolder}/{tag}; condor_submit submit.jdl; cd -", shell=True
            )
            process.wait()

    def __init__(
        self,
        outputPath,
        batchFolder,
        headersPath,
        runnerPath,
        tag,
        samples,
        d,
        batchVars,
    ):
        self.outputPath = outputPath
        self.batchFolder = batchFolder
        self.headersPath = headersPath
        self.runnerPath = runnerPath
        self.tag = tag

        self.samples = samples
        self.d = d
        self.batchVars = batchVars

        self.folders = []

    def createBatch(self, sample):
        # 1. create submission folder
        # 2. create executable python file
        # 3. create bash file
        # 4. create condor file
        # 5. append condor file to submit files

        # submission folder
        sampleName = sample[0]
        i = sample[3]
        try:
            Path(f"{self.batchFolder}/{self.tag}/{sampleName}_{str(i)}").mkdir(
                parents=True, exist_ok=False
            )
        except:  # noqa E722
            print("Removing dir:", os.path.abspath(f"{self.batchFolder}/{self.tag}"))
            shutil.rmtree(os.path.abspath(f"{self.batchFolder}/{self.tag}"))
            Path(f"{self.batchFolder}/{self.tag}/{sampleName}_{str(i)}").mkdir(
                parents=True, exist_ok=False
            )
        self.folders.append(f"{sampleName}_{str(i)}")
        # python file

        txtpy = "from collections import OrderedDict\n"

        _samples = [sample]

        txtpy += f"samples = {str(_samples)}\n"

        for var in self.batchVars:
            _var = var
            if not isinstance(var, str):
                _var = var[0]

            if _var == "samples":
                continue
            if isinstance(self.d[_var], int) or isinstance(self.d[_var], float):
                txtpy += f"{_var} = {self.d[_var]}\n"
            else:
                txtpy += f"{_var} = {str(self.d[_var])}\n"

        with open(
            f"{self.batchFolder}/{self.tag}/{sampleName}_{str(i)}/script.py", "w"
        ) as f:
            f.write(txtpy)

    def createBatches(self):
        for sample in self.samples:
            self.createBatch(sample)

    def submit(self, dryRun=0, queue='workday'):
        txtsh = ""
        with open(os.environ['STARTPATH']) as file:
            txtsh += file.read()

        mE = self.d.get("mountEOS", [])
        for line in mE:
            txtsh += line

        txtsh += "time python runner.py\n"

        outputFileTrunc = ".".join(self.d["outputFile"].split(".")[:-1])

        print("\n\nReal output path:", os.path.realpath(self.outputPath), "\n\n")

        if os.path.realpath(self.outputPath).startswith("/eos"):
            # eos is not supported -> use xrdcp
            fullOutfile = f"{os.path.realpath(self.outputPath)}/"
        else:
            fullOutfile = f"{self.outputPath}/"

        fullOutfile += f"{outputFileTrunc}__ALL__" + "${1}.root"
        txtsh += f"cp output.root {fullOutfile}\n"
        txtsh += "rm output.root\n"
        txtsh += "rm script.py\n"

        # write the run.sh file
        with open(f"{self.batchFolder}/{self.tag}/run.sh", "w") as file:
            file.write(txtsh)
        # make it executable
        process = subprocess.Popen(
            f"chmod +x {self.batchFolder}/{self.tag}/run.sh", shell=True
        )
        process.wait()

        txtjdl = "universe = vanilla \n"
        txtjdl += "executable = run.sh\n"
        txtjdl += "arguments = $(Folder)\n"

        txtjdl += "should_transfer_files = YES\n"
        txtjdl += f"transfer_input_files = $(Folder)/script.py, {self.headersPath}, {self.runnerPath}\n"

        txtjdl += "output = $(Folder)/out.txt\n"
        txtjdl += "error  = $(Folder)/err.txt\n"
        txtjdl += "log    = $(Folder)/log.txt\n"

        txtjdl += "request_cpus   = 1\n"
        txtjdl += f'+JobFlavour = "{queue}"\n'

        txtjdl += f'queue 1 Folder in {", ".join(self.folders)}\n'
        with open(f"{self.batchFolder}/{self.tag}/submit.jdl", "w") as file:
            file.write(txtjdl)
        if dryRun != 1:
            process = subprocess.Popen(
                f"cd {self.batchFolder}/{self.tag}; condor_submit submit.jdl; cd -",
                shell=True,
            )
            process.wait()
