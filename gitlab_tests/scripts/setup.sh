#!/usr/bin/env bash

action() {
    # Determine the shell type (zsh or bash)
    local shell_is_zsh="$( [ -z "${ZSH_VERSION}" ] && echo "false" || echo "true" )"
    local this_file="$( ${shell_is_zsh} && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local this_dir="$( cd "$( dirname "${this_file}" )" && pwd )"

    #
    # mkShapesRDF setup
    #

    # Clone mkShapesRDF if not already present
    if [ ! -d "${this_dir}/mkShapesRDF" ]; then
        echo "Cloning mkShapesRDF repository..."
        git clone https://github.com/latinos/mkShapesRDF.git "${this_dir}/mkShapesRDF"
        if [ $? -ne 0 ]; then
            echo "[ERROR] Failed to clone mkShapesRDF"
            return 1
        fi

        (cd "${this_dir}/mkShapesRDF" && source install.sh)
        if [ $? -ne 0 ]; then
            echo "[ERROR] mkShapesRDF install.sh failed"
            return 2
        fi
    else
        echo "mkShapesRDF is already installed."
    fi

    # Activate the mkShapesRDF environment
    source "${this_dir}/mkShapesRDF/start.sh"
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to source start.sh"
        return 3
    fi

    echo "mkShapesRDF setup complete."

    cd ${this_dir}/mkShapesRDF/gitlab_tests
}

action "$@"
