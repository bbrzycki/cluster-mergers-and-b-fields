# bunch of functions to write data to file
import os
import sys
import glob
import errno
import yt
import h5py
import numpy as np

# center_method
def find_center(ds,
                center_method = '100part',
                halo = 1):
    # Find the gravitational potential minimum
    print('Finding gravitational potential minimum')
    if center_method == 'gpot':
        # gas gpot
        v, c = ds.find_min('gpot')
    elif center_method == 'particle_gpot':
        # dark matter particle prescription, first iteration
        v, c = ds.find_min(('io','particle_gpot_halo1'))
    elif center_method == 'most_bound':
        # Get all the data
        dd = ds.all_data()
        # Find the mean velocity of halo 1's particles
        logic = dd['particle_halo'].astype('int') == halo
        pvx = (dd['particle_velocity_x']*logic).mean()
        pvy = (dd['particle_velocity_y']*logic).mean()
        pvz = (dd['particle_velocity_z']*logic).mean()
        # We use ds.arr to compute a YTArray from this because we need
        # code_length that only ds knows about
        pv = ds.arr([pvx, pvy, pvz])
        # Set the field parameter 'bulk_velocity' to the mean of all
        # halo 1's particles
        dd.set_field_parameter('bulk_velocity', pv)
        # This gives you the center
        idx = np.argmin(dd['io','particle_ener'])
        c = dd['particle_position'][idx]
        # Should reset bulk_velocity to zero now
        dd.set_field_parameter('bulk_velocity', ds.arr([0.0, 0.0, 0.0], 'code_length'))
    elif center_method == '100part':
        # Get all the data
        dd = ds.all_data()
        # Find the halo's particles
        logic = dd['io','particle_halo'].astype('int') == halo
        idx = np.argsort(dd['io','particle_gpot']*logic)[:100]
        c = dd['io','particle_position'][idx,:].mean(axis=0)
    else:
        print('Return a valid centering method!')
        return -1
    return c

# returns profile object
# R in kpc
def generate_profiles(ds,
                      field_list,
                      R = 2000,
                      n_bins = 100,
                      center_method = 'gpot'):
    print('Finding gravitational potential minimum')
    # Find the gravitational potential minimum
    c = find_center(ds, center_method)

    # Make a sphere at this point
    sp = ds.sphere(c, ds.quan(R, 'kpc'))

    print('Creating profiles')
    p = yt.create_profile(sp, 'radius', field_list, n_bins=n_bins)

    print('Finished creating profiles')
    return p

# write profile p with field_list to HDF5 file filename
# groupname is 0500_profiles, 0000_profiles, etc
def write_profiles_to_hdf5(filename,
                           groupname,
                           profile,
                           field_list):
    # test if file exists
    f = h5py.File(filename, 'a')
    yt.YTArray.write_hdf5(profile.x,filename, dataset_name='/%s/radius' % groupname)
    for field in field_list:
        yt.YTArray.write_hdf5(profile[field],filename, dataset_name='/%s/%s_mean' % (groupname,field))
        yt.YTArray.write_hdf5(profile.standard_deviation['gas','%s'%field],filename, dataset_name='/%s/%s_stddev' % (groupname,field))
    f.close()

