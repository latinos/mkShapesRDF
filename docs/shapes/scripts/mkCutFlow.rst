
mkCutFlow: yields and composition
================================

``mkCutFlow`` is the installed yield and MC composition reporting
command. It reads existing ROOT histograms, calculates nominal event
yields and their statistical uncertainties, and reports the relative
contribution of each MC sample to the selected regions.

By default, it produces three CSV tables and prints yields, statistical
uncertainties and MC composition percentages to the terminal.

Basic usage
-----------

From an analysis directory containing ``configuration.py`` and
``cuts.py``:

.. code-block:: bash

   mkCutFlow
   mkCutFlow --inputFile rootFiles/my_shapes.root --outputDir tables

Or run from another directory:

.. code-block:: bash

   mkCutFlow --folder /path/to/my/analysis --outputDir tables

Relative input, configuration, cuts and output paths resolve inside
``--folder``.

The default input is ``outputFolder/outputFile`` from
``configuration.py``. If ``outputFile`` is absent, it falls back to
``outputFolder/mkShapes__<tag>.root``.

The ``cutsFile`` defaults to ``cuts.py``. The ``--pycfg`` and
``--cutsFile`` options override these filenames. Local imports
in the analysis configuration are supported.


Event-counting histogram
------------------------

The default histogram variable is ``events``.

Add an event-counting scalar variable to your analysis
``variables.py`` before producing shapes:

.. code-block:: python

   variables['events'] = {
       'name': '0.5',
       'range': (1, 0, 1),
       'xaxis': 'Events',
       'fold': 3
   }

This creates a single-bin histogram, filled once per selected event
using the corresponding event weight.

The command reads existing shapes. Adding this variable requires
regenerating the shapes.

Alternatively, select an existing histogram with:

.. code-block:: bash

   mkCutFlow --variable my_variable

Its integral represents the event yield only if it contains one
entry per event and covers the complete selected phase space.

Underflow and overflow are included by default. To exclude them:

.. code-block:: bash

   mkCutFlow --excludeFlow


Yields and statistical uncertainties
------------------------------------

For each region and sample, ``mkCutFlow`` calculates the nominal
event yield by summing the histogram bin contents.

For weighted MC events, the yield is

.. math::

   N_{\mathrm{MC}} = \sum_i w_i

and its statistical uncertainty is

.. math::

   \sigma_{\mathrm{stat}} = \sqrt{\sum_i w_i^2}

The implementation uses ROOT's ``GetBinContent()`` and
``GetBinError()`` methods, summing the squared bin uncertainties
and taking their square root.

This correctly propagates the statistical uncertainties stored
in the histogram, assuming its bin errors were constructed
using the appropriate sum of squared weights.

Negative MC weights are retained in the nominal yields.

Only statistical uncertainties are included. Systematic
uncertainties associated with JES, JER, pileup, b-tagging,
luminosity and other nuisance parameters are not included.

By default, MC yields are displayed as:

.. code-block:: text

   Sample             Yield
   TTTo2L2Nu          2183.923 +/- 9.168
   ST                  246.943 +/- 7.417
   DY                   92.046 +/- 21.151
   DATA               2648.000

The values above are illustrative.

DATA samples are displayed without statistical uncertainties.


Disabling statistical uncertainties
-----------------------------------

Statistical uncertainties are enabled by default.

To report only the nominal yields, use:

.. code-block:: bash

   mkCutFlow --noStatErrors

For example:

.. code-block:: bash

   mkCutFlow --inputFile rootFiles/my_shapes.root --noStatErrors

This option removes statistical uncertainties from the terminal
output and generated CSV tables.

When disabled, ``Stat_error`` columns are omitted from the CSV
files, and the nominal yields and composition percentages remain
unchanged.

The option only affects reporting. The underlying histogram
contents and yield calculations are not modified.

It can also be combined with the other output formats:

.. code-block:: bash

   mkCutFlow --format markdown --noStatErrors
   mkCutFlow --format latex --noStatErrors


Default output files
--------------------

By default, three CSV files are produced using the ``tag`` from
the analysis configuration.

**1.** ``yields_<tag>.csv``

A wide table containing samples as rows and analysis regions as
columns.

Each MC entry contains its nominal yield and statistical uncertainty
in the form ``yield +/- error``.

DATA entries contain only the observed yield.

**2.** ``yields_<tag>_long.csv``

A long-format table with the following columns:

.. code-block:: text

   Cut, Sample, Yield, Stat_error

Each row corresponds to one region and one sample.

The ``Stat_error`` column contains the absolute statistical
uncertainty for MC samples and is blank for DATA.

**3.** ``composition_<tag>.csv``

A table with the following columns:

.. code-block:: text

   Cut, Sample, Yield, Stat_error, Composition_percent

In addition to nominal yields and statistical uncertainties, this
table reports the fraction of the total MC expectation contributed
by each individual MC sample.

The statistical error is an absolute uncertainty on the yield,
not an uncertainty on the composition percentage.

When ``--noStatErrors`` is supplied, the files retain their
original yield-only structure:

.. code-block:: text

   yields_<tag>_long.csv:
   Cut, Sample, Yield

   composition_<tag>.csv:
   Cut, Sample, Yield, Composition_percent

The output directory can be selected with:

.. code-block:: bash

   mkCutFlow --outputDir tables


MC composition
--------------

For each region, the MC composition percentage is defined as:

.. math::

   f_i = 100 \times \frac{N_i}{\sum_{j \in \mathrm{MC}} N_j}

where ``N_i`` is the nominal yield of the corresponding MC sample.

The denominator contains the sum of the selected non-data
sample yields.

DATA does not contribute to the MC total and its composition
percentage is left blank.

If the total MC yield is zero, the composition percentage is
undefined. In this case, it is printed as ``N/A`` in the
terminal and left blank in the CSV output.

Negative MC weights are retained when calculating yields and
composition percentages. Consequently, individual percentages
are not necessarily bounded between 0 and 100.


Formatted tables
----------------

In addition to the three default CSV reports, ``mkCutFlow``
supports region-by-sample tables in text, Markdown, CSV and
LaTeX formats.

Select the output format with ``--format``:

.. code-block:: bash

   mkCutFlow --format text
   mkCutFlow --format markdown
   mkCutFlow --format csv
   mkCutFlow --format latex

To save a formatted table:

.. code-block:: bash

   mkCutFlow --format markdown --outputFile cutflow.md
   mkCutFlow --format latex --outputFile cutflow.tex
   mkCutFlow --format csv --outputFile cutflow.csv

The formatted tables display nominal yields and statistical
uncertainties by default.

For example, the Markdown output contains entries such as:

.. code-block:: text

   2183.923 +/- 9.168

For LaTeX, the statistical uncertainty is written using
``\pm`` in math mode:

.. code-block:: latex

   2183.923 $\pm$ 9.168

The generated LaTeX output retains the complete ``tabular``
environment, and special characters in region and sample names,
such as underscores, are escaped.

The ``--noStatErrors`` option is supported in every format:

.. code-block:: bash

   mkCutFlow --format latex --outputFile cutflow.tex --noStatErrors

When ``--outputFile`` is supplied without ``--format``,
the text format is used by default.

Unlike the three default CSV reports, the formatted table
contains regions as rows and samples as columns.

To make large tables easier to read, specific regions or
samples can be selected using ``--onlyCut`` and
``--onlySample``.


Regions and sample discovery
----------------------------

Categories and nested categories are expanded to their
corresponding ROOT directory names.

In the default mode, nominal samples are discovered directly
from the existing ROOT file.

The discovery excludes standard ``Up`` and ``Down`` nuisance
variations and histograms containing ``SPECIAL_NUIS``.

Genuine samples that share a name prefix are retained.

For nonstandard nuisance variation names, explicitly select
the nominal samples with ``--onlySample`` or use a compiled
configuration.

No execution of ``samples.py`` or remote sample discovery
is required in the default mode.

To select specific regions:

.. code-block:: bash

   mkCutFlow --onlyCut ttdm_sr_2l_1b,ttdm_sr_2l_2b

To select specific samples:

.. code-block:: bash

   mkCutFlow --onlySample DATA,DY,TTTo2L2Nu,ST

Both options accept comma-separated names.

Missing histograms are treated as errors and are never
silently reported as zero yields.


DATA identification
-------------------

DATA samples are automatically identified using the name
``DATA`` (case insensitive).

For analyses with different data sample names, use:

.. code-block:: bash

   mkCutFlow --dataSamples Electron,Muon

This overrides automatic DATA classification.

When using a compiled configuration, the ``isData`` metadata
from ``samples`` or ``structure`` is also recognized.

DATA samples are excluded from MC composition totals and are
reported without MC statistical uncertainties.


Using a compiled configuration
------------------------------

To report the exact cuts and samples saved during shapes
production, instead of executing the current Python
configuration, use:

.. code-block:: bash

   mkCutFlow --configFile configs/config_<timestamp>.pkl --outputDir tables

Alternatively, use the latest compiled configuration in
a directory:

.. code-block:: bash

   mkCutFlow --configsFolder configs --outputDir tables

This avoids differences between the current analysis
configuration and the one used to produce the ROOT shapes.

Compiled-configuration mode also supports a per-sample
input directory containing files named:

.. code-block:: text

   plots_<tag>_ALL_<sample>.root

The ``--onlyCut`` and ``--onlySample`` options can still
be used to restrict the reported regions and samples.


Important considerations
------------------------

All reported yields already include the preselections
defined in the analysis configuration.

Different signal and control regions are not necessarily
successive steps of a cumulative cutflow.

To obtain a cumulative cutflow, define cumulative regions
before producing the ROOT shapes.

The command does not recompute selections or event weights.
It only integrates the existing histograms.

For MC samples, the reported statistical uncertainties
represent the uncertainties stored in the histogram bins.
They should not be interpreted as the total uncertainty
on the predicted event yields.


Command-line reference
----------------------

.. argparse::
   :module: mkShapesRDF.shapeAnalysis.latinos.mkCutFlow
   :func: defaultParser
   :prog: mkCutFlow

