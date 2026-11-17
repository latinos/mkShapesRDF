mkPostFitHistos: post-fit histograms for plotting
=================================================

``mkPostFitHistos.py`` (the ``LawnMower`` script) converts the output of a
Combine fit into a ROOT file with the same layout as the ``mkShapes``
output, so that the prefit or post-fit distributions can be plotted with
the usual plotting tools (for example ``mkPlot``).

It reads the shapes saved by Combine's ``FitDiagnostics``, renames them
following the ``histo_<sample>`` convention, optionally adopts the
binning of the observed DATA histogram, and writes everything to a new
ROOT file organised as ``<cut>/<variable>/histo_<name>``.

By default, it reads one Combine channel and one variable per call and
writes the individual sample histograms together with the signal,
background and total histograms.


Basic usage
-----------

.. code-block:: bash

   mkPostFitHistos.py \
       --inputFileCombine fitDiagnostics.root \
       --inputFile rootFiles/my_shapes.root \
       --outputFile postfit.root \
       --structureDir /path/to/my/analysis \
       --cut ch1 \
       --cutNameInOriginal ttdm_sr_2l_1b \
       --variable mll \
       --kind s

Each call processes one cut and one variable. To produce several
regions or variables, run the script once per combination.

``--structureDir`` must be the directory containing ``structure.py``.
That file must define the dictionary ``structure``.


Inputs
------

The script uses up to two input files.

**Combine file** (``--inputFileCombine``)

The ``FitDiagnostics`` output containing the folders
``shapes_prefit``, ``shapes_fit_s`` and ``shapes_fit_b``. Inside each
folder, histograms are searched under ``<cut>/<name>``, where ``<cut>``
is the Combine channel name given by ``--cut``.

**Shapes or datacard file** (``--inputFile``)

The file produced by ``mkShapes`` or by the datacard production. It is
used to retrieve the observed DATA histogram. It is also used to
retrieve the nominal MC histograms when ``--MCStatFromInput`` is
enabled.

By default, the file is expected to have the ``mkShapes`` layout, in
which a histogram is read from

.. code-block:: text

   <cutNameInOriginal>/<variable>/histo_<sample>

With ``--isInputFileFromDatacard 1``, the file is instead assumed to
come from the datacard shapes, and histograms are read from the top
level of the file as ``histo_<sample>``. The DATA histogram is then
read as ``histo_Data``.


The structure file
------------------

The ``structure`` dictionary defines which samples are processed.
Every key is looked up in the Combine output, and the iteration order
follows the dictionary.

Keys containing a ``/`` are interpreted as binned samples:

.. code-block:: text

   structure key:       sample/bin
   sample name:         sample
   Combine histogram:   sample__bin
   input file shape:    binned/bin/<cutNameInOriginal>/<variable>/histo_sample

Any sample whose ``removeFromCuts`` list contains the current
``--cutNameInOriginal`` is skipped.

The sample name ``DATA`` (case sensitive) is treated specially, as
described below.

If ``--structureDir`` is not provided, or does not exist, the script
cannot continue: ``structure`` is never defined and Python raises a
``NameError``.


Fit kinds
---------

The ``--kind`` option selects which Combine folder is used as the main
source of shapes:

.. code-block:: text

   s    shapes_fit_s     signal + background fit (default)
   b    shapes_fit_b     background-only fit
   p    shapes_prefit    prefit distributions

Any other value prints a message and the script exits without
producing histograms.

Prefit histograms are always also read from ``shapes_prefit`` for the
total and total background, regardless of ``--kind``.


Output histograms
-----------------

For the selected cut and variable, the output file contains the
directory ``<cutNameInOriginal>/<variable>`` with the following
histograms.

**Sample histograms**

.. code-block:: text

   histo_<cardName>

One histogram per sample in ``structure``, taken from the selected
Combine folder. For binned samples, ``cardName`` replaces ``/`` with
``__``.

**DATA**

.. code-block:: text

   histo_DATA

Copied from ``--inputFile`` without modification.

**Signal**

.. code-block:: text

   histo_total_signal

**Background**

.. code-block:: text

   histo_total_background
   histo_total_background_prefit
   histo_total_background_postfit_<kind>

**Total**

.. code-block:: text

   histo_total
   histo_total_prefit
   histo_total_postfit_<kind>

``histo_total_background`` and ``histo_total`` are taken from the
folder selected with ``--kind``. The ``_prefit`` versions always come
from ``shapes_prefit``, and the ``_postfit_<kind>`` versions from the
selected folder.


DATA and binning
----------------

If ``DATA`` is present in ``structure``, its histogram is read from
``--inputFile``, written to the output file, and cloned as a
binning template.

