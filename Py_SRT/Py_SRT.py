print('''You are using Py-SRT an open-source module developed by Researchers at the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw DWR (Doppler Weather Radar) files into Py-ART compatible NetCDF files. Furthermore, Py-SRT provides useful tools and visualisation functions to make working with the radar data easier and more enjoyable.''')


import os
import pyart
import os
import datetime as dt
import xarray as xr
import numpy as np

def fread(fid, nelements, dtype):
    if dtype is np.str_:
        dt = np.uint8  
    else:
        dt = dtype

    data_array = np.fromfile(fid, dt, nelements)
    data_array.shape = (nelements, 1)
    return data_array


def dwr2nc(dwr_path, nc_directory):
    with open(dwr_path, 'rb') as fid:
        print('Processing file:',os.path.basename(dwr_path))
        m5 = np.fromfile(fid, dtype='uint8')
        m5 = m5.astype(float)

        status = fid.seek(0, 0)
        mode = fread(fid, 1, np.uint16)
        site_num = mode[0, 0]

        status = fid.seek(2, 0)
        s1 = np.fromfile(fid, dtype=np.uint8, count=20, sep='')
        st = str(s1.tobytes())
        Station = (st.split(sep='\\x')[0]).split(sep="'")[1]

        status = fid.seek(32, 0)
        s2 = np.fromfile(fid, dtype=np.uint8, count=10, sep='')
        rd = str(s2.tobytes())
        Radar = (rd.split(sep='\\x')[0]).split(sep="'")[1]

        St_Year = hex(((m5[42:44:2] + 256 * m5[43])[0].astype(int))).split(sep='x')[1]
        St_Month = hex((m5[44]).astype(int)).split(sep='x')[1]
        St_Day = hex((m5[45]).astype(int)).split(sep='x')[1]
        St_Hour = hex((m5[46]).astype(int)).split(sep='x')[1]
        St_Minute = hex((m5[47]).astype(int)).split(sep='x')[1]
        St_Sec = hex((m5[48]).astype(int)).split(sep='x')[1]

        Start_Time = St_Year + '-' + St_Month.zfill(2) + '-' + St_Day.zfill(2) + ' , ' + St_Hour.zfill(2) + ':' + St_Minute.zfill(2) + ':' + St_Sec.zfill(2)
        date = Start_Time[0:-10]
        time = Start_Time[12:]

        PRFH = m5[573:632:2] + 256 * m5[574:633:2]
        PRFL = m5[633:692:2] + 256 * m5[634:693:2]
        Pulse_width = (m5[693:752:2] + 256 * m5[694:753:2]) / 100

        status = fid.seek(26, 0)
        lat_temp = fread(fid, 1, np.uint32)
        lat = lat_temp[0, 0] / 10000

        status = fid.seek(22, 0)
        lon_temp = fread(fid, 1, np.uint32)
        lon = lon_temp[0, 0] / 10000

        status = fid.seek(30, 0)
        h = fread(fid, 1, np.uint16)
        h = h[0, 0]

        status = fid.seek(394, 0)
        mod = fread(fid, 1, np.uint32)
        freq = mod[0, 0] * 1000

        elev_ang1 = (m5[408:467:2] + 256 * m5[409:468:2]) / 10
        elevation = np.unique(elev_ang1)
        num_el = len(elevation)

        rang_res = m5[754:813:2] + 256 * m5[755:814:2]
        range_val = rang_res[0]
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
                m7 = m6[s2 * (fn1 - 1):s2 * fn1]  # 2nd elevation data

            m8 = np.reshape(m7, (int(no_bin_ele[0]) * 7 + 4, 360 * 1), order='F')

            m9 = m8[:][4:]
            z = m9[0::7][:]
            z = (z - 1) / 2 - 31.5
            z1 = np.copy(z)

            zf = z1[:, 359]
            zf = np.reshape(zf, (len(zf), 1), order='F')
            Z1 = np.hstack((z1, zf))

            prf = m5[573:582:2] + 256 * m5[574:583:2]
            prfl = m5[633:692:2] + 256 * m5[634:693:2]
            lamd = (3e8) / freq

            if prfl[0] == 0:
                v = m9[1::7][:]
                v = np.where((v == 0), np.nan, v)
                v = (((v - 128) / 128) * (lamd * prf[0] / (4)))
            else:
                prt_dul = (1 / prfl[0]) - (1 / prf[0])
                v = m9[1::7][:]
                v = np.where((v == 0), np.nan, v)
                v = ((v - 128) / 128) * (lamd / (prt_dul * 4))

            v1 = np.copy(v)
            vf = v1[:, 359]
            vf = np.reshape(vf, (len(vf), 1), order='F')
            V1 = np.hstack((v1, vf))

            sw = m9[2::7][:]
            sw = sw / 10
            sw[sw < -0] = -0
            sw[sw > 16] = 16
            sw1 = np.copy(sw)
            swf = sw1[:, 359]
            swf = np.reshape(swf, (len(swf), 1), order='F')
            SW1 = np.hstack((sw1, swf))

            zdr = m9[3::7][:]
            zdr = zdr / 20 - 4
            zdr1 = np.copy(zdr)
            zdrf = zdr1[:, 359]
            zdrf = np.reshape(zdrf, (len(zdrf), 1), order='F')
            ZDR1 = np.hstack((zdr1, zdrf))

            phidp = m9[4::7][:] + 256 * m9[5::7][:]
            phidp = phidp * 0.088
            phidp1 = phidp - 180
            phidpf = phidp1[:, 359]
            phidpf = np.reshape(phidpf, (len(phidpf), 1), order='F')
            PHIDP1 = np.hstack((phidp1, phidpf))

            rdp = m9[6::7][:]
            rdp = rdp / 256
            rdp1 = np.copy(rdp)
            rdpf = rdp1[:, 359]
            rdpf = np.reshape(rdpf, (len(rdpf), 1), order='F')
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

        dats = [
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
            RDP1t
        ]



        # def isro_radar_object(dats, dwr_directory):
        radar = pyart.testing.make_empty_ppi_radar(1600, 360, 10)

        data = np.array(np.linspace(0.0555555556, 399.944444444, 3600), dtype=np.float64)
        tstart = dats[1][:-1]+'T'+dats[2][1:]+'Z'

        radar.time = {
        'data': data.astype(np.float64),
        'standard_name': 'time',
        'long_name': 'time_in_seconds_since_volume_start',
        'units': 'seconds since ' + tstart,
        'calendar': 'gregorian'
        }

        radar.latitude["data"] = np.array([dats[5]])
        radar.longitude["data"] = np.array([dats[4]])
        radar.range["data"] = np.linspace(75.0, 150.0 * (1600 - 1), 1600)
        radar.fixed_angle["data"] = np.array(dats[8][:10], dtype=np.float32).flatten()
        radar.sweep_number["data"] = np.array(range(10))

        radar.sweep_start_ray_index['data'] = np.arange(0, radar.nrays, radar.nrays/10, dtype='int64')
        radar.sweep_end_ray_index['data'] = radar.sweep_start_ray_index['data'] + int((radar.nrays/10)-1)
        radar.init_gate_longitude_latitude()
        radar.init_gate_altitude()
        radar.init_gate_x_y_z()

        #radar.sweep_start_ray_index["data"] = np.array(np.arange(0, 3600, 360), dtype=np.int64)
        #radar.sweep_end_ray_index["data"] = np.array(np.arange(359, 3600, 360), dtype=np.int64)
        radar.altitude['data'] = np.array(dats[6], dtype=np.int32).flatten()
        radar.azimuth["data"] = np.repeat(np.arange(360, dtype=np.float32), 10)
        radar.sweep_mode['data'] = np.array([
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b''],
            [b'a', b'z', b'i', b'm', b'u', b't', b'h', b' ', b's', b'u', b'r', b'v', b'e', b'i', b'l', b'l', b'a', b'n', b'c', b'e', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'', b'']
        ], dtype='|S1')

        radar.elevation["data"] = np.array(np.repeat(dats[8][:10], 360))
        radar.metadata = {'instrument_name': 'Sohra S-band Dual-pol DWR', 'Created using': 'Py-SRT Module developed at SIGMA Research Lab, IIT Indore', 'version': 'Version 1.0', 'title': 'S Band DWR data','institution': 'ISRO', 'references': 'Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html', 'source': 'DWR volume scan data ', 'history': 'DWR raw (.dwr) data encoded into Py-ART compatible NetCDF file', 'comment': '', 'platform_type': 'fixed', 'instrument_type': 'radar', 'primary_axis': 'axis_z'}


        ref = (np.array(np.reshape(dats[14][:,:360,:], (dats[14][:,:360,:].shape[0], -1)))).T
        ref = np.nan_to_num(ref, nan=0.0)
        fill_value = ref[0,0]

        vel = (np.array(np.reshape(dats[15][:,:360,:], (dats[15][:,:360,:].shape[0], -1)))).T
        vel = np.nan_to_num(vel, nan=0.0)
        fill_value = vel[0,0]

        sw = (np.array(np.reshape(dats[16][:,:360,:], (dats[16][:,:360,:].shape[0], -1)))).T
        sw = np.nan_to_num(sw, nan=0.0)
        fill_value = sw[0,0]

        zdr = (np.array(np.reshape(dats[17][:,:360,:], (dats[17][:,:360,:].shape[0], -1)))).T
        zdr = np.nan_to_num(zdr, nan=0.0)
        fill_value = zdr[0,0]

        phidp = (np.array(np.reshape(dats[18][:,:360,:], (dats[18][:,:360,:].shape[0], -1)))).T
        phidp = np.nan_to_num(phidp, nan=0.0)
        fill_value = phidp[0,0]

        rdp = (np.array(np.reshape(dats[19][:,:360,:], (dats[19][:,:360,:].shape[0], -1)))).T
        rdp = np.nan_to_num(rdp, nan=0.0)
        fill_value = rdp[0,0]

        radar.fields['DBZ'] = {
            'data': ref.astype(np.float32),
            'units': 'dBZ',
            'standard_name': 'equivalent_reflectivity_factor',
            'Polarization': 'Horizontal',
            '_FillValue': fill_value
        }

        radar.fields['VEL'] = {
            'data': vel.astype(np.float32),
            'units': 'm/s',
            'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
            'Polarization': 'Horizontal',
            '_FillValue': fill_value
        }

        radar.fields['WIDTH'] = {
            'data': sw.astype(np.float32),
            'units': 'm/s',
            'standard_name': 'doppler_spectrum_width',
            'Polarization': 'Horizontal',
            '_FillValue': fill_value
        }

        radar.fields['ZDR'] = {
            'data': zdr.astype(np.float32),
            'units': 'dB',
            'standard_name': 'log_differential_reflectivity_hv',
            'Polarization': 'Horizontal and Vertical',
            '_FillValue': fill_value
        }

        radar.fields['PHIDP'] = {
            'data': phidp.astype(np.float32),
            'units': 'degrees',
            'standard_name': 'differential_phase_hv',
            'Polarization': 'Horizontal and Vertical',
            '_FillValue': fill_value
        }

        radar.fields['RHOHV'] = {
            'data': rdp.astype(np.float32),
            'units': 'unitless',
            'standard_name': 'cross_correlation_ratio_hv',
            'Polarization': 'Horizontal and Vertical',
            '_FillValue': fill_value
        }
        # Create the "updated" subdirectory if it doesn't exist
        updated_dir = os.path.join(nc_directory, "radar_ncfiles")
        os.makedirs(updated_dir, exist_ok=True)

        # Specify the new file path
        filepath =os.path.basename(dwr_path)
        new_file_name = f"new_{filepath[:-4]}.nc"  # Remove the last 4 characters (.dwr)
        new_file_path = os.path.join(updated_dir, new_file_name)
        print('File ',os.path.basename(dwr_path),' converted successfully')
        return pyart.io.write_cfradial(new_file_path, radar, format='NETCDF4')

