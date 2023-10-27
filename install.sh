#!/bin/bash

# sourceCommand="source /root/.bashrc && mamba activate cern"
sourceCommand="source /cvmfs/sft.cern.ch/lcg/views/LCG_103/x86_64-centos7-gcc11-opt/setup.sh"

eval "$sourceCommand"
python -m venv --system-site-packages myenv
source myenv/bin/activate

python -m pip install -e .[docs,dev]

python -m pip install --no-binary=correctionlib correctionlib

cat << EOF > start.sh
#!/bin/bash
$sourceCommand
source `pwd`/myenv/bin/activate
export STARTPATH=`pwd`/start.sh
EOF

chmod +x start.sh

wget https://gpizzati.web.cern.ch/mkShapesRDF/jsonpog-integration.tar.gz
tar -xzvf jsonpog-integration.tar.gz
rm -r jsonpog-integration.tar.gz
mv jsonpog-integration mkShapesRDF/processor/data/
