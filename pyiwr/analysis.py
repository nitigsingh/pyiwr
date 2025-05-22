#!/usr/bin/env python
"""
@author1: Nitig Singh
@author2: Vaibhav Tyagi
@author3: Hamid Ali Syed

@email1: nitig14rdfsma[at]gmail[dot]com
@email2: vaibhavtyagi7191[at]gmail[dot]com

"""

from datetime import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as tj
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.ticker import NullFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def cappi(
    xg,
    altitude_level,
    field_name="DBZ",
    radar_location="CHERRAPUNJI",
    grid=False,
    rings=False,
    coord_system="km",  # <-- new param: 'km', 'm', or 'geo'
    save_image=False,
    img_name=None,
):

    """
    Plot CAPPI at the specified altitude level.

    Parameters:
        xg (xarray.Dataset): Pyiwr Xarray Dataset containing gridded radar data.
        altitude_level (int): Altitude level in kilometers (e.g., 3 km = 6, 3.5 km = 7).
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        radar_location (str, optional): Radar location name. Default is 'CHERRAPUNJI',
            other options are 'SHAR' and 'TERLS'.
        grid (bool, optional): If True, display gridlines. Default is False.
        rings (bool, optional): If True, display range rings. Default is False.
        coord_system (str, optional): Coordinate system for plotting. Choose from:
            - 'km': Cartesian coordinates in kilometers.
            - 'm': Cartesian coordinates in meters.
            - 'geo': Geographic coordinates (longitude and latitude).
            Default is 'km'.
        save_image (bool, optional): If True, save the image as a PNG file. Default is False.
        img_name (str, optional): Name of the PNG file to save. Required if save_image is True.

    Example usage:
        pyiwr.visualize.cappi(
            xg,
            altitude_level=3,
            field_name='DBZ',
            radar_location='CHERRAPUNJI',
            grid=False,
            rings=True,
            coord_system='geo',
            save_image=True,
            img_name='cappi_image.png'
        )
    """

    alt_index = int(
        altitude_level * 2
    )  # Calculate the index corresponding to the altitude level

    # Define colormap based on the field_name
    colormaps = {
        "DBZ": "NWSRef",
        "VEL": "NWSVel",
        "WIDTH": "NWS_SPW",
        "PHIDP": "PD17",
        "RHOHV": "EWilson17",
        "ZDR": "RefDiff",
    }

    # Define levels for the color bar
    levels = {
        "DBZ": [-20, 70],
        "VEL": [-30, 30],
        "WIDTH": [0, 10],
        "PHIDP": [0, 360],
        "RHOHV": [0.6, 1],
        "ZDR": [-10, 10],
    }

    # Access the field from the xg dataset using the field_name parameter
    if coord_system == "geo":
        x = xg.lon
        y = xg.lat
        xlabel = "Longitude due East"
        ylabel = "Latitude due North"
    elif coord_system == "m":
        x = xg.x
        y = xg.y
        xlabel = "Range (in m) of Radar (at Center) in Cartesian"
        ylabel = "Range (in m) of Radar (at Center) in Cartesian"
    else:  # Default to 'km'
        x = xg.x / 1000
        y = xg.y / 1000
        xlabel = "Range (in km) of Radar (at Center) in Cartesian"
        ylabel = "Range (in km) of Radar (at Center) in Cartesian"
    
    plt.contourf(
        x,
        y,
        xg[field_name][0][alt_index],
        levels=np.linspace(*levels.get(field_name, [-20, 70]), 31),
        cmap=colormaps.get(field_name, "NWSRef"),
    )


    plt.colorbar(label=field_name)

    if radar_location == "CHERRAPUNJI":
        k = "CHERRAPUNJI S-band Dual-Pol DWR"
    elif radar_location == "SHAR":
        k = "SHAR S-band Dual-pol DWR"
    else:
        k = "TERLS C-band Dual-pol DWR"

    plt.title(
        f"{k} {xg[field_name].standard_name}\nTime: {str(xg.time['time'].values[0])[:19]}, CAPPI @ Altitude {altitude_level} km"
    )

    if grid:
        plt.grid()

    if rings and coord_system != "geo":
        t = np.linspace(0, 2 * np.pi)
        if coord_system == "km":
            ring_radii = [50, 150, 250]  # in kilometers
            scale = 1  # already in km
        elif coord_system == "m":
            ring_radii = [50000, 150000, 250000]  # in meters
            scale = 1  # already in meters
    
        for r in ring_radii:
            plt.plot(
                r * np.cos(t) * scale,
                r * np.sin(t) * scale,
                color="0.5",
            )


    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


    # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=600, bbox_inches="tight")
    plt.show()

