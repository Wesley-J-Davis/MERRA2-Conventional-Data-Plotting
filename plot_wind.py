def plot_wind_analysis(ds):
    fig, axes = plt.subplots(1, 2, figsize=(20, 8), 
                            subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Surface winds from scatterometer
    ax = axes[0]
    ax.coastlines()
    ax.gridlines(draw_labels=True)
    ax.add_feature(cfeature.LAND, alpha=0.3)
    ax.add_feature(cfeature.OCEAN, alpha=0.1)
    
    # Subsample for cleaner vector plot
    skip = 8
    u_scat = ds.u_scat.isel(time=0)[::skip, ::skip]
    v_scat = ds.v_scat.isel(time=0)[::skip, ::skip]
    lon_sub = ds.lon[::skip]
    lat_sub = ds.lat[::skip]
    
    # Only plot where we have data
    mask = ~(np.isnan(u_scat) | np.isnan(v_scat))
    
    ax.quiver(lon_sub, lat_sub, u_scat, v_scat, 
             transform=ccrs.PlateCarree(), scale=300, alpha=0.7)
    ax.set_title('Scatterometer Surface Winds')
    
    # Wind speed magnitude
    ax = axes[1]
    ax.coastlines()
    ax.gridlines(draw_labels=True)
    
    wind_speed = np.sqrt(ds.u_scat**2 + ds.v_scat**2)
    wind_speed.isel(time=0).plot(ax=ax, transform=ccrs.PlateCarree(),
                                cmap='viridis', cbar_kwargs={'label': 'm/s'})
    ax.set_title('Scatterometer Wind Speed')
    
    plt.tight_layout()
    plt.show()

plot_wind_analysis()
