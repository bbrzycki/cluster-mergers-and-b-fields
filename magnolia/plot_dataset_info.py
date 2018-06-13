"""
Series of functions to plot profile and energy over time data. Includes
general functions to generate 3x1 or 3x3 paneled plots.

Currently incomplete, since the annotations and labels for the plots that
will appear in analysis require finetuning. This will be done using
Jupyter notebooks located within the repo.
"""

import yt
from yt.units import kboltz, mp
import os
import sys
import glob
import errno
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import AxesGrid
mpl.use('agg')
import numpy as np
import matplotlib.pyplot as plt
import operator
import h5py

mu = 0.588
mu_e = 1.14
gamma = 5/3

def make_multiplot(field,ds_paths,zlim1,zlim2,cmap,output_fn):

    plt.close('all')

    fig = plt.figure()

    grid = AxesGrid(fig, (0.075,0.075,0.85,0.85),
                    nrows_ncols = (2, 3),
                    axes_pad = 0.05,
                    label_mode = "1",
                    share_all = True,
                    cbar_location="right",
                    cbar_mode="single",
                    cbar_size="3%",
                    cbar_pad="0%")

    for i, path in enumerate(ds_paths):
        # Load the data and create a single plot
        ds = yt.load(path) # load data
        slc = yt.SlicePlot(ds, 'z', [field], width=(8,'Mpc'))

        slc.set_font({'family':'dejavuserif', 'size':14})

        slc.set_zlim(field, zlim1, zlim2)
        slc.set_cmap(field=field, cmap=cmap)
        if field == ('deposit', 'all_cic'):
            slc.set_log("all_cic", True)
        slc.annotate_timestamp(corner='upper_left',redshift=False,draw_inset_box=True)
        slc.annotate_scale(corner='lower_right')

        # This forces the SlicePlot to redraw itself on the AxesGrid axes.
        plot = slc.plots[field]
        plot.figure = fig
        plot.axes = grid[i].axes
        plot.cax = grid.cbar_axes[i]

        # Finally, this actually redraws the plot.
        slc._setup_plots()

    plt.gcf().subplots_adjust(right=0.15)
    plt.savefig(output_fn, bbox_inches='tight')