def nc_datim_correct(file_path):
    # Open the dataset
    
    print('Processing file: ',os.path.basename(file_path))

    raw = xr.open_dataset(file_path, decode_times=False)
    raw.attrs.clear()
    
    Station = os.path.basename(file_path)[2:5]
    if Station == 'CHR':
        a = 'Sohra S-band Dual-pol DWR'
    elif Station == 'SHR':
        a = 'SHAR S-band Dual-pol DWR'
    else: 
        a = 'TERLS C-band Dual-pol DWR'  
        
        
    # Add attributes to the dataset in the given order
    raw.attrs['instrument_name'] = a
    raw.attrs['Created using'] = 'Py-SRT Module developed by Researchers at SIGMA Research Lab, IIT Indore'
    raw.attrs['version'] = 'Version 1.0'
    raw.attrs['title'] = a[0:13] +'DWR data'
    raw.attrs['institution'] = 'ISRO'
    raw.attrs['references'] = 'Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html'
    raw.attrs['source'] = 'DWR volume scan data'
    raw.attrs['comment'] = ''
    raw.attrs['Conventions'] = 'CF/Radial'
    raw.attrs['field_names'] = 'DBZ, VEL, WIDTH, ZDR, PHIDP, RHOHV'
    raw.attrs['history'] = 'DWR mosdac files (.nc) data encoded into Py-ART compatible NetCDF file'
    raw.attrs['volume_number'] = 0
    raw.attrs['platform_type'] = 'fixed'
    raw.attrs['instrument_type'] = 'radar'
    raw.attrs['primary_axis'] = 'axis_z'

    # Extract the start time from the dataset and convert it to datetime object
    start_time_str = "".join(raw.time_coverage_start.astype(str).values)
    start_time = dt.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%SZ")

    # Update the "time_coverage_start" variable in the dataset with the correct datetime object
    raw["time_coverage_start"] = start_time

    # Update the "units" attribute of the "time" variable to match the correct format
    time_units = f"seconds since {start_time}"
    raw["time"].attrs["units"] = time_units

    # Decode the CF conventions of the dataset
    radar_pol = xr.decode_cf(raw)

    # Create the "corrected" subdirectory if it doesn't exist
    corrected_dir = os.path.join(os.path.dirname(file_path), "corrected")
    os.makedirs(corrected_dir, exist_ok=True)

    # Specify the new file path
    new_file_name = f"corrected_{os.path.basename(file_path)}"
    new_file_path = os.path.join(corrected_dir, new_file_name)

    print('Date Time of Mosdac File ',os.path.basename(file_path),' corrected successfully')

    # Save the updated dataset to a new netCDF file
    return radar_pol.to_netcdf(new_file_path)


def sweeps2grid(radar, grid_shape=(31, 501, 501), height=16.313, length=250):
    """
    Example:
    Returns grid object from radar object.
    grid_shape=(60, 500, 500), no. of bins of z,y,x respectively.

    height:(int) = 15, height in km
    length:(int) = 250, Range of radar in km
    
    # 0.5 km vertical resoltion
    # 1 km resolution horizontally
    #radar installed at 1.313 km height
    """
    grid = pyart.map.grid_from_radars(
        radar, grid_shape=grid_shape,
        grid_limits=((radar.altitude['data'][0], height * 1e3),
                     (-length * 1e3, length * 1e3),
                     (-length * 1e3, length*1e3)),
        fields=radar.fields.keys(),
        weighting_function='Barnes2',
        min_radius=length)
    return grid
