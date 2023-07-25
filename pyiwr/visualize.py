#!/usr/bin/env python
# coding: utf-8
'''
@author1: Nitig Singh
@author2: Vaibhav Tyagi

@email: nitig14rdfsma[at]gmail[dot]com
@email: vaibhavtyagi7191[at]gmail[dot]com
'''

import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime



def cappi(xg, altitude_level, field_name='DBZ', radar_location='SOHRA', grid=False, rings=False, ticks_in_km=True):
    """
    Plot CAPPI at the specified altitude level.

    Parameters:
        xg (xarray.Dataset): Py_SRT Xarray Dataset containing gridded radar data.
        altitude_level (int): Altitude level in kilometers (e.g., 3 km = 6, 3.5 km = 7).
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        radar_location (str, optional): Radar location name. Default is 'SOHRA', other options are SHAR and TERLS.
        grid (bool, optional): If True, display gridlines. Default is True.
        rings (bool, optional): If True, display range rings. Default is True.
        ticks_in_km (bool, optional): If True, display ticks in kilometers. Default is True.

        Example usage:
        cappi(xg, altitude_level=3, field_name='DBZ', radar_location='SOHRA', grid=False, rings=False, ticks_in_km=True)
    """
    alt_index = int(altitude_level * 2)  # Calculate the index corresponding to the altitude level

    # Define colormap based on the field_name
    colormaps = {
        'DBZ': 'pyart_NWSRef',
        'VEL': 'pyart_NWSVel',
        'WIDTH': 'pyart_NWS_SPW',
        'PHIDP': 'pyart_PD17',
        'RHOHV': 'pyart_EWilson17',
        'ZDR': 'pyart_RefDiff',
    }

    # Define levels for each field
    levels = {
        'DBZ': [-20, 70],
        'VEL': [-30, 30],
        'WIDTH': [-30, 30],
        'PHIDP': [-10, 20],
        'RHOHV': [-300, 300],
        'ZDR': [-10, 30],
    }

    # Access the field from the xg dataset using the field_name parameter
    if ticks_in_km:
        plt.contourf(xg.x / 1000, xg.y / 1000, xg[field_name][0][alt_index], levels=np.linspace(*levels.get(field_name, [-20, 70]), 31), cmap=colormaps.get(field_name, 'pyart_NWSRef'))
    else:
        plt.contourf(xg.x, xg.y, xg[field_name][0][alt_index], levels=np.linspace(*levels.get(field_name, [-20, 70]), 31), cmap=colormaps.get(field_name, 'pyart_NWSRef'))

    plt.colorbar(label='dBZ')

    if radar_location == 'SOHRA':
        k = 'Sohra S-band Dual-Pol DWR'
    elif radar_location == 'SHAR':
        k = 'SHAR S-band Dual-pol DWR'
    else:
        k = 'TERLS C-band Dual-pol DWR'

    plt.title(f"{k} {xg[field_name].standard_name}\nTime: {str(xg.time['time'].values[0])[:19]}, CAPPI @ Altitude {altitude_level} km")

    if grid:
        plt.grid()

    if rings:
        if ticks_in_km:
            t = np.linspace(0, 2 * np.pi)
            for r in [50, 150, 250]:
                a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')
        else:
            t = np.linspace(0, 2 * np.pi)
            for r in [50000, 150000, 250000]:
                a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')

    if ticks_in_km:
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')
    else:
        plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')

    plt.show()




