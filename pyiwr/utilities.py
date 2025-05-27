#!/usr/bin/env python
"""
@author1: Nitig Singh
@author2: Vaibhav Tyagi

@email: nitig14rdfsma[at]gmail[dot]com
@email: vaibhavtyagi7191[at]gmail[dot]com

@reference for 'fread' and 'raw_product_list' data reading function: Shahla KP/Sci-Eng -SC/RDA-ISTRAC ISRO
@reference for 'sorting_key' and 'make_grid' file, sorting and data gridding function respectively: Hamid Ali Syed

"""

import datetime as dt
import os
import re
import glob
from pyproj import CRS, Transformer

import numpy as np
import wradlib as wrl
from wradlib.classify import classify_echo_fuzzy
import pyart
import pyart.map
import xarray as xr



def fread(fid, nelements, dtype):
    if dtype is np.str_:
        dt = np.uint8
    else:
        dt = dtype

    data_array = np.fromfile(fid, dt, nelements)
    data_array.shape = (nelements, 1)
    return data_array


def raw_product_list(dwr_path):
    with open(dwr_path, "rb") as fid:
        print("Processing file:", os.path.basename(dwr_path))
        m5 = np.fromfile(fid, dtype="uint8")
        m5 = m5.astype(float)

        fid.seek(0, 0)
        mode = fread(fid, 1, np.uint16)
        mode[0, 0]

        fid.seek(2, 0)
        s1 = np.fromfile(fid, dtype=np.uint8, count=20, sep="")
        st = str(s1.tobytes())
        Station = (st.split(sep="\\x")[0]).split(sep="'")[1]

        fid.seek(32, 0)
        s2 = np.fromfile(fid, dtype=np.uint8, count=10, sep="")
        rd = str(s2.tobytes())
        Radar = (rd.split(sep="\\x")[0]).split(sep="'")[1]

        St_Year = hex((m5[42:44:2] + 256 * m5[43])[0].astype(int)).split(sep="x")[1]
        St_Month = hex((m5[44]).astype(int)).split(sep="x")[1]
        St_Day = hex((m5[45]).astype(int)).split(sep="x")[1]
        St_Hour = hex((m5[46]).astype(int)).split(sep="x")[1]
        St_Minute = hex((m5[47]).astype(int)).split(sep="x")[1]
        St_Sec = hex((m5[48]).astype(int)).split(sep="x")[1]

        Start_Time = (
            St_Year
            + "-"
            + St_Month.zfill(2)
            + "-"
            + St_Day.zfill(2)
            + " , "
            + St_Hour.zfill(2)
            + ":"
            + St_Minute.zfill(2)
            + ":"
            + St_Sec.zfill(2)
        )
        date = Start_Time[0:-10]
        time = Start_Time[12:]

        PRFH = m5[573:632:2] + 256 * m5[574:633:2]
        PRFL = m5[633:692:2] + 256 * m5[634:693:2]
        (m5[693:752:2] + 256 * m5[694:753:2]) / 100

        fid.seek(26, 0)
        lat_temp = fread(fid, 1, np.uint32)
        lat = lat_temp[0, 0] / 10000

        fid.seek(22, 0)
        lon_temp = fread(fid, 1, np.uint32)
        lon = lon_temp[0, 0] / 10000

        fid.seek(30, 0)
        h = fread(fid, 1, np.uint16)
        h = h[0, 0]

        fid.seek(394, 0)
        mod = fread(fid, 1, np.uint32)
        freq = mod[0, 0] * 1000

        elev_ang1 = (m5[408:467:2] + 256 * m5[409:468:2]) / 10
        elevation = np.unique(elev_ang1)
        num_el = len(elevation)

        rang_res = m5[754:813:2] + 256 * m5[755:814:2]
        rang_res[0]
        no_bin_ele = m5[12038:12217:2] + 256 * m5[12039:12218:2]
        no_bin = no_bin_ele[0].astype(int)
        azval = np.arange(0, 361, 1).astype(int)

        Z1t = np.full((no_bin, len(azval), len(elevation)), np.nan)
        V1t = np.full((no_bin, len(azval), len(elevation)), np.nan)
        SW1t = np.full((no_bin, len(azval), len(elevation)), np.nan)
        ZDR1t = np.full((no_bin, len(azval), len(elevation)), np.nan)
        PHIDP1t = np.full((no_bin, len(azval), len(elevation)), np.nan)
        RDP1t = np.full((no_bin, len(azval), len(elevation)), np.nan)

        m6 = m5[12513:]

        s2 = int(((no_bin_ele[0] * 7 + 4) * 360) * 1)
        m7 = m6[0:s2]
        for i in range(len(elevation)):
            fn1 = i + 1
            if fn1 == 1:
                m7 = m6[0:s2]  # 1st elevation data
            else:
                m7 = m6[s2 * (fn1 - 1) : s2 * fn1]  # 2nd elevation data

            m8 = np.reshape(m7, (int(no_bin_ele[0]) * 7 + 4, 360 * 1), order="F")

            m9 = m8[:][4:]
            z = m9[0::7][:]
            z = (z - 1) / 2 - 31.5
            z1 = np.copy(z)

            zf = z1[:, 359]
            zf = np.reshape(zf, (len(zf), 1), order="F")
            Z1 = np.hstack((z1, zf))

            prf = m5[573:582:2] + 256 * m5[574:583:2]
            prfl = m5[633:692:2] + 256 * m5[634:693:2]
            lamd = (3e8) / freq

            if prfl[0] == 0:
                v = m9[1::7][:]
                v = np.where((v == 0), np.nan, v)
                v = ((v - 128) / 128) * (lamd * prf[0] / (4))
            else:
                prt_dul = (1 / prfl[0]) - (1 / prf[0])
                v = m9[1::7][:]
                v = np.where((v == 0), np.nan, v)
                v = ((v - 128) / 128) * (lamd / (prt_dul * 4))

            v1 = np.copy(v)
            vf = v1[:, 359]
            vf = np.reshape(vf, (len(vf), 1), order="F")
            V1 = np.hstack((v1, vf))

            sw = m9[2::7][:]
            sw = sw / 10
            sw[sw < -0] = -0
            sw[sw > 16] = 16
            sw1 = np.copy(sw)
            swf = sw1[:, 359]
            swf = np.reshape(swf, (len(swf), 1), order="F")
            SW1 = np.hstack((sw1, swf))

            zdr = m9[3::7][:]
            zdr = zdr / 20 - 4
            zdr1 = np.copy(zdr)
            zdrf = zdr1[:, 359]
            zdrf = np.reshape(zdrf, (len(zdrf), 1), order="F")
            ZDR1 = np.hstack((zdr1, zdrf))

            phidp = m9[4::7][:] + 256 * m9[5::7][:]
            phidp = phidp * 0.088
            phidp1 = phidp - 180
            phidpf = phidp1[:, 359]
            phidpf = np.reshape(phidpf, (len(phidpf), 1), order="F")
            PHIDP1 = np.hstack((phidp1, phidpf))

            rdp = m9[6::7][:]
            rdp = rdp / 256
            rdp1 = np.copy(rdp)
            rdpf = rdp1[:, 359]
            rdpf = np.reshape(rdpf, (len(rdpf), 1), order="F")
            RDP1 = np.hstack((rdp1, rdpf))

            Z1t[:, :, i] = np.copy(Z1)
            V1t[:, :, i] = np.copy(V1)
            SW1t[:, :, i] = np.copy(SW1)
            ZDR1t[:, :, i] = np.copy(ZDR1)
            PHIDP1t[:, :, i] = np.copy(PHIDP1)
            RDP1t[:, :, i] = np.copy(RDP1)

        Z1t[Z1t == -32] = np.nan  # no data points
        SW1t[SW1t == 0] = np.nan
        ZDR1t[ZDR1t == -4] = np.nan
        PHIDP1t[PHIDP1t <= -180] = np.nan
        RDP1t[RDP1t == 0] = np.nan
        V1t[V1t == -1] = np.nan

    return [
        Station,
        date,
        time,
        Radar,
        lon,
        lat,
        h,
        freq,
        elev_ang1,
        num_el,
        no_bin,
        rang_res[0],
        PRFH,
        PRFL,
        Z1t,
        V1t,
        SW1t,
        ZDR1t,
        PHIDP1t,
        RDP1t,
    ]


