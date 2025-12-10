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

def get_short_title(name):
    """Extract a short title from observation name"""
    if ": " in name:
        return name.split(": ", 1)[1]  # Split only at first occurrence
    else:
        return name

def plot_observation_summary(ds):
    """Plot observations grouped by platform/instrument"""
    
    platform_groups = {
        'RADIOSONDE': {
            'RADIOSONDE: Virtual temperature': 'tv_raob_nobs',
            'RADIOSONDE: Specific humidity': 'qv_raob_nobs',
            'RADIOSONDE: Zonal wind': 'u_raob_nobs',
            'RADIOSONDE: Meridional wind': 'v_raob_nobs',
            'RADIOSONDE: Surface pressure': 'ps_raob_nobs'
        },
        'AIRCRAFT': {
            'AIRCRAFT: Virtual temperature': 'tv_acraft_nobs',
            'AIRCRAFT: Specific humidity': 'qv_acraft_nobs',
            'AIRCRAFT: Zonal wind': 'u_acraft_nobs',
            'AIRCRAFT: Meridional wind': 'v_acraft_nobs'
        },
        'SATELLITE': {
            'SCATTEROMETER: Zonal wind': 'u_scat_nobs',
            'SCATTEROMETER: Meridional wind': 'v_scat_nobs',
            'SSMI: Wind speed': 'w_ssmi_nobs',
            'ATMOS MOTION VECTORS: Zonal wind': 'u_amv_nobs',
            'ATMOS MOTION VECTORS: Meridional wind': 'v_amv_nobs',
            'GPSRO Bending Angle': 'bang_gps_nobs'
        },
        'SURFACE': {
            'SEA SURFACE: Sea surface temperature': 'sst_sea_nobs',
            'SEA SURFACE: Virtual temperature': 'tv_sea_nobs',
            'SEA SURFACE: Surface pressure': 'ps_sea_nobs',
            'SEA SURFACE: Zonal wind': 'u_sea_nobs',
            'SEA SURFACE: Meridional wind': 'v_sea_nobs',
            'SEA SURFACE: Specific humidity': 'qv_sea_nobs',
            'LAND SURFACE: Surface pressure': 'ps_land_nobs'
        },
        'OTHER': {
            'PROFILER: Zonal wind': 'u_prof_nobs',
            'PROFILER: Meridional wind': 'v_prof_nobs',
            'PAOB SURFACE: Synthetic surface pressure': 'ps_paob_nobs',
            'Drifting Buoy: Virtual Temperature': 'tv_drift_nobs',
            'MLS: Virtual Temperature': 'tv_mls_nobs',
            'Drifting Buoy: Zonal wind': 'u_drift_nobs',
            'Drifting Buoy: Meridional wind': 'v_drift_nobs',
            'Drifting Buoy: Surface Pressure': 'ps_drift_nobs'
        }
    }
    
    for platform_name, obs_types in platform_groups.items():
        n_plots = len(obs_types)
        n_cols = 3
        n_rows = (n_plots + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        fig.suptitle(f'{platform_name} OBSERVATIONS', fontsize=16, fontweight='bold')
        
        # Handle single row case and ensure axes is always 2D
        if n_rows == 1 and n_cols == 1:
            axes = np.array([[axes]])
        elif n_rows == 1:
            axes = axes.reshape(1, -1)
        elif n_cols == 1:
            axes = axes.reshape(-1, 1)
        
        axes_flat = axes.flatten()
        
        for i, (name, var) in enumerate(obs_types.items()):
            ax = axes_flat[i]
            short_title = get_short_title(name)
            
            if var in ds.data_vars:
                data = ds[var].isel(time=0)
                
                # Handle 4D variables
                if len(data.dims) == 3:  # Has vertical levels
                    data = data.sum(dim='lev')
                    title_suffix = f'\nTotal: {data.sum().values:.0f}'
                else:
                    title_suffix = f'\nTotal: {data.sum().values:.0f}'
                
                data_masked = data.where(data > 0)
                
                if not data_masked.isnull().all():
                    im = data_masked.plot(ax=ax, cmap='viridis', add_colorbar=True, 
                                        cbar_kwargs={'shrink': 0.8})
                    ax.set_title(f'{short_title}{title_suffix}', fontsize=10)
                else:
                    ax.set_title(f'{short_title}\nNo observations', fontsize=10)
            else:
                ax.set_title(f'{short_title}\nNot available', fontsize=10)
            
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
        
        # Hide unused subplots
        for i in range(len(obs_types), len(axes_flat)):
            axes_flat[i].set_visible(False)
        
        plt.tight_layout()
        plt.show()
        plt.savefig(base_dir + 'merra2.conv.19800101_00z.png')
            
base_dir = "/discover/nobackup/projects/gmao/merra2/data/obs/.WORK/"
ds = xr.open_dataset(base_dir + 'products_revised/conv/d/Y1980/M01/' + 'D01/merra2.conv.19800101_00z.nc4')
            
explore_data_structure(ds)
plot_observation_summary(ds)
