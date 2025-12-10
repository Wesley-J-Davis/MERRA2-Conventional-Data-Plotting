#!/usr/local/other/GEOSpyD/24.3.0-0/2024-08-29/envs/py3.11/bin/python

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.features as cfeature
import numpy as np

base_dir = "/gpfsm/dnb10/projects/p53/merra2/data/obs/.WORK/products_revised/conv/d/"

# Load and explore the data
ds = xr.open_dataset(base_dir + 'D01/merra2.conv.19800101_00z.nc4')

# Create a multi-panel geographic view
fig = plt.figure(figsize=(20, 12))

# Surface pressure observations
ax1 = plt.subplot(2, 3, 1, projection=ccrs.PlateCarree())
ax1.coastlines()
ax1.gridlines(draw_labels=True)
ds.ps_raob_nobs.isel(time=0).plot(ax=ax1, transform=ccrs.PlateCarree(), 
                                  cmap='viridis', cbar_kwargs={'label': 'Number of obs'})
ax1.set_title('Radiosonde Surface Pressure - Number of Observations')

# Wind observations at surface
ax2 = plt.subplot(2, 3, 2, projection=ccrs.PlateCarree())
ax2.coastlines()
ax2.gridlines(draw_labels=True)
ds.u_scat_nobs.isel(time=0).plot(ax=ax2, transform=ccrs.PlateCarree(),
                                 cmap='plasma', cbar_kwargs={'label': 'Number of obs'})
ax2.set_title('Scatterometer Winds - Number of Observations')

# Temperature OMF
ax3 = plt.subplot(2, 3, 3, projection=ccrs.PlateCarree())
ax3.coastlines()
ax3.gridlines(draw_labels=True)
ds.tv_sea_omf.isel(time=0).plot(ax=ax3, transform=ccrs.PlateCarree(),
                                cmap='RdBu_r', center=0, cbar_kwargs={'label': 'K'})
ax3.set_title('Sea Surface Virtual Temperature - OMF')

plt.tight_layout()
plt.show()
