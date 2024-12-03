#!/bin/bash 

sourceCommand="echo 'first source of start.sh'"

env=$(hostname)

OS=$(hostnamectl | grep "CPE OS Name")
echo "OS ""$OS"

echo "Custom install ""$1"

if [ -z "$1" ]; then 
    if [[ "$OS" == *"centos:7"* ]]; then
        echo centos7
        sourceCommand="$sourceCommand""; source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-centos7-gcc11-opt/setup.sh"
    elif [[ "$OS" == *"linux:9"* ]]; then
        echo el9
        sourceCommand="$sourceCommand""; source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh"
    else
        echo "$OS"" not supported"
        exit 1
    fi
elif [ "$1" == "docker" ]; then
    sourceCommand="export LD_LIBRARY_PATH=$(root-config --libdir):$(pwd)/xrdfs_locallib/lib:/.singularity.d/libs"
else
    echo "$1"" custom install not supported"
    exit 1
fi

echo "sourceCommand"
echo "$sourceCommand"
eval "$sourceCommand"

if [ "$1" == "docker" ]; then
    ln -s /usr/bin/python3 /usr/bin/python
    which python
    python --version
fi

python -m venv --system-site-packages myenv
source myenv/bin/activate

if [ "$1" == "docker" ]; then
    python -m pip --version
    python -m pip install --upgrade pip
    python -m pip --version
fi

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
export PYTHONPATH=`pwd`/myenv/lib64/python3.9/site-packages:\$PYTHONPATH
export PATH=`pwd`/utils/bin:\$PATH
EOF


chmod +x start.sh

mkdir mkShapesRDF/processor/data/jsonpog-integration
cp -r /cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG mkShapesRDF/processor/data/jsonpog-integration/


#wget https://gpizzati.web.cern.ch/mkShapesRDF/jsonpog-integration.tar.gz
#tar -xzvf jsonpog-integration.tar.gz
#rm -r jsonpog-integration.tar.gz
#mv jsonpog-integration mkShapesRDF/processor/data/