def cappi_max(
    xg,
    radar_location="CHERRAPUNJI",
    field_name="DBZ",
    rings=False,
    grids=False,
    marginal_cross_sect=True,
    coord_system="km",
    save_image=False,
    img_name=None,
):
    """
    Plot the MAX-Z CAPPI (Constant Altitude Plan Position Indicator) with optional marginal_cross_sections 
    for the given xarray Dataset.

    Parameters:
        xg (xarray.Dataset): Gridded radar data in xarray format (as output by PyIWR).
        radar_location (str, optional): Name of the radar location. Default is 'CHERRAPUNJI'.
        field_name (str, optional): Radar variable/field to plot (e.g., 'DBZ', 'VEL'). Default is 'DBZ'.
        rings (bool, optional): If True, draw range rings around radar. Default is False.
        grids (bool, optional): If True, overlay gridlines on the plot. Default is False.
        marginal_cross_sect (bool, optional): If True, plot vertical cross-sections along centerlines. Default is True.
        coord_system (str, optional): Coordinate system to use for plotting. One of:
            - 'km': Cartesian coordinates in kilometers from radar center.
            - 'm' : Cartesian coordinates in meters from radar center.
            - 'geo': Geographic coordinates (longitude and latitude).
            Default is 'km'.

            Note: When using 'geo', the plot uses 2D latitude/longitude arrays and colorbar is 
            manually added (unlike 'km' or 'm', where it is auto-handled by xarray).

        save_image (bool, optional): If True, save the plot to disk as a PNG file. Default is False.
        img_name (str, optional): Filename for the PNG output. Required if save_image is True.

    Example usage:
        marginal_max(
            xg,
            radar_location='SHAR',
            field_name='WIDTH',
            rings=True,
            grids=True,
            marginal_cross_sect=True,
            coord_system='geo',
            save_image=True,
            img_name='marg_max_image.png'
        )
    """

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect(1.0)

    # Define colormap and levels
    colormaps = {
        "DBZ": "NWSRef", "VEL": "NWSVel", "WIDTH": "NWS_SPW",
        "PHIDP": "PD17", "RHOHV": "EWilson17", "ZDR": "RefDiff"
    }
    cmap = colormaps.get(field_name, "pyart_NWSRef")
    levels = {
        "DBZ": [-20, 70], "VEL": [-30, 30], "WIDTH": [0, 10],
        "PHIDP": [0, 360], "RHOHV": [0.6, 1], "ZDR": [-10, 10]
    }
    cmap_levels = levels.get(field_name, [-20, 70])
    
    # Prepare CAPPI
    cappi = xg[field_name][0].max("z")  # shape ('y', 'x')

    
    # Choose coordinates
    if coord_system == "geo":
        x, y = xg["lon"].values, xg["lat"].values  # These are 2D (y, x)
        xlabel = "Longitude due East"
        ylabel = "Latitude due North"
        cf = ax.contourf(x, y, cappi.values,
                         cmap=cmap,
                         levels=range(cmap_levels[0], cmap_levels[1] + 1)
        )
        # Add colorbar manually
        cbar = plt.colorbar(cf, ax=ax, pad=0.02, shrink=0.8)
        cbar.set_label(f"{field_name}")  # Optional label
        
    else:
        if coord_system == "km":
            x = xg["x"].values / 1000  # 1D in km
            y = xg["y"].values / 1000
            cappi.coords["x"] = x
            cappi.coords["y"] = y
        
        else:
            x = xg["x"].values  # 1D in meters
            y = xg["y"].values
            cappi.coords["x"] = x
            cappi.coords["y"] = y
            
        xlabel = f"East-West distance (in {coord_system}) from radar center"
        ylabel = f"North-South distance (in {coord_system}) from radar center"
    
        # Cartesian: 1D coordinates
        cf = cappi.plot.contourf(
            ax=ax,
            cmap=cmap,
            levels=range(cmap_levels[0], cmap_levels[1] + 1),
            cbar_kwargs={"pad": 0.02, "shrink": 0.84},
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)



    # Title
    radar_titles = {
        "CHERRAPUNJI": "CHERRAPUNJI S-band Dual-Pol DWR",
        "SHAR": "SHAR S-band Dual-pol DWR",
        "TERLS": "TERLS C-band Dual-pol DWR"
    }
    radar_title = radar_titles.get(radar_location.upper(), radar_location)
    title_str = f"{radar_title} {xg[field_name].standard_name}\nTime: {str(xg.time['time'].values[0])[:19]}, MAXZ CAPPI"
    plt.title(title_str, pad=100 if marginal_cross_sect else None)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    
    if grids and coord_system != "geo":
        plt.grid()

    if rings and coord_system != "geo":
        t = np.linspace(0, 2 * np.pi)
        ring_scale = 1 if coord_system == "m" else 1e-3
        for r in [50000, 150000, 250000]:
            radius = r * ring_scale
            plt.plot(radius * np.cos(t), radius * np.sin(t), color="0.5")

    if marginal_cross_sect:
        divider = make_axes_locatable(ax)
        ax_x = divider.append_axes("top", 1.2, pad=0.05)
        ax_y = divider.append_axes("right", 1.2, pad=0.05)

        xg[field_name][0].max(axis=1).plot.contourf(
            cmap=cmap,
            levels=range(cmap_levels[0], cmap_levels[1] + 1),
            add_colorbar=False,
            ax=ax_x,
        )
        xg[field_name][0].max(axis=2).T.plot.contourf(
            cmap=cmap,
            levels=range(cmap_levels[0], cmap_levels[1] + 1),
            add_colorbar=False,
            ax=ax_y,
        )

        ax_x.xaxis.set_major_formatter(NullFormatter())
        ax_y.yaxis.set_major_formatter(NullFormatter())
        ax_x.set_title(None)
        ax_y.set_title(None)
        ax_y.set_ylabel(None)
        ax_x.set_xlabel(None)
        ax_x.set_ylabel("Height AMSL (m)", size=10)
        ax_y.set_xlabel("Height AMSL (m)", size=10)

        # Add corner box with annotations
        if coord_system == "geo":
            left, bottom, width, height = 0.641, 0.694, 0.12, 0.12
        else:
            left, bottom, width, height = 0.641, 0.704, 0.12, 0.12
        ax_cnr = inset_axes(ax,
                            width="100%", height="100%",
                            bbox_to_anchor=(left, bottom, width, height),
                            bbox_transform=ax.figure.transFigure,
                            loc="upper left")
        plt.sca(ax_cnr)
        plt.tick_params(axis="both", which="both", bottom=False, top=False, left=False, right=False, labelbottom=False)
        ax_cnr.yaxis.set_major_formatter(NullFormatter())
        ax_cnr.xaxis.set_major_formatter(NullFormatter())

        plt.text(0.06, 0.8, "MAX-CAPPI", size=12, weight="bold")
        plt.text(0.02, 0.65, f"Max Range: {int(xg.x[-1] / 1e3)}km", size=8)
        plt.text(0.02, 0.5, f"Max Height: {int(xg.z[-1] / 1e3)}km", size=8)

        timestamp = str(xg.time["time"].values[0])
        plt.text(0.15, 0.3, timestamp[11:19], weight="bold", size=12)
        dt = datetime.strptime(timestamp[:10], "%Y-%m-%d")
        plt.text(0.1, 0.2, dt.strftime("%d %B"), size=10, ha="left", va="center")
        plt.text(0.2, 0.08, dt.strftime("%Y UTC"), size=10, ha="left", va="center")

    if save_image:
        if img_name is None:
            raise ValueError("Please provide the 'img_name' parameter to save the image.")
        plt.savefig(img_name, dpi=600, bbox_inches="tight")

    plt.show()

