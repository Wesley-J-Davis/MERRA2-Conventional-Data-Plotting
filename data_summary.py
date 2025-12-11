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
    obs_vars = [var for var in ds.data_vars if '_nobs' in var or 'obrate' in var]
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
            'RADIOSONDE: Virtual temperature (nobs)': 'tv_raob_nobs',
            'RADIOSONDE: Virtual temperature (obrate)': 'tv_raob_obrate',
            'RADIOSONDE: Specific humidity (nobs)': 'qv_raob_nobs',
            'RADIOSONDE: Specific humidity (obrate)': 'qv_raob_obrate',
            'RADIOSONDE: Zonal wind (nobs)': 'u_raob_nobs',
            'RADIOSONDE: Zonal wind (obrate)': 'u_raob_obrate',
            'RADIOSONDE: Meridional wind (nobs)': 'v_raob_nobs',
            'RADIOSONDE: Meridional wind (obrate)': 'v_raob_obrate',
            'RADIOSONDE: Surface pressure (nobs)': 'ps_raob_nobs',
            'RADIOSONDE: Surface pressure (obrate)': 'ps_raob_obrate'
        },
        'AIRCRAFT': {
            'AIRCRAFT: Virtual temperature (nobs)': 'tv_acraft_nobs',
            'AIRCRAFT: Virtual temperature (obrate)': 'tv_acraft_obrate',
            'AIRCRAFT: Specific humidity (nobs)': 'qv_acraft_nobs',
            'AIRCRAFT: Specific humidity (obrate)': 'qv_acraft_obrate',
            'AIRCRAFT: Zonal wind (nobs)': 'u_acraft_nobs',
            'AIRCRAFT: Zonal wind (obrate)': 'u_acraft_obrate',
            'AIRCRAFT: Meridional wind (nobs)': 'v_acraft_nobs',
            'AIRCRAFT: Meridional wind (obrate)': 'v_acraft_obrate'
        },
        'SATELLITE': {
            'SCATTEROMETER: Zonal wind (nobs)': 'u_scat_nobs',
            'SCATTEROMETER: Zonal wind (obrate)': 'u_scat_obrate',
            'SCATTEROMETER: Meridional wind (nobs)': 'v_scat_nobs',
            'SCATTEROMETER: Meridional wind (obrate)': 'v_scat_obrate',
            'SSMI: Wind speed (nobs)': 'w_ssmi_nobs',
            'SSMI: Wind speed (obrate)': 'w_ssmi_obrate',
            'ATMOS MOTION VECTORS: Zonal wind (nobs)': 'u_amv_nobs',
            'ATMOS MOTION VECTORS: Zonal wind (obrate)': 'u_amv_obrate',
            'ATMOS MOTION VECTORS: Meridional wind (nobs)': 'v_amv_nobs',
            'ATMOS MOTION VECTORS: Meridional wind (obrate)': 'v_amv_obrate',
            'GPSRO Bending Angle (nobs)': 'bang_gps_nobs',
            'GPSRO Bending Angle (obrate)': 'bang_gps_obrate'
        },
        'SURFACE': {
            'SEA SURFACE: Sea surface temperature (nobs)': 'sst_sea_nobs',
            'SEA SURFACE: Sea surface temperature (obrate)': 'sst_sea_obrate',
            'SEA SURFACE: Virtual temperature (nobs)': 'tv_sea_nobs',
            'SEA SURFACE: Virtual temperature (obrate)': 'tv_sea_obrate',
            'SEA SURFACE: Surface pressure (nobs)': 'ps_sea_nobs',
            'SEA SURFACE: Surface pressure (obrate)': 'ps_sea_obrate',
            'SEA SURFACE: Zonal wind (nobs)': 'u_sea_nobs',
            'SEA SURFACE: Zonal wind (obrate)': 'u_sea_obrate',
            'SEA SURFACE: Meridional wind (nobs)': 'v_sea_nobs',
            'SEA SURFACE: Meridional wind (obrate)': 'v_sea_obrate',
            'SEA SURFACE: Specific humidity (nobs)': 'qv_sea_nobs',
            'SEA SURFACE: Specific humidity (obrate)': 'qv_sea_obrate',
            'LAND SURFACE: Surface pressure (nobs)': 'ps_land_nobs',
            'LAND SURFACE: Surface pressure (obrate)': 'ps_land_obrate'
        },
        'OTHER': {
            'PROFILER: Zonal wind (nobs)': 'u_prof_nobs',
            'PROFILER: Zonal wind (obrate)': 'u_prof_obrate',
            'PROFILER: Meridional wind (nobs)': 'v_prof_nobs',
            'PROFILER: Meridional wind (obrate)': 'v_prof_obrate',
            'PAOB SURFACE: Synthetic surface pressure (nobs)': 'ps_paob_nobs',
            'PAOB SURFACE: Synthetic surface pressure (obrate)': 'ps_paob_obrate',
            'Drifting Buoy: Virtual Temperature (nobs)': 'tv_drift_nobs',
            'Drifting Buoy: Virtual Temperature (obrate)': 'tv_drift_obrate',
            'MLS: Virtual Temperature (nobs)': 'tv_mls_nobs',
            'MLS: Virtual Temperature (obrate)': 'tv_mls_obrate',
            'Drifting Buoy: Zonal wind (nobs)': 'u_drift_nobs',
            'Drifting Buoy: Zonal wind (obrate)': 'u_drift_obrate',
            'Drifting Buoy: Meridional wind (nobs)': 'v_drift_nobs',
            'Drifting Buoy: Meridional wind (obrate)': 'v_drift_obrate',
            'Drifting Buoy: Surface Pressure (nobs)': 'ps_drift_nobs',
            'Drifting Buoy: Surface Pressure (obrate)': 'ps_drift_obrate'
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
        plt.savefig(base_dir + f'{platform_name}_merra2.conv.19800101_00z.png')
            
base_dir = "/discover/nobackup/projects/gmao/merra2/data/obs/.WORK/"
ds = xr.open_dataset(base_dir + 'products_revised/conv/d/Y1980/M01/' + 'D01/merra2.conv.19800101_00z.nc4')
            
explore_data_structure(ds)
plot_observation_summary(ds)
