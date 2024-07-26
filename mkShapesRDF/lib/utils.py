import os


def getFrameworkPath():
    r"""Utility function to get the absolute path to the mkShapesRDF framework

    Returns
    -------
        string
            absolute path to the mkShapesRDF framework (ends with ``/``)
    """

    try:
        fwPath = os.environ["STARTPATH"]
        fwPath = fwPath[: -len("start.sh")]
    except Exception as _:
        raise Exception(
            "STARTPATH is not set! Please be sure you've activated the environment"
        )

    return fwPath
