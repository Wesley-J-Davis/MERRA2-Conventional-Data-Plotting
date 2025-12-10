#!/usr/local/other/GEOSpyD/24.3.0-0/2024-08-29/envs/py3.11/bin/python

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

def explore_data_structure(ds):
    """Explore the data structure and basic statistics"""
    print("Dataset dimensions:")
    print(f"Longitude: {len(ds.lon)} points ({ds.lon.min().values:.1f}° to {ds.lon.max().values:.1f}°)")
    print(f"Latitude: {len(ds.lat)} points ({ds.lat.min().values:.1f}° to {ds.lat.max().values:.1f}°)")
    print(f"Levels: {len(ds.lev)} levels ({ds.lev.min().values:.1f} to {ds.lev.max().values:.1f} hPa)")
    print(f"Time: {len(ds.time)} time step(s)")
    
    print("\nAvailable observation types:")
    obs_vars = [var for var in ds.data_vars if '_nobs' in var]
    for var in obs_vars:
        total_obs = ds[var].isel(time=0).sum().values
        if total_obs > 0:
            print(f"  {var}: {total_obs:.0f} total observations")

def plot_observation_summary(ds):
    """Plot summary of observations by type"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Count observations by type
    obs_types = {
        'Radiosonde Temp': 'tv_raob_nobs',
        'Aircraft Temp': 'tv_acraft_nobs', 
        'Sea Surface Pressure': 'ps_sea_nobs',
        'Land Surface Pressure': 'ps_land_nobs'
    }
    
    for i, (name, var) in enumerate(obs_types.items()):
        ax = axes[i//2, i%2]
        if var in ds.data_vars:
            data = ds[var].isel(time=0)
            # Only plot where observations exist
            data_masked = data.where(data > 0)
            data_masked.plot(ax=ax, cmap='viridis')
            ax.set_title(f'{name}\nMax obs: {data.max().values:.0f}')
        else:
            ax.set_title(f'{name} - Not available')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
    
    plt.tight_layout()
    plt.show()
    plt.savefig(base_dir + 'merra2.conv.19800101_00z.png')
  
base_dir = "/discover/nobackup/projects/gmao/merra2/data/obs/.WORK/"
ds = xr.open_dataset(base_dir + 'products_revised/conv/d/M01/' + 'D01/merra2.conv.19800101_00z.nc4')

explore_data_structure(ds)
plot_observation_summary(ds)