All other histograms from the Combine file are then rebuilt as
``TH1D`` with the bin edges of the DATA histogram. For each bin
``1..N``, the content and error are copied from the Combine histogram.

Consequently:

* The number of bins of the Combine and DATA histograms must match.
  The edges are replaced, not rebinned.
* Underflow and overflow bins are not propagated to the rebuilt
  histograms.

If the DATA histogram cannot be found, the script raises a
``RuntimeError`` indicating whether the file is expected to come from
a datacard.

DATA must be present in ``structure``. The input file is opened when
the DATA entry is processed, and is needed later for the MC histograms
used by ``--MCStatFromInput``.


Signal from prefit
------------------

By default, ``histo_total_signal`` is read from the folder selected by
``--kind``.

To take the signal shape and normalization from ``shapes_prefit``
instead, use:

.. code-block:: bash

   mkPostFitHistos.py ... --kind b --getSignalFromPrefit 1

This is needed for exclusion analyses, where the fitted signal
strength is zero, and for showing the expected signal on top of a
background-only fit.


Adding the MC statistical uncertainty
-------------------------------------

For bystander fits, where MC statistical uncertainties are not part of
the Combine model, use:

.. code-block:: bash

   mkPostFitHistos.py ... --MCStatFromInput 1

The script sums the nominal MC histograms from ``--inputFile`` and adds
the bin errors of that sum, in quadrature, to the existing errors of
``histo_total``, ``histo_total_prefit`` and
``histo_total_postfit_<kind>``:

.. math::

   \sigma_{\mathrm{new}} = \sqrt{\sigma_{\mathrm{fit}}^2 + \sigma_{\mathrm{MC,stat}}^2}

Only the three total histograms are modified. The sample, signal and
background histograms are not.

The MC sum is built from every non-DATA sample of ``structure`` that
can be read from the input file. A sample that cannot be read triggers
a warning and is left out of the sum.

If the first non-DATA sample cannot be read, the running sum is not
initialised and later additions fail. Check the warnings printed by
the script.


Missing samples and folders
---------------------------

Missing items are handled in two different ways.

**Sample not found in the Combine output.** A highlighted warning is
printed and the sample is skipped. It is not written to the output
file. This is normal when a sample is absent from the datacard or is
not included in ``structure.py``.

**Folder or total histogram not found.** A ``RuntimeError`` is raised
if ``<folder>/<cut>`` does not exist, or if ``total_signal``,
``total_background`` or ``total`` is missing from the required folders.

Samples that are skipped are not replaced by empty histograms.


Output file handling
--------------------

If ``--outputFile`` already exists, a warning is printed. After five
seconds, the file is deleted and recreated. Interrupt the script
within this window if the file should be kept.

The output file is opened in update mode so that the directory
``<cutNameInOriginal>/<variable>`` can be created. Since an existing
file is removed first, histograms for several cuts or variables are
not accumulated in the same file across separate calls. Use a
different ``--outputFile`` for each call, or merge the files
afterwards.

If ``--cutNameInOriginal`` is an empty string, ``--cut`` is used
instead.


Important considerations
------------------------

The script does not run any fit and does not recompute any yields. It
only reads, renames, optionally rebins and writes histograms that
already exist in the Combine output.

The directory name in the output (``--cutNameInOriginal``) and the
channel name in the Combine file (``--cut``) are independent. Set both
explicitly, since the default of ``--cutNameInOriginal`` is a fixed
placeholder, ``hww2l2v_13TeV_0j``.

The uncertainties stored in the post-fit histograms are those
computed by Combine. They include the effect of the fitted nuisance
parameters and their correlations. They are not the statistical
uncertainties of the input shapes, unless ``--MCStatFromInput`` is
used.

Combine's ``norm_fit_s`` object is loaded but not used.


Command-line reference
----------------------

.. code-block:: text

   --inputFileCombine        Combine FitDiagnostics output.
                             Default: input.root
   --inputFile               File with the DATA (and nominal MC) histograms.
                             Default: input.root
   --isInputFileFromDatacard Set to 1 if --inputFile contains datacard shapes
                             rather than mkShapes output. Default: 0
   --outputFile              Output ROOT file, in mkShapes format.
                             Default: output.root
   --variable                Variable name. Default: mll
   --cut                     Channel name as it appears in the Combine file.
                             Default: ch1
   --cutNameInOriginal       Cut name as it appears in cuts.py, with the
                             category appended.
                             Default: hww2l2v_13TeV_0j
   --kind                    s (signal + background), b (background only)
                             or p (prefit). Default: s
   --structureDir            Directory containing structure.py. Required.
   --getSignalFromPrefit     Set to 1 to take the signal from shapes_prefit.
                             Default: 0
   --MCStatFromInput         Set to 1 to add the input MC statistical
                             uncertainty to the totals. Default: 0