#%matplotlib inline
import yt
from yt.units import dimensions, kboltz, mp
import os, sys, glob, errno
import matplotlib as mpl
mpl.use("agg")
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import operator

################################################################
################################################################
# initialize all fields

mu = 0.588

def _density1(field, data):
    return data["density"] * data["clr1"]
yt.add_field(("gas", "density1"), function=_density1, units="g/cm**3")

def _density2(field, data):
    return data["density"] * data["clr2"]
yt.add_field(("gas", "density2"), function=_density2, units="g/cm**3")

def _density_total(field, data):
    return data["density1"]+data["density2"]
yt.add_field(("gas","density_total"), function=_density_total, units="g/cm**3")

def _mass1(field, data):
    return data["density1"]*data["cell_volume"]
yt.add_field(("gas", "mass1"), function=_mass1, units="g")

def _mass2(field, data):
    return data["density2"]*data["cell_volume"]
yt.add_field(("gas", "mass2"), function=_mass2, units="g")

def _mass_total(field, data):
    return data["mass1"]+data["mass2"]
yt.add_field(("gas","mass_total"), function=_mass_total, units="g")

def _kinetic_energy1(field, data):
    return 0.5*data["density1"]*data["velocity_magnitude"]**2 * data["cell_volume"]
yt.add_field(("gas","kinetic_energy1"), function=_kinetic_energy1, units="erg")

def _kinetic_energy2(field, data):
    return 0.5*data["density2"]*data["velocity_magnitude"]**2 * data["cell_volume"]
yt.add_field(("gas","kinetic_energy2"), function=_kinetic_energy2, units="erg")

def _kinetic_energy_total(field, data):
    return data["kinetic_energy1"]+data["kinetic_energy2"]
yt.add_field(("gas","kinetic_energy_total"), function=_kinetic_energy_total, units="erg")

def _kinetic_pressure(field, data):
    return data["kinetic_energy_total"]/data["cell_volume"]
yt.add_field(("gas","kinetic_pressure"), function=_kinetic_pressure, units="erg/cm**3")

def _internal_energy1(field, data):
    return 1.5*data["density1"]*kboltz * data["temperature"] / (mu * mp) * data["cell_volume"]
yt.add_field(("gas","internal_energy1"), function=_internal_energy1, units="erg")

def _internal_energy2(field, data):
    return 1.5*data["density2"]*kboltz * data["temperature"] / (mu * mp) * data["cell_volume"]
yt.add_field(("gas","internal_energy2"), function=_internal_energy2, units="erg")

def _internal_energy_total(field, data):
    return data["internal_energy1"]+data["internal_energy2"]
yt.add_field(("gas","internal_energy_total"), function=_internal_energy_total, units="erg")

def _magnetic_energy1(field, data):
   return 1.0/(8*np.pi) * data["magnetic_field_strength"]**2 * data["clr1"] * data["cell_volume"]
yt.add_field(("gas","magnetic_energy1"), function=_magnetic_energy1, units="erg")

def _magnetic_energy2(field, data):
   return 1.0/(8*np.pi) * data["magnetic_field_strength"]**2 * data["clr2"] * data["cell_volume"]
yt.add_field(("gas","magnetic_energy2"), function=_magnetic_energy2, units="erg")

def _magnetic_energy_total(field, data):
   return data["magnetic_energy1"]+data["magnetic_energy2"]
yt.add_field(("gas","magnetic_energy_total"), function=_magnetic_energy_total, units="erg")

def _magnetic_pressure(field, data):
   return data["magnetic_energy_total"]/data["cell_volume"]
yt.add_field(("gas","magnetic_pressure"), function=_magnetic_pressure, units="erg/cm**3")

def _gravitational_potential_energy1(field, data):
    return 0.5 * data["density1"] * data["gpot"] * data["cell_volume"]
yt.add_field(("gas","gravitational_potential_energy1"), function=_gravitational_potential_energy1, units="erg")
    
def _gravitational_potential_energy2(field, data):
    return 0.5 * data["density2"] * data["gpot"] * data["cell_volume"]
yt.add_field(("gas","gravitational_potential_energy2"), function=_gravitational_potential_energy2, units="erg")

