# bunch of functions to write data to file
import mag_initialize as m
import numpy as np

def find_center(ds1):
    print('Finding gravitational potential minimum')
    # Find the gravitational potential minimum                                                                                                   
    #####                                                                                                                                        
    # Get all the data                    
    dd = ds1.all_data()

    # Find the halo's particles                                                                                                                                
    print(1)
    print(dd["io","particle_halo"][:10])
    logic = dd["io","particle_halo"].astype("int") == 1
    print(2)
    idx = np.argsort(dd['io','particle_gpot']*logic)[:100]
    print(3)
    c = dd["io","particle_position"][idx,:].mean(axis=0)
    print(4)
    
    return c

# returns profile object
def create_profiles(ds, field_list):
    print('Finding gravitational potential minimum')
    # Find the gravitational potential minimum
    v, c = ds.find_min("gpot")
    
    #####
#     # Get all the data
#     dd = ds.all_data()

#     # Find the mean velocity of halo 1's particles
#     logic = dd["particle_halo"].astype("int") == 1

#     pvx = (dd["particle_velocity_x"]*logic).mean()
#     pvy = (dd["particle_velocity_y"]*logic).mean()
#     pvz = (dd["particle_velocity_z"]*logic).mean()

#     # We use ds.arr to compute a YTArray from this because we need 
#     # code_length that only ds knows about
#     pv = ds.arr([pvx, pvy, pvz])

#     # Set the field parameter "bulk_velocity" to the mean of all 
#     # halo 1's particles
#     dd.set_field_parameter("bulk_velocity", pv)
    
#     # This gives you the center
#     #c = dd.argmin(('io','particle_ener'))
    
#     idx = m.np.argmin(dd['io','particle_ener'])
#     c = dd["particle_position"][idx]
    
#     # Should reset bulk_velocity to zero now
#     dd.set_field_parameter("bulk_velocity", ds.arr([0.0, 0.0, 0.0], "code_length"))
    #####
    
    # dark matter particle prescription, first iteration (deprecated)
    # v, c = ds.find_min(('io','particle_gpot2'))

    # Make a sphere at this point
    sp = ds.sphere(c, (2.0, "Mpc"))

    print('Creating profiles')
    p = m.yt.create_profile(sp, "radius", field_list, n_bins=100)
    
    print('Finished creating profiles')
    return p

# write profile p with field_list to HDF5 file filename
# groupname is 0500_profiles, 0000_profiles, etc
def write_profiles(filename, groupname, p, field_list):
    # test if file exists
    f = m.h5py.File(filename, 'a')
    m.yt.YTArray.write_hdf5(p.x,filename, dataset_name="/%s/radius" % groupname)
    for field in field_list:
        m.yt.YTArray.write_hdf5(p[field],filename, dataset_name="/%s/%s_mean" % (groupname,field))
        m.yt.YTArray.write_hdf5(p.standard_deviation['gas','%s'%field],filename, dataset_name="/%s/%s_stddev" % (groupname,field))
    f.close()

# k is 0.15 or 1.0
def create_total_box_time_series(ts, field_list, k):
    # text
    print("hello??")
    ts_data = {}
    #centers = []
    #time=[]
    ts_data["centers"]=[]
    ts_data["time"]=[]
    for field in field_list:
        ts_data[field]=[]
        # ts_data[field+"1"]=[]
        # ts_data[field+"2"]=[]
        # ts_data[field+"_total"]=[]
    for ds in ts:
        try:
            # list1=[]
            # list2=[]
            # list_total=[]
            quan_list=[]
            
#             #####
#             # Get all the data
#             dd = ds.all_data()

#             # Find the mean velocity of halo 1's particles
#             logic = dd["particle_halo"].astype("int") == 1
            

#             pvx = (dd["particle_velocity_x"]*logic).mean()
#             pvy = (dd["particle_velocity_y"]*logic).mean()
#             pvz = (dd["particle_velocity_z"]*logic).mean()

#             # We use ds.arr to compute a YTArray from this because we need 
#             # code_length that only ds knows about
#             pv = ds.arr([pvx, pvy, pvz])

#             # Set the field parameter "bulk_velocity" to the mean of all 
#             # halo 1's particles
#             dd.set_field_parameter("bulk_velocity", pv)
            
#             # This gives you the center
#             #c = dd.argmin(('io','particle_ener'))
            
#             idx = m.np.argmin(dd['io','particle_ener'])
#             c = dd["particle_position"][idx]
            

#             # Should reset bulk_velocity to zero now
#             dd.set_field_parameter("bulk_velocity", ds.arr([0.0, 0.0, 0.0], "code_length"))
#             #####

#             dd = ds.all_data()

