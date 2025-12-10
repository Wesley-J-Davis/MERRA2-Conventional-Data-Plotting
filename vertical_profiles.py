def plot_vertical_profiles(ds):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Select a region (e.g., around 40°N, 100°W)
    lat_idx = np.argmin(np.abs(ds.lat - 40))
    lon_idx = np.argmin(np.abs(ds.lon - 260))  # 260°E = 100°W
    
    # Temperature profiles
    ax = axes[0, 0]
    tv_raob = ds.tv_raob.isel(time=0, lat=lat_idx, lon=lon_idx)
    tv_acraft = ds.tv_acraft.isel(time=0, lat=lat_idx, lon=lon_idx)
    
    ax.plot(tv_raob, ds.lev, 'o-', label='Radiosonde', linewidth=2)
    ax.plot(tv_acraft, ds.lev, 's-', label='Aircraft', linewidth=2)
    ax.set_ylabel('Pressure (hPa)')
    ax.set_xlabel('Virtual Temperature (K)')
    ax.invert_yaxis()
    ax.legend()
    ax.set_title('Temperature Profiles')
    ax.grid(True, alpha=0.3)
    
    # Wind profiles
    ax = axes[0, 1]
    u_raob = ds.u_raob.isel(time=0, lat=lat_idx, lon=lon_idx)
    v_raob = ds.v_raob.isel(time=0, lat=lat_idx, lon=lon_idx)
    wind_speed = np.sqrt(u_raob**2 + v_raob**2)
    
    ax.plot(wind_speed, ds.lev, 'o-', linewidth=2, color='green')
    ax.set_ylabel('Pressure (hPa)')
    ax.set_xlabel('Wind Speed (m/s)')
    ax.invert_yaxis()
    ax.set_title('Wind Speed Profile (Radiosonde)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