# ds_path is the full path to the dataset file
# hdf5_directory is desired directory name for HDF5 files
# R in kpc
def make_profiles(ds_path,
                  field_list,
                  hdf5_directory,
                  hdf5_filename,
                  hdf5_groupname,
                  R = 2000,
                  n_bins = 100,
                  center_method = 'gpot'):
    # try creating directory if it doesn't exist
    try:
        os.makedirs(hdf5_directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    ds = yt.load(ds_path)
    profile = generate_profiles(ds,
                                field_list,
                                center_method = center_method,
                                R = ds.quan(R, 'kpc'),
                                n_bins = n_bins)
    write_profiles_to_hdf5(hdf5_directory + '/' + hdf5_filename,
                           hdf5_groupname,
                           profile,
                           field_list)

# r500_multiplier is 0.15 or 1.0, r200 in kpc
# region is either 'sphere' or 'full_box'
def generate_energy_over_time(ts,
                              field_list,
                              region = 'sphere',
                              r500_multiplier = 0.15,
                              r200 = 1550,
                              center_method = '100part'):
    ts_data = {}
    ts_data['centers'] = []
    ts_data['time'] = []
    for field in field_list:
        ts_data[field] = []
    for ds in ts:
        try:
            quan_list = []

            if region == 'sphere':
                # Find the gravitational potential minimum
                c = find_center(ds, center_method)

                r500 = r200 * 0.65
                ts_data['centers'].append(c)
                ts_data['time'].append(ds.current_time.in_units('Gyr'))

                R = ds.quan(r500_multiplier * r500, 'kpc') # where r500 is the value taken from the ZuHone 2011 paper
                sp = ds.sphere(c, R)
            elif region == 'full_box':
                sp = ds.all_data()
            else:
                sys.exit("Specified invalid region!")

            for field in field_list:
                if field == 'turbulent_kinetic_energy':

                    # Find the average velocity of the sphere
                    bvx = sp.mean('velocity_x')
                    bvy = sp.mean('velocity_y')
                    bvz = sp.mean('velocity_z')

                    # We use ds.arr to compute a YTArray from this because we need
                    # code_length that only ds knows about
                    bv = ds.arr([bvx, bvy, bvz])

                    # Set the field parameter 'bulk_velocity' to this mean for the
                    # sphere
                    sp.set_field_parameter('bulk_velocity', bv)

                    # Then you compute the total kinetic energy in the sphere. As a sanity check,
                    # at t = 0 it should be equal to zero (or close), especially for the 0.15*r500
                    # sphere
                    print('Calculating total %s -- %s' % ('turbulent_kinetic_energy',ds))
                    quan=sp.quantities.total_quantity(['kinetic_energy'+'_total'])
                    print('turbulent KE:',quan)

                    # After you are done, you should set the bulk velocity back to zero

                    sp.set_field_parameter('bulk_velocity', ds.arr([0.0, 0.0, 0.0], 'code_length'))

                else:
                    print('Calculating total %s -- %s' % (field,ds))
                    quan = sp.quantities.total_quantity([field+'_total'])
                    if field == 'kinetic_energy':
                        print('overall KE:',quan)

                print('Saving...')
                ts_data[field].append(quan)

        except Exception as error:
            f = open('error.txt','a')
            f.write('%s -- %s\n' % (ds, error))
            f.close()
    return ts_data

# groupname = time_series
def write_energy_over_time_to_hdf5(filename,
                                   groupname,
                                   ts_data,
                                   field_list):
    # text
    f = h5py.File(filename, 'a')
    for field in field_list:
        yt.YTArray.write_hdf5(yt.YTArray(ts_data[field]),filename, dataset_name='/%s/%s' % (groupname,field))
    # write centers
    yt.YTArray.write_hdf5(yt.YTArray(ts_data['centers']),filename, dataset_name='/%s/%s' % (groupname,'centers'))
    yt.YTArray.write_hdf5(yt.YTArray(ts_data['time']),filename, dataset_name='/%s/%s' % (groupname,'time'))
    f.close()

# ds_paths is a list of full paths to the dataset files
# hdf5_directory is desired directory name for HDF5 files
# r200 in kpc
def make_energy_over_time(ds_paths,
                          field_list,
                          hdf5_directory,
                          hdf5_filename,
                          hdf5_groupname,
                          region = 'sphere',
                          r500_multiplier = 0.15,
                          r200 = 1550,
                          center_method = 'gpot'):
    # try creating directory if it doesn't exist
    try:
        os.makedirs(hdf5_directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    ts = yt.DatasetSeries(ds_paths)

    ts_data = generate_energy_over_time(ts,
                                        field_list,
                                        region = region,
                                        r500_multiplier = r500_multiplier,
                                        r200 = r200,
                                        center_method = center_method)
    write_energy_over_time_to_hdf5(hdf5_directory + '/' + hdf5_filename,
                                   hdf5_groupname,
                                   ts_data,
                                   field_list)
