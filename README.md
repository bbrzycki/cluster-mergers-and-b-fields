# cluster-mergers-and-b-fields
Quantify the impact of magnetic fields on the cores of galaxy cluster mergers by comparing both magnetized and unmagnetized hydrodynamic simulations.

Basic structure of repository:
```
cluster-mergers-and-b-fields/
    py-scripts/
    shell-scripts/
    jupyter-notebooks/
```

After running scripts to generate HDF5 files, slice plots, and movies,
the structure will look something like:
```
cluster-mergers-and-b-fields/
    py-scripts/
    shell-scripts/
    jupyter-notebooks/
    processed-data/
    slice-plots/
    movies/
```

TO DO:

mag vs no-mag
methods and functions that apply to both mag and no-mag, and then others for mag

slice plots
    should be able to make movies from these
energy vs time
radial profiles at final timestep
    at initial
    potentially at each timestep???

i want a method to look inside hdf5, i.e. if i import it interactively
i.e. list all the profiles or timesteps that live within it already