#             # Find the halo's particles         
#             print(1)
#             print(dd["particle_halo"][:10])
#             logic = dd["particle_halo"].astype("int") == 1
#             print(2)
#             idx = np.argsort(dd['io','particle_gpot']*logic)[:100]
#             print(3)
#             c = dd['particle_position'][idx,:].mean(axis=0)
#             print(4)
            
            dd = ds.all_data()
            logic = dd["io","particle_halo"].astype("int") == 1
            idx = np.argsort(dd['io','particle_gpot']*logic)[:100]
            #print(idx)
            c = dd['particle_position'][idx,:].mean(axis=0)
            
            # c = find_center(ds)
            # print(c,"test")
            
            #ad = ds.all_data()
            #v, c = ds.find_min("gpot")
            #v, c = ds.find_min(('io','particle_gpot2'))
            r_200=1550
            r_500=r_200*0.65
            ts_data["centers"].append(c)
            ts_data["time"].append(ds.current_time.in_units('Gyr'))

            R = ds.quan(k*r_500, "kpc") # where r_500 is the value taken from the ZuHone 2011 paper
            sp = ds.sphere(c, R)
            for field in field_list:
                if field=="turbulent_kinetic_energy":
                    #####
                    # Find the average velocity of the sphere
                    bvx = sp.mean("velocity_x")
                    bvy = sp.mean("velocity_y")
                    bvz = sp.mean("velocity_z")

                    # We use ds.arr to compute a YTArray from this because we need 
                    # code_length that only ds knows about
                    bv = ds.arr([bvx, bvy, bvz])

                    # Set the field parameter "bulk_velocity" to this mean for the
                    # sphere
                    sp.set_field_parameter("bulk_velocity", bv)

                    # Then you compute the total kinetic energy in the sphere. As a sanity check,
                    # at t = 0 it should be equal to zero (or close), especially for the 0.15*r500
                    # sphere
                    # print(bv)
                    # print(sp.get_field_parameter("bulk_velocity"))
                    print("Calculating total %s -- %s" % ("turbulent_kinetic_energy",ds))
                    # quan1=sp.quantities.total_quantity(["kinetic_energy"+"1"])
                    # quan2=sp.quantities.total_quantity(["kinetic_energy"+"2"])
                    quan=sp.quantities.total_quantity(["kinetic_energy"+"_total"])
                    # print("NEW:",sp.quantities.total_quantity(["kinetic_energy"+"_total"]))
                    # print("OLD:",quan)
                    print("turbulent KE:",quan)
                    
                    # After you are done, you should set the bulk velocity back to zero

                    sp.set_field_parameter("bulk_velocity", ds.arr([0.0, 0.0, 0.0], "code_length"))
                    #####
                else:
                    print("Calculating total %s -- %s" % (field,ds))
                    quan=sp.quantities.total_quantity([field+"_total"])
                    if field=="kinetic_energy":
                        print("overall KE:",quan)
                
                # print("Calculating total %s -- %s" % (field+"1",ds))
                # quan1=ad.quantities.total_quantity([field+"1"])
                # print("Finished calculating total %s" % (field+"1"))
                # print("Calculating total %s" % (field+"2") )     
                # quan2=ad.quantities.total_quantity([field+"2"])
                # print("Finished calculating total %s" % (field+"2"))
                # quan_total=quan1+quan2
                
                print("Saving...")
                ts_data[field].append(quan)
                # ts_data[field+"1"].append(quan1)
                # ts_data[field+"2"].append(quan2)
                # ts_data[field+"_total"].append(quan_total)
                
        except Exception as error:
            f = open("error.txt",'a')
            f.write("%s -- %s\n" % (ds, error))
            f.close()
    return ts_data
    
# groupname = time_series
def write_total_box_time_series(filename,groupname,ts_data,field_list):
    # text
    f = m.h5py.File(filename, 'a')
    for field in field_list:
        m.yt.YTArray.write_hdf5(m.yt.YTArray(ts_data[field]),filename, dataset_name="/%s/%s" % (groupname,field))
        # m.yt.YTArray.write_hdf5(m.yt.YTArray(ts_data[field+"1"]),filename, dataset_name="/%s/%s" % (groupname,field+"1"))
        # m.yt.YTArray.write_hdf5(m.yt.YTArray(ts_data[field+"2"]),filename, dataset_name="/%s/%s" % (groupname,field+"2"))
        # m.yt.YTArray.write_hdf5(m.yt.YTArray(ts_data[field+"_total"]),filename, dataset_name="/%s/%s" % (groupname,field+"_total"))
    # write centers
    m.yt.YTArray.write_hdf5(m.yt.YTArray(ts_data["centers"]),filename, dataset_name="/%s/%s" % (groupname,"centers"))
    m.yt.YTArray.write_hdf5(m.yt.YTArray(ts_data["time"]),filename, dataset_name="/%s/%s" % (groupname,"time"))
    f.close()