def cappi_max(xg, field_name='DBZ', radar_location='SOHRA', grid=False, rings=False, ticks_in_km=True):
    """
    Plot MAX Z CAPPI.

    Parameters:
        xg (xarray.Dataset): Py_SRT Xarray Dataset containing gridded radar data.
        radar_location (str, optional): Radar location name. Default is 'SOHRA', other options are SHAR and TERLS.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        grid (bool, optional): If True, display gridlines. Default is True.
        rings (bool, optional): If True, display range rings. Default is True.
        ticks_in_km (bool, optional): If True, display ticks in kilometers. Default is True.
        
        Example usage:
        cappi_max(xg, field_name='DBZ', radar_location='SOHRA', grid=False, rings=False, ticks_in_km=True)
    """
    if radar_location == 'SOHRA':
        k = 'Sohra S-band Dual-Pol DWR'
    elif radar_location == 'SHAR':
        k = 'SHAR S-band Dual-pol DWR'
    else:
        k = 'TERLS C-band Dual-pol DWR'

    # Define colormap based on the field_name
    colormaps = {
        'DBZ': 'pyart_NWSRef',
        'VEL': 'pyart_NWSVel',
        'WIDTH': 'pyart_NWS_SPW',
        'PHIDP': 'pyart_PD17',
        'RHOHV': 'pyart_EWilson17',
        'ZDR': 'pyart_RefDiff',
    }

    # Define levels for each field
    levels = {
        'DBZ': [-20, 70],
        'VEL': [-30, 30],
        'WIDTH': [-30, 30],
        'PHIDP': [-10, 20],
        'RHOHV': [-300, 300],
        'ZDR': [-10, 30],
    }

    if ticks_in_km:
        plt.contourf(xg.x / 1000, xg.y / 1000, xg[field_name][0].max("z"), levels=np.linspace(*levels.get(field_name, [-20, 70]), 31), cmap=colormaps.get(field_name, 'pyart_NWSRef'))
    else:
        plt.contourf(xg.x, xg.y, xg[field_name][0].max("z"), levels=np.linspace(*levels.get(field_name, [-20, 70]), 31), cmap=colormaps.get(field_name, 'pyart_NWSRef'))

    plt.colorbar(label='dBZ')

    plt.title(f"{k} {xg[field_name].standard_name}\nTime: {str(xg.time['time'].values[0])[:19]}, MAXZ CAPPI")

    if grid:
        plt.grid()

    if rings:
        if ticks_in_km:
            t = np.linspace(0, 2*np.pi)
            for r in [50, 150, 250]:
                a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')
        else:
            t = np.linspace(0, 2*np.pi)
            for r in [50000, 150000, 250000]:
                a, = plt.plot(r * np.cos(t), r * np.sin(t), color='k')

    if ticks_in_km:
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')
    else:
        plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')

    plt.show()



