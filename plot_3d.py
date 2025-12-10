from mpl_toolkits.mplot3d import Axes3D

def plot_3d_obs_distribution(ds):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create meshgrid for lat/lon
    lon_2d, lat_2d = np.meshgrid(ds.lon, ds.lat)
    
    # Get aircraft temperature data at a specific pressure level (e.g., 500 hPa)
    lev_idx = np.argmin(np.abs(ds.lev - 500))  # Find 500 hPa level
    tv_data = ds.tv_acraft.isel(time=0, lev=lev_idx)
    
    # Create surface plot
    surf = ax.plot_surface(lon_2d, lat_2d, tv_data, 
                          cmap='coolwarm', alpha=0.8, linewidth=0)
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Virtual Temperature (K)')
    ax.set_title('Aircraft Temperature Observations at 500 hPa')
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=20)
    
    plt.show()
