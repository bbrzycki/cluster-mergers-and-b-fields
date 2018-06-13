#!/usr/bin/env tcsh
echo "hi"
setenv PATH "/data/mimir/jzuhone/miniconda3/bin":$PATH
# python mag_generate_slice_plots.py
# python no_mag_generate_slice_plots.py
python ../mag_write_slice_multiplots.py