def marginal_max(xg, radar_location='SOHRA', field_name='DBZ', show_rings=False, show_grid=False, show_cross_sections=True):
    """
    Plot the MAX-Z CAPPI with cross-sections for the given xarray Dataset.

    Parameters:
        xg (xarray.Dataset): Py_SRT Xarray Dataset containing gridded radar data.
        radar_location (str, optional): Radar location name. Default is 'SOHRA'.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        show_rings (bool, optional): If True, display range rings. Default is False.
        show_grid (bool, optional): If True, display gridlines. Default is False.
        show_cross_sections (bool, optional): If True, display cross-sections. Default is True.

        Example usage:
        marginal_maxz(xg, radar_location='SHAR', field_name='WIDTH', show_rings=True, show_grid=True, show_cross_sections=True)
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect(1.)

    # Define colormap based on the field_name
    colormaps = {
        'DBZ': 'pyart_NWSRef',
        'VEL': 'pyart_NWSVel',
        'WIDTH': 'pyart_NWS_SPW',
        'PHIDP': 'pyart_PD17',
        'RHOHV': 'pyart_EWilson17',
        'ZDR': 'pyart_RefDiff',
    }
    
    # Get the colormap for the field_name
    cmap = colormaps.get(field_name, 'pyart_NWSRef')
    
    # Define levels for each field_name
    levels = {
        'DBZ': [-20, 70],
        'VEL': [-30, 30],
        'WIDTH': [-30, 30],
        'PHIDP': [-10, 20],
        'RHOHV': [-300, 300],
        'ZDR': [-10, 30],
    }
    
    # Get the levels for the field_name
    cmap_levels = levels.get(field_name, [-20, 70])

    # Plot the MAX-Z CAPPI
    cappi = xg[field_name][0].max("z")
    cappi.plot.contourf(cmap=cmap, levels=range(cmap_levels[0], cmap_levels[1]+1), cbar_kwargs={'pad': 0.02, 'shrink': 0.8}, ax=ax)

    if radar_location == 'SOHRA':
        k = 'Sohra S-band Dual-Pol DWR'
    elif radar_location == 'SHAR':
        k = 'SHAR S-band Dual-pol DWR'
    else:
        k = 'TERLS C-band Dual-pol DWR'
    
    # Title
    title_str = f"{k} {xg[field_name].standard_name}\nTime: {str(xg.time['time'].values[0])[:19]}, MAXZ CAPPI"

    if show_cross_sections:
        plt.title(title_str, pad=100)
    else:
        plt.title(title_str)
    plt.xlabel('X distance (in m) from Radar (at Center) in Cartesian')
    plt.ylabel('Y distance (in m) from Radar (at Center) in Cartesian')
    if show_grid:
        plt.grid()


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
        xg[field_name][0].max(axis=1).plot.contourf(cmap=cmap, levels=range(cmap_levels[0], cmap_levels[1]+1), ax=ax_x)
        xg[field_name][0].max(axis=2).T.plot.contourf(cmap=cmap, levels=range(cmap_levels[0], cmap_levels[1]+1), ax=ax_y)

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



def elevation(radar, field_name='DBZ', elevation_index=0, rings=True, grid=True, range_in_km=True):
    """
    Plot radar data for the specified elevation.

    Parameters:
        radar: MOSDAC corrected Py-SRT Radar object based on pyart.core.Radar.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        elevation_index (int, optional): Index of the desired elevation. Default is 0.
        rings (bool, optional): If True, display range rings. Default is True.
        grid (bool, optional): If True, display gridlines. Default is True.
        range_in_km (bool, optional): If True, display range axis in kilometers. Default is True.
    """
    fig, ax = plt.subplots()
        
    if range_in_km:
        rngs = radar.range['data'] / 1000.
        xs0 = rngs[:, np.newaxis] * np.sin(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))
        ys0 = rngs[:, np.newaxis] * np.cos(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))

    else:
        rngs = radar.range['data']
        xs0 = rngs[:, np.newaxis] * np.sin(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))
        ys0 = rngs[:, np.newaxis] * np.cos(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))

    ele_data = radar.fields[field_name]['data'][radar.sweep_start_ray_index['data'][elevation_index]:radar.sweep_end_ray_index['data'][elevation_index]+1].T
    
    # Define colormap based on the field_name
    colormaps = {
        'DBZ': 'pyart_NWSRef',
        'VEL': 'pyart_NWSVel',
        'WIDTH': 'pyart_NWS_SPW',
        'PHIDP': 'pyart_PD17',
        'RHOHV': 'pyart_EWilson17',
        'ZDR': 'pyart_RefDiff',
    }
    
    # Get the colormap for the field_name
    cmap = colormaps.get(field_name, 'pyart_NWSRef')
    
    # Define levels for the color bar
    levels_dict = {
        'DBZ': [-20, 70],
        'VEL': [-30, 30],
        'WIDTH': [-30, 30],
        'PHIDP': [-10, 20],
        'RHOHV': [-300, 300],
        'ZDR': [-10, 30],
    }
    levels = levels_dict.get(field_name, [-20, 70])
    
    # Plot radar data for the specified elevation
    plt.contourf(xs0, ys0, ele_data, levels=range(*levels), cmap=cmap)
    plt.colorbar(label=field_name)
    
    if range_in_km:
        plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')

    else:
        plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
        plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')
    
    k = radar.metadata['instrument_name']
    title_str = f"{k} {radar.fields[field_name]['standard_name']}\nTime: {str(radar.time['units'])[14:]}, PPI @ elevation {str(radar.fixed_angle['data'][elevation_index])}"

    # Title
    plt.title(title_str)

    if grid:
        plt.grid()

    if rings:
        if range_in_km:
            t = np.linspace(0, 2 * np.pi)
            for r in [50, 150, 250]:
                x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                ax.plot(r * np.cos(t), r * np.sin(t), color='k')  # Plot the circle
                ax.text(x+15, y+15, f"{r}", ha='center', va='center', fontsize=10)
        else:
            t = np.linspace(0, 2 * np.pi)
            for r in [50000, 150000, 250000]:
                x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                ax.plot(r * np.cos(t), r * np.sin(t), color='k')  # Plot the circle
                ax.text(x+17000, y+17000, f"{int(r/1000)}", ha='center', va='center', fontsize=10)

    plt.tight_layout()
    plt.show()


    plt.show()




def all_elevation(radar, field_name='DBZ', rings=True, grid=True, range_in_km=True):
    """
    Plot radar data for all elevation angles.

    Parameters:
        radar: MOSDAC corrected Py-SRT Radar object based on pyart.core.Radar.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        rings (bool, optional): If True, display range rings. Default is True.
        grid (bool, optional): If True, display gridlines. Default is True.
        range_in_km (bool, optional): If True, display range axis in kilometers. Default is True.
    """
    fig = plt.figure(figsize=(15, 15))  # Increase figure size for better visibility
    k = radar.metadata['instrument_name']
    title_str = f"{k} {radar.fields[field_name]['standard_name']} @ various elevation angles"

    # Title
    fig.suptitle(title_str, fontsize=16, y=1.0)

    if range_in_km:
        rngs = radar.range['data'] / 1000.
        xs0 = rngs[:, np.newaxis] * np.sin(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))
        ys0 = rngs[:, np.newaxis] * np.cos(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))
    else:
        rngs = radar.range['data']
        xs0 = rngs[:, np.newaxis] * np.sin(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))
        ys0 = rngs[:, np.newaxis] * np.cos(np.deg2rad(np.around(radar.azimuth['data'][0:360]*100) / 100))

    colormaps = {
        'DBZ': 'pyart_NWSRef',
        'VEL': 'pyart_NWSVel',
        'WIDTH': 'pyart_NWS_SPW',
        'PHIDP': 'pyart_PD17',
        'RHOHV': 'pyart_EWilson17',
        'ZDR': 'pyart_RefDiff',
    }

    levels_dict = {
        'DBZ': [-20, 70],
        'VEL': [-30, 30],
        'WIDTH': [-30, 30],
        'PHIDP': [-10, 20],
        'RHOHV': [-300, 300],
        'ZDR': [-10, 30],
    }
    
    # Get the colormap for the field_name
    cmap = colormaps.get(field_name, 'pyart_NWSRef')
    levels = levels_dict.get(field_name, [-20, 70])

    for i in range(radar.fixed_angle['data'].size):
        ax = fig.add_subplot(4, 3, i+1)
        slice_indices = radar.get_slice(i)
        all_ele = radar.fields[field_name]['data'][slice_indices].T

        plt.contourf(xs0, ys0, all_ele, levels=range(*levels), cmap=cmap)
        plt.colorbar(label=field_name)
        plt.title("PPI @ Elevation angle = %.3f" % radar.fixed_angle['data'][i])

        if range_in_km:
            plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
            plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')
        else:
            plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
            plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')

        if grid:
            plt.grid()

        if rings:
            if range_in_km:
                t = np.linspace(0, 2 * np.pi)
                for r in [50, 150, 250]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    ax.plot(r * np.cos(t), r * np.sin(t), color='k')  # Plot the circle
                    ax.text(x + 15, y + 15, f"{r}", ha='center', va='center', fontsize=10)
            else:
                t = np.linspace(0, 2 * np.pi)
                for r in [50000, 150000, 250000]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    ax.plot(r * np.cos(t), r * np.sin(t), color='k')  # Plot the circle
                    ax.text(x + 17000, y + 17000, f"{int(r/1000)}", ha='center', va='center', fontsize=10)

    plt.tight_layout()
    plt.show()




def fields_elevation(radar, elevation_index=0, range_in_km=True, rings=True, grid=True):
    """
    Plot multiple radar products at the specified elevation.

    Parameters:
        radar: MOSDAC corrected Py-SRT Radar object based on pyart.core.Radar.
        elevation_index (int, optional): Index of the desired elevation. Default is 0.
        range_in_km (bool, optional): If True, display range axis in kilometers. Default is True.
        rings (bool, optional): If True, display range rings. Default is True.
        grid (bool, optional): If True, display gridlines. Default is True.
    """
    
    fig = plt.figure(figsize=(15, 10))
    k = radar.metadata['instrument_name']
    title_str = f"{k} \nTime: {str(radar.time['units'])[14:]}, PPI Products @ elevation {str(radar.fixed_angle['data'][elevation_index])}"

    fig.suptitle(title_str, fontsize=16, y=1)    

    product_names = ['DBZ', 'VEL', 'WIDTH', 'ZDR', 'PHIDP', 'RHOHV']
    titles = ['Reflectivity', 'Doppler Velocity', 'Spectral Width', 'Differential Reflectivity',
              'Differential Phase', 'Correlation Coefficient']
    cmap_names = ['pyart_NWSRef', 'pyart_NWSVel', 'pyart_NWS_SPW', 'pyart_RefDiff', 'pyart_PD17', 'pyart_EWilson17']
    levels = [[-20, 70], [-30, 30], [-30, 30], [-10, 20], [-300, 300], [-10, 30]]

    if range_in_km:
        rngs = radar.range['data'] / 1000.
        xs0 = rngs[:, np.newaxis] * np.sin(np.deg2rad(np.around(radar.azimuth['data'][0:360] * 100) / 100))
        ys0 = rngs[:, np.newaxis] * np.cos(np.deg2rad(np.around(radar.azimuth['data'][0:360] * 100) / 100))

    else:
        rngs = radar.range['data']
        xs0 = rngs[:, np.newaxis] * np.sin(np.deg2rad(np.around(radar.azimuth['data'][0:360] * 100) / 100))
        ys0 = rngs[:, np.newaxis] * np.cos(np.deg2rad(np.around(radar.azimuth['data'][0:360] * 100) / 100))

    for i, product_name in enumerate(product_names):
        ax = fig.add_subplot(2, 3, i + 1)
        ele_data = radar.fields[product_name]['data'][radar.sweep_start_ray_index['data'][elevation_index]:radar.sweep_end_ray_index['data'][elevation_index] + 1].T
        
        # Get the colormap for the product
        cmap = cmap_names[i]
        
        vmin, vmax = levels[i]
        
        plt.contourf(xs0, ys0, ele_data, levels=np.linspace(vmin, vmax, 31), cmap=cmap, vmin=vmin, vmax=vmax)
        plt.colorbar(label=product_name)
        plt.title(titles[i])
        if range_in_km:
            plt.xlabel('Range (in km) of Radar (at Center) in Cartesian')
            plt.ylabel('Range (in km) of Radar (at Center) in Cartesian')
        else:
            plt.xlabel('Range (in m) of Radar (at Center) in Cartesian')
            plt.ylabel('Range (in m) of Radar (at Center) in Cartesian')
        if grid:
            plt.grid()
        if rings:
            if range_in_km:
                t = np.linspace(0, 2 * np.pi)
                for r in [50, 150, 250]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    ax.plot(r * np.cos(t), r * np.sin(t), color='k')  # Plot the circle
                    ax.text(x + 15, y + 15, f"{r}", ha='center', va='center', fontsize=10)  # Display the radius at 30 degrees
            else:
                t = np.linspace(0, 2 * np.pi)
                for r in [50000, 150000, 250000]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    ax.plot(r * np.cos(t), r * np.sin(t), color='k')  # Plot the circle
                    ax.text(x + 17000, y + 17000, f"{int(r/1000)}", ha='center', va='center', fontsize=10)  # Display the radius at 30 degrees

    plt.tight_layout()  # Adjust subplot parameters to avoid overlapping
    plt.subplots_adjust(top=0.90, hspace=0.3)  # Adjust top margin and horizontal spacing between subplots
    plt.show()
