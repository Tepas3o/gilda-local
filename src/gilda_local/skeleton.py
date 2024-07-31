"""This is the gilda_opt main program."""

import argparse
import logging
import sys
import os

from gilda_local import __version__
from gilda_local.system import System
from gilda_local.system_lp import SystemLP

__author__ = "Marcelo Matus"
__copyright__ = "Marcelo Matus"
__license__ = "EPL-1.0"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from gilda_local.skeleton import fib`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters."""
    parser = argparse.ArgumentParser(
        prog="gilda_local", description="Gilda Optimization Scheduler"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"gilda-local {__version__}",
    )
    parser.add_argument(
        "-i",
        "--infile",
        dest="infile",
        help="Json input file. Stdinp is used if not provided.",
        type=argparse.FileType("r"),
        metavar="INFILE_NAME",
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--outfile",
        dest="outfile",
        help="Json output file. Stdout is used if not provided.",
        type=argparse.FileType("w"),
        metavar="OUTFILE_NAME",
        default=sys.stdout,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-k",
        "--keepfiles",
        action="store_true",
        default=False,
        help="If included, the solver keepfiles option is used",
    )
    parser.add_argument(
        "-s",
        "--solver",
        type=str,
        default="cbc",
        help="Defines the solver to be used (default: cbc)",
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Set basic logging.

    Arguments:
    ----------
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrap allowing gild_opt to be called with string arguments in a CLI fashion."""
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting gilda opt ...")

    file_contents = args.infile.read()
    try:
        system = System.from_json(file_contents)
    except Exception as e:  # pylint: disable=W0718
        print(
            "An error occurred parsing the input file",
            os.path.basename(args.infile.name),
        )
        print(e)
        sys.exit(1)

    system_lp = SystemLP(system)
    status = system_lp.solve(keepfiles=args.keepfiles, solver=args.solver)

    if status == "ok":
        sched = system_lp.get_sched()
        str_sched = sched.to_json(indent=4)
        args.outfile.write(str_sched)
        args.outfile.write("\n")


def run():
    """Call :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`.

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m gilda_local.skeleton
    #
    run()
