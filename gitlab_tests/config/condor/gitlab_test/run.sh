#!/bin/bash
echo 'first source of start.sh'; source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
source /afs/cern.ch/user/s/squinto/private/work/mkShapesRDF_histogramming/myenv/bin/activate
export STARTPATH=/afs/cern.ch/user/s/squinto/private/work/mkShapesRDF_histogramming/start.sh 
export PYTHONPATH=/afs/cern.ch/user/s/squinto/private/work/mkShapesRDF_histogramming/myenv/lib64/python3.9/site-packages:$PYTHONPATH
export PATH=/afs/cern.ch/user/s/squinto/private/work/mkShapesRDF_histogramming/utils/bin:$PATH
time python runner.py
cp output.root /afs/cern.ch/user/s/squinto/private/work/mkShapesRDF/gitlab_tests/config/gitlab_rootFiles/gitlab_test/mkShapes__gitlab_test__ALL__${1}.root
rm output.root
rm script.py