def marginal_max_map(
    xg,
    radar_location="CHERRAPUNJI",
    field_name="DBZ",
    background="terrain-background",
    cross_sections=True,
    save_image=False,
    img_name=None,
):
    """
    Plot the MAX-Z CAPPI on a base map using cartopy.

    Parameters:
        xg (xarray.Dataset): Py_SRT Xarray Dataset containing gridded radar data.
        radar_location (str, optional): Radar location name. Default is 'CHERRAPUNJI'.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        background (str, optional): Type of background map to use. Options are 'watercolor', 'terrain', 'toner', or 'terrain-background'. Default is 'terrain-background'.
        cross_sections (bool, optional): If True, display cross-sections. Default is True.
        save_image (bool, optional): If True, the plot will be saved as an image. Default is False.
        img_name (str, optional): The file name to save the plot as an image. This parameter is required if save_image is True.


        # Example usage
        marginal_max_map(xg, radar_location='TERLS', field_name='DBZ', background='terrain-background', cross_sections=True, save_image=True, img_name='cartmaxcappi.png')
    """
    plt.figure(figsize=[10, 10])
    ax = plt.axes(projection=ccrs.PlateCarree())
    if radar_location == "SHAR":
        ax.set_extent(
            [78, 82.52043879663267, 11.5, 15.901390588443753], crs=ccrs.PlateCarree()
        )
        ax.set_xticks(np.arange(78, 82.52043879663267, 1), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(11.5, 15.901390588443753, 1), crs=ccrs.PlateCarree())
        k = "SHAR S-band Dual-Pol DWR"
    elif radar_location == "CHERRAPUNJI":
        ax.set_extent([89, 94.5, 22.5, 28], crs=ccrs.Geodetic())
        ax.set_xticks(np.arange(89, 94.5, 1), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(22.5, 28, 1), crs=ccrs.PlateCarree())
        k = "CHERRAPUNJI S-band Dual-pol DWR"
    else:
        ax.set_extent(
            [74.5, 79.12701779571718, 6.0, 10.77846057031159], crs=ccrs.Geodetic()
        )
        ax.set_xticks(np.arange(74.5, 79.12701779571718, 1), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(6, 10.77846057031159, 1), crs=ccrs.PlateCarree())
        k = "TERLS C-band Dual-pol DWR"

    ax.add_feature(cfeature.BORDERS, alpha=0.9, lw=0.9)
    ax.add_feature(cfeature.COASTLINE, alpha=0.5, lw=0.5)
    ax.add_feature(cfeature.STATES.with_scale("10m"), alpha=0.5, lw=0.5)
    ax.add_feature(cfeature.LAND, alpha=0.5)
    ax.add_feature(cfeature.OCEAN, alpha=0.5)

    # For the x-axis
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))

    # For the y-axis
    ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y)}"))

    if background == "watercolor":
        st = tj.Stamen(background)
    elif background == "terrain":
        st = tj.Stamen(background)
    elif background == "toner":
        st = tj.Stamen(background)
    else:
        background == "terrain-background"
        st = tj.Stamen(background)

    ax.add_image(st, 8)

    # Define colormap based on the field_name
    colormaps = {
        "DBZ": "NWSRef",
        "VEL": "NWSVel",
        "WIDTH": "NWS_SPW",
        "PHIDP": "PD17",
        "RHOHV": "EWilson17",
        "ZDR": "RefDiff",
    }

    # Get the colormap for the field_name
    cmap = colormaps.get(field_name, "pyart_NWSRef")

    # Define levels for each field_name
    levels = {
        "DBZ": [-10, 70],
        "VEL": [-30, 30],
        "WIDTH": [-30, 30],
        "PHIDP": [-10, 20],
        "RHOHV": [-300, 300],
        "ZDR": [-10, 30],
    }

    # Get the levels for the field_name
    cmap_levels = levels.get(field_name, [-10, 70])

    # Plot main contourf
    cf_main = ax.contourf(
        xg.x["lon"],
        xg.y["lat"],
        xg[field_name][0].max("z"),
        levels=range(cmap_levels[0], cmap_levels[1] + 1),
        cmap=cmap,
    )

    # Title
    title_str = f"{k} {xg[field_name].standard_name}\nTime: {str(xg.time['time'].values[0])[:19]}, MAXZ CAPPI"

    if cross_sections:
        plt.title(title_str, fontsize=16, pad=100)
        plt.colorbar(cf_main, label=xg[field_name].units, fraction=0.039, pad=0.2)

    else:
        plt.title(title_str, fontsize=16)
        plt.colorbar(cf_main, label=xg[field_name].units, fraction=0.044, pad=0.03)

    # Set labels and title
    plt.xlabel("Longitudes due East", fontsize=14)
    plt.ylabel("Latitude due North", fontsize=14)

    if radar_location == "SHAR":
        # Site locations
        site = (80.2274, 13.6645, 29)
        site1 = (80.237617, 13.6067439, 6.7)

        # Plot site locations
        ax.plot(site[0], site[1], "ro", markersize=8)
        ax.plot(site1[0], site1[1], "bo", markersize=8)

        # Add text labels for site locations
        ax.text(
            site[0] + 0.3,
            site[1] + 0.05,
            "SHAR DWR",
            ha="center",
            va="bottom",
            fontsize=15,
        )
        ax.text(
            site1[0] + 0.4,
            site1[1] - 0.1,
            "Chennai",
            ha="center",
            va="bottom",
            fontsize=15,
        )

    elif radar_location == "CHERRAPUNJI":
        # Site locations
        site = (91.73, 25.26, 1313)
        site1 = (91.893254, 25.578773, 1496)

        # Plot site locations
        ax.plot(site[0], site[1], "ro", markersize=8)
        ax.plot(site1[0], site1[1], "bo", markersize=8)

        # Add text labels for site locations
        ax.text(
            site[0] + 0.3,
            site[1] + 0.05,
            "CHERRAPUNJI DWR",
            ha="center",
            va="bottom",
            fontsize=15,
        )
        ax.text(
            site1[0] + 0.4,
            site1[1] - 0.1,
            "Shillong",
            ha="center",
            va="bottom",
            fontsize=15,
        )

    else:
        # Site locations
        site = (76.8657, 8.5374, 27)
        site1 = (76.94924, 8.4855, 10)

        # Plot site locations
        ax.plot(site[0], site[1], "ro", markersize=8)
        ax.plot(site1[0], site1[1], "bo", markersize=8)

        # Add text labels for site locations
        ax.text(
            site[0] + 0.3,
            site[1] + 0.05,
            "TERLS DWR",
            ha="center",
            va="bottom",
            fontsize=15,
        )
        ax.text(
            site1[0] + 0.4,
            site1[1] - 0.2,
            "Thiruvananthapuram",
            ha="center",
            va="bottom",
            fontsize=15,
        )

    if cross_sections:
        if radar_location == "SHAR":
            # Create inset axes for shared contourf on top and right
            ax_x = inset_axes(
                ax,
                width="100%",
                height="25%",
                loc="upper center",
                bbox_to_anchor=(0, 0.41, 1, 0.8),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )
            ax_y = inset_axes(
                ax,
                width="25%",
                height="100%",
                loc="upper right",
                bbox_to_anchor=(0.41, 0, 0.8, 1),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )

            ax_x.xaxis.set_tick_params(labelbottom=False)
            ax_y.yaxis.set_tick_params(labelleft=False)

            ax_x.contourf(
                xg.x["lon"],
                xg.z,
                xg[field_name][0].max(axis=1),
                cmap=cmap,
                levels=range(cmap_levels[0], cmap_levels[1] + 1),
            )
            x_diff = ax_x.get_xticks()[1] - ax_x.get_xticks()[0]
            ax_x.set_xlim(ax_x.get_xticks()[0] + x_diff, ax_x.get_xlim()[1])

            ax_y.contourf(
                xg.z,
                xg.y["lat"],
                xg[field_name][0].max(axis=2).T,
                cmap=cmap,
                levels=range(cmap_levels[0], cmap_levels[1] + 1),
            )
            y_diff = ax_y.get_yticks()[1] - ax_y.get_yticks()[0]
            ax_y.set_ylim(ax_y.get_yticks()[0] + y_diff, ax_y.get_ylim()[1])

            ax_x.set_title(None)
            ax_y.set_title(None)
            ax_y.set_ylabel(None)
            ax_x.set_xlabel(None)
            ax_x.set_ylabel("Height AMSL (m)", size=10)
            ax_y.set_xlabel("Height AMSL (m)", size=10)

            # Add corner box
            left1, bottom1, width1, height1 = 0.721, 0.788, 0.118, 0.1155
            ax_cnr = plt.axes((left1, bottom1, width1, height1))
            plt.sca(ax_cnr)
            plt.tick_params(
                axis="both",
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
            )
            ax_cnr.yaxis.set_major_formatter(NullFormatter())
            ax_cnr.xaxis.set_major_formatter(NullFormatter())

            # Labels along the bottom edge are off
            plt.text(0.2, 0.8, "MAX-Z", size=14, weight="bold")
            plt.text(0.02, 0.65, "Max Range: 250 km", size=8)
            plt.text(0.02, 0.5, "Max Height: 15 km", size=8)
            plt.text(
                0.02, 0.3, str(xg.time["time"].values[0])[11:19], weight="bold", size=17
            )
            plt.text(
                0.1,
                0.2,
                datetime.strptime(
                    str(xg.time["time"].values[0])[:10], "%Y-%m-%d"
                ).strftime("%d %B"),
                size=10,
                ha="left",
                va="center",
            )
            plt.text(
                0.2,
                0.08,
                datetime.strptime(
                    str(xg.time["time"].values[0])[:10], "%Y-%m-%d"
                ).strftime("%Y UTC"),
                size=10,
                ha="left",
                va="center",
            )
        elif radar_location == "CHERRAPUNJI":
            # Create inset axes for shared contourf on top and right
            ax_x = inset_axes(
                ax,
                width="100%",
                height="25%",
                loc="upper center",
                bbox_to_anchor=(0, 0.41, 1, 0.8),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )
            ax_y = inset_axes(
                ax,
                width="25%",
                height="100%",
                loc="upper right",
                bbox_to_anchor=(0.41, 0, 0.8, 1),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )

            ax_x.xaxis.set_tick_params(labelbottom=False)
            ax_y.yaxis.set_tick_params(labelleft=False)

            ax_x.contourf(
                xg.x["lon"],
                xg.z,
                xg[field_name][0].max(axis=1),
                cmap=cmap,
                levels=range(cmap_levels[0], cmap_levels[1] + 1),
            )
            x_diff = ax_x.get_xticks()[1] - ax_x.get_xticks()[0]
            ax_x.set_xlim(ax_x.get_xticks()[0] + x_diff, ax_x.get_xlim()[1])

            ax_y.contourf(
                xg.z,
                xg.y["lat"],
                xg[field_name][0].max(axis=2).T,
                cmap=cmap,
                levels=range(cmap_levels[0], cmap_levels[1] + 1),
            )
            y_diff = ax_y.get_yticks()[1] - ax_y.get_yticks()[0]
            ax_y.set_ylim(ax_y.get_yticks()[0] + y_diff, ax_y.get_ylim()[1])

            ax_x.set_title(None)
            ax_y.set_title(None)
            ax_y.set_ylabel(None)
            ax_x.set_xlabel(None)
            ax_x.set_ylabel("Height AMSL (m)", size=10)
            ax_y.set_xlabel("Height AMSL (m)", size=10)

            # Add corner box
            left1, bottom1, width1, height1 = 0.721, 0.797, 0.118, 0.1175
            ax_cnr = plt.axes((left1, bottom1, width1, height1))
            plt.sca(ax_cnr)
            plt.tick_params(
                axis="both",
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
            )
            ax_cnr.yaxis.set_major_formatter(NullFormatter())
            ax_cnr.xaxis.set_major_formatter(NullFormatter())

            # Labels along the bottom edge are off
            plt.text(0.2, 0.8, "MAX-Z", size=14, weight="bold")
            plt.text(0.02, 0.65, "Max Range: 250 km", size=8)
            plt.text(0.02, 0.5, "Max Height: 15 km", size=8)
            plt.text(
                0.02, 0.3, str(xg.time["time"].values[0])[11:19], weight="bold", size=17
            )
            plt.text(
                0.1,
                0.2,
                datetime.strptime(
                    str(xg.time["time"].values[0])[:10], "%Y-%m-%d"
                ).strftime("%d %B"),
                size=10,
                ha="left",
                va="center",
            )
            plt.text(
                0.2,
                0.08,
                datetime.strptime(
                    str(xg.time["time"].values[0])[:10], "%Y-%m-%d"
                ).strftime("%Y UTC"),
                size=10,
                ha="left",
                va="center",
            )
        else:
            # Create inset axes for shared contourf on top and right
            ax_x = inset_axes(
                ax,
                width="100%",
                height="25%",
                loc="upper center",
                bbox_to_anchor=(0, 0.41, 1, 0.8),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )
            ax_y = inset_axes(
                ax,
                width="25%",
                height="100%",
                loc="upper right",
                bbox_to_anchor=(0.41, 0, 0.8, 1),
                bbox_transform=ax.transAxes,
                borderpad=0,
            )

            ax_x.xaxis.set_tick_params(labelbottom=False)
            ax_y.yaxis.set_tick_params(labelleft=False)

            ax_x.contourf(
                xg.x["lon"],
                xg.z,
                xg[field_name][0].max(axis=1),
                cmap=cmap,
                levels=range(cmap_levels[0], cmap_levels[1] + 1),
            )
            x_diff = ax_x.get_xticks()[1] - ax_x.get_xticks()[0]
            ax_x.set_xlim(ax_x.get_xticks()[0] + x_diff / 2, ax_x.get_xlim()[1])

            ax_y.contourf(
                xg.z,
                xg.y["lat"],
                xg[field_name][0].max(axis=2).T,
                cmap=cmap,
                levels=range(cmap_levels[0], cmap_levels[1] + 1),
            )
            y_diff = ax_y.get_yticks()[1] - ax_y.get_yticks()[0]
            ax_y.set_ylim(ax_y.get_yticks()[0], ax_y.get_ylim()[1])

            ax_x.set_title(None)
            ax_y.set_title(None)
            ax_y.set_ylabel(None)
            ax_x.set_xlabel(None)
            ax_x.set_ylabel("Height AMSL (m)", size=10)
            ax_y.set_xlabel("Height AMSL (m)", size=10)

            # Add corner box
            left1, bottom1, width1, height1 = 0.721, 0.805, 0.118, 0.1228
            ax_cnr = plt.axes((left1, bottom1, width1, height1))
            plt.sca(ax_cnr)
            plt.tick_params(
                axis="both",
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
            )
            ax_cnr.yaxis.set_major_formatter(NullFormatter())
            ax_cnr.xaxis.set_major_formatter(NullFormatter())

            # Labels along the bottom edge are off
            plt.text(0.06, 0.8, "MAX-CAPPI", size=12, weight="bold")
            plt.text(0.02, 0.65, "Max Range:" + str(int(xg.x[-1]) / 1e3) + "km", size=8)
            plt.text(0.02, 0.5, "Max Height:" + str(int(xg.z[-1]) / 1e3) + "km", size=8)
            plt.text(
                0.15, 0.3, str(xg.time["time"].values[0])[11:19], weight="bold", size=12
            )
            plt.text(
                0.1,
                0.2,
                datetime.strptime(
                    str(xg.time["time"].values[0])[:10], "%Y-%m-%d"
                ).strftime("%d %B"),
                size=10,
                ha="left",
                va="center",
            )
            plt.text(
                0.2,
                0.08,
                datetime.strptime(
                    str(xg.time["time"].values[0])[:10], "%Y-%m-%d"
                ).strftime("%Y UTC"),
                size=10,
                ha="left",
                va="center",
            )

    # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=600, bbox_inches="tight")
    plt.show()


