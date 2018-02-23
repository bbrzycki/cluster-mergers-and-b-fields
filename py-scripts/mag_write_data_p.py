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
        
sim_names_mag=['1to1_b0','1to1_b0.5','1to1_b1',
               '1to3_b0','1to3_b0.5','1to3_b1',
               '1to10_b0','1to10_b0.5','1to10_b1']
# sim_names_mag=['1to10_b0.5','1to10_b1']

# do all profiles
for sim_name in sim_names_mag:
    
    ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % sim_name
    full_path_header=DATA_DIR+"fid_mag/"+sim_name+"/"+ds_fn_head_mag
    
    
    #ds0000 = m.yt.load(full_path_header+"0000")
    #ds0250 = m.yt.load(full_path_header+"0250")
    #ds0400 = m.yt.load(full_path_header+"0400")
    field_list_p = ["kT","density","density_total","velocity_spherical_radius", "velocity_spherical_theta", "velocity_spherical_phi", "magnetic_field_spherical_radius", "magnetic_field_spherical_theta", "magnetic_field_spherical_phi"]
    
    # # MAKING FINAL STATE PROFILES
    # # profiles_0250, profiles_0250_gpot, profiles_0250_gpot_afterfix, "profiles_0250_80b"
    # if sim_name=='1to3_b1':
    #     # this simulation doesn't go out to 0500
    #     ds0450 = m.yt.load(full_path_header+"0450")
    #     p=mwdf.create_profiles(ds0450, field_list_p)
    #     mwdf.write_profiles("%s_mag.hdf5"%sim_name, "profiles_0450_gpot_afterfix", p, field_list_p)
    #     #mwdf.write_profiles("%s_mag.hdf5"%sim_name, "profiles_0450_80b", p, field_list_p)
    # else:
    #     ds0500 = m.yt.load(full_path_header+"0500")
    #     p=mwdf.create_profiles(ds0500, field_list_p)
    #     mwdf.write_profiles("%s_mag.hdf5"%sim_name, "profiles_0500_gpot_afterfix", p, field_list_p)
    #     #mwdf.write_profiles("%s_mag.hdf5"%sim_name, "profiles_0500_80b", p, field_list_p)
        
    # MAKING INITIAL STATE PROFILES
    ds0000 = m.yt.load(full_path_header+"0000")
    p=mwdf.create_profiles(ds0000, field_list_p)
    mwdf.write_profiles("%s_mag.hdf5"%sim_name, "profiles_0000_gpot_afterfix", p, field_list_p)