def raw_reshape_stack(radar_products, num_sweeps):
    """
    Raw reshaping the data in the input array `radar_products` vertically `sweeps` times
    and stack them to create a new two dimensional array with the final shape(sweeps * rays, gates).

    Parameters:
    - radar_products (ndarray): Input array with shape (sweeps, rays, gates).
    - num_sweeps (int): Number of times to vertically repeat the data.

    Returns:
    - ndarray: Resulting array with shape (sweeps * rays, gates).
    """

    # Get the shape of the input array
    rows, cols = radar_products.shape[1:]

    # Calculate the final shape of the resulting array
    final_shape = (num_sweeps * rows, cols)

    # Initialize an empty array to store the result
    result = np.empty((0, final_shape[1]), dtype=radar_products.dtype)

    # Iterate through ref and append slices
    for i in range(num_sweeps):
        slice_data = radar_products[i, :, :]
        result = np.vstack((result, slice_data))

    return result


def raw2object(dwr_path, dats):
    radar = pyart.testing.make_empty_ppi_radar(dats[10], 360, dats[9])

    # Add the condition to determine the 'source' attribute
    Station = dats[0]
    if Station == "CHERRAPUNJEE":
        if os.path.basename(dwr_path)[-6:] == "6n.dwr":
            data = np.array(
                np.linspace(0.0555555556, 399.944444444, 3600), dtype=np.float64
            )
        else:
            data = np.array(
                np.linspace(0.0555555556, 79.944444444, 720), dtype=np.float64
            )
    elif Station == "SHAR":
        if os.path.basename(dwr_path)[-6:] == "6n.dwr":
            data = np.array(
                np.linspace(0.0555555556, 399.944444444, 3600), dtype=np.float64
            )
        else:
            data = np.array(
                np.linspace(0.0555555556, 79.944444444, 720), dtype=np.float64
            )
    else:
        if os.path.basename(dwr_path)[-6:] == "6n.dwr":
            data = np.array(
                np.linspace(0.0555555556, 399.944444444, 3600), dtype=np.float64
            )
        else:
            data = np.array(
                np.linspace(0.0555555556, 79.944444444, 720), dtype=np.float64
            )

    tstart = dats[1][:-1] + "T" + dats[2][1:] + "Z"

    radar.time = {
        "data": data.astype(np.float64),
        "standard_name": "time",
        "long_name": "time_in_seconds_since_volume_start",
        "units": "seconds since " + tstart,
        "calendar": "gregorian",
    }

    radar.latitude["data"] = np.array([dats[5]])
    radar.longitude["data"] = np.array([dats[4]])
    radar.range["data"] = np.linspace(75.0, dats[11] * (dats[10] - 1), dats[10])
    radar.fixed_angle["data"] = np.array(dats[8][: dats[9]], dtype=np.float32).flatten()
    radar.sweep_number["data"] = np.array(range(dats[9]))

    radar.sweep_start_ray_index["data"] = np.arange(
        0, radar.nrays, radar.nrays / dats[9], dtype="int64"
    )
    radar.sweep_end_ray_index["data"] = radar.sweep_start_ray_index["data"] + int(
        (radar.nrays / dats[9]) - 1
    )
    radar.init_gate_longitude_latitude()
    radar.init_gate_altitude()
    radar.init_gate_x_y_z()

    radar.altitude["data"] = np.array(dats[6], dtype=np.int32).flatten()
    radar.azimuth["data"] = np.tile(
        np.arange(radar.nrays / dats[9], dtype=np.float32), dats[9]
    )

    # Add the condition to determine the 'source' attribute
    if os.path.basename(dwr_path)[-6:] == "6n.dwr":
        a = "DWR Short Volume Scan File (250km)"
    else:
        a = "DWR Long Volume Scan File (500km)"

    # Add the condition to determine the 'source' attribute
    if os.path.basename(dwr_path)[-6:] == "6n.dwr":
        radar.sweep_mode["data"] = np.array(
            [
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
            ],
            dtype="|S1",
        )
    else:
        radar.sweep_mode["data"] = np.array(
            [
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
                [
                    b"a",
                    b"z",
                    b"i",
                    b"m",
                    b"u",
                    b"t",
                    b"h",
                    b" ",
                    b"s",
                    b"u",
                    b"r",
                    b"v",
                    b"e",
                    b"i",
                    b"l",
                    b"l",
                    b"a",
                    b"n",
                    b"c",
                    b"e",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                    b"",
                ],
            ],
            dtype="|S1",
        )

    # Add the condition to determine the 'source' attribute
    if Station == "CHERRAPUNJEE":
        b = "Cherrapunji S-band Dual-pol DWR"
    elif Station == "SHAR":
        b = "SHAR S-band Dual-pol DWR"
    elif Station == "TERLS":
        a = "TERLS C-band Dual-pol DWR"
    else:
        b = "DWR"

    # radar.elevation["data"] = np.array(np.repeat(dats[8][:10], 360))
    # radar.metadata = {
    #     "instrument_name": "TEST (b earlier)",   
    #     "Created using": "pyiwr (Indian Weather Radar Toolkit) Module developed at SIGMA Research Lab, IIT Indore",
    #     "version": "Version 1.0.1",
    #     "institution": "Indian: ISRO/IMD/IITM",
    #     "references": "Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html",
    #     "history": f"DWR raw ({os.path.basename(dwr_path)[-6:]}) data file encoded into standard radar object NetCDF file",
    #     "comment": "",
    #     "platform_type": "fixed",
    #     "instrument_type": "radar",
    #     "primary_axis": "axis_z",
    # }

    radar.elevation["data"] = np.array(np.repeat(dats[8][:10], 360))
    radar.metadata = {
        "instrument_name": b,   
        "Created using": "pyiwr (Indian Weather Radar Toolkit) Module developed at SIGMA Research Lab, IIT Indore",
        "version": "Version 1.0.1",
        "title": b[:-3] + "DWR data",
        "institution": "Indian: ISRO/IMD/IITM",
        "references": "Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html",
        "source": a,  # 'a' determines the 'source' attribute based on the condition
        "history": f"DWR raw ({os.path.basename(dwr_path)[-6:]}) data file encoded into standard radar object NetCDF file",
        "comment": "",
        "platform_type": "fixed",
        "instrument_type": "radar",
        "primary_axis": "axis_z",
    }

    ref = np.array(dats[14][:, :360, :].T)
    ref = raw_reshape_stack(ref, dats[9])
    fill_value = ref[0, 0]

    vel = np.array(dats[15][:, :360, :].T)
    fill_value = ref[0, 0]
    vel = raw_reshape_stack(vel, dats[9])

    sw = np.array(dats[16][:, :360, :].T)
    fill_value = ref[0, 0]
    sw = raw_reshape_stack(sw, dats[9])

    zdr = np.array(dats[17][:, :360, :].T)
    fill_value = ref[0, 0]
    zdr = raw_reshape_stack(zdr, dats[9])

    phidp = np.array(dats[18][:, :360, :].T)
    fill_value = ref[0, 0]
    phidp = raw_reshape_stack(phidp, dats[9])

    rdp = np.array(dats[19][:, :360, :].T)
    fill_value = ref[0, 0]
    rdp = raw_reshape_stack(rdp, dats[9])

    radar.fields["DBZ"] = {
        "data": ref.astype(np.float32),
        "units": "dBZ",
        "standard_name": "equivalent_reflectivity_factor",
        "Polarization": "Horizontal",
        "_FillValue": fill_value,
    }

    radar.fields["VEL"] = {
        "data": vel.astype(np.float32),
        "units": "m/s",
        "standard_name": "radial_velocity_of_scatterers_away_from_instrument",
        "Polarization": "Horizontal",
        "_FillValue": fill_value,
    }

    radar.fields["WIDTH"] = {
        "data": sw.astype(np.float32),
        "units": "m/s",
        "standard_name": "doppler_spectrum_width",
        "Polarization": "Horizontal",
        "_FillValue": fill_value,
    }

    radar.fields["ZDR"] = {
        "data": zdr.astype(np.float32),
        "units": "dB",
        "standard_name": "log_differential_reflectivity_hv",
        "Polarization": "Horizontal and Vertical",
        "_FillValue": fill_value,
    }

    radar.fields["PHIDP"] = {
        "data": phidp.astype(np.float32),
        "units": "degrees",
        "standard_name": "differential_phase_hv",
        "Polarization": "Horizontal and Vertical",
        "_FillValue": fill_value,
    }

    radar.fields["RHOHV"] = {
        "data": rdp.astype(np.float32),
        "units": "unitless",
        "standard_name": "cross_correlation_ratio_hv",
        "Polarization": "Horizontal and Vertical",
        "_FillValue": fill_value,
    }

    return radar

