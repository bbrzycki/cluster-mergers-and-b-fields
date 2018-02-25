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

    # do all time series
    for sim_name in sim_names:
        hdf5_filename = '%s_no_mag.hdf5' % sim_name
        # time_series_r_200_follow just tracking gas gravitational potential minimum
        # time_series_0.15r_500_part_gpm
        # time_series_1.0r_500_part_gpm
        # time_series_0.15r_500_gpm1
        hdf5_groupname_0 = 'time_series_0.15r_500_100part'
        hdf5_groupname_1 = 'time_series_1.0r_500_100part'

        ds_header = 'fiducial_%s_hdf5_plt_cnt_' % sim_name
        ds_full_paths = m.glob.glob(data_dir+'fid/'+sim_name+'/'+ds_header+'0[0-9][0-9][05]')
        ds_full_paths.sort()

        field_list = ['mass',
                      'internal_energy',
                      'kinetic_energy',
                      'turbulent_kinetic_energy']

        magnolia.make_energy_over_time(ds_full_paths,
                                       field_list,
                                       hdf5_dir,
                                       hdf5_filename,
                                       hdf5_groupname_0,
                                       r500_multiplier = 0.15)
        magnolia.make_energy_over_time(ds_full_paths,
                                       field_list,
                                       hdf5_dir,
                                       hdf5_filename,
                                       hdf5_groupname_1,
                                       r500_multiplier = 1.0)
