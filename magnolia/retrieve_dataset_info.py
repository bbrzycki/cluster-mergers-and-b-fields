import yt
from yt.units import kboltz, mp
import numpy as np
import h5py

mu = 0.588
mu_e = 1.14
gamma = 5/3

# gets untis from YTArray
def get_units(L):
    temp_str = str(L[-1:])
    k = temp_str.rfind("]") + 2
    return temp_str[k:]

def get_groups(filename):
    f = h5py.File(filename,'r')
    groups = f.keys()
    f.close()
    return groups

def list_groups(filename):
    print(get_groups(filename))
    return

def get_fields(filename,groupname):
    f = h5py.File(filename,'r')
    fields = f[groupname]
    f.close()
    return fields

def list_fields(filename,groupname):
    print(get_fields(filename,groupname))
    return

def list_all_fields(filename):
    f = h5py.File(filename,'r')
    for groupname in f.keys():
        print(groupname)
        for field in get_fields(filename,groupname):
            print("-- " + field)
    f.close()
    return

# field is a string
def get_field(filename,groupname,full_fieldname):
    return yt.YTArray.from_hdf5(filename, dataset_name="/%s/%s"%(groupname,full_fieldname))

def get_mean(filename,groupname,field):
    return yt.YTArray.from_hdf5(filename, dataset_name="/%s/%s_mean"%(groupname,field))

def get_stddev(filename,groupname,field):
    return yt.YTArray.from_hdf5(filename, dataset_name="/%s/%s_stddev"%(groupname,field))

# convenience functions
def density(filename,groupname):
    return yt.YTArray.from_hdf5(filename, dataset_name="/%s/density_mean"%groupname)

def kT(filename,groupname):
    return yt.YTArray.from_hdf5(filename, dataset_name="/%s/kT_mean"%groupname)

# radial
def velocity_r_variance(filename,groupname):
    v_r_stddev=yt.YTArray.from_hdf5(filename, dataset_name="/%s/velocity_spherical_radius_stddev"%groupname)
    return v_r_stddev**2

# tangential
def velocity_t_variance(filename,groupname):
    v_theta_stddev=yt.YTArray.from_hdf5(filename, dataset_name="/%s/velocity_spherical_theta_stddev"%groupname)
    v_phi_stddev=yt.YTArray.from_hdf5(filename, dataset_name="/%s/velocity_spherical_phi_stddev"%groupname)
    return v_theta_stddev**2+v_phi_stddev**2

# filename is HDF5 file, groupname is 0500_profiles
def velocity_variance(filename,groupname):
    return velocity_r_variance(filename,groupname)+velocity_t_variance(filename,groupname)

# mean squared
def velocity_mean_squared(filename,groupname):
    v_r_mean=yt.YTArray.from_hdf5(filename, dataset_name="/%s/velocity_spherical_radius_mean"%groupname)
    v_t_mean=yt.YTArray.from_hdf5(filename, dataset_name="/%s/velocity_spherical_theta_mean"%groupname)
    v_p_mean=yt.YTArray.from_hdf5(filename, dataset_name="/%s/velocity_spherical_phi_mean"%groupname)
    return v_r_mean**2+v_t_mean**2+v_p_mean**2

def mag_field_r_variance(filename,groupname):
    B_r_stddev=m.yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_field_spherical_radius_stddev"%groupname)[a:]
    return B_r_stddev**2

# tangential
def mag_field_t_variance(filename,groupname):
    B_theta_stddev=m.yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_field_spherical_theta_stddev"%groupname)[a:]
    B_phi_stddev=m.yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_field_spherical_phi_stddev"%groupname)[a:]
    return B_theta_stddev**2+B_phi_stddev**2

# filename is HDF5 file, groupname is 0500_profiles
def mag_field_variance(filename,groupname):
    return mag_field_r_variance(filename,groupname)+mag_field_t_variance(filename,groupname)

# mean squared
def mag_field_mean_squared(filename,groupname):
    B_r_mean=yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_field_spherical_radius_mean"%groupname)
    B_t_mean=yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_field_spherical_theta_mean"%groupname)
    B_p_mean=yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_field_spherical_phi_mean"%groupname)
    return B_r_mean**2+B_t_mean**2+B_p_mean**2

def mag_field_squared_mean(filename,groupname):
    return (mag_field_variance(filename,groupname)+mag_field_mean_squared(filename,groupname))

# sound speed sq
def c_s_squared(filename,groupname):
    return gamma*kT(filename,groupname)/(mu*mp)

# Alfven speed sq
def v_A_squared(filename,groupname):
    return mag_field_squared_mean(filename,groupname)/(4*np.pi*density(filename,groupname))

def n_e(filename,groupname):
    return density(filename,groupname)/(mu_e*mp)

def entropy(filename,groupname):
    return kT(filename,groupname)/(n_e(filename,groupname))**(2/3)

def get_mass(filename,groupname):
    M=yt.YTArray.from_hdf5(filename, dataset_name="/%s/mass"%groupname).in_units('Msun')
    return M

def get_IE(filename,groupname):
    IE=yt.YTArray.from_hdf5(filename, dataset_name="/%s/internal_energy"%groupname).in_units('erg')
    return IE

def get_KE(filename,groupname):
    KE=yt.YTArray.from_hdf5(filename, dataset_name="/%s/kinetic_energy"%groupname).in_units('erg')
    return KE

def get_tKE(filename,groupname):
    tKE=yt.YTArray.from_hdf5(filename, dataset_name="/%s/turbulent_kinetic_energy"%groupname).in_units('erg')
    return tKE

def get_total_ME(filename,groupname):
    ME=yt.YTArray.from_hdf5(filename, dataset_name="/%s/magnetic_energy"%groupname).in_units('erg')
    return ME
