# import sys
# sys.path.insert(0, 'pipeline_scripts/')

import no_mag_initialize as nm
import no_mag_write_data_functions as nmwdf

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
    nm.os.makedirs("img")
except OSError as e:
    if e.errno != nm.errno.EEXIST:
        raise

# double check this is the same for each simulation
# ds_fn_head_no_mag="fiducial_%s_hdf5_plt_cnt_" % SIM_TYPE
# ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % SIM_TYPE

sim_names_no_mag=['1to1_b0','1to1_b0.5','1to1_b1',
                  '1to3_b0','1to3_b0.5','1to3_b1',
                  '1to10_b0','1to10_b0.5','1to10_b1']
#sim_names_no_mag=['1to10_b0', '1to10_b0.5','1to10_b1']
        
# profiles
for sim_name in sim_names_no_mag:
    ds_fn_head_no_mag="fiducial_%s_hdf5_plt_cnt_" % sim_name
    full_path_header=DATA_DIR+"fid/"+sim_name+"/"+ds_fn_head_no_mag
    
    ds0500 = nm.yt.load(full_path_header+"0500")
    field_list_p = ["kT","density","density_total","velocity_spherical_radius", "velocity_spherical_theta", "velocity_spherical_phi"]
    
    # make and write profiles
    p=nmwdf.create_profiles(ds0500, field_list_p)
    nmwdf.write_profiles("%s_no_mag.hdf5"%sim_name, "profiles_0500_gpot", p, field_list_p)
    #nmwdf.write_profiles("%s_no_mag.hdf5"%sim_name, "profiles_0500_80b", p, field_list_p)
   