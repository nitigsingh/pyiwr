#!/usr/bin/env python

"""pyiwr is an advanced open-source library
developed by researchers at the SIGMA Research
Lab at IIT Indore. This powerful tool is
designed to effortlessly read, analyze, and 
visualize Indian Doppler Weather Radar (DWR) data.
pyiwr also provides a range of useful tools and visualization
functions to facilitate Radar Reflectivity correction, 
Radar QPE (Polarimetric), Radar Reflectivity 
Contour Frequency by Altitude Diagram 
and Time Series Analysis  working with and
analyzing weather radar data.

@author1: Nitig Singh
@author2: Vaibhav Tyagi
@author3: Hamid Ali Syed (special acknowledgement in his contribution for sweeps2mergednc function.

@email: nitig14rdfsma[at]gmail[dot]com
@email: vaibhavtyagi7191[at]gmail[dot]com
"""

import os
import tempfile
import datetime as dt
from netCDF4 import Dataset
import xarray as xr
import numpy as np
from pyart.config import get_metadata
import pyart
import pyart.map


from .utilities import (
    raw2object,
    fread,
    raw_product_list,
    raw_reshape_stack,
    update_xarray_dataset,
    extract_start_time,
    make_grid,
    sorting_key
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
        grid = make_grid(radar, grid_shape=grid_shape, height=height, length=length, fields=radar.fields.keys(), weighting_function="Barnes2", min_radius=length,)           

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

        pyart.io.write_grid(new_file_path, xg0)
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



def sweeps2mergednc(path_string,
                    start_index = 0,
                    end_index=None,
                    scan_type="B",
                    no_swps = None,
                    dualpol=False,
                    gridder=False,
                    grid_shape=(30, 500, 500), 
                    height=15, 
                    length=250,
                    save_file=False,
                    ):
    
    
    """
    The function sweeps2mergednc is used to merge multiple sweeps file for Indian radars and aggregating them to a 
    single cfradial1 file format, there is also a provision for saving the file either in cfradial or gridded format.
    
    Parameters:

    input_dir(str): Enter path of single sweep data directory,
    start_index: Enter the starting index of first file,
    end_index: Enter the ending index of first file,
    scan_type(str): "B", "C". B is for short range PPI,
                    & C is for long range PPI.
    no_swps(int): for short scan file it is usually 10/11 and for long scan it is 2/3, default is None,
                  so it will choose 10 scan files for short scan 2 for long scan.
    dualpol(bool): True, False. (If the data contains
                   dual-pol products e.g., ZDR, RHOHV and KDP),
    gridder(bool): True, False, 
    grid_shape: the grid shape example, (30, 500, 500), 
    height: maximum height in km example 15, 
    length: maximum scan distance radially from radar example 250,
    save_file: option to save the file made after merging optional and by default it is False,
    
    Example Usage:
    
    radar = sweeps2mergednc(directory[4], start_index = 0, end_index=None, scan_type="B", no_swps = None, dualpol=False,
                gridder=True, grid_shape=(31, 501, 501), save_file=False,
                )
    """
       
    # List of file names with the .nc extension
    folder_path = glob.glob(os.path.join(path_string, "*nc*"))
    startt = dt.datetime.now()
    if end_index is None:
        end_index = len(folder_path) - 1
    files = folder_path[start_index:end_index+1]

    files = sorted(files, key=sorting_key)
   
    print("Number of total sweep files: ", len(files))
    bb = list()
    if scan_type == "B":
        if no_swps is None:
            no_swps = 10
        for i in range(0, len(files), no_swps):
            bb.append(files[i : i + no_swps])
    elif scan_type == "C":
        if no_swps is None:
            no_swps = 2
        for i in range(0, len(files), no_swps):
            bb.append(files[i : i + no_swps])
    print(f"Total no. of output files: {len(bb)}.")
    print("Merging all scans into one Volume")
              
    for i in range(0, len(bb)):
        en = []
        a1 = []
        t1 = []
        e1 = []
        Z1 = []
        T1 = []
        V1 = []
        W1 = []
        ZDR1 = []
        KDP1 = []
        PHIDP1 = []
        SQI1 = []
        RHOHV1 = []
        HCLASS1 = []
        nyquist = []
        unambigrange = []
        for j in range(0, no_swps):
            ds = Dataset(bb[i][j])
            az = ds.variables["radialAzim"][:]
            time = ds.variables["radialTime"][:]
            ele = ds.variables["radialElev"][:]
            Z = ds.variables["Z"][:]
            # T = ds.variables['T'][:]
            V = ds.variables["V"][:]
            W = ds.variables["W"][:]
            EN = ds.variables["elevationNumber"][:]
            a1.extend(az)
            t1.extend(time)
            e1.extend(ele)
            Z1.extend(Z)
            # T1.extend(T)
            V1.extend(V)
            W1.extend(W)
            en.append(EN)
            nyquist.append(ds.variables["nyquist"][:])
            unambigrange.append(ds.variables["unambigRange"][:])
            if dualpol:
                if "ZDR" in ds.variables:
                    ZDR = ds.variables["ZDR"][:]
                    ZDR1.extend(ZDR)

                if "PHIDP" in ds.variables:
                    PHIDP = ds.variables["PHIDP"][:]
                    PHIDP1.extend(PHIDP)

                if "KDP" in ds.variables:
                    KDP = ds.variables["KDP"][:]
                    KDP1.extend(KDP)

                if "SQI" in ds.variables:
                    SQI = ds.variables["SQI"][:]
                    SQI1.extend(SQI)

                if "RHOHV" in ds.variables:
                    RHOHV = ds.variables["RHOHV"][:]
                    RHOHV1.extend(RHOHV)

                if "HCLASS" in ds.variables:
                    HCLASS = ds.variables["HCLASS"][:]
                    HCLASS1.extend(HCLASS)


        fname = os.path.basename(bb[i][0]).split(".nc")[0]

        radar = pyart.testing.make_empty_ppi_radar(
            ds.dimensions["bin"].size, ds.dimensions["radial"].size * no_swps, 1
        )
        radar.nsweeps = no_swps
        radar.time["data"] = np.array(t1)
        # 'seconds since 1970-01-01T00:00:00Z'
        radar.time["units"] = ds.variables["radialTime"].units
        radar.latitude["data"] = np.array([ds.variables["siteLat"][:]])
        radar.longitude["data"] = np.array([ds.variables["siteLon"][:]])
        radar.altitude["data"] = np.array([ds.variables["siteAlt"][:]])
        radar.range["data"] = np.arange(
            0,
            ds.dimensions["bin"].size * ds.variables["gateSize"][:].data,
            int(ds.variables["gateSize"][:].data),
        )

        radar.fixed_angle["data"] = ds.variables["elevationList"]

        radar.sweep_number["data"] = np.array(en)

        radar.sweep_start_ray_index["data"] = np.arange(
            0, ds.dimensions["radial"].size * no_swps, ds.dimensions["radial"].size
        )

        radar.sweep_end_ray_index["data"] = np.arange(
            ds.dimensions["radial"].size - 1,
            ds.dimensions["radial"].size * no_swps,
            ds.dimensions["radial"].size,
        )

        radar.azimuth["data"] = np.ma.array(a1)
        radar.elevation["data"] = np.ma.array(e1)
        radar.metadata["instrument_name"] = fname[:3]
        radar.init_gate_altitude()
        radar.init_gate_longitude_latitude()
        ref_dict = get_metadata("reflectivity")
        ref_dict["data"] = np.ma.array(Z1)
        ref_dict["units"] = "dBZ"
        VEL_dict = get_metadata("velocity")
        VEL_dict["data"] = np.ma.array(V1)
        VEL_dict["units"] = "m/s"
        W_dict = get_metadata("spectrum_width")
        W_dict["data"] = np.ma.array(W1)
        W_dict["units"] = "m/s"
        radar.instrument_parameters = {}
        radar.instrument_parameters["nyquist_velocity"] = {
            "units": "m/s",
            "comments": "Unambiguous velocity",
            "meta_group": "instrument_parameters",
            "long_name": "Nyquist velocity",
        }
        radar.instrument_parameters["nyquist_velocity"]["data"] = np.ma.array(nyquist)
        radar.instrument_parameters["unambiguous_range"] = {
            "units": "meters",
            "comments": "Unambiguous range",
            "meta_group": "instrument_parameters",
            "long_name": "Unambiguous range",
        }
        radar.instrument_parameters["unambiguous_range"]["data"] = np.ma.array(
            unambigrange
        )

        radar.fields = {"REF": ref_dict, "VEL": VEL_dict, "WIDTH": W_dict}

        if dualpol:
            ZDR_dict = get_metadata("differential_reflectivity")
            ZDR_dict["units"] = "dB"
            if "ZDR" in ds.variables:
                ZDR_dict["data"] = np.ma.array(ZDR1)
                radar.fields["ZDR"] = ZDR_dict
            
            PHIDP_dict = get_metadata("differential_phase")
            PHIDP_dict["units"] = "degrees"
            if "PHIDP" in ds.variables:
                PHIDP_dict["data"] = np.ma.array(PHIDP1)
                radar.fields["PHIDP"] = PHIDP_dict
            

            KDP_dict = get_metadata("specific_differential_phase")
            KDP_dict["units"] = "degrees/km"
            if "KDP" in ds.variables:
                KDP_dict["data"] = np.ma.array(KDP1)
                radar.fields["KDP"] = KDP_dict


            RHOHV_dict = get_metadata("cross_correlation_ratio")
            RHOHV_dict["units"] = "unitless"
            if "RHOHV" in ds.variables:
                RHOHV_dict["data"] = np.ma.array(RHOHV1)
                radar.fields["RHOHV"] = RHOHV_dict 
            

            SQI_dict = get_metadata("normalized_coherent_power")
            SQI_dict["units"] = "unitless"
            if "SQI" in ds.variables:
                SQI_dict["data"] = np.ma.array(SQI1)
                radar.fields["SQI"] = SQI_dict
            

            HCLASS_dict = get_metadata("radar_echo_classification")
            HCLASS_dict["units"] = "unitless"
            if "HCLASS" in ds.variables:
                HCLASS_dict["data"] = np.ma.array(HCLASS1)
                radar.fields["HCLASS"] = HCLASS_dict

              
        # Save the updated dataset to a new netCDF file if specified
        if save_file:
            # Create the "corrected" subdirectory if it doesn't exist
            merged_dir = os.path.join(os.path.dirname(path_string), "merged")
            os.makedirs(merged_dir, exist_ok=True)

            # Specify the new file path
            new_file_name = f"merged_cfrad_{fname}.nc"
            new_file_path = os.path.join(merged_dir, new_file_name)
            pyart.io.write_cfradial(new_file_path, radar, format="NETCDF4")
              
            if gridder:
                grid = make_grid(radar, grid_shape=grid_shape, height=height, length=length)           
                new_file_name = f"merged_grid_{fname}.nc"
                new_file_path = os.path.join(merged_dir, new_file_name)
                pyart.io.write_grid(new_file_path, grid)
                del radar, grid
            else:
                pass
        else:
            if gridder:
                grid = make_grid(radar, grid_shape=grid_shape, height=height, length=length)           
                return grid.to_xarray()
            else:
                return radar
    print("Data merging done \nTotal Time Elapsed: ", dt.datetime.now() - startt) 
