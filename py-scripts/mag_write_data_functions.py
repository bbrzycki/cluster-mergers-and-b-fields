# bunch of functions to write data to file
import yt
import h5py
import numpy as np

# center_method
def find_center(ds, center_method='100part', halo=1):
    # Find the gravitational potential minimum
    print('Finding gravitational potential minimum')
    if center_method == 'gpot':
        # gas gpot
        v, c = ds.find_min('gpot')
    elif center_method == 'particle_gpot':
        # dark matter particle prescription, first iteration
        v, c = ds.find_min(('io','particle_gpot2'))
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
def create_profiles(ds, field_list, R=yt.quan(ds,(2.0,'Mpc')), n_bins=100):
    print('Finding gravitational potential minimum')
    # Find the gravitational potential minimum
    c = find_center(ds, center_method='gpot')

    # Make a sphere at this point
    sp = ds.sphere(c, R)

    print('Creating profiles')
    p = yt.create_profile(sp, 'radius', field_list, n_bins=n_bins)

    print('Finished creating profiles')
    return p

# write profile p with field_list to HDF5 file filename
# groupname is 0500_profiles, 0000_profiles, etc
def write_profiles(filename, groupname, p, field_list):
    # test if file exists
    f = h5py.File(filename, 'a')
    yt.YTArray.write_hdf5(p.x,filename, dataset_name='/%s/radius' % groupname)
    for field in field_list:
        yt.YTArray.write_hdf5(p[field],filename, dataset_name='/%s/%s_mean' % (groupname,field))
        yt.YTArray.write_hdf5(p.standard_deviation['gas','%s'%field],filename, dataset_name='/%s/%s_stddev' % (groupname,field))
    f.close()

# k is 0.15 or 1.0, r_200 in kpc
def create_total_box_time_series(ts, field_list, k, r_200=1550):
    ts_data = {}
    ts_data['centers']=[]
    ts_data['time']=[]
    for field in field_list:
        ts_data[field]=[]
    for ds in ts:
        try:
            quan_list=[]

            # Find the gravitational potential minimum
            c = find_center(ds, center_method='100part')

            r_500=r_200*0.65
            ts_data['centers'].append(c)
            ts_data['time'].append(ds.current_time.in_units('Gyr'))

            R = ds.quan(k*r_500, 'kpc') # where r_500 is the value taken from the ZuHone 2011 paper
            sp = ds.sphere(c, R)
            for field in field_list:
                if field=='turbulent_kinetic_energy':

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
                    quan=sp.quantities.total_quantity([field+'_total'])
                    if field=='kinetic_energy':
                        print('overall KE:',quan)

                print('Saving...')
                ts_data[field].append(quan)

        except Exception as error:
            f = open('error.txt','a')
            f.write('%s -- %s\n' % (ds, error))
            f.close()
    return ts_data

# groupname = time_series
def write_total_box_time_series(filename,groupname,ts_data,field_list):
    # text
    f = h5py.File(filename, 'a')
    for field in field_list:
        yt.YTArray.write_hdf5(yt.YTArray(ts_data[field]),filename, dataset_name='/%s/%s' % (groupname,field))
    # write centers
    yt.YTArray.write_hdf5(yt.YTArray(ts_data['centers']),filename, dataset_name='/%s/%s' % (groupname,'centers'))
    yt.YTArray.write_hdf5(yt.YTArray(ts_data['time']),filename, dataset_name='/%s/%s' % (groupname,'time'))
    f.close()
