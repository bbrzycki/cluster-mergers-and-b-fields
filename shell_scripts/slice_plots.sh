#!/usr/bin/env tcsh
setenv PATH "/data/odin/BACKUPS/jzuhone/miniconda3/bin:"$PATH
echo "hi"
python mag_generate_slice_plots.py
python no_mag_generate_slice_plots.py