def _gravitational_potential_energy_total(field, data):
    return data["gravitational_potential_energy1"] + data["gravitational_potential_energy2"]
yt.add_field(("gas","gravitational_potential_energy_total"), function=_gravitational_potential_energy_total, units="erg")

def _particle_gpot2(field, data):
    logic = data["io","particle_halo"] == 1.
    return data["io","particle_gpot"]*logic
yt.add_field(("io", "particle_gpot2"), function=_particle_gpot2, units="dimensionless",particle_type=True,force_override=True)

def get_units(L):
    temp_str = str(L[-1:])
    k = temp_str.rfind("]") + 2
    return temp_str[k:]

################################################################
################################################################
# initialize filenames / relevant strings

DATA_DIR = "/data/mimir/jzuhone/data/"


# double check this is the same for each simulation
# ds_fn_head_no_mag="fiducial_%s_hdf5_plt_cnt_" % SIM_TYPE
# ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % SIM_TYPE
        
sim_names_mag=['1to1_b0']
#sim_names_mag=['1to1_b0']
slice_fields = ['particle_gpot2','particle_gpot']

# do all time series
for sim_name in sim_names_mag:
    IMG_DIR="data_products/mag/"+sim_name+"/"
    
    try:
        os.makedirs(IMG_DIR+"slice_plots")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
    # DYBO: dynamic bounds -- ie not static. change bounds once we see resultant movie
    for field in slice_fields:
        try:
            os.makedirs(IMG_DIR+"slice_plots/"+field+"_6Mpc_dybo")
            #os.makedirs(IMG_DIR+"slice_plots/"+field+"_6Mpc")
            #os.makedirs(IMG_DIR+"slice_plots/"+field)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
    if sim_name[:4]=='1to3':
        ds_fn_head_mag="fiducial_%s_hdf5_plt_cnt_" % sim_name
    else:
        ds_fn_head_mag="fiducial_%s_mag_hdf5_plt_cnt_" % sim_name
    full_path_header=DATA_DIR+"fid_mag/"+sim_name+"/"+ds_fn_head_mag    
    
    data_fns = glob.glob(full_path_header + "0[0-5][0-9][05]")
    #data_fns = m.glob.glob(full_path_header + "0[0-9][0-9][05]")
    # Sort them
    data_fns.sort()

    # Get a collection of datasets to iterate over
    ts = yt.DatasetSeries(data_fns)
    axis="z"

    # Now loop over the datasets
    for ds in ts:
        for field in slice_fields:
            fn = IMG_DIR+"slice_plots/"+field+"_6Mpc_dybo"+"/"+str(ds)+"_Slice_"+axis+"_"+field+".png"
            #fn = IMG_DIR+"slice_plots/"+field+"_6Mpc"+"/"+str(ds)+"_Slice_"+axis+"_"+field+".png"
            #fn = IMG_DIR+"slice_plots/"+field+"/"+str(ds)+"_Slice_"+axis+"_"+field+".png"
            #print("STARTSTARTSTART")
            if not os.path.exists(fn):
                #print("NONONONONONOONO")
                slc = yt.SlicePlot(ds, axis, ('io',field), width = (6,'Mpc'), center=("min","gpot"))
                #slc = yt.SlicePlot(ds, axis, field)
                
                # if field=="density":
                #     zlim1=1e-30
                #     zlim2=1e-25
                # elif field=="kT":
                #     zlim1=1e-1
                #     zlim2=1e2
                # elif field=="magnetic_field_strength":
                #    zlim1=1e-10
                #    zlim2=1e-5
                # else:
                #     print("Welp, that failed. No %s field found." % field)
                #     #sys.exit()
                # slc.set_zlim(field,zlim1,zlim2)
                
                slc.annotate_timestamp(redshift=False,draw_inset_box=True)
                slc.save(IMG_DIR+"slice_plots/"+field+"_6Mpc_dybo")
                #slc.save(IMG_DIR+"slice_plots/"+field+"_6Mpc")
                #slc.save(IMG_DIR+"slice_plots/"+field)
                print("%s %s saved" % (ds,field))

    print("Ended slice images of density, kT, and magnetic field strength")

