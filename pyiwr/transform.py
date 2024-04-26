#!/usr/bin/env python

"""pyiwr is an advanced open-source library
developed by researchers at the SIGMA Research
Lab at IIT Indore. This powerful tool is
designed to effortlessly convert raw ISRO
Doppler Weather Radar (DWR) data files and
Restructure and format correct the DWR NetCDF files.
pyiwr is capable of merging multiple sweep files into a single volumetric CFradial file,
with facility of saving the files into gridded or CFradial format data after format correction.
pyiwr also provides a range of useful tools and visualization
functions to facilitate working with and
analyzing weather radar data.

@author1: Nitig Singh
@author2: Vaibhav Tyagi

@email: nitig14rdfsma[at]gmail[dot]com
@email: vaibhavtyagi7191[at]gmail[dot]com
"""

import os
import tempfile

import pyart
import pyart.map
import xarray as xr

from .utilities import (
    raw2object,
    read,
    raw_product_list,
    raw_reshape_stack,
    update_xarray_dataset,
)

# "raw2nc" function takes in any raw dual-pol .dwr file and restructures it into a radar object to be visualized by pyiwr and also makes it compatible with Py-ART
# The user is provided with the advantage of choosing whether to save the file


# "raw2nc" function takes in any raw dual-pol .dwr file and restructures it into a radar object to be visualized by pyiwr
# The user is provided with the advantage of choosing whether to save the file


def raw2nc(dwr_path, save_file=False):
    """
    `raw2nc` function takes in any raw dual-pol .dwr file
    restructures it into a radar object to be visualized by pyiwr
    The user is provided with the advantage of choosing whether to save the file in netCDF format
    """

    if dwr_path[-3:] == "dwr":
        dat = raw_product_list(dwr_path)
        radar = raw2object(dwr_path, dat)

        # Save the radar object to a NetCDF file if specified
        if save_file:
            # Create the "radar_ncfiles" subdirectory if it doesn't exist
            nc_directory = os.path.join(os.path.dirname(dwr_path), "radar_ncfiles")
            os.makedirs(nc_directory, exist_ok=True)

            # Specify the new file path
            filepath = os.path.basename(dwr_path)
            new_file_name = (
                f"new_{filepath[:-4]}.nc"  # Remove the last 4 characters (.dwr)
            )
            new_file_path = os.path.join(nc_directory, new_file_name)
            print(
                "File",
                os.path.basename(dwr_path),
                'converted successfully and saved in the "radar_ncfiles" folder',
            )
            pyart.io.write_cfradial(new_file_path, radar, format="NETCDF4")
            return pyart.io.read_cfradial(new_file_path)

        else:
            # Save the radar object to a temporary in-memory file
            with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp_file:
                pyart.io.write_cfradial(tmp_file.name, radar, format="NETCDF4")

            # Read the data from the in-memory file and return the Py-ART radar object
            radar = pyart.io.read_cfradial(tmp_file.name)

            # Delete the temporary in-memory file
            os.remove(tmp_file.name)
            print("File", os.path.basename(dwr_path), "converted into radar object successfully")
            return radar

    else:
        read = pyart.io.read(dwr_path)
        return read


# "format_correctednc" function takes in any DWR NetCDF file and restructures it into a radar object to be visualized by pyiwr and also format correct the radar files and removes all the errors
# The user is provided with the advantage of choosing whether to save the file


def format_correctednc(file_path, save_file=False):
    """
    "format_correctednc" function takes in any DWR NetCDF file and restructures it into a radar object to be visualized by pyiwr 
    and also format correct the radar files and removes all the errors
    The user is provided with the advantage of choosing whether to save the file.
    Returns all corrected radar objects from any Cf/Radial object file.
    corrects all date and Time issues.
    resolves missing sweep ray index and updates metadata
    """

    # Open the dataset
    print("Processing file: ", os.path.basename(file_path))
    raw = xr.open_dataset(file_path, decode_times=False)
    raw = update_xarray_dataset(file_path, raw, xg=raw)
    radar_pol = raw
    # Save the corrected xarray.Dataset to a temporary in-memory file
    with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp_file:
        radar_pol.to_netcdf(tmp_file.name)

    # Read the data from the in-memory file and return the Py-ART radar object
    radar = pyart.io.read_cfradial(tmp_file.name)

    # Save the updated dataset to a new netCDF file if specified
    if save_file:
        # Create the "corrected" subdirectory if it doesn't exist
        corrected_dir = os.path.join(os.path.dirname(file_path), "corrected")
        os.makedirs(corrected_dir, exist_ok=True)

        # Specify the new file path
        new_file_name = f"corrected_{os.path.basename(file_path)}"
        new_file_path = os.path.join(corrected_dir, new_file_name)

        radar_pol.to_netcdf(new_file_path)
        print(
            "File",
            os.path.basename(file_path),
            'format corrected and restructured successfully and saved in the newly added "corrected" folder in your file path',
        )
        return pyart.io.read_cfradial(new_file_path)
    else:
        # Save the corrected xarray.Dataset to a temporary in-memory file
        with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp_file:
            radar_pol.to_netcdf(tmp_file.name)

        # Read the data from the in-memory file and return the Py-ART radar object
        radar = pyart.io.read_cfradial(tmp_file.name)

        # Delete the temporary in-memory file
        os.remove(tmp_file.name)
        print(
            "File",
            os.path.basename(file_path),
            "format corrected and restructured successfully",
        )
        return radar


