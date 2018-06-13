import magnolia
import magnolia.derived_field_definitions
import magnolia.magfields
import glob, os, errno
import yt

if __name__ == '__main__':

    data_dir = '/data/mimir/jzuhone/data/'
    img_dir = 'slice-plots'

    sim_names = ['1to1_b0',
                 '1to1_b0.5',
                 '1to1_b1',
                 '1to3_b0',
                 '1to3_b0.5',
                 '1to3_b1',
                 '1to10_b0',
                 '1to10_b0.5',
                 '1to10_b1']

    center_methods = ['gpot',
                      'particle_gpot',
                      'most_bound',
                      'gpot_final']

    # do all time series
    for sim_name in sim_names:

        ds_header = 'fiducial_%s_mag_hdf5_plt_cnt_' % sim_name
        ds_full_paths = glob.glob(data_dir+'fid_mag/'+sim_name+'/'+ds_header+'0[0-9][0-9][05]')
        ds_full_paths.sort()

        # Get a collection of datasets to iterate over
        ts = yt.DatasetSeries(ds_full_paths)
        axis='z'

        ds_final = yt.load(ds_full_paths[-1])
        c_final = magnolia.find_center(ds_final, center_method = 'gpot')

        for center_method in center_methods:
            try:
                os.makedirs(img_dir+'/'+sim_name+'/magnetic_field_strength_4Mpc/'+center_method)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            for ds in ts:

                if center_method == 'gpot_final':
                    c = c_final
                else:
                    c = magnolia.find_center(ds, center_method = center_method)

                slc = yt.SlicePlot(ds, axis, 'magnetic_field_strength', width = (4,'Mpc'), center = c)

                zlim1=1e-10
                zlim2=1e-5
                slc.set_zlim('magnetic_field_strength',zlim1,zlim2)

                slc.annotate_timestamp(redshift=False,draw_inset_box=True)
                slc.annotate_streamlines('magnetic_field_x', 'magnetic_field_y',
                                         factor=16, density = 5, field_color='magnetic_field_strength')

                slc.save(img_dir+'/'+sim_name+'/magnetic_field_strength_4Mpc/'+center_method)
                print('%s %s saved' % (ds,center_method))
    print('Completed slice images')
