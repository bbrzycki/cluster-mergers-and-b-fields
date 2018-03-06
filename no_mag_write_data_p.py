import magnolia

if __name__ == '__main__':

    data_dir = '/data/mimir/jzuhone/data/'
    hdf5_dir = 'processed-data'

    sim_names = ['1to1_b0',
                 '1to1_b0.5',
                 '1to1_b1',
                 '1to3_b0',
                 '1to3_b0.5',
                 '1to3_b1',
                 '1to10_b0',
                 '1to10_b0.5',
                 '1to10_b1']

    # do all profiles
    for sim_name in sim_names:

        hdf5_filename = '%s_no_mag.hdf5' % sim_name
        # sample groupnames: profiles_0250, profiles_0250_gpot,
        # profiles_0250_gpot_afterfix, 'profiles_0250_80b'
        hdf5_groupname = 'profiles_0500_most_bound'

        ds_header = 'fiducial_%s_hdf5_plt_cnt_' % sim_name
        ds_full_path = data_dir+'fid/'+sim_name+'/'+ds_header+'0500'

        field_list = ['kT',
                      'density',
                      'velocity_spherical_radius',
                      'velocity_spherical_theta',
                      'velocity_spherical_phi']

        magnolia.make_profiles(ds_full_path,
                               field_list,
                               hdf5_dir,
                               hdf5_filename,
                               hdf5_groupname,
                               center_method = 'most_bound')
