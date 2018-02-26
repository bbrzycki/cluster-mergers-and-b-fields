"""
Series of functions to plot profile and energy over time data. Includes
general functions to generate 3x1 or 3x3 paneled plots.

Currently incomplete, since the annotations and labels for the plots that
will appear in my thesis require a bit more finetuning. This will be done using
Jupyter notebooks located within the repo.
"""

import yt
from yt.units import kboltz, mp
import os
import sys
import glob
import errno
import matplotlib as mpl
mpl.use('agg')
import numpy as np
import matplotlib.pyplot as plt
import operator
import h5py

mu = 0.588
mu_e = 1.14
gamma = 5/3

# y_field is a YTArray
def estimate_y_bounds(y_field):
    min = 0
    max = 0
    print("Not yet implemented!"")
    return (min, max)

# plot 3x1 panel, 3 solid lines per panel
def create_3x1_3lpp():
    print("Not yet implemented!"")
    return

# plot 3x1 panel, 3 solid lines and 3 dashed lines per panel
def create_3x1_6lpp():
    print("Not yet implemented!"")
    return

# plot 3x3 panel, 3 solid lines and 2 dashed lines per panel
# primarily reserved for energy over time plots
def create_3x3_5lpp():
    print("Not yet implemented!"")
    return
