Getting Started
===============

Installation
------------

Git clone the project and work with the `master` branch

.. code:: bash

   git clone https://github.com/latinos/mkShapesRDF.git

Lxplus is currently the suggested machine to work with. In general one should need
``cvmfs`` with ``sft.cern.ch`` and ``cms.cern.ch``. 

A docker image is also provided at ``/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-analysis/general/mkshapesrdf:master``.
The latter should be used on the INFN Analysis Facility.



Automatic installation
~~~~~~~~~~~~~~~~~~~~~~

mkShapesRDF has its own install script: ``install.sh``: it first sources the correct
python environment (it should contain a recent python3 and ROOT bindings) and then
proceeds with the creation of a virtual environment `myenv` where all the needed
packages and the framework scripts will be installed.

Be careful to have a clean environment before running the install script! E.g. not after a cmsenv

You're free to change the environment with conda/mamba insted of a LCG release inside
``install.sh``.

When you're ready just run:

.. code:: bash

   ./install.sh

It will create a ``start.sh`` script that should be run everytime to activate the
environment.

Manual installation
~~~~~~~~~~~~~~~~~~~

In order to install the package it's first necessary to source the right LCG release:

.. code:: bash

   source /cvmfs/sft.cern.ch/lcg/views/LCG_103/x86_64-centos7-gcc11-opt/setup.sh

now the right python version (3.9) and it's bindings with ROOT are setup. It's highly
reccomended to create a virtual environment for the installation:

.. code:: bash

   python -m venv --system-site-packages myenv

and of course activate it:

.. code:: bash

   source myenv/bin/activate

Now you can proceed to the simple installation:

.. code:: bash

   pip install -e ".[docs,dev,processor]"

Now to work with ``mkShapes.processor`` one should also install correctionlib and
compile it:

.. code:: bash

   python -m pip install --no-binary=correctionlib correctionlib

From now on, when you will login again on that machine you will just have to run the setup
command:

.. code:: bash

   source start.sh


Another step needed when using the ``processor`` is to download the ``jsonpog-integration`` folder:

.. code:: bash

   wget https://gpizzati.web.cern.ch/mkShapesRDF/jsonpog-integration.tar.gz
   tar -xzvf jsonpog-integration.tar.gz
   rm -r jsonpog-integration.tar.gz
   mv jsonpog-integration mkShapesRDF/processor/data/


Shape analysis: Run the analysis with the provided example
-----------------------------------------------------------------------

Configure the configuration folder (e.g. ``examples/Full2018_v9``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation on the configuration folder structure at :doc:`the configuration folder
structure <shapes/configuration>`.

Compile the configuration folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inside a configuration folder one can compile it into ``.json`` and ``.pkl``. The
compiled version are used across all the operating modes of mkShapesRDF

.. code:: bash

   mkShapesRDF -c 1

Run the analysis
~~~~~~~~~~~~~~~~

.. code:: bash

   mkShapesRDF -o 0 -b 1

`-o` indicates the operationMode: - 0 run analysis - 1 check batch output and errs - 2
merge root files

For the provided example (Full2018_v9) it's estimated an execution time of ~ 10 mins
running on lxbatch (condor on lxplus) @ CERN when disabling nuisances.

It's highly recommended to limit input ROOT files at the first run to check for errors.
The following command will only take 1 event for each sample type:

.. code:: bash

   mkShapesRDF -o 0 -l 1

Check for errors
~~~~~~~~~~~~~~~~

After all the jobs finished (or most of them did) you can run ``mkShapesRDF -o 1``
to know which jobs failed and why.

One can resubmit failed jobs with ``mkShapesRDF -o 1 -r 1``.

While if one wants to resubmit jobs that are still running, the option ``-r 2`` should
be used.

Merge files
~~~~~~~~~~~

If all the jobs succeeded run the merger with the option:

.. code:: bash

   mkShapesRDF -o 2

Plots
~~~~~

Plot with

.. code:: bash

   mkPlot

which will create the plots to the specified paths provided in ``configuration.py``


Processor: run the post processing
----------------------------------

See the dedicated section