def elevation(
    radar,
    field_name="DBZ",
    elevation_index=0,
    rings=True,
    grid=True,
    range_in_km=True,
    save_image=False,
    img_name=None,
):
    """
    Plot radar data for the specified elevation.

    Parameters:
        radar: MOSDAC corrected Py-SRT Radar object based on pyart.core.Radar.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        elevation_index (int, optional): Index of the desired elevation. Default is 0.
        rings (bool, optional): If True, display range rings. Default is True.
        grid (bool, optional): If True, display gridlines. Default is True.
        range_in_km (bool, optional): If True, display range axis in kilometers. Default is True.
        save_image (bool, optional): If True, save the image as a PNG file. Default is False.
        img_name (str, optional): Name of the PNG file to save. Required if save_image is True.


        Example usage:
        pyiwr.visualize.elevation(radar, field_name='DBZ', elevation_index=0, rings=True, grid=True, range_in_km=True, save_image=True, img_name='ele_image.png')
    """
    fig, ax = plt.subplots()

    if range_in_km:
        rngs = radar.range["data"] / 1000.0
        xs0 = rngs[:, np.newaxis] * np.sin(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )
        ys0 = rngs[:, np.newaxis] * np.cos(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )

    else:
        rngs = radar.range["data"]
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

    # Define colormap based on the field_name
    colormaps = {
        "DBZ": "pyart_NWSRef",
        "VEL": "pyart_NWSVel",
        "WIDTH": "pyart_NWS_SPW",
        "PHIDP": "pyart_PD17",
        "RHOHV": "pyart_EWilson17",
        "ZDR": "pyart_RefDiff",
    }

    # Get the colormap for the field_name
    cmap = colormaps.get(field_name, "pyart_NWSRef")

    # Define levels for the color bar
    levels_dict = {
        "DBZ": [-20, 70],
        "VEL": [-30, 30],
        "WIDTH": [0, 10],
        "PHIDP": [0, 360],
        "RHOHV": [0.6, 1],
        "ZDR": [-10, 10],
    }
    levels = levels_dict.get(field_name, [-20, 70])

    # Plot radar data for the specified elevation
    plt.contourf(xs0, ys0, ele_data, levels=range(*levels), cmap=cmap)
    plt.colorbar(label=radar.fields[field_name]["units"])

    if range_in_km:
        plt.xlabel("Range (in km) of Radar (at Center) in Cartesian")
        plt.ylabel("Range (in km) of Radar (at Center) in Cartesian")

    else:
        plt.xlabel("Range (in m) of Radar (at Center) in Cartesian")
        plt.ylabel("Range (in m) of Radar (at Center) in Cartesian")

    k = radar.metadata["instrument_name"]
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
                ax.plot(
                    r * np.cos(t), r * np.sin(t), color="0.5"
                )  # Use '0.5' for medium grey color  # Plot the circle
                ax.text(x + 15, y + 15, f"{r}", ha="center", va="center", fontsize=10)
        else:
            t = np.linspace(0, 2 * np.pi)
            for r in [50000, 150000, 250000]:
                x = r * np.cos(np.radians(30))  # Calculate x-coordinate of the label
                y = r * np.sin(np.radians(30))  # Calculate y-coordinate of the label
                ax.plot(
                    r * np.cos(t), r * np.sin(t), color="0.5"
                )  # Use '0.5' for medium grey color  # Plot the circle
                ax.text(
                    x + 17000,
                    y + 17000,
                    f"{int(r/1000)}",
                    ha="center",
                    va="center",
                    fontsize=10,
                )

    # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=600, bbox_inches="tight")
    plt.show()


