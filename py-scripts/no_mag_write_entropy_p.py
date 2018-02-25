import no_mag_initialize as nm
import no_mag_write_data_functions as nmwdf

DATA_DIR = '/data/mimir/jzuhone/data/'
IMG_DIR='img'

try:
    nm.os.makedirs('img')
except OSError as e:
    if e.errno != nm.errno.EEXIST:
        raise

# double check this is the same for each simulation
# ds_fn_head_no_mag='fiducial_%s_hdf5_plt_cnt_' % SIM_TYPE
# ds_fn_head_mag='fiducial_%s_mag_hdf5_plt_cnt_' % SIM_TYPE

sim_names_no_mag=['1to1_b0',
                  '1to1_b0.5',
                  '1to1_b1',
                  '1to3_b0',
                  '1to3_b0.5',
                  '1to3_b1',
                  '1to10_b0',
                  '1to10_b0.5',
                  '1to10_b1']

# profiles
for sim_name in sim_names_no_mag:
    ds_fn_head_no_mag='fiducial_%s_hdf5_plt_cnt_' % sim_name
    full_path_header=DATA_DIR+'fid/'+sim_name+'/'+ds_fn_head_no_mag

    #data_fns = m.glob.glob(full_path_header + '0450')
    data_fns = nm.glob.glob(full_path_header + '0[0-9][02468]0')
    # grab core passage
    data_fns.append(full_path_header + '0070')
    if sim_name=='1to3_b1':
        data_fns.append(full_path_header + '0450')
    # Sort them
    data_fns.sort()

    # Get a collection of datasets to iterate over
    ts = nm.yt.DatasetSeries(data_fns)
    field_list_p = ['kT',
                    'density',
                    'entropy']
    for ds in ts:
        print('On %s entropy generation')
        index=str(ds)[-4:]
        p=nmwdf.create_profiles(ds, field_list_p)
        nmwdf.write_profiles('%s_no_mag.hdf5'%sim_name, 'profiles_%s_80b'%index, p, field_list_p)
