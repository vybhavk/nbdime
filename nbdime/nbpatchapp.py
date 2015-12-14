"""Utilities for patching notebooks"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
import sys
import nbformat
import json
from ._version import __version__
from .patching import patch_notebook


_usage = """\
Apply patch from nbpatch to a Jupyter notebook.

This is nbpatch from nbdime version {}.

Example usage:

  jupyter nbpatch before.ipynb patch.json after.ipynb
""".format(__version__)


def main_patch(bfn, dfn, afn):
    for fn in (bfn, dfn):
        if not os.path.exists(fn):
            print("Missing file {}".format(fn))
            return 1

    before = nbformat.read(bfn, as_version=4)
    with open(dfn) as df:
        d = json.load(df)

    after = patch_notebook(before, d)

    verbose = True
    if verbose:
        print(after)

    print("Writing", afn)
    nbformat.write(after, afn)
    return 0


def main():
    args = sys.argv[1:]
    if len(args) != 3:
        r = 1
    else:
        r = main_patch(*args)
    if r:
        print(_usage)
    sys.exit(r)