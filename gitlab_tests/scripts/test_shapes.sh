#!/usr/bin/env bash -x

set -e

# This only pauses if you are running locally (interactive terminal) and NOT in GitLab CI.
function finish {
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo "FAILED with exit code $EXIT_CODE"
        # Check if stdin is a terminal AND we are NOT in GitLab CI
        if [ -t 0 ] && [ -z "$GITLAB_CI" ]; then
            echo "Local terminal detected. Press Enter to close..."
            read
        fi
    fi
}
trap finish EXIT


echo "Getting framework path..."

# Get framework path using Python
FWPATH=$(python3 - <<EOF
from mkShapesRDF.lib.utils import getFrameworkPath
print(getFrameworkPath())
EOF
)

echo "Framework path: $FWPATH"

if [ ! -d "$FWPATH" ]; then
    echo "Error: Framework path does not exist: $FWPATH"
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
# Test 2: Run 100000 event in test_folder
########################################

echo "Running 100000-event test (gitlab_tests/config)..."

cd "$FWPATH/gitlab_tests/config"
mkShapesRDF -c 1 -o 0 -l 1000000

########################################
# Test 3: Plot 100000 event in test_folder
########################################
cd "$FWPATH/gitlab_tests/config"
mkdir -p gitlab_Plots
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png

echo "All tests completed successfully."