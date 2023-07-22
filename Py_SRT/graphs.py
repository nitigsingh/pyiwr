print('''You are using Py-SRT an open-source module developed by Researchers at the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw DWR (Doppler Weather Radar) files into Py-ART compatible NetCDF files. Furthermore, Py-SRT provides useful tools and visualisation functions to make working with the radar data easier and more enjoyable.''')


import matplotlib.pyplot as plt
import numpy as np
import os

def plot_cappi_at_altitude(xg, altitude_level, grid=False, rings=False, ticks_in_km=True):
    """
    Plot CAPPI at the specified altitude level.

    Parameters:
        xg (xarray.Dataset): Xarray Dataset containing gridded radar data.
        altitude_level (int): Altitude level in kilometers (e.g., 3 km = 6, 3.5 km = 7).
        grid (bool, optional): If True, display gridlines. Default is True.
        rings (bool, optional): If True, display range rings. Default is True.
        ticks_in_km (bool, optional): If True, display ticks in kilometers. Default is True.
    """
    alt_index = int(altitude_level * 2)  # Calculate the index corresponding to the altitude level
    if ticks_in_km==True:
        plt.contourf(xg.x / 1000, xg.y / 1000, xg['DBZ'][0][alt_index], levels=range(-20, 70), cmap='pyart_NWSRef')
    else:
        plt.contourf(xg.x, xg.y, xg['DBZ'][0][alt_index], levels=range(-20, 70), cmap='pyart_NWSRef')
 
    plt.colorbar(label='dBZ')

    # Extracting the station code from the file name
    a = os.path.basename(filenamel4)[0:5]
    if a == 'RSCHR':
        k = 'Sohra S-band Dual-Pol DWR'
    elif a == 'RSSHR':
        k = 'SHAR S-band Dual-pol DWR'
    else:
        k = 'TERLS C-band Dual-pol DWR'

    plt.title(f"{k} Radar Reflectivity (dBZ)\nTime: {str(xg.time['time'].values[0])[:19]}, CAPPI @ Altitude {altitude_level} km")

    if grid:
        plt.grid()
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')

    if rings:
        if ticks_in_km==True:
            t = np.linspace(0, 2*np.pi)
            for r in [50, 150, 250]:
                a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')
        else:
            t = np.linspace(0,2*np.pi)
            for r in [50000,150000,250000]:
                a, = plt.plot(r*np.cos(t),r*np.sin(t), color='k')
            
    if ticks_in_km:
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')
    else:
        plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')

    plt.show()


import matplotlib.pyplot as plt
import numpy as np
import os

def cappi_max(xg, grid=False, rings=False, ticks_in_km=True):
    """
    Plot CAPPI at the specified altitude level.

    Parameters:
        xg (xarray.Dataset): Xarray Dataset containing gridded radar data.
        altitude_level (int): Altitude level in kilometers (e.g., 3 km = 6, 3.5 km = 7).
        grid (bool, optional): If True, display gridlines. Default is True.
        rings (bool, optional): If True, display range rings. Default is True.
        ticks_in_km (bool, optional): If True, display ticks in kilometers. Default is True.
    """
    if ticks_in_km:
        plt.contourf(xg.x / 1000, xg.y / 1000, xg['DBZ'][0].max("z"), levels=range(-20, 70), cmap='pyart_NWSRef')
    else:
        plt.contourf(xg.x, xg.y, xg['DBZ'][0].max("z"), levels=range(-20, 70), cmap='pyart_NWSRef')
    plt.colorbar(label='dBZ')

    # Extracting the station code from the file name
    a = os.path.basename(filenamel4)[0:5]
    if a == 'RSCHR':
        k = 'Sohra S-band Dual-Pol DWR'
    elif a == 'RSSHR':
        k = 'SHAR S-band Dual-pol DWR'
    else:
        k = 'TERLS C-band Dual-pol DWR'

    plt.title(f"{k} Radar Reflectivity (dBZ)\nTime: {str(xg.time['time'].values[0])[:19]}, MAXZ CAPPI")

    if grid:
        plt.grid()
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')

    if rings:
        if ticks_in_km==True:
            t = np.linspace(0, 2*np.pi)
            for r in [50, 150, 250]:
                a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')
        else:
            t = np.linspace(0,2*np.pi)
            for r in [50000,150000,250000]:
                a, = plt.plot(r*np.cos(t),r*np.sin(t), color='k')
            
    if ticks_in_km:
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')
    else:
        plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')

    plt.show()


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime

