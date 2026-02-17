#!/bin/bash 

sourceCommand="echo 'first source of start.sh'"
env=$(hostname)
OS=$(grep "^CPE_NAME=" /etc/os-release | cut -d= -f2- | tr -d '"')
echo "OS ""$OS"

echo "Custom install ""$1"


sourceCommand="$sourceCommand""; source "$1"setup.sh"

echo "sourceCommand"
echo "$sourceCommand"
eval "$sourceCommand"

python -m venv --system-site-packages myenv
source myenv/bin/activate
which python
python --version
python -m pip --version

python -m pip install -e ".[docs,dev,processor]"

python -m pip install --no-binary=correctionlib correctionlib

cd utils
mkdir -p bin

cd src && c++ hadd.cxx -o hadd2 $(root-config --cflags --libs) && cd .. && mv src/hadd2 bin/hadd2

if [ $? -ne 0 ]; then
    echo "Failed compiling hadd"
    exit 1
fi
cd ..

cat <<EOF > start.sh
#!/bin/bash
$sourceCommand
source `pwd`/myenv/bin/activate
export STARTPATH=`pwd`/start.sh 
export PYTHONPATH=`pwd`/myenv/lib64/python3.11/site-packages:\$PYTHONPATH
export PATH=`pwd`/utils/bin:\$PATH
EOF

chmod +x start.sh

mkdir mkShapesRDF/processor/data/jsonpog-integration
cp -r /cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG mkShapesRDF/processor/data/jsonpog-integration/