def all_elevation(
    radar,
    field_name="DBZ",
    rings=True,
    grid=True,
    range_in_km=True,
    save_image=False,
    img_name=None,
):
    """
    Plot radar data for all elevation angles.

    Parameters:
        radar: MOSDAC corrected Py-SRT Radar object based on pyart.core.Radar.
        field_name (str, optional): Name of the radar field to plot. Default is 'DBZ'.
        rings (bool, optional): If True, display range rings. Default is True.
        grid (bool, optional): If True, display gridlines. Default is True.
        range_in_km (bool, optional): If True, display range axis in kilometers. Default is True.
        save_image (bool, optional): If True, save the image as a PNG file. Default is False.
        img_name (str, optional): Name of the PNG file to save. Required if save_image is True.


        Example usage:
        pyiwr.visualize.all_elevation(radar, field_name='DBZ', rings=True, grid=True, range_in_km=True, save_image=True, img_name='all_ele_image.png')
    """
    fig = plt.figure(figsize=(20, 18))  # Increase figure size for better visibility
    k = radar.metadata["instrument_name"]
    title_str = f"{k} \nTime: {str(radar.time['units'])[14:]}, {radar.fields[field_name]['standard_name']} @ various elevation angles"

    # Title
    fig.suptitle(title_str, fontsize=16, y=1.0)

    if range_in_km:
        rngs = radar.range["data"] / 1000.0
        xs0 = rngs[:, np.newaxis] * np.sin(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )
        ys0 = rngs[:, np.newaxis] * np.cos(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )
    else:
        rngs = radar.range["data"]
        xs0 = rngs[:, np.newaxis] * np.sin(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )
        ys0 = rngs[:, np.newaxis] * np.cos(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )

    colormaps = {
        "DBZ": "pyart_NWSRef",
        "VEL": "pyart_NWSVel",
        "WIDTH": "pyart_NWS_SPW",
        "PHIDP": "pyart_PD17",
        "RHOHV": "pyart_EWilson17",
        "ZDR": "pyart_RefDiff",
    }

    # Define levels for the color bar
    levels_dict = {
        "DBZ": [-20, 70],
        "VEL": [-30, 30],
        "WIDTH": [0, 10],
        "PHIDP": [0, 360],
        "RHOHV": [0.6, 1],
        "ZDR": [-10, 10],
    }

    # Get the colormap for the field_name
    cmap = colormaps.get(field_name, "pyart_NWSRef")
    levels = levels_dict.get(field_name, [-20, 70])

    for i in range(radar.fixed_angle["data"].size):
        ax = fig.add_subplot(4, 3, i + 1)
        slice_indices = radar.get_slice(i)
        all_ele = radar.fields[field_name]["data"][slice_indices].T

        plt.contourf(xs0, ys0, all_ele, levels=range(*levels), cmap=cmap)
        plt.colorbar(label=field_name)
        plt.title("PPI @ Elevation angle = %.3f" % radar.fixed_angle["data"][i])

        if range_in_km:
            plt.xlabel("Range (in km) of Radar (at Center) in Cartesian")
            plt.ylabel("Range (in km) of Radar (at Center) in Cartesian")
        else:
            plt.xlabel("Range (in m) of Radar (at Center) in Cartesian")
            plt.ylabel("Range (in m) of Radar (at Center) in Cartesian")

        if grid:
            plt.grid()

        if rings:
            if range_in_km:
                t = np.linspace(0, 2 * np.pi)
                for r in [50, 150, 250]:
                    x = r * np.cos(
                        np.radians(30)
                    )  # Calculate x-coordinate of the label
                    y = r * np.sin(
                        np.radians(30)
                    )  # Calculate y-coordinate of the label
                    ax.plot(
                        r * np.cos(t), r * np.sin(t), color="0.5"
                    )  # Use '0.5' for medium grey color  # Plot the circle
                    ax.text(
                        x + 15, y + 15, f"{r}", ha="center", va="center", fontsize=10
                    )
            else:
                t = np.linspace(0, 2 * np.pi)
                for r in [50000, 150000, 250000]:
                    x = r * np.cos(
                        np.radians(30)
                    )  # Calculate x-coordinate of the label
                    y = r * np.sin(
                        np.radians(30)
                    )  # Calculate y-coordinate of the label
                    ax.plot(
                        r * np.cos(t), r * np.sin(t), color="0.5"
                    )  # Use '0.5' for medium grey color  # Plot the circle
                    ax.text(
                        x + 17000,
                        y + 17000,
                        f"{int(r/1000)}",
                        ha="center",
                        va="center",
                        fontsize=10,
                    )

    plt.subplots_adjust(
        top=0.95, hspace=0.3
    )  # Adjust top margin and horizontal spacing between subplots
    # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=600, bbox_inches="tight")
    plt.tight_layout()
    plt.show()


