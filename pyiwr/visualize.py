#!/usr/bin/env python
"""
@author1: Nitig Singh
@author2: Vaibhav Tyagi

@email1: nitig14rdfsma[at]gmail[dot]com
@email2: vaibhavtyagi7191[at]gmail[dot]com

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import warnings
from .utilities import xy2latlon




def elevation(
    radar,
    field_name="DBZ",
    elevation_index=0,
    scan_type = "short_scan",
    coord_system = "geo",
    figwidth = 8,
    figheight = 8,
    show_label = True,
    xlabel=None,
    ylabel=None,
    label_size=10,
    show_tick_labels = True,
    tick_label_size = 10,
    show_bounding_box=True,
    show_grid=True,
    grid_alpha=1.0,
    clmp = 'jet',
    colorbar_range=None,
    set_cbar_label = None,
    cbar_label_size=10,
    cbar_tick_label_size = None,
    show_title=True, 
    title_str= None,
    title_size = 14,
    show_rings=True,
    ring_alpha=1.0,
    ring_color = '0.5',
    show_ring_label=True, 
    ring_label_size=10, 
    ring_label_xloc_adjust=-5, 
    ring_label_yloc_adjust=15,
    save_image=False,
    img_dpi = 600,
    img_name=None,
    ):
  
    """
        
    Plot radar data at a specified elevation angle.

    Parameters:
    
    
        - radar (required): Radar object containing data and metadata.
        - field_name (str): Name of the field to plot. (Optional, default="DBZ")
        - elevation_index (int): Index of the elevation angle to plot. (Optional, default=0)
        - scan_type (str): Type of scan, e.g., 'PPI' or 'RHI'. (Optional, default="short_scan")
        - figwidth (int): control width size for the whole plot. (Optional, default= 8)
        - figheight (int): control height size for the whole plot. (Optional, default= 8)
        - coord_system = "geo", it will be plotted in latitudes and longitudes, else in km
        - show_label (bool): Whether to show axis labels. (Optional, default=True)
        - xlabel= provide x label for the plot.(Optional, default=None)
        - ylabel= provide y label for the plot.(Optional, default=None)
        - label_size (int): Size of axis labels. (Optional, default=10)
        - show_tick_labels (bool): Whether to show tick labels. (Optional, default=True)
        - tick_label_size (int): Size of tick labels. (Optional, default=10)
        - show_bounding_box (bool): Whether to show a bounding box around the plot. (Optional, default=False)
        - show_grid (bool): Whether to show grid lines on the plot. (Optional, default=True)
        - grid_alpha (float): Transparency of grid lines. (Optional, default=1.0)
        - clmp is the parameter for providing the colorbar 
        - colorbar_range (tuple): Range of values for colorbar scaling. (Optional, default=None)
        - set_cbar_label (bool): set the colorbar label. (Optional, default=fields_Unit)
        - cbar_label_size (int): Size of colorbar label. (Optional, default=10)
        - cbar_tick_label_size: int or None, optional Size of the colorbar tick label font. Default is None (uses default tick label size).
        - show_title (bool): Whether to display plot title. (Optional, default=True)
        - title_str (str): Custom title for the plot. (Optional, default=None)
        - title_size (int): Size of the plot title. (Optional, default=14)
        - show_rings (bool): Whether to plot range rings. (Optional, default=True)
        - ring_alpha (float): Transparency of range rings. (Optional, default=1.0)
        - ring_color (str): Color of range rings. (Optional, default='0.5')
        - show_ring_label (bool): Whether to show the labels of range of rings. (Optional, default=True)
        - ring_label_size (int): Size of range ring labels. (Optional, default=10)
        - ring_label_xloc_adjust (int): Adjustment for x position of ring labels. (Optional, default=-5  for short scan)
        - ring_label_yloc_adjust (int): Adjustment for y position of ring labels. (Optional, default=15  for short scan)
        - save_image (bool): Whether to save the plot as an image file. (Optional, default=False)
        - img_dpi (int): give the dots per inch(Optional, default=600)
        - img_name (str): Name of the image file to save. (required, default=None)

    

        Example usage:
        
        pyiwr.visualize.elevation(radar, field_name='DBZ', elevation_index=0, figwidth = 10, figheight = 8, show_label = True, 
        xlabel=None, ylabel=None, label_size=15, show_tick_labels = True, tick_label_size = 15, show_bounding_box = True, 
        show_grid = True, grid_alpha=0.5, show_rings = True, ring_color = "0.5", ring_alpha = 0.5, show_ring_label=True, 
        ring_label_size=15, ring_label_xloc_adjust=5, ring_label_yloc_adjust=50, show_title = True, title_str = None, 
        title_size = 14, scan_type = "short_scan", colorbar_range=None, set_cbar_label = None, cbar_label_size=15, 
        cbar_tick_label_size = None, save_image=False, img_dpi = 600, img_name='ele_image_uncorr.png')   
        
        """
    
    
    fig, ax = plt.subplots(figsize=(figwidth, figheight), dpi=img_dpi)

    # Assuming xs0 and ys0 are already computed as in your code
    radar_lat = radar.latitude['data'][0]
    radar_lon = radar.longitude['data'][0]
    
    rngs = radar.range["data"] / 1000.0
    xs0 = rngs[:, np.newaxis] * np.sin(
        np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
    )
    ys0 = rngs[:, np.newaxis] * np.cos(
        np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
    )


    ele_data = radar.fields[field_name]["data"][
        radar.sweep_start_ray_index["data"][
            elevation_index
        ] : radar.sweep_end_ray_index["data"][elevation_index]
        + 1
    ].T
    
    lats, lons = xy2latlon(xs0, ys0, radar_lat, radar_lon)
    
    if clmp == None:
        colormaps = {
            'DBZ': 'NWSRef',
            'VEL': 'NWSVel',
            'corrected_reflectivity': 'NWSRef',
            'corrected_velocity': 'NWSVel',
            'WIDTH': 'NWS_SPW',
            'PHIDP': 'PD17',
            'RHOHV': 'EWilson17',
            'ZDR': 'RefDiff',
            }
    else:
        colormaps = {
            'DBZ': clmp,
            'VEL': clmp,
            'corrected_reflectivity': clmp,
            'corrected_velocity': clmp,
            'WIDTH': clmp,
            'PHIDP': clmp,
            'RHOHV': clmp,
            'ZDR': clmp,
            }

    cmap = colormaps.get(field_name, colormaps)

    levels_dict = {
        'DBZ': [0, 70],
        'VEL': [-30, 30],
        'corrected_reflectivity': [0, 70],
        'corrected_velocity': [-30, 30],
        'WIDTH': [0, 10],
        'PHIDP': [0, 360],
        'RHOHV': [0.6, 1],
        'ZDR': [-10, 10],
        }

    if coord_system == "geo":      
        if colorbar_range is not None:
            plt.contourf(lons, lats, ele_data, levels=range(*colorbar_range), cmap=cmap)
        else:
            plt.contourf(lons, lats, ele_data, levels=range(*levels_dict[field_name]), cmap=cmap)  
    else:
        if colorbar_range is not None:
            plt.contourf(xs0, ys0, ele_data, levels=range(*colorbar_range), cmap=cmap)
        else:
            plt.contourf(xs0, ys0, ele_data, levels=range(*levels_dict[field_name]), cmap=cmap)
            
        
    # Show or hide tick labels based on the value of show_tick_labels
    if not show_tick_labels:
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        ax.tick_params(axis='x', labelsize=tick_label_size)
        ax.tick_params(axis='y', labelsize=tick_label_size)
        
        
        
    if field_name == 'corrected_reflectivity':
        plt.colorbar(label='DBZ', fontsize=cbar_label_size, ticks=cbar_tick_label_size)
    elif field_name == 'corrected_velocity':
        plt.colorbar(label='VEL', fontsize=cbar_label_size, ticks=cbar_tick_label_size)
    else:
        cbar = plt.colorbar()
        
        if set_cbar_label is None:
            set_cbar_label = cbar.set_label(radar.fields[field_name]["units"], fontsize=cbar_label_size)                
            if cbar_tick_label_size is not None:
                cbar.ax.tick_params(labelsize=cbar_tick_label_size)           

        else:
            cbar.set_label(set_cbar_label, fontsize=cbar_label_size)
            if cbar_tick_label_size is not None:
                cbar.ax.tick_params(labelsize=cbar_tick_label_size) 
                      
        
        
    # Set x and y labels if show_label is True
    if show_label:   
        if coord_system == "geo":      
            if xlabel is not None:
                ax.set_xlabel(xlabel, fontsize=label_size)
            else:
                ax.set_xlabel('Longitude due East', fontsize=label_size)
            
            if ylabel is not None:
                ax.set_ylabel(ylabel, fontsize=label_size)
            else:
                ax.set_ylabel('Latitude due North', fontsize=label_size)
        else:
            if xlabel is not None:
                ax.set_xlabel(xlabel, fontsize=label_size)
            else:
                ax.set_xlabel('East - West distance (in km) from Radar center', fontsize=label_size)
            
            if ylabel is not None:
                ax.set_ylabel(ylabel, fontsize=label_size)
            else:
                ax.set_ylabel('North - South distance (in km) from Radar center', fontsize=label_size)
    
    else:
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        
        
    k = radar.metadata["instrument_name"]
    title_string = f"{k} {radar.fields[field_name]['standard_name']}\nTime: {str('2022-03-26T16.01:32Z')}, PPI @ elevation {str(radar.fixed_angle['data'][elevation_index])}"

    # Title
    if show_title:
        if title_str is None:
            title_str = title_string
        else:
            plt.title(title_str, fontsize=title_size)
            
            
        plt.title(title_str, fontsize=title_size)

    if show_bounding_box:
        if show_grid:
            plt.grid(alpha=grid_alpha)  # Set the grid with adjustable alpha
            
    else:
        ax.set_frame_on(False)
        ax.grid(False)

    if coord_system != "geo":      
        if show_rings:
            if scan_type == "long_scan":
                t = np.linspace(0, 2 * np.pi)
                for r in [100, 250, 500]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    plt.plot(r * np.cos(t), r * np.sin(t), color=ring_color, alpha=ring_alpha)  # ring_color from 0 for black to 1 for white, Use '0.5' for medium grey color, Adjust the ring alpha as desired from 0 for light to 1 for dark
                    if show_ring_label:
                        plt.text(x + ring_label_xloc_adjust, y + ring_label_yloc_adjust, f"{r} Km", ha='center', va='center', fontsize=ring_label_size)                
            else:
                t = np.linspace(0, 2 * np.pi)
                for r in [50, 150, 250]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    plt.plot(r * np.cos(t), r * np.sin(t), color=ring_color, alpha=ring_alpha)  # ring_color from 0 for black to 1 for white, Use '0.5' for medium grey color, Adjust the ring alpha as desired from 0 for light to 1 for dark
                    if show_ring_label:
                        plt.text(x + ring_label_xloc_adjust, y + ring_label_yloc_adjust, f"{r} Km", ha='center', va='center', fontsize=ring_label_size)

                # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=img_dpi, bbox_inches="tight")
    plt.tight_layout()
    plt.show()



def all_elevation(
    radar,
    field_name="DBZ",
    scan_type = "short_scan",
    figwidth = 20,
    figheight = 18,
    coord_system = "geo",
    show_label = True,
    xlabel=None,
    ylabel=None,
    label_size=10,
    show_tick_labels = True,
    tick_label_size = 10,
    show_bounding_box = True, 
    show_grid = True, 
    grid_alpha=0.5,
    clmp = None,
    colorbar_range=None,
    set_cbar_label = None,    
    cbar_label_size=10,
    cbar_tick_label_size = None,    
    show_suptitle=True, 
    suptitle_str= None,
    suptitle_size = 14,
    suptitle_vspace = 1.0,
    show_subtitle=True, 
    subtitle_size = 14,
    subplots_vspace = 0.95,
    subplots_hspace = 0.3,
    show_rings=True,
    ring_alpha=1.0,
    ring_color = '0.5',
    show_ring_label=True, 
    ring_label_size=10, 
    ring_label_xloc_adjust=-5, 
    ring_label_yloc_adjust=15,    
    save_image=False,
    img_dpi = 600,
    img_name=None,
):
    """
    Plot radar data for all elevation angles.

    Parameters:
    
    
        - radar (required): Radar object containing data and metadata.
        - field_name (str): Name of the field to plot. (Optional, default="DBZ")
        - scan_type (str): Type of scan, e.g., 'PPI' or 'RHI'. (Optional, default="short_scan")
        - figwidth (int): control width size for the whole plot. (Optional, default= 20)
        - figheight (int): control height size for the whole plot. (Optional, default= 18)
        - coord_system = "geo", it will be plotted in latitudes and longitudes, else in km
        - show_label (bool): Whether to show axis labels. (Optional, default=True)
        - xlabel= provide x label for the plot.(Optional, default=None)
        - ylabel= provide y label for the plot.(Optional, default=None)
        - label_size (int): Size of axis labels. (Optional, default=10)
        - show_tick_labels (bool): Whether to show tick labels. (Optional, default=True)
        - tick_label_size (int): Size of tick labels. (Optional, default=10)
        - show_bounding_box (bool): Whether to show a bounding box around the plot. (Optional, default=True)
        - show_grid (bool): Whether to show grid lines on the plot. (Optional, default=True)
        - grid_alpha (float): Transparency of grid lines. (Optional, default=1.0)
        - clmp is the parameter for providing the colorbar scheme for th radar field plotting
        - colorbar_range (tuple): Range of values for colorbar scaling. (Optional, default=None)
        - set_cbar_label (bool): set the colorbar label. (Optional, default=fields_Unit)
        - cbar_label_size (int): Size of colorbar label. (Optional, default=10)
        - cbar_tick_label_size: int or None, optional Size of the colorbar tick label font. (Optional, default=None)
        - show_suptitle (bool): Whether to display super plot title. (Optional, default=True)
        - suptitle_str (str): Custom title for the whole plot. (Optional, default=None)
        - suptitle_size (int): Size of the super plot title. (Optional, default=14)        
        - suptitle_vspace (int): vertical space between subplots and the super title. (Optional, default = 1.0)
        - show_subtitle (bool): Whether to display subplot title. (Optional, default=True)
        - subtitle_str (str): Custom title for the subplot. (Optional, default=None)
        - subtitle_size (int): Size of the subplot title. (Optional, default=14)
        - subplots_vspace (int): vertical space between subplots. (Optional, default = 0.95)
        - subplots_hspace (int): horizontal space between subplots. (Optional, default = 0.3)
        - show_rings (bool): Whether to plot range rings. (Optional, default=True)
        - ring_alpha (float): Transparency of range rings. (Optional, default=1.0)
        - ring_color (str): Color of range rings. (Optional, default='0.5')
        - show_ring_label (bool): Whether to show the labels of range of rings. (Optional, default=True)
        - ring_label_size (int): Size of range ring labels. (Optional, default=10)
        - ring_label_xloc_adjust (int): Adjustment for x position of ring labels. (Optional, default=-5  for short scan)
        - ring_label_yloc_adjust (int): Adjustment for y position of ring labels. (Optional, default=15  for short scan)
        - save_image (bool): Whether to save the plot as an image file. (Optional, default=False)
        - img_dpi (int): give the dots per inch(Optional, default=600)
        - img_name (str): Name of the image file to save. (required, default=None)

    
        
        
        Example usage:
        
        pyiwr.visualize.all_elevation(radar, field_name='DBZ', scan_type = "short_scan", figwidth = 20, figheight = 18,
        show_label = True, xlabel=None, ylabel=None,label_size=18, show_tick_labels = True, tick_label_size = 15, 
        show_bounding_box = True, show_grid = True, grid_alpha=0.5, show_rings = True, ring_color = "0.5", ring_alpha = 0.5, 
        show_ring_label=True, ring_label_size=15, ring_label_xloc_adjust=5, ring_label_yloc_adjust=50, show_suptitle = True, 
        suptitle_str = None, suptitle_size = 20, suptitle_vspace = 1.0, show_subtitle = True, subtitle_str = None, 
        subtitle_size = 20, colorbar_range=[0,70], set_cbar_label = None, cbar_label_size=25, cbar_tick_label_size = 20, 
        img_dpi = 600, save_image=False, img_name='all_ele_imagenew.png')  
        
        """
    
    
    fig = plt.figure(figsize=(figwidth, figheight))  # Increase figure size for better visibility
    
    k = radar.metadata["instrument_name"]
    suptitle_string = f"{k} \nTime: {str(radar.time['units'])[14:]}, {radar.fields[field_name]['standard_name']} @ various elevation angles"

    # Title
#     fig.suptitle(suptitle_str, fontsize=16, y=1.0)

    # Title
    if show_suptitle:
        if suptitle_str is None:
            suptitle_str = suptitle_string
        else:
            fig.suptitle(suptitle_str, fontsize=suptitle_size, y= suptitle_vspace)   
        fig.suptitle(suptitle_str, fontsize=suptitle_size, y= suptitle_vspace)    


    
    # Assuming xs0 and ys0 are already computed as in your code
    radar_lat = radar.latitude['data'][0]
    radar_lon = radar.longitude['data'][0]
    
#     if range_in_km:
    rngs = radar.range["data"] / 1000.0
    xs0 = rngs[:, np.newaxis] * np.sin(
        np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
    )
    ys0 = rngs[:, np.newaxis] * np.cos(
        np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
    )

    lats, lons = xy2latlon(xs0, ys0, radar_lat, radar_lon)
    
    if clmp == None:
        colormaps = {
            'DBZ': 'NWSRef',
            'VEL': 'NWSVel',
            'corrected_reflectivity': 'NWSRef',
            'corrected_velocity': 'NWSVel',
            'WIDTH': 'NWS_SPW',
            'PHIDP': 'PD17',
            'RHOHV': 'EWilson17',
            'ZDR': 'RefDiff',   
        }
    else:
        colormaps = {
            'DBZ': clmp,
            'VEL': clmp,
            'corrected_reflectivity': clmp,
            'corrected_velocity': clmp,
            'WIDTH': clmp,
            'PHIDP': clmp,
            'RHOHV': clmp,
            'ZDR': clmp,
            }

    cmap = colormaps.get(field_name, colormaps)

    levels_dict = {
        'DBZ': [0, 70],
        'VEL': [-30, 30],
        'corrected_reflectivity': [0, 70],
        'corrected_velocity': [-30, 30],
        'WIDTH': [0, 10],
        'PHIDP': [0, 360],
        'RHOHV': [0.6, 1],
        'ZDR': [-10, 10],
    }

    
    
    for i in range(radar.fixed_angle["data"].size):
        ax = fig.add_subplot(4, 3, i + 1)
        slice_indices = radar.get_slice(i)
        all_ele = radar.fields[field_name]["data"][slice_indices].T     
    
    
    
        if coord_system == "geo":      
            if colorbar_range is not None:
                plt.contourf(lons, lats, all_ele, levels=range(*colorbar_range), cmap=cmap)
            else:
                plt.contourf(lons, lats, all_ele, levels=range(*levels_dict[field_name]), cmap=cmap)  
        else:
            if colorbar_range is not None:
                plt.contourf(xs0, ys0, all_ele, levels=range(*colorbar_range), cmap=cmap)
            else:
                plt.contourf(xs0, ys0, all_ele, levels=range(*levels_dict[field_name]), cmap=cmap)

        
        # Show or hide tick labels based on the value of show_tick_labels
        if not show_tick_labels:
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            ax.tick_params(axis='x', labelsize=tick_label_size)
            ax.tick_params(axis='y', labelsize=tick_label_size)            
            
            
        if field_name == 'corrected_reflectivity':
            plt.colorbar(label='DBZ', fontsize=cbar_label_size, ticks=cbar_tick_label_size)
        elif field_name == 'corrected_velocity':
            plt.colorbar(label='VEL', fontsize=cbar_label_size, ticks=cbar_tick_label_size)
        else:
            cbar = plt.colorbar()

            if set_cbar_label is None:
                set_cbar_label = cbar.set_label(radar.fields[field_name]["units"], fontsize=cbar_label_size)                
                if cbar_tick_label_size is not None:
                    cbar.ax.tick_params(labelsize=cbar_tick_label_size)           
                    
            else:
#                 set_cbar_label = cbar.set_label(field_name, fontsize=cbar_label_size)
                cbar.set_label(set_cbar_label, fontsize=cbar_label_size)
                if cbar_tick_label_size is not None:
                    cbar.ax.tick_params(labelsize=cbar_tick_label_size)                     
            
            
            
        # Set x and y labels if show_label is True
        if show_label:  
            if coord_system == "geo":      
                if xlabel is not None:
                    ax.set_xlabel(xlabel, fontsize=label_size)
                else:
                    ax.set_xlabel('Longitude due East', fontsize=label_size)
                
                if ylabel is not None:
                    ax.set_ylabel(ylabel, fontsize=label_size)
                else:
                    ax.set_ylabel('Latitude due North', fontsize=label_size)
            else:
                if xlabel is not None:
                    ax.set_xlabel(xlabel, fontsize=label_size)
                else:
                    ax.set_xlabel('East - West distance (in km) from Radar center', fontsize=label_size)
                
                if ylabel is not None:
                    ax.set_ylabel(ylabel, fontsize=label_size)
                else:
                    ax.set_ylabel('North - South distance (in km) from Radar center', fontsize=label_size)
           
        else:
            ax.set_xlabel('')
            ax.set_ylabel('')  
        
        
        subtitle_string = "PPI @ Elevation angle = %.3f" % radar.fixed_angle["data"][i]
        
        # Title
        if show_subtitle:
            plt.title(subtitle_string, fontsize=subtitle_size)        
            
            
        if show_bounding_box:
            if show_grid:
                plt.grid(alpha=grid_alpha)  # Set the grid with adjustable alpha            
        else:
            ax.set_frame_on(False)
            ax.grid(False)     
            
        if coord_system != "geo":      
            if show_rings:
                if scan_type == "long_scan":
                    t = np.linspace(0, 2 * np.pi)
                    for r in [100, 250, 500]:
                        x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                        y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                        plt.plot(r * np.cos(t), r * np.sin(t), color=ring_color, alpha=ring_alpha)  # ring_color from 0 for black to 1 for white, Use '0.5' for medium grey color, Adjust the ring alpha as desired from 0 for light to 1 for dark
                        if show_ring_label:
                            plt.text(x + ring_label_xloc_adjust, y + ring_label_yloc_adjust, f"{r} Km", ha='center', va='center', fontsize=ring_label_size)                
                else:
                    t = np.linspace(0, 2 * np.pi)
                    for r in [50, 150, 250]:
                        x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                        y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                        plt.plot(r * np.cos(t), r * np.sin(t), color=ring_color, alpha=ring_alpha)  # ring_color from 0 for black to 1 for white, Use '0.5' for medium grey color, Adjust the ring alpha as desired from 0 for light to 1 for dark
                        if show_ring_label:
                            plt.text(x + ring_label_xloc_adjust, y + ring_label_yloc_adjust, f"{r} Km", ha='center', va='center', fontsize=ring_label_size)


    plt.subplots_adjust(
        top=subplots_vspace, hspace=subplots_vspace
    )  # Adjust top margin and horizontal spacing between subplots
    
    
    
    # Save the image if save_image is True and file_name is provided   
    
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=img_dpi, bbox_inches="tight")
    plt.tight_layout()
    plt.show()


def fields_elevation(
    radar,
    elevation_index=0,
    scan_type="short_scan",
    figwidth=20,
    figheight=15,
    show_label=True,
    xlabel=None,
    ylabel=None,
    label_size=10,
    show_tick_labels=True,
    tick_label_size=10,
    show_bounding_box=True,
    show_grid=True,
    grid_alpha=0.5,
    clmp = ['jet', 'turbo', 'jet', 'turbo', 'jet', 'turbo'],
    cbar_label_size=10,
    cbar_tick_label_size=None,
    colorbar_range=None,  
    show_suptitle=True,
    suptitle_str=None,
    suptitle_size=14,
    suptitle_vspace=1.0,
    show_subtitle=True,
    subtitle_size=14,
    subplots_vspace=0.95,
    subplots_hspace=0.3,
    show_rings=True,
    ring_alpha=1.0,
    ring_color="0.5",
    show_ring_label=True,
    ring_label_size=10,
    ring_label_xloc_adjust=-5,
    ring_label_yloc_adjust=15,
    save_image=False,
    img_dpi=600,
    img_name=None,
):
    """
    Plot multiple radar products at the specified elevation.
    Parameters:
    
        - radar (required): Radar object containing data and metadata.
        - elevation_index (int): Index of the elevation angle to plot. (Optional, default=0)
        - scan_type (str): Type of scan, e.g., 'PPI' or 'RHI'. (Optional, default="short_scan")
        - figwidth (int): control width size for the whole plot. (Optional, default= 20)
        - figheight (int): control height size for the whole plot. (Optional, default= 18)
        - show_label (bool): Whether to show axis labels. (Optional, default=True)
        - xlabel= provide x label for the plot.(Optional, default=None)
        - ylabel= provide y label for the plot.(Optional, default=None)
        - label_size (int): Size of axis labels. (Optional, default=10)
        - show_tick_labels (bool): Whether to show tick labels. (Optional, default=True)
        - tick_label_size (int): Size of tick labels. (Optional, default=10)
        - show_bounding_box (bool): Whether to show a bounding box around the plot. (Optional, default=True)
        - show_grid (bool): Whether to show grid lines on the plot. (Optional, default=True)
        - grid_alpha (float): Transparency of grid lines. (Optional, default=1.0)
        - clmp is the list for providing the color scheme for all the radar fields 
        - colorbar_range (tuple): Range of values for colorbar scaling. (Optional, default=None)
          inthis way use r should enter #[[0, 70], [-30, 30], [0, 10], [-10, 10], [0, 360], [0.6, 1]]
        - cbar_label_size (int): Size of colorbar label. (Optional, default=10)
        - cbar_tick_label_size: int or None, optional Size of the colorbar tick label font. (Optional, default=None)
        - show_suptitle (bool): Whether to display super plot title. (Optional, default=True)
        - suptitle_str (str): Custom title for the whole plot. (Optional, default=None)
        - suptitle_size (int): Size of the super plot title. (Optional, default=14)        
        - suptitle_vspace (int): vertical space between subplots and the super title. (Optional, default = 1.0)
        - show_subtitle (bool): Whether to display subplot title. (Optional, default=True)
        - subtitle_str (str): Custom title for the subplot. (Optional, default=None)
        - subtitle_size (int): Size of the subplot title. (Optional, default=14)
        - subplots_vspace (int): vertical space between subplots. (Optional, default = 0.95)
        - subplots_hspace (int): horizontal space between subplots. (Optional, default = 0.3)
        - show_rings (bool): Whether to plot range rings. (Optional, default=True)
        - ring_alpha (float): Transparency of range rings. (Optional, default=1.0)
        - ring_color (str): Color of range rings. (Optional, default='0.5')
        - show_ring_label (bool): Whether to show the labels of range of rings. (Optional, default=True)
        - ring_label_size (int): Size of range ring labels. (Optional, default=10)
        - ring_label_xloc_adjust (int): Adjustment for x position of ring labels. (Optional, default=-5  for short scan)
        - ring_label_yloc_adjust (int): Adjustment for y position of ring labels. (Optional, default=15  for short scan)
        - save_image (bool): Whether to save the plot as an image file. (Optional, default=False)
        - img_dpi (int): give the dots per inch(Optional, default=600)
        - img_name (str): Name of the image file to save. (required, default=None)
        
        Example usage:
        pyiwr.visualize.fields_elevation(radar, elevation_index=2, scan_type = "short_scan",  figwidth = 20, figheight = 18, 
        show_label = True, xlabel=None, ylabel=None, label_size=15, show_tick_labels = True, tick_label_size = 12, 
        show_bounding_box = True, show_grid = True, grid_alpha=0.5, show_rings = True, ring_color = "0.5", ring_alpha = 0.5, 
        show_ring_label=True, ring_label_size=15, ring_label_xloc_adjust=5, ring_label_yloc_adjust=50, show_suptitle = True, 
        suptitle_str = None, suptitle_size = 20, suptitle_vspace = 1.0, show_subtitle = True, subtitle_size = 20, 
        subplots_vspace = 0.95, subplots_hspace = 0.3, colorbar_range=None, cbar_label_size=20, cbar_tick_label_size = 20, 
        save_image=False, img_dpi = 600, img_name='fields_ele_imagenew.png')
        
        
    """

    fig = plt.figure(figsize=(figwidth, figheight))  # Increase figure size for better visibility

    k = radar.metadata["instrument_name"]
    suptitle_string = f"{k} \nTime: {str(radar.time['units'])[14:]}, PPI Products @ elevation {str(radar.fixed_angle['data'][elevation_index])}"

    # Title
    if show_suptitle:
        if suptitle_str is None:
            suptitle_str = suptitle_string
        else:
            fig.suptitle(suptitle_str, fontsize=suptitle_size, y=suptitle_vspace)
        fig.suptitle(suptitle_str, fontsize=suptitle_size, y=suptitle_vspace)

    product_names = ["DBZ", "VEL", "WIDTH", "ZDR", "PHIDP", "RHOHV"]
    titles = [
        "Reflectivity",
        "Doppler Velocity",
        "Spectral Width",
        "Differential Reflectivity",
        "Differential Phase",
        "Correlation Coefficient",
    ]
    if clmp:
        cmap_names = [clmp[0],
                      clmp[1],
                      clmp[2],
                      clmp[3],
                      clmp[4],
                      clmp[5],
                     ]
    else: 
        cmap_names = ["NWSRef",
                      "NWSVel",
                      "NWS_SPW",
                      "RefDiff",
                      "PD17",
                      "EWilson17",
                      ]
    levels = [[0, 70], [-30, 30], [0, 10], [-10, 10], [0, 360], [0.6, 1]]

    rngs = radar.range["data"] / 1000.0
    xs0 = rngs[:, np.newaxis] * np.sin(
        np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
    )
    ys0 = rngs[:, np.newaxis] * np.cos(
        np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
    )

    for i, product_name in enumerate(product_names):
        ax = fig.add_subplot(3, 3, i + 1)
        ele_data = radar.fields[product_name]["data"][
            radar.sweep_start_ray_index["data"][elevation_index]
            : radar.sweep_end_ray_index["data"][elevation_index]
            + 1
        ].T

        # Get the colormap for the product
        cmap = cmap_names[i]

        # Get the colorbar range for the current product
        if colorbar_range is not None:
            vmin, vmax = colorbar_range[i]
        else:
            vmin, vmax = levels[i]

        plt.contourf(
            xs0,
            ys0,
            ele_data,
            levels=np.linspace(vmin, vmax, 31),
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
        )

        # Show or hide tick labels based on the value of show_tick_labels
        if not show_tick_labels:
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            ax.tick_params(axis="x", labelsize=tick_label_size)
            ax.tick_params(axis="y", labelsize=tick_label_size)

        # Create the colorbar object
        cbar = plt.colorbar()

        # Set the label and adjust its font size
        cbar.set_label(product_name, fontsize=cbar_label_size)

        # Adjust the tick labels' font size if cbar_tick_label_size is provided
        if cbar_tick_label_size is not None:
            cbar.ax.tick_params(axis="y", labelsize=cbar_tick_label_size)

        plt.title(titles[i])

        # Set x and y labels if show_label is True
        if show_label:
            if xlabel is not None:
                ax.set_xlabel(xlabel, fontsize=label_size)
            else:
                ax.set_xlabel("Range (in km) of Radar", fontsize=label_size)

            if ylabel is not None:
                ax.set_ylabel(ylabel, fontsize=label_size)
            else:
                ax.set_ylabel("Range (in km) of Radar", fontsize=label_size)
        else:
            ax.set_xlabel("")
            ax.set_ylabel("")

        if show_bounding_box:
            if show_grid:
                plt.grid(alpha=grid_alpha)  # Set the grid with adjustable alpha
        else:
            ax.set_frame_on(False)
            ax.grid(False)

        if show_rings:
            if scan_type == "long_scan":
                t = np.linspace(0, 2 * np.pi)
                for r in [100, 250, 500]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    plt.plot(
                        r * np.cos(t),
                        r * np.sin(t),
                        color=ring_color,
                        alpha=ring_alpha,
                    )  # ring_color from 0 for black to 1 for white, Use '0.5' for medium grey color, Adjust the ring alpha as desired from 0 for light to 1 for dark
                    if show_ring_label:
                        plt.text(
                            x + ring_label_xloc_adjust,
                            y + ring_label_yloc_adjust,
                            f"{r} Km",
                            ha="center",
                            va="center",
                            fontsize=ring_label_size,
                        )
            else:
                t = np.linspace(0, 2 * np.pi)
                for r in [50, 150, 250]:
                    x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                    y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                    plt.plot(
                        r * np.cos(t),
                        r * np.sin(t),
                        color=ring_color,
                        alpha=ring_alpha,
                    )  # ring_color from 0 for black to 1 for white, Use '0.5' for medium grey color, Adjust the ring alpha as desired from 0 for light to 1 for dark
                    if show_ring_label:
                        plt.text(
                            x + ring_label_xloc_adjust,
                            y + ring_label_yloc_adjust,
                            f"{r} Km",
                            ha="center",
                            va="center",
                            fontsize=ring_label_size,
                        )

    plt.subplots_adjust(
        top=subplots_vspace, hspace=subplots_vspace
    )  # Adjust top margin and horizontal spacing between subplots

    # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError("Please provide the 'img_name' parameter to save the image.")

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=img_dpi, bbox_inches="tight")

    plt.tight_layout()
    plt.show()

