#!/usr/bin/env bash

set -e

echo "Getting framework path..."

# Get framework path using Python
FWPATH=$(python - <<EOF
from mkShapesRDF.lib.utils import getFrameworkPath
print(getFrameworkPath())
EOF
)

echo "Framework path: $FWPATH"

if [ ! -d "$FWPATH" ]; then
    echo "Error: Framework path does not exist: $FWPATH"
    exit 1
fi

cd "$FWPATH"

echo "Sourcing start.sh..."
source start.sh

########################################
# Test 1: Compile gitlab_tests/config
########################################

echo "Running compile test (gitlab_tests/config)..."

cd gitlab_tests/config
mkShapesRDF -c 1

echo "Compile test passed."

########################################
# Test 2: Run 1000 event in test_folder
########################################

echo "Running 1000-event test (gitlab_tests/config)..."

cd "$FWPATH/gitlab_tests/config"
mkShapesRDF -c 1 -o 0 -l 1

########################################
# Test 3: Plot 1000 event in test_folder
########################################
cd "$FWPATH/gitlab_tests/config"
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png

echo "All tests completed successfully."