# for files that are read from mosdac or if manually corrected/restructured/added fields files, the function helps in extracting start time using Try and Except block
def extract_start_time(raw):
    try:
        # Try : extracting the start time using the first method
        start_time_str = "".join(raw.time_coverage_start.astype(str).values)
        start_time = dt.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%SZ")
    except TypeError:
        # If the first method fails with a Type Error, the second method is used
        try:
            start_time_str = raw.time_coverage_start.item().decode("utf-8")
            start_time = dt.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%SZ")
        except AttributeError:
            # For Attribute error extracting the start time from raw.time_coverage_start.data
            start_time_from_data = raw.time_coverage_start.data

            # Converting the ndarray to a string
            start_time_from_data_str = str(start_time_from_data)
            # Defining the desired format pattern using a regular expression to be compared
            desired_format_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
            # Checking, if the extracted start time matches the desired format pattern
            if re.match(desired_format_pattern, start_time_from_data_str):
                start_time = start_time_from_data_str

    return start_time


def xy2latlon(xs_km, ys_km, radar_lat, radar_lon):
    """
    Convert radar-centered X/Y (in km) grid to latitude and longitude grid.
    Parameters:
        xs_km (2D array): X coordinates (east-west) in km
        ys_km (2D array): Y coordinates (north-south) in km
        radar_lat (float): Radar latitude (center point)
        radar_lon (float): Radar longitude (center point)
    Returns:
        lats (2D array): Latitude grid matching shape of xs_km
        lons (2D array): Longitude grid matching shape of xs_km
    """
    proj_aeqd = CRS.from_proj4(f"+proj=aeqd +lat_0={radar_lat} +lon_0={radar_lon} +datum=WGS84 +units=m +no_defs")
    proj_geo = CRS.from_epsg(4326) 
    transformer = Transformer.from_crs(proj_aeqd, proj_geo, always_xy=True)
    xs_m = xs_km * 1000
    ys_m = ys_km * 1000
    lons, lats = transformer.transform(xs_m, ys_m)
    return lats, lons


def update_xarray_dataset(file_path, raw, xg):
    xg.attrs.clear()
    raw.attrs.clear()

    # Creating a new DataArray with the added data for 'sweep_start_ray_index'
    sweep_start_ray_index_data = np.arange(
        0, raw.time.size, raw.time.size // raw.sweep.size, dtype="int64"
    )
    sweep_start_ray_index_da = xr.DataArray(sweep_start_ray_index_data, dims=["sweep"])

    # Including the new DataArray as a new variable in the Dataset
    xg["sweep_start_ray_index"] = sweep_start_ray_index_da

    # Creating a new DataArray with the added data for 'sweep_end_ray_index'
    sweep_end_ray_index_data = sweep_start_ray_index_data + int(
        (raw.time.size // raw.sweep.size) - 1
    )
    sweep_end_ray_index_da = xr.DataArray(sweep_end_ray_index_data, dims=["sweep"])

    # Including the new DataArray as a new variable in the Dataset
    xg["sweep_end_ray_index"] = sweep_end_ray_index_da

    # Defining the desired format pattern using a regular expression to be compared
    desired_format_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
    start_time = extract_start_time(raw)

    try:
        # Check if the extracted start time matches the desired format pattern
        if re.match(desired_format_pattern, start_time):
            start_time_str = start_time
        else:
            raise TypeError  # Trigger the except block to handle the exception
    except TypeError:
        start_time_str = start_time.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )  # Format the start time as string

    # Update the "time_coverage_start" variable in the dataset with the correct datetime object
    xg["time_coverage_start"] = start_time_str

    # Update the "units" attribute of the "time" variable to match the correct format
    time_units = f"seconds since {start_time_str}"
    xg["time"].attrs["units"] = time_units

    Station = os.path.basename(file_path)[-31:-28]
    if Station == "CHR":
        a = "Cherrapunji S-band Dual-pol DWR"
    elif Station == "SHR":
        a = "SHAR S-band Dual-pol DWR"
    elif Station == "TLS":
        a = "TERLS C-band Dual-pol DWR"
    else:
        a =  "DWR"

    # Add attributes to the dataset in the given order
    xg.attrs["instrument_name"] = a
    xg.attrs[
        "Created using"
    ] = "pyiwr (Python Indian Weather Radar Toolkit) Module developed by Researchers at SIGMA Research Lab, IIT Indore"
    xg.attrs["version"] = "Version 1.0.1"
    xg.attrs["title"] = a[0:-3] + "DWR data"
    xg.attrs["institution"] = "Indian: ISRO/IMD/IITM"
    xg.attrs[
        "references"
    ] = "Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html"
    xg.attrs["source"] = "DWR volume scan data"
    xg.attrs["comment"] = ""
    xg.attrs["Conventions"] = "CF/Radial"
    xg.attrs["field_names"] = "DBZ, VEL, WIDTH, ZDR, PHIDP, RHOHV"
    xg.attrs[
        "history"
    ] = "DWR (.nc) data encoded into format_corrected NetCDF file"
    xg.attrs["volume_number"] = 0
    xg.attrs["platform_type"] = "fixed"
    xg.attrs["instrument_type"] = "radar"
    xg.attrs["primary_axis"] = "axis_z"

    return xg

def make_grid(radar, height_km=20, length_km=250, vert_res_km=0.5, horiz_res_km=1, gridding_algo='map_gates_to_grid', copy_field_dtypes=True,):

    """
    Returns grid object from radar object.
    grid_shape=(60, 500, 500), no. of bins of z,y,x respectively.
    height:(int) = 15, height in km
    length:(int) = 250, Range of radar in km
    """
    # Calculate the number of vertical levels and horizontal points
    vertical_levels = int(height_km / vert_res_km) + 1
    horizontal_points = int((2 * length_km) / horiz_res_km) + 1

    # Define the grid shape
    grid_shape = (vertical_levels, horizontal_points, horizontal_points)
    
    # Calculate the grid limits
    height = (0, height_km * 1000)  # convert to meters
    length = (-length_km * 1000, length_km * 1000)  # convert to meters
    
    # Define the grid limits
    grid_limits = (height, length, length)
    
    # Create the grid from radars
    grid = pyart.map.grid_from_radars(radar, grid_shape=grid_shape, grid_limits=grid_limits, gridding_algo='map_gates_to_grid', copy_field_dtypes=True,)
    
    return grid


def sorting_key(s, _re=re.compile(r"(\d+)")):
    return [int(t) if i & 1 else t.lower() for i, t in enumerate(_re.split(s))]


#Convert to reflectivity factor Z (unit: mm6/m3 )
def db2si(x):
    return 10.0 ** (x / 10.0)


def extract_values_location(xg, field_name, elevation_index, target_lat, target_lon):
    """
    Extract the value of the specified field at the specified location from the radar data.

    Parameters:
        xg (pyart.core.Grid): Radar data object.
        field_name (str): Name of the radar field to extract.
        elevation_index (int): Index of the desired elevation.
        target_lat (float): Latitude of the target location.
        target_lon (float): Longitude of the target location.

    Returns:
        extracted_value: Value of the specified field at the specified location.
    """
    # Access the field from the radar data object
    radar_data_array = xg[field_name][0][elevation_index]

    # Round the target latitude and longitude coordinates to match the nearest grid point
    rounded_lat = np.round(target_lat, decimals=3)
    rounded_lon = np.round(target_lon, decimals=3)

    # Find the nearest indices in the latitude and longitude coordinates
    nearest_lat_idx = np.abs(radar_data_array.lat - rounded_lat).argmin().item()
    nearest_lon_idx = np.abs(radar_data_array.lon - rounded_lon).argmin().item()

    # Extract the value at the nearest indices
    extracted_value = radar_data_array[nearest_lat_idx, nearest_lon_idx]

    return extracted_value


