#!/bin/bash

# Usage:
# ./test_postproc.sh <production> <step> <sample>

set -e  # stop on first error

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <production> <step> <sample>"
    exit 1
fi

PRODUCTION=$1
STEP=$2
SAMPLE=$3

# --- Get framework path ---
# Equivalent to getFrameworkPath()
FWPATH=$(python - <<EOF
from mkShapesRDF.lib.utils import getFrameworkPath
print(getFrameworkPath())
EOF
)

echo "Framework path: $FWPATH"

CONDOR_PATH="${FWPATH}mkShapesRDF/processor/condor/${PRODUCTION}/${STEP}/${SAMPLE}__part0"

echo "Condor path: $CONDOR_PATH"

# --- Go to framework and load environment ---
cd "$FWPATH"
source start.sh

# --- Dry run mkPostProc ---
mkPostProc -o 0 \
    -p "$PRODUCTION" \
    -s "$STEP" \
    -T "$SAMPLE" \
    --limitFiles 1 \
    --dryRun 1

# --- Move to generated condor folder ---
cd "$CONDOR_PATH"

# --- Create test folder ---
mkdir -p test
cd test

# --- Copy generated script ---
cp ../script.py .

# --- Limit to 10 events ---
sed -i -E 's|(readRDF\(.*\))|\1\ndf.df = df.df.Range(10)|g' script.py

# --- Replace EOS output path with local folder ---
sed -i -E 's|/eos/cms/store/group/phys_[^/]+/[^'\'']+|test_output|g' script.py

# --- Copy run script ---
cp ../../run.sh .

# --- Run locally ---
./run.sh

echo "Test completed successfully."