def fields_elevation(
    radar,
    elevation_index=0,
    range_in_km=True,
    rings=True,
    grid=True,
    save_image=False,
    img_name=None,
):
    """
    Plot multiple radar products at the specified elevation.

    Parameters:
        radar: MOSDAC corrected Py-SRT Radar object based on pyart.core.Radar.
        elevation_index (int, optional): Index of the desired elevation. Default is 0.
        range_in_km (bool, optional): If True, display range axis in kilometers. Default is True.
        rings (bool, optional): If True, display range rings. Default is True.
        grid (bool, optional): If True, display gridlines. Default is True.
        save_image (bool, optional): If True, save the image as a PNG file. Default is False.
        img_name (str, optional): Name of the PNG file to save. Required if save_image is True.



        Example usage:
        pyiwr.visualize.fields_elevation(radar, elevation_index=0, range_in_km=True, rings=True, grid=True, save_image=True, img_name='fields_ele_image.png')
    """

    fig = plt.figure(figsize=(20, 10))
    k = radar.metadata["instrument_name"]
    title_str = f"{k} \nTime: {str(radar.time['units'])[14:]}, PPI Products @ elevation {str(radar.fixed_angle['data'][elevation_index])}"

    fig.suptitle(title_str, fontsize=16, y=0.98)

    product_names = ["DBZ", "VEL", "WIDTH", "ZDR", "PHIDP", "RHOHV"]
    titles = [
        "Reflectivity",
        "Doppler Velocity",
        "Spectral Width",
        "Differential Reflectivity",
        "Differential Phase",
        "Correlation Coefficient",
    ]
    cmap_names = [
        "pyart_NWSRef",
        "pyart_NWSVel",
        "pyart_NWS_SPW",
        "pyart_RefDiff",
        "pyart_PD17",
        "pyart_EWilson17",
    ]
    levels = [[-20, 70], [-30, 30], [0, 10], [-10, 10], [0, 360], [0.6, 1]]

    if range_in_km:
        rngs = radar.range["data"] / 1000.0
        xs0 = rngs[:, np.newaxis] * np.sin(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )
        ys0 = rngs[:, np.newaxis] * np.cos(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )

    else:
        rngs = radar.range["data"]
        xs0 = rngs[:, np.newaxis] * np.sin(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )
        ys0 = rngs[:, np.newaxis] * np.cos(
            np.deg2rad(np.around(radar.azimuth["data"][0:360] * 100) / 100)
        )

    for i, product_name in enumerate(product_names):
        ax = fig.add_subplot(2, 3, i + 1)
        ele_data = radar.fields[product_name]["data"][
            radar.sweep_start_ray_index["data"][
                elevation_index
            ] : radar.sweep_end_ray_index["data"][elevation_index]
            + 1
        ].T

        # Get the colormap for the product
        cmap = cmap_names[i]

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
        plt.colorbar(label=product_name)
        plt.title(titles[i])
        if range_in_km:
            plt.xlabel("Range (in km) of Radar (at Center) in Cartesian")
            plt.ylabel("Range (in km) of Radar (at Center) in Cartesian")
        else:
            plt.xlabel("Range (in m) of Radar (at Center) in Cartesian")
            plt.ylabel("Range (in m) of Radar (at Center) in Cartesian")
        if grid:
            plt.grid()
        if rings:
            if range_in_km:
                t = np.linspace(0, 2 * np.pi)
                for r in [50, 150, 250]:
                    x = r * np.cos(
                        np.radians(30)
                    )  # Calculate x-coordinate of the label
                    y = r * np.sin(
                        np.radians(30)
                    )  # Calculate y-coordinate of the label
                    ax.plot(
                        r * np.cos(t), r * np.sin(t), color="0.5"
                    )  # Use '0.5' for medium grey color  # Plot the circle
                    ax.text(
                        x + 15, y + 15, f"{r}", ha="center", va="center", fontsize=10
                    )  # Display the radius at 30 degrees
            else:
                t = np.linspace(0, 2 * np.pi)
                for r in [50000, 150000, 250000]:
                    x = r * np.cos(
                        np.radians(30)
                    )  # Calculate x-coordinate of the label
                    y = r * np.sin(
                        np.radians(30)
                    )  # Calculate y-coordinate of the label
                    ax.plot(
                        r * np.cos(t), r * np.sin(t), color="0.5"
                    )  # Use '0.5' for medium grey color # Plot the circle
                    ax.text(
                        x + 17000,
                        y + 17000,
                        f"{int(r/1000)}",
                        ha="center",
                        va="center",
                        fontsize=10,
                    )  # Display the radius at 30 degrees

    plt.subplots_adjust(
        top=0.90, hspace=0.3
    )  # Adjust top margin and horizontal spacing between subplots
    # Save the image if save_image is True and file_name is provided
    if save_image:
        if img_name is None:
            raise ValueError(
                "Please provide the 'img_name' parameter to save the image."
            )

        # Save the image as a PNG file with 600 DPI
        plt.savefig(img_name, dpi=600, bbox_inches="tight")

    plt.tight_layout()
    plt.show()