def marginal_maxz(xg, max_range=250, max_height=15, show_rings=True, show_grid=True, show_cross_sections=True):
    """
    Plot the MAX-Z CAPPI with cross-sections for the given xarray Dataset.

    Parameters:
        xg (xarray.Dataset): Xarray Dataset containing gridded radar data.
        show_rings (bool, optional): If True, display range rings. Default is True.
        show_grid (bool, optional): If True, display gridlines. Default is True.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect(1.)

    # Plot the MAX-Z CAPPI
    cappi = xg['DBZ'][0].max("z")
    cappi.plot.contourf(cmap='pyart_NWSRef', levels=range(-10, 70), cbar_kwargs={'pad': 0.02, 'shrink': 0.8}, ax=ax)

    # Extracting the station code from the file name
    a = os.path.basename(filenamel4)[0:5]
    if a == 'RSCHR':
        k = 'Sohra S-band Dual-Pol DWR'
    elif a == 'RSSHR':
        k = 'SHAR S-band Dual-pol DWR'
    else:
        k = 'TERLS C-band Dual-pol DWR'
    
    # Title
    title_str = f"{k} Radar Reflectivity (dBZ)\nTime: {str(xg.time['time'].values[0])[:19]}, MAXZ CAPPI"

    if show_cross_sections:
        plt.title(title_str, pad=100)
    else:
        plt.title(title_str)

    if show_grid:
        plt.grid()
        plt.xlabel('X distance (in m) from Radar (at Center) in Cartesian')
        plt.ylabel('Y distance (in m) from Radar (at Center) in Cartesian')

    if show_rings:
        # Range rings
        t = np.linspace(0, 2 * np.pi)
        for r in [50000, 150000, 250000]:
            a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')
    
    if show_cross_sections:

        # Create new axes for displaying cross-sections
        divider = make_axes_locatable(ax)
        ax_x = divider.append_axes("top", 1.2, pad=0.05)
        ax_y = divider.append_axes("right", 1.2, pad=0.05)

        # Plot cross-sections
        xg['DBZ'][0].max(axis=1).plot.contourf(cmap='pyart_NWSRef', levels=range(-10, 70), add_colorbar=False, add_title=None, ax=ax_x)
        xg['DBZ'][0].max(axis=2).T.plot.contourf(cmap='pyart_NWSRef', levels=range(-10, 70), add_colorbar=False, add_title=None, ax=ax_y)

        ax_x.xaxis.set_major_formatter(NullFormatter())
        ax_y.yaxis.set_major_formatter(NullFormatter())

        ax_x.set_title(None)
        ax_y.set_title(None)
        ax_y.set_ylabel(None)
        ax_x.set_xlabel(None)
        ax_x.set_ylabel("Height AMSL (m)", size=10)
        ax_y.set_xlabel("Height AMSL (m)", size=10)

        # Add corner box
        left, bottom, width, height = 0.647, 0.697, 0.12, 0.12
        ax_cnr = plt.axes((left, bottom, width, height))
        plt.sca(ax_cnr)
        plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False)
        ax_cnr.yaxis.set_major_formatter(NullFormatter())
        ax_cnr.xaxis.set_major_formatter(NullFormatter())

        # Labels along the bottom edge are off
        plt.text(0.2, 0.8, 'MAX-Z', size=14, weight='bold')
        plt.text(0.02, 0.65, 'Max Range: 250 km', size=8)
        plt.text(0.02, 0.5, 'Max Height: 15 km', size=8)

        # Show the datetime
        plt.text(0.02, 0.3, str(xg.time['time'].values[0])[11:19], weight='bold', size=17)
        plt.text(0.02, 0.15, datetime.strptime(str(xg.time['time'].values[0])[:10], '%Y-%m-%d').strftime('%d %B, %Y UTC'), size=9)

    plt.show()
