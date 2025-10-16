# mkShapesRDF: Simple Parallel RDF version of [LatinoAnalysis](https://github.com/latinos/LatinoAnalysis/)
[![Documentation Status](https://readthedocs.org/projects/mkshapesrdf/badge/?version=latest)](https://mkshapesrdf.readthedocs.io/en/latest/?badge=latest)
[![tests](https://github.com/giorgiopizz/mkShapesRDF/actions/workflows/ci_lint_format_test.yml/badge.svg)](https://github.com/giorgiopizz/mkShapesRDF/actions/workflows/ci_lint_format_test.yml)


Please refer to the [documentation](https://mkshapesrdf.readthedocs.io/en/shapes-dev-fix/index.html) for installation and a quick start guide.

Latest presentation at Latinos meeting [here](https://indico.cern.ch/event/1233729/contributions/5380538/attachments/2636898/4562210/mkShapesRDF%2026_04.pdf)

### Install

Clone the repository:

    git clone git@github.com:latinos/mkShapesRDF.git

    cd mkShapesRDF

In case you want to use the framework in its latest stable version, move to the most recent tag:

    git checkout tags/Run3_production_v1

The previous step can be skipped if you want to develop new features in the framework. In any case, you have to run the following command to complete the installation:

    source install.sh

### Setup the environment

After you installed the framework, and every time you log-in, you have to setup the environment in order to use it:

    cd <your_base_directory>/mkShapesRDF/

	source start.sh

### Post-process nanoAOD files

The first step is always to setup the environment. After that, you need to create a proxy to access files in the grid:

    voms-proxy-init --voms cms -valid 192:0

If you have already installed mkShapesRDF and you are having problems creating the proxy, modify the file `start.sh` so that it looks like this:

    #!/bin/bash
    echo 'first source of start.sh'; source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
    source `pwd`/myenv/bin/activate
    export STARTPATH=`pwd`/start.sh
    export JAVA_HOME=/cvmfs/sft.cern.ch/lcg/releases/java/11.0.21p9-cabd2/x86_64-el9-gcc13-opt
    export PATH=$JAVA_HOME/bin:$PATH
    export PYTHONPATH=`pwd`/myenv/lib64/python3.9/site-packages:\$PYTHONPATH
    export PATH=`pwd`/utils/bin:\$PATH
    
where `pwd` represents the path in which you have installed the framework.

The actual command to post-process files will look like the following:

    mkPostProc -o 0 -p Summer22EE_130x_nAODv12_Full2022v12 -s MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight -T <sample_name>

More information about the inputs requested by mkPostProc can be found in the latest [framework tutorial](https://indico.cern.ch/event/1414035/timetable/?view=standard#b-563854-latinos-tutorial).