# "sweeps2gridnc" function makes a cartesian grid object from a cfradial NetCDF
# file using Py-ART, which is then saved as a gridded Xarray object.
# The function takes in parameters like filename, grid shape (altitude levels, x-axis grids, and y-axis grids),
# and height in km to be considered for making grid levels for altitude and length of radar range with an option of saving this gridded data into NetCDF file format.


def sweeps2gridnc(
    file_path, grid_shape=(31, 501, 501), height=15, length=250, save_file=False
):
    """
    The function takes in parameters like filename, grid shape (altitude levels, x-axis grids, and y-axis grids),
    height in km to be considered for making grid levels for altitude and length of radar range with an option of saving this gridded data into NetCDF file format.
    Returns grid object from radar object.
    "sweeps2gridnc" function makes a cartesian grid object from a cfradial NetCDF file using Py-ART, which is then saved as a gridded Xarray object.


    grid_shape=(61, 500, 500), no. of bins of z,y,x respectively.

    height:(int) = 15, height in km
    length:(int) = 250, Range of radar in km

    0.5 km vertical resolution
    1 km resolution horizontally
    radar installed at 1.313 km height
    """

    print("Processing file: ", os.path.basename(file_path))
    # for files which are already gridded and needed to be just read
    if "gridded" in os.path.basename(file_path):
        xg0 = xr.open_dataset(file_path)
    else:  # for gridding the CF/radial format
        raw = xr.open_dataset(file_path, decode_times=False, engine="netcdf4")
        raw = update_xarray_dataset(file_path, raw, xg=raw)
        # Decode the CF conventions of the dataset
        radar_pol = xr.decode_cf(raw)
        # Save the corrected xarray.Dataset to a temporary in-memory file
        with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp_file:
            radar_pol.to_netcdf(tmp_file.name)

        # Read the data from the in-memory file and return the Py-ART radar object
        radar = pyart.io.read_cfradial(tmp_file.name)
        # Read the data from the in-memory file and return the Py-ART radar object
        grid = pyart.map.grid_from_radars(
            radar,
            grid_shape=grid_shape,
            grid_limits=(
                (0, height * 1e3),
                (-length * 1e3, length * 1e3),
                (-length * 1e3, length * 1e3),
            ),
            fields=radar.fields.keys(),
            weighting_function="Barnes2",
            min_radius=length,
        )
        xg = grid.to_xarray()
        xg0 = update_xarray_dataset(file_path, raw, xg)

        # Remove variables 'sweep_start_ray_index', 'sweep_end_ray_index' and 'time_coverage_start'
        xg0 = xg0.drop_vars(
            ["sweep_start_ray_index", "sweep_end_ray_index", "time_coverage_start"]
        )

        # Remove attributes 'time_coverage_start' and 'units' from the 'time' variable
        if "time_coverage_start" in xg0.attrs:
            del xg0.attrs["time_coverage_start"]

        if "units" in xg0["time"].attrs:
            del xg0["time"].attrs["units"]

    if save_file and "gridded" not in os.path.basename(file_path):
        # Create the "updated" subdirectory if it doesn't exist
        updated_dir = os.path.join(os.path.dirname(file_path), "gridded_radar_ncfiles")
        os.makedirs(updated_dir, exist_ok=True)

        # Specify the new file path
        filepath = os.path.basename(file_path)
        new_file_name = (
            f"gridded_{filepath[:-4]}.nc"  # Remove the last 4 characters (.dwr)
        )
        new_file_path = os.path.join(updated_dir, new_file_name)

        xg0.to_netcdf(new_file_path)
        print(
            "Xarray gridding of volumetric sweeps of radar PPI scan file:",
            os.path.basename(file_path),
            "done successfully and saved in",
            new_file_name,
            'in the newly added "gridded_radar_ncfiles" folder in your file path',
        )
        return xg0
    else:
        print(
            "Xarray gridding of volumetric sweeps of radar PPI scan file:",
            os.path.basename(file_path),
            "done successfully",
        )
        return xg0
