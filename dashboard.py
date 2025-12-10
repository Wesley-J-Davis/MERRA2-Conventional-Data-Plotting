def create_comprehensive_dashboard(ds):
    fig = plt.figure(figsize=(20, 16))
    
    # Main geographic plot
    ax_main = plt.subplot(3, 3, (1, 5), projection=ccrs.PlateCarree())
    ax_main.coastlines()
    ax_main.gridlines(draw_labels=True)
    
    # Plot observation density
    total_obs = (ds.ps_land_nobs.isel(time=0) + 
                ds.ps_sea_nobs.isel(time=0) + 
                ds.tv_drift_nobs.isel(time=0))
    
    im = total_obs.plot(ax=ax_main, transform=ccrs.PlateCarree(),
                       cmap='plasma', cbar_kwargs={'label': 'Total Observations'})
    ax_main.set_title('Total Surface Observations Distribution')
    
    # Time series (if you have multiple files)
    ax_ts = plt.subplot(3, 3, 3)
    # This would be for multiple time steps - placeholder for now
    ax_ts.set_title('Time Series (placeholder)')
    
    # Statistics plots
    ax_hist1 = plt.subplot(3, 3, 6)
    omf_data = ds.tv_sea_omf.isel(time=0).values.flatten()
    omf_clean = omf_data[~np.isnan(omf_data)]
    ax_hist1.hist(omf_clean, bins=30, alpha=0.7)
    ax_hist1.set_title('Sea Surface Temperature OMF Distribution')
    ax_hist1.set_xlabel('OMF (K)')
    
    plt.tight_layout()
    plt.show()