def qpe_estimators(ref_val = 'DBZ', diffref_val = 'ZDR', kdp = 'KDP', a=267, b=1.3, c = None, a_c= None, b_c= None, a_s= None, b_s= None):
    """
    Calculate rain rate using the Z-R relationship and mask values below 0.1.

    Parameters:
        value: Value of the radar field.
        A (float): Parameter 'A' for the radar polarimetric fields-R relationship.
        b (float): Parameter 'b' for the radar polarimetric fields-R relationship.
        c (float): Parameter 'c' for the radar polarimetric fields-R relationship.
    Returns:
        rain_rate: Calculated rain rate.
    """
    
    #Convert reflectivity factor Z (unit: mm6/m3 ) to Rain Rate(mm/h) through Z-R Relation followed by DWR_Sohra Currently
    radar_ref_array = decibel(ref_val)
    radar_difref_array = decibel(diffref_val)
    radar_kdp_array = kdp

    # Apply the Z-R relationship
    rain_rate = (radar_ref_array / a) ** (1.0 / b)
    rain_rate = (a * (radar_ref_array**b) * (radar_difref_array**c))
    rain_rate = (a * (radar_kdp_array**b))
    rain_rate = (a * (radar_kdp_array**b) * (radar_difref_array**c))

    # Mask values below 0.1
    rain_rate = ma.masked_where(rain_rate < 0.1, rain_rate)

    return rain_rate


def classify_echo_filter_dbzh(radar, elevation_index=0, static_clutter_map=None):
    """
    Apply Gabella filtering and fuzzy echo classification on radar data.

    Parameters:
    ----------
    radar : pyart radar objects
        Radar object with polarimetric fields.
    elevation_index : int
        Index of sweep elevation to process (default: 0)
    static_clutter_map : ndarray or None
        Optional user-provided static clutter map (same shape as sweep)

    Returns:
    -------
    cleaned_dbzh : masked_array
        Reflectivity field with combined clutter mask applied.
    combined_mask : ndarray
        Combined mask from Gabella filter and fuzzy classification.

    Example usage:
    cleaned_dbzh, combined_mask = classify_echo_filter_dbzh(radar, elevation_index=0)
    cleaned_dbzh, combined_mask = classify_echo_filter_dbzh(radar, elevation_index=0, static_clutter_map=my_static_map)
   
    """
    # Extract sweep data
    sweep_start = radar.sweep_start_ray_index["data"][elevation_index]
    sweep_end = radar.sweep_end_ray_index["data"][elevation_index] + 1

    dbzh = radar.fields["DBZ"]["data"][sweep_start:sweep_end]
    zdr = radar.fields["ZDR"]["data"][sweep_start:sweep_end]
    rho = radar.fields["RHOHV"]["data"][sweep_start:sweep_end]
    phi = radar.fields["PHIDP"]["data"][sweep_start:sweep_end]
    dop = radar.fields["VEL"]["data"][sweep_start:sweep_end]

    # Apply Gabella filter
    clutter_mask_gabella = wrl.classify.filter_gabella(
        dbzh,
        wsize=5,
        thrsnorain=0.0,
        tr1=6.0,
        n_p=6,
        tr2=1.3,
        rm_nans=True,
        radial=False,
        cartesian=False,
    )

    # Prepare input dict for fuzzy classification
    dat = {
        "zdr": zdr,
        "rho": rho,
        "phi": phi,
        "dop": dop,
        "map": static_clutter_map.astype(float) if static_clutter_map is not None else clutter_mask_gabella.astype(float)
    }

    # Fuzzy echo classification
    prob, fuzzy_mask = classify_echo_fuzzy(dat)

    # Combine masks
    combined_mask = np.logical_or(clutter_mask_gabella, fuzzy_mask)

    # Masked reflectivity
    cleaned_dbzh = np.ma.array(dbzh, mask=combined_mask)

    return cleaned_dbzh, combined_mask


def read_byindex(output_files, index):
    if index < 0 or index >= len(output_files):
        raise IndexError(f"Index {index} is out of range for {len(output_files)} output files.")
    
    file_path = output_files[index]
    if "_grid" in file_path:
        radar_data = pyart.io.read_grid(file_path)
        radar_data = radar_data.to_xarray()
    else:
        radar_data = pyart.io.read_cfradial(file_path)
    return radar_data


def list_dirfil (path_string, ):
    folder_path = glob.glob(os.path.join(path_string, "*nc*"))
    return folder_path
