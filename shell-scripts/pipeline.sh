#!/usr/bin/env tcsh
setenv PATH "/data/odin/BACKUPS/jzuhone/miniconda3/bin:"$PATH
echo "hi"
python ../mag_write_data_p.py
python ../no_mag_write_data_p.py
python ../mag_write_data_ts.py
python ../no_mag_write_data_ts.py
# python mag_write_entropy_p.py
# python plot_data.py
