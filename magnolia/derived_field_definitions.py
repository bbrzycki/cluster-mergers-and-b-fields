import yt
from yt.units import kboltz, mp
import os
import sys
import glob
import errno
import matplotlib as mpl
mpl.use('agg')
import numpy as np
import matplotlib.pyplot as plt
import operator
import h5py

mu = 0.588
mu_e = 1.14
gamma = 5/3

def _density1(field, data):
    return data['density'] * data['clr1']
yt.add_field(('gas', 'density1'), function=_density1, units='g/cm**3')

def _density2(field, data):
    return data['density'] * data['clr2']
yt.add_field(('gas', 'density2'), function=_density2, units='g/cm**3')

def _density_total(field, data):
    return data['density1']+data['density2']
yt.add_field(('gas','density_total'), function=_density_total, units='g/cm**3')

def _density_squared_total(field, data):
    return data['density_total']**2
yt.add_field(('gas','density_squared_total'), function=_density_squared_total, units='g**2/cm**6')

def _mass1(field, data):
    return data['density1']*data['cell_volume']
yt.add_field(('gas', 'mass1'), function=_mass1, units='g')

def _mass2(field, data):
    return data['density2']*data['cell_volume']
yt.add_field(('gas', 'mass2'), function=_mass2, units='g')

def _mass_total(field, data):
    return data['mass1']+data['mass2']
yt.add_field(('gas','mass_total'), function=_mass_total, units='g')

def _kinetic_energy1(field, data):
    return 0.5*data['density1']*data['velocity_magnitude']**2 * data['cell_volume']
yt.add_field(('gas','kinetic_energy1'), function=_kinetic_energy1, units='erg')

def _kinetic_energy2(field, data):
    return 0.5*data['density2']*data['velocity_magnitude']**2 * data['cell_volume']
yt.add_field(('gas','kinetic_energy2'), function=_kinetic_energy2, units='erg')

# def _kinetic_energy_total(field, data):
#     return data['kinetic_energy1']+data['kinetic_energy2']
# yt.add_field(('gas','kinetic_energy_total'), function=_kinetic_energy_total, units='erg')

def _kinetic_energy_total(field, data):
    bv = data.get_field_parameter('bulk_velocity')
    if bv is None:
        bv = yt.YTArray([0,0,0], 'cm/s')
    disp = (data['velocity_x']-bv[0])**2+(data['velocity_y']-bv[1])**2+(data['velocity_z']-bv[2])**2
    return 0.5*data['density_total']*disp*data['cell_volume']
yt.add_field(('gas','kinetic_energy_total'), function=_kinetic_energy_total, units='erg')

def _kinetic_pressure(field, data):
    return data['kinetic_energy_total']/data['cell_volume']
yt.add_field(('gas','kinetic_pressure'), function=_kinetic_pressure, units='erg/cm**3')

def _internal_energy1(field, data):
    return 1.5*data['density1']*kboltz * data['temperature'] / (mu * mp) * data['cell_volume']
yt.add_field(('gas','internal_energy1'), function=_internal_energy1, units='erg')

def _internal_energy2(field, data):
    return 1.5*data['density2']*kboltz * data['temperature'] / (mu * mp) * data['cell_volume']
yt.add_field(('gas','internal_energy2'), function=_internal_energy2, units='erg')

def _internal_energy_total(field, data):
    return data['internal_energy1']+data['internal_energy2']
yt.add_field(('gas','internal_energy_total'), function=_internal_energy_total, units='erg')

def _gravitational_potential_energy1(field, data):
    return 0.5 * data['density1'] * data['gpot'] * data['cell_volume']
yt.add_field(('gas','gravitational_potential_energy1'), function=_gravitational_potential_energy1, units='erg')

def _gravitational_potential_energy2(field, data):
    return 0.5 * data['density2'] * data['gpot'] * data['cell_volume']
yt.add_field(('gas','gravitational_potential_energy2'), function=_gravitational_potential_energy2, units='erg')

def _gravitational_potential_energy_total(field, data):
    return data['gravitational_potential_energy1'] + data['gravitational_potential_energy2']
yt.add_field(('gas','gravitational_potential_energy_total'), function=_gravitational_potential_energy_total, units='erg')

def _particle_gpot_halo1(field, data):
    logic = data['io','particle_halo'] == 1.
    return data['io','particle_gpot']*logic
yt.add_field(('io', 'particle_gpot_halo1'), function=_particle_gpot_halo1, units='dimensionless',particle_type=True,force_override=True)

def _particle_ener(field, data):
    # '.d' drops the units in the next line because particle_gpot is unitless
    ke = 0.5*data['io','particle_velocity_magnitude'].d**2
    pe = data['io','particle_gpot']
    logic = data['io','particle_halo'].astype('int') == 1
    return (ke+pe)*logic
yt.add_field(('io', 'particle_ener'), function=_particle_ener, units='dimensionless',
             particle_type=True, force_override=True)

# L is a YTArray
def get_units(L):
    temp_str = str(L[-1:])
    k = temp_str.rfind(']') + 2
    return temp_str[k:]
