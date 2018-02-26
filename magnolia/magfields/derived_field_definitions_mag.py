"""
A host of derived field definitions regarding magnetic energy,
some taking into account the proportions of a certain fields due to
either cluster 1 or 2.
"""

import yt

def _magnetic_energy1(field, data):
    return 1.0/(8*np.pi) * data['magnetic_field_strength']**2 * data['clr1'] * data['cell_volume']
yt.add_field(('gas','magnetic_energy1'), function=_magnetic_energy1, units='erg')

def _magnetic_energy2(field, data):
    return 1.0/(8*np.pi) * data['magnetic_field_strength']**2 * data['clr2'] * data['cell_volume']
yt.add_field(('gas','magnetic_energy2'), function=_magnetic_energy2, units='erg')

def _magnetic_energy_total(field, data):
    return data['magnetic_energy1']+data['magnetic_energy2']
yt.add_field(('gas','magnetic_energy_total'), function=_magnetic_energy_total, units='erg')

def _magnetic_pressure(field, data):
    return data['magnetic_energy_total']/data['cell_volume']
yt.add_field(('gas','magnetic_pressure'), function=_magnetic_pressure, units='erg/cm**3')
