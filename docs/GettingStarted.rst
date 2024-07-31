***************
Getting Started
***************

===================
System Requirements
===================

To use ``GILDA-LOCAL`` you will need:

* Python 3.11.9, up and running. We strongly recommend the use of `pyenv`_  or `virtualenv`_ for this, either in Linux or Windows.
* Python libraries or packages (`pyomo`, `numpy` and others), but these will
  be installed automatically. Please try to work over a vanilla version of
  Python. We recommend, again, you use `pyenv`_ for this.
* A mixed integer linear programming solver (as `CBC`, `Gurobi`). You may install
  the CBC solver in Linux using your favorite package manager. For example, in
  Ubuntu you may try:

``$ sudo apt install coinor-cbc``

* In windows you may use `chocolatey`_, or something similar, to install Python
  and `CBC`.


============
Installation
============

The sources for ``GILDA-LOCAL`` can be downloaded from the `Github repository`_.

0. Verify that `python` is working with the expected version.

   ``$ python --version``

   You should receive the following output:

   ``Python 3.11.9``

   Also verify if ``cbc`` is installed and working

   ``$ cbc``


1. You can either download or clone the public repository. For cloning use:

   ``$ git clone https://github.com/marcelomatus/gilda-local.git``

   This is the preferred method to install ``GILDA-LOCAL``, as it will always
   install the most recent stable release.


2. Once you have a copy of the source, you can install it running this command
   in your terminal:

  ``$ cd gilda-local``

  ``$ pip install .``


Once installed, you can verify that ``GILDA-LOCAL`` is available by executing:

   ``$ gilda_local -h``

This should display the following ``GILDA-LOCAL`` options:

=======================================  =================================================
-h, --help                               show this help message and exit
--version                                show program's version number and exit
-i INFILE_NAME, --infile INFILE_NAME     JSON input file. Stdinp is used if not provided.
-o OUTFILE_NAME, --outfile OUTFILE_NAME  JSON output file. Stdout is used if not provided.
-v, --verbose                            set loglevel to INFO
-vv, --very-verbose                      set loglevel to DEBUG
-k, --keepfiles                          If included, the solver keepfiles option is used
-s SOLVER, --solver SOLVER               Defines the solver to be used (default: cbc)
=======================================  =================================================

=============
Running Gilda
=============

To run a simulation, you must follow three steps. First, prepare the input data
to define all of the relevant system parameters. Then invoke the function to run
the simulation. Finally, you can access the results saved in output data files.

^^^^^^^^^^^^^^^^^^^^^^^^^
Preparing Case Input Data
^^^^^^^^^^^^^^^^^^^^^^^^^

The full details of the input data files are documented in :ref:`Modeling`. The
``GILDA-LOCAL`` distribution also includes some :ref:`Examples` that illustrate
how to accurately input data to construct and simulate the system.


^^^^^^^^^^^^^^^^^^^^
Trying some examples
^^^^^^^^^^^^^^^^^^^^

``GILDA-LOCAL`` invoked by calling the command `gilda_local` and passing a JSON
file describing the scenario to optimize.

For example, in the `cases` directory inside the `gilda_local` distribution, you
will find several examples to run. One of them is ``demand_grid.json``, which
describes a simple demand and grid configuration.

To run ``GILDA-LOCAL`` on this case, type the following  ``shell``  command:

``$ gilda_local -i cases/demand_grid.json``


^^^^^^^^^^^^^^^^^^^^^
Accessing the Results
^^^^^^^^^^^^^^^^^^^^^

The results of the simulation will be printed on the screen. If you want to save
the output in a given output file, use the following command:

``$ gilda_local -i cases/demand_grid.json -o demand_grid_output.json``

The output file, which contains the optimal scheduling of the scenario, is also
a JSON file, which can be read visually or using some very interesting JSON
libraries, such as `orjson`_.

=============
Documentation
=============

The primary source of documentation for ``GILDA-LOCAL`` is this manual, which
gives an overview of ``GILDA-LOCAL``’s capabilities, describes the elements
structure, modeling and formulations behind the code. It can be found in your
``GILDA-LOCAL`` distribution from the `Github repository`_.


.. _pyenv: https://github.com/pyenv/pyenv
.. _virtualenv: https://pypi.org/project/orjson/
.. _Github repository: https://github.com/marcelomatus/gilda-local
.. _chocolatey: https://chocolatey.org
.. _orjson: https://pypi.org/project/orjson
