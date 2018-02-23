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
        
#sim_names_mag=['1to1_b0','1to3_b1']
sim_names_mag=['1to1_b0.5','1to1_b1',
               '1to3_b0','1to3_b0.5','1to10_b0']
print("test")
# do all time series
for sim_name in sim_names_mag:
    if sim_name[:4]=='1to3':
        ds_fn_head_mag="fiducial_%s_hdf5_plt_cnt_" % sim_name
    else:
        ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % sim_name
    full_path_header=DATA_DIR+"fid_mag/"+sim_name+"/"+ds_fn_head_mag    
    
    #data_fns = m.glob.glob(full_path_header + "0450")
    data_fns = m.glob.glob(full_path_header + "0[0-9][02468]0")
    # grab core passage
    data_fns.append(full_path_header + "0070")
    if sim_name=='1to3_b1':
        data_fns.append(full_path_header + "0450")
    # Sort them
    data_fns.sort()

    # Get a collection of datasets to iterate over
    ts = m.yt.DatasetSeries(data_fns)
    field_list_p = ["kT","density","entropy"]
    for ds in ts:
        print("On %s entropy generation")
        index=str(ds)[-4:]
        p=mwdf.create_profiles(ds, field_list_p)
        mwdf.write_profiles("%s_mag.hdf5"%sim_name, "profiles_%s_80b"%index, p, field_list_p)
print("Entropy profiles complete")
    