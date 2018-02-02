# import sys
# sys.path.insert(0, 'pipeline_scripts/')

import mag_initialize as m
import mag_write_data_functions as mwdf

#SIM_TYPE11 = "1to1_b0"
#SIM_TYPE21 = "1to3_b0"
#SIM_TYPE31 = "1to10_b0"
#SIM_TYPE12 = "1to1_b0.5"
#SIM_TYPE22 = "1to3_b0.5"
#SIM_TYPE32 = "1to10_b0.5"
#SIM_TYPE13 = "1to1_b1"
#SIM_TYPE23 = "1to3_b1"
#SIM_TYPE33 = "1to10_b1"

DATA_DIR = "/data/mimir/jzuhone/data/"
IMG_DIR="img"

try:
    m.os.makedirs("img")
except OSError as e:
    if e.errno != m.errno.EEXIST:
        raise

# double check this is the same for each simulation
# ds_fn_head_no_mag="fiducial_%s_hdf5_plt_cnt_" % SIM_TYPE
# ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % SIM_TYPE
        
# sim_names_mag=['1to1_b0','1to1_b0.5','1to1_b1',
#                '1to3_b0','1to3_b0.5','1to3_b1','1to10_b0']
sim_names_mag=['1to10_b0.5','1to10_b1']

# do all time series
for sim_name in sim_names_mag:
    ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % sim_name
    full_path_header=DATA_DIR+"fid_mag/"+sim_name+"/"+ds_fn_head_mag    
    
    data_fns = m.glob.glob(full_path_header + "0[0-9][0-9][05]")
    # Sort them
    data_fns.sort()

    # Get a collection of datasets to iterate over
    ts = m.yt.DatasetSeries(data_fns)
    field_list_ts = ["mass","internal_energy","kinetic_energy","magnetic_energy","turbulent_kinetic_energy"]
    #field_list_ts = ["turbulent_kinetic_energy"]

    #field_list_ts = ["internal_energy","mass","kinetic_energy","magnetic_energy","turbulent_kinetic_energy"]
    
    ts_data=mwdf.create_total_box_time_series(ts, field_list_ts, 0.15)
    # time_series_r_200_follow just tracking gas gravitational potential minimum
    # time_series_0.15r_500_part_gpm
    # time_series_1.0r_500_part_gpm
    # time_series_0.15r_500_gpm1
    mwdf.write_total_box_time_series("%s_mag.hdf5"%sim_name,"time_series_0.15r_500",ts_data,field_list_ts)
    
    ts_data=mwdf.create_total_box_time_series(ts, field_list_ts, 1.0)
    # time_series_r_200_follow just tracking gas gravitational potential minimum
    # time_series_0.15r_500_part_gpm
    # time_series_1.0r_500_part_gpm
    # time_series_0.15r_500_gpm1
    mwdf.write_total_box_time_series("%s_mag.hdf5"%sim_name,"time_series_1.0r_500",ts_data,field_list_ts)
