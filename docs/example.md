```python
#Displaying multiple output of a single cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
```
pip install --upgrade pyiwr

```python
!conda info
```

    
         active environment : DWR
        active env location : C:\Users\SIGMA-W-VT\.conda\envs\DWR
                shell level : 1
           user config file : C:\Users\SIGMA-W-VT\.condarc
     populated config files : C:\Users\SIGMA-W-VT\.condarc
              conda version : 23.3.1
        conda-build version : 3.24.0
             python version : 3.10.9.final.0
           virtual packages : __archspec=1=x86_64
                              __cuda=11.1=0
                              __win=0=0
           base environment : C:\ProgramData\anaconda3  (read only)
          conda av data dir : C:\ProgramData\anaconda3\etc\conda
      conda av metadata url : None
               channel URLs : https://repo.anaconda.com/pkgs/main/win-64
                              https://repo.anaconda.com/pkgs/main/noarch
                              https://repo.anaconda.com/pkgs/r/win-64
                              https://repo.anaconda.com/pkgs/r/noarch
                              https://repo.anaconda.com/pkgs/msys2/win-64
                              https://repo.anaconda.com/pkgs/msys2/noarch
              package cache : C:\ProgramData\anaconda3\pkgs
                              C:\Users\SIGMA-W-VT\.conda\pkgs
                              C:\Users\SIGMA-W-VT\AppData\Local\conda\conda\pkgs
           envs directories : C:\Users\SIGMA-W-VT\.conda\envs
                              C:\ProgramData\anaconda3\envs
                              C:\Users\SIGMA-W-VT\AppData\Local\conda\conda\envs
                   platform : win-64
                 user-agent : conda/23.3.1 requests/2.28.1 CPython/3.10.9 Windows/10 Windows/10.0.22621
              administrator : False
                 netrc file : None
               offline mode : False
    
    


```python
import os
import pyiwr
```

# RAW DWR FILES

## Single dwr format file conversion to NetCDF cfradial (polar) data compatible to PyART


```python
filename = 'Z:\\test_dataset\\test_dataset\\dwr\\cherrapunjee_weather_2021_05_01_06_21_40_dsfisro6n.dwr'
```


```python
out_path = 'Z:\\test_dataset\\test_dataset\\dwr\\'
```


```python
pyiwr.format_transform.dwr2nc(filename, out_path)
```

    Processing file: cherrapunjee_weather_2021_05_01_06_21_40_dsfisro6n.dwr
    File  cherrapunjee_weather_2021_05_01_06_21_40_dsfisro6n.dwr  converted successfully
    


```python
radar = pyart.io.read('E:\\radar_ncfiles\\new_cherrapunjee_weather_2021_05_01_06_21_40_dsfisro6n.nc')
radar.info()
```

    altitude:
    	data: <ndarray of type: int32 and shape: (1,)>
    	long_name: Altitude
    	units: meters
    	standard_name: Altitude
    	positive: up
    altitude_agl: None
    antenna_transition: None
    azimuth:
    	data: <ndarray of type: float32 and shape: (3600,)>
    	long_name: azimuth_angle_from_true_north
    	units: degrees
    	standard_name: beam_azimuth_angle
    	axis: radial_azimuth_coordinate
    	comment: Azimuth of antenna relative to true north
    elevation:
    	data: <ndarray of type: float64 and shape: (3600,)>
    	long_name: elevation_angle_from_horizontal_plane
    	units: degrees
    	standard_name: beam_elevation_angle
    	axis: radial_elevation_coordinate
    	comment: Elevation of antenna relative to the horizontal plane
    fields:
    	DBZ:
    		data: <ndarray of type: float32 and shape: (3600, 1600)>
    		_FillValue: 0.0
    		units: dBZ
    		standard_name: equivalent_reflectivity_factor
    		Polarization: Horizontal
    	VEL:
    		data: <ndarray of type: float32 and shape: (3600, 1600)>
    		_FillValue: 0.0
    		units: m/s
    		standard_name: radial_velocity_of_scatterers_away_from_instrument
    		Polarization: Horizontal
    	WIDTH:
    		data: <ndarray of type: float32 and shape: (3600, 1600)>
    		_FillValue: 0.0
    		units: m/s
    		standard_name: doppler_spectrum_width
    		Polarization: Horizontal
    	ZDR:
    		data: <ndarray of type: float32 and shape: (3600, 1600)>
    		_FillValue: 0.0
    		units: dB
    		standard_name: log_differential_reflectivity_hv
    		Polarization: Horizontal and Vertical
    	PHIDP:
    		data: <ndarray of type: float32 and shape: (3600, 1600)>
    		_FillValue: 0.0
    		units: degrees
    		standard_name: differential_phase_hv
    		Polarization: Horizontal and Vertical
    	RHOHV:
    		data: <ndarray of type: float32 and shape: (3600, 1600)>
    		_FillValue: 0.0
    		units: unitless
    		standard_name: cross_correlation_ratio_hv
    		Polarization: Horizontal and Vertical
    fixed_angle:
    	data: <ndarray of type: float32 and shape: (10,)>
    	long_name: Target angle for sweep
    	units: degrees
    	standard_name: target_fixed_angle
    instrument_parameters: None
    latitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	long_name: Latitude
    	units: degrees_north
    	standard_name: Latitude
    longitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	long_name: Longitude
    	units: degrees_east
    	standard_name: Longitude
    nsweeps: 10
    ngates: 1600
    nrays: 3600
    radar_calibration: None
    range:
    	data: <ndarray of type: float64 and shape: (1600,)>
    	long_name: range_to_measurement_volume
    	units: meters
    	standard_name: projection_range_coordinate
    	axis: radial_range_coordinate
    	spacing_is_constant: true
    	comment: Coordinate variable for range. Range to center of each bin.
    scan_rate: None
    scan_type: ppi
    sweep_end_ray_index:
    	data: <ndarray of type: int64 and shape: (10,)>
    	long_name: Index of last ray in sweep, 0-based
    	units: count
    sweep_mode:
    	data: <ndarray of type: |S1 and shape: (10, 32)>
    	long_name: Sweep mode
    	units: unitless
    	standard_name: sweep_mode
    	comment: Options are: "sector", "coplane", "rhi", "vertical_pointing", "idle", "azimuth_surveillance", "elevation_surveillance", "sunscan", "pointing", "manual_ppi", "manual_rhi"
    sweep_number:
    	data: <ndarray of type: int32 and shape: (10,)>
    	long_name: Sweep number
    	units: count
    	standard_name: sweep_number
    sweep_start_ray_index:
    	data: <ndarray of type: int64 and shape: (10,)>
    	long_name: Index of first ray in sweep, 0-based
    	units: count
    target_scan_rate: None
    time:
    	data: <ndarray of type: float64 and shape: (3600,)>
    	long_name: time_in_seconds_since_volume_start
    	units: seconds since 2021-05-01T06:21:40Z
    	standard_name: time
    	calendar: gregorian
    metadata:
    	instrument_name: Sohra S-band Dual-pol DWR
    	Created using: pyiwr (Indian Weather Radar) Module developed at SIGMA Research Lab, IIT Indore
    	version: Version 1.0.0
    	title: S Band DWR data
    	institution: ISRO
    	references: Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html
    	source: DWR volume scan data 
    	comment: 
    	Conventions: CF/Radial
    	field_names: DBZ, VEL, WIDTH, ZDR, PHIDP, RHOHV
    	history: DWR raw (.dwr) data encoded into Py-ART compatible NetCDF file
    	volume_number: 0
    	platform_type: fixed
    	instrument_type: radar
    	primary_axis: axis_z
    

## Multiple dwr format files conversion to NetCDF cfradial (polar) data compatible to PyART


```python
dwr_directory = 'C:\\Users\\dell\\codes\\test_data\\short format'
```


```python
out_path = 'E:\\'
```


```python
# Loop through the files in the directory
for filename in os.listdir(dwr_directory):
    if filename.endswith('.dwr'):
        #DWR file read programme
        file_path = os.path.join(dwr_directory, filename)
        ir.format_transform.dwr2nc(file_path, out_path)
```

    Processing file: cherrapunjee_weather_2021_05_01_06_21_40_dsfisro6n.dwr
    File  cherrapunjee_weather_2021_05_01_06_21_40_dsfisro6n.dwr  converted successfully
    Processing file: cherrapunjee_weather_2021_05_01_06_36_36_dsfisro6n.dwr
    File  cherrapunjee_weather_2021_05_01_06_36_36_dsfisro6n.dwr  converted successfully
    Processing file: cherrapunjee_weather_2021_05_01_06_52_00_dsfisro6n.dwr
    File  cherrapunjee_weather_2021_05_01_06_52_00_dsfisro6n.dwr  converted successfully
    

# MOSDAC RADAR FILES


```python
import os
file_path_short = 'C:\\Users\\dell\\codes\\test_data\\mosdac\\short'
file_list_short = os.listdir(file_path_short)
file_list_short
```




    ['corrected',
     'gridded_radar_ncfiles',
     'RCTLS_03SEP2018_051827_L2B_STD.nc',
     'RCTLS_03SEP2018_053343_L2B_STD.nc',
     'RSCHR_11JUL2019_071439_L2B_STD.nc',
     'RSCHR_24MAR2022_173414_L2B_STD.nc',
     'RSSHR_11JUL2019_193045_L2B_STD.nc',
     'RSSHR_11JUL2019_195144_L2B_STD.nc']




```python
# Access files by indexing the list
# For example, to access the file in the list:
filenames1 = os.path.join(file_path_short, file_list_short[6])
filenames2 = os.path.join(file_path_short, file_list_short[7])
filenames3 = os.path.join(file_path_short, file_list_short[2])
filenames4 = os.path.join(file_path_short, file_list_short[3])
filenames5 = os.path.join(file_path_short, file_list_short[4])
filenames6 = os.path.join(file_path_short, file_list_short[5])
```


```python
import os
file_path_long = 'C:\\Users\\dell\\codes\\test_data\\mosdac\\long'
file_list_long = os.listdir(file_path_long)
file_list_long
```




    ['corrected',
     'gridded_radar_ncfiles',
     'RCTLS_03SEP2018_052448_L2B_STD.nc',
     'RSCHR_11JUL2019_023140_L2B_STD.nc',
     'RSCHR_24MAR2022_004350_L2B_STD.nc',
     'RSSHR_11JUL2019_193241_L2B_STD.nc',
     'RSSHR_11JUL2019_195339_L2B_STD.nc']




```python
# Access files by indexing the list
# For example, to access the file in the list:
filenamel1 = os.path.join(file_path_long, file_list_long[5])
filenamel2 = os.path.join(file_path_long, file_list_long[6])
filenamel3 = os.path.join(file_path_long, file_list_long[2])
filenamel4 = os.path.join(file_path_long, file_list_long[3])
filenamel5 = os.path.join(file_path_long, file_list_long[4])
```

## Single mosdac nc format file sweeps correction and conversion  to time corrected NetCDF cfradial (polar) data compatible to PyART


```python
# "save_file=True" will save the radar nc file and also enable the radar objects be read in a variable
radar = ir.format_transform.mosdac_correctednc(filenames2, save_file=True)
```

    Processing file:  RSSHR_11JUL2019_195144_L2B_STD.nc
    Date Time of Mosdac File RSSHR_11JUL2019_195144_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    


```python
radar.info()
```

    altitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	_FillValue: nan
    	units: meters
    altitude_agl: None
    antenna_transition: None
    azimuth:
    	data: <ndarray of type: float32 and shape: (720,)>
    	_FillValue: nan
    	standard_name: ray_azimuth_angle
    	units: degrees
    	long_name: azimuth_angle_from_true_north
    	axis: radial_azimuth_coordinate
    elevation:
    	data: <ndarray of type: float32 and shape: (720,)>
    	_FillValue: nan
    	standard_name: ray_elevation_angle
    	units: degrees
    	long_name: elevation_angle_from_horizontal_plane
    	axis: radial_azimuth_coordinate
    fields:
    	DBZ:
    		data: <ndarray of type: float32 and shape: (720, 1633)>
    		_FillValue: 0.0
    		units: dBZ
    		standard_name: equivalent_reflectivity_factor
    		Polarization: Horizontal
    		coordinates: time range
    	VEL:
    		data: <ndarray of type: float32 and shape: (720, 1633)>
    		_FillValue: 0.0
    		units: m/s
    		standard_name: radial_velocity_of_scatterers_ away_from_instrument
    		Polarization: Horizontal
    		coordinates: time range
    	WIDTH:
    		data: <ndarray of type: float32 and shape: (720, 1633)>
    		_FillValue: 0.0
    		units: m/s
    		standard_name: doppler_spectrum_width
    		Polarization: Horizontal
    		coordinates: time range
    	ZDR:
    		data: <ndarray of type: float32 and shape: (720, 1633)>
    		_FillValue: 0.0
    		units: dB
    		standard_name: log_differential_reflectivity_hv
    		Polarization: Horizontal and Vertical
    		coordinates: time range
    	PHIDP:
    		data: <ndarray of type: float32 and shape: (720, 1633)>
    		_FillValue: 0.0
    		units: degrees
    		standard_name: differential_phase_hv
    		Polarization: Horizontal and Vertical
    		coordinates: time range
    	RHOHV:
    		data: <ndarray of type: float32 and shape: (720, 1633)>
    		_FillValue: 0.0
    		units: 
    		standard_name: cross_correlation_ratio_hv
    		Polarization: Horizontal and Vertical
    		coordinates: time range
    fixed_angle:
    	data: <ndarray of type: float32 and shape: (2,)>
    	_FillValue: nan
    	units: degrees
    instrument_parameters: None
    latitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	_FillValue: nan
    	units: degrees_north
    longitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	_FillValue: nan
    	units: degrees_east
    nsweeps: 2
    ngates: 1633
    nrays: 720
    radar_calibration: None
    range:
    	data: <ndarray of type: float64 and shape: (1633,)>
    	_FillValue: nan
    	standard_name: projection_range_coordinate
    	long_name: range_to_measurement_volume
    	units: meters
    	spacing_is_constant: true
    	meters_to_center_of_first_gate: true
    	axis: radial_range_coordinate
    scan_rate: None
    scan_type: ppi
    sweep_end_ray_index:
    	data: <ndarray of type: int64 and shape: (2,)>
    sweep_mode:
    	data: <ndarray of type: |S1 and shape: (2, 32)>
    sweep_number:
    	data: <ndarray of type: int32 and shape: (2,)>
    sweep_start_ray_index:
    	data: <ndarray of type: int64 and shape: (2,)>
    target_scan_rate: None
    time:
    	data: <ndarray of type: float64 and shape: (720,)>
    	_FillValue: nan
    	standard_name: time
    	long_name: time_in_seconds_since_volume_start
    	units: seconds since 2019-07-11T19:51:44
    	calendar: gregorian
    metadata:
    	instrument_name: SHAR S-band Dual-pol DWR
    	Created using: pyiwr (Indian Weather Radar) Module developed by Researchers at SIGMA Research Lab, IIT Indore
    	version: Version 1.0
    	title: SHAR S-band DDWR data
    	institution: ISRO
    	references: Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html
    	source: DWR volume scan data
    	comment: 
    	Conventions: CF/Radial
    	field_names: DBZ, VEL, WIDTH, ZDR, PHIDP, RHOHV
    	history: DWR mosdac files (.nc) data encoded into Py-ART compatible NetCDF file
    	volume_number: 0
    	platform_type: fixed
    	instrument_type: radar
    	primary_axis: axis_z
    


```python
# "save_file=False" will only enable the radar objects be read in a variable
radar = ir.format_transform.mosdac_correctednc(filenamel2, save_file=False)
radar.info()
```

    Processing file:  RSSHR_11JUL2019_195339_L2B_STD.nc
    Date Time of Mosdac File RSSHR_11JUL2019_195339_L2B_STD.nc corrected successfully
    altitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	_FillValue: nan
    	units: meters
    altitude_agl: None
    antenna_transition: None
    azimuth:
    	data: <ndarray of type: float32 and shape: (3960,)>
    	_FillValue: nan
    	standard_name: ray_azimuth_angle
    	units: degrees
    	long_name: azimuth_angle_from_true_north
    	axis: radial_azimuth_coordinate
    elevation:
    	data: <ndarray of type: float32 and shape: (3960,)>
    	_FillValue: nan
    	standard_name: ray_elevation_angle
    	units: degrees
    	long_name: elevation_angle_from_horizontal_plane
    	axis: radial_azimuth_coordinate
    fields:
    	DBZ:
    		data: <ndarray of type: float32 and shape: (3960, 1600)>
    		_FillValue: 0.0
    		units: dBZ
    		standard_name: equivalent_reflectivity_factor
    		Polarization: Horizontal
    		coordinates: time range
    	VEL:
    		data: <ndarray of type: float32 and shape: (3960, 1600)>
    		_FillValue: 0.0
    		units: m/s
    		standard_name: radial_velocity_of_scatterers_ away_from_instrument
    		Polarization: Horizontal
    		coordinates: time range
    	WIDTH:
    		data: <ndarray of type: float32 and shape: (3960, 1600)>
    		_FillValue: 0.0
    		units: m/s
    		standard_name: doppler_spectrum_width
    		Polarization: Horizontal
    		coordinates: time range
    	ZDR:
    		data: <ndarray of type: float32 and shape: (3960, 1600)>
    		_FillValue: 0.0
    		units: dB
    		standard_name: log_differential_reflectivity_hv
    		Polarization: Horizontal and Vertical
    		coordinates: time range
    	PHIDP:
    		data: <ndarray of type: float32 and shape: (3960, 1600)>
    		_FillValue: 0.0
    		units: degrees
    		standard_name: differential_phase_hv
    		Polarization: Horizontal and Vertical
    		coordinates: time range
    	RHOHV:
    		data: <ndarray of type: float32 and shape: (3960, 1600)>
    		_FillValue: 0.0
    		units: 
    		standard_name: cross_correlation_ratio_hv
    		Polarization: Horizontal and Vertical
    		coordinates: time range
    fixed_angle:
    	data: <ndarray of type: float32 and shape: (11,)>
    	_FillValue: nan
    	units: degrees
    instrument_parameters: None
    latitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	_FillValue: nan
    	units: degrees_north
    longitude:
    	data: <ndarray of type: float64 and shape: (1,)>
    	_FillValue: nan
    	units: degrees_east
    nsweeps: 11
    ngates: 1600
    nrays: 3960
    radar_calibration: None
    range:
    	data: <ndarray of type: float64 and shape: (1600,)>
    	_FillValue: nan
    	standard_name: projection_range_coordinate
    	long_name: range_to_measurement_volume
    	units: meters
    	spacing_is_constant: true
    	meters_to_center_of_first_gate: true
    	axis: radial_range_coordinate
    scan_rate: None
    scan_type: ppi
    sweep_end_ray_index:
    	data: <ndarray of type: int64 and shape: (11,)>
    sweep_mode:
    	data: <ndarray of type: |S1 and shape: (11, 32)>
    sweep_number:
    	data: <ndarray of type: int32 and shape: (11,)>
    sweep_start_ray_index:
    	data: <ndarray of type: int64 and shape: (11,)>
    target_scan_rate: None
    time:
    	data: <ndarray of type: float64 and shape: (3960,)>
    	_FillValue: nan
    	standard_name: time
    	long_name: time_in_seconds_since_volume_start
    	units: seconds since 2019-07-11T19:53:39
    	calendar: gregorian
    metadata:
    	instrument_name: SHAR S-band Dual-pol DWR
    	Created using: pyiwr (Indian Weather Radar) Module developed by Researchers at SIGMA Research Lab, IIT Indore
    	version: Version 1.0
    	title: SHAR S-band DDWR data
    	institution: ISRO
    	references: Py-art_https://arm-doe.github.io/pyart/notebooks/basic_ingest_using_test_radar_object.html
    	source: DWR volume scan data
    	comment: 
    	Conventions: CF/Radial
    	field_names: DBZ, VEL, WIDTH, ZDR, PHIDP, RHOHV
    	history: DWR mosdac files (.nc) data encoded into Py-ART compatible NetCDF file
    	volume_number: 0
    	platform_type: fixed
    	instrument_type: radar
    	primary_axis: axis_z
    

## Multiple mosdac nc format file conversion to time corrected NetCDF cfradial (polar) data compatible to PyART


```python
file_path_short
file_path_long
```




    'C:\\Users\\dell\\codes\\test_data\\mosdac\\short'






    'C:\\Users\\dell\\codes\\test_data\\mosdac\\long'




```python
# Iterate over the files in the original directory
for filename in os.listdir(file_path_short):
    if filename.endswith('.nc'):
        # Get the full file path
        file_path = os.path.join(file_path_short, filename)
        ir.format_transform.mosdac_correctednc(file_path, save_file=True)
```

    Processing file:  RCTLS_03SEP2018_051827_L2B_STD.nc
    Date Time of Mosdac File RCTLS_03SEP2018_051827_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x2570059d8e0>



    Processing file:  RCTLS_03SEP2018_053343_L2B_STD.nc
    Date Time of Mosdac File RCTLS_03SEP2018_053343_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x257005f2550>



    Processing file:  RSCHR_11JUL2019_071439_L2B_STD.nc
    Date Time of Mosdac File RSCHR_11JUL2019_071439_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x25700603520>



    Processing file:  RSCHR_24MAR2022_173414_L2B_STD.nc
    Date Time of Mosdac File RSCHR_24MAR2022_173414_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x25700603e50>



    Processing file:  RSSHR_11JUL2019_193045_L2B_STD.nc
    Date Time of Mosdac File RSSHR_11JUL2019_193045_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x25700619a60>



    Processing file:  RSSHR_11JUL2019_195144_L2B_STD.nc
    Date Time of Mosdac File RSSHR_11JUL2019_195144_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x257005aa700>




```python
# Iterate over the files in the original directory
for filename in os.listdir(file_path_long):
    if filename.endswith('.nc'):
        # Get the full file path
        file_path = os.path.join(file_path_long, filename)
        ir.format_transform.mosdac_correctednc(file_path, save_file=True)
```

    Processing file:  RCTLS_03SEP2018_052448_L2B_STD.nc
    Date Time of Mosdac File RCTLS_03SEP2018_052448_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x257005ba160>



    Processing file:  RSCHR_11JUL2019_023140_L2B_STD.nc
    Date Time of Mosdac File RSCHR_11JUL2019_023140_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x257005f2d30>



    Processing file:  RSCHR_24MAR2022_004350_L2B_STD.nc
    Date Time of Mosdac File RSCHR_24MAR2022_004350_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x257005cd9a0>



    Processing file:  RSSHR_11JUL2019_193241_L2B_STD.nc
    Date Time of Mosdac File RSSHR_11JUL2019_193241_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x25700663610>



    Processing file:  RSSHR_11JUL2019_195339_L2B_STD.nc
    Date Time of Mosdac File RSSHR_11JUL2019_195339_L2B_STD.nc corrected successfully and saved in the newly added "corrected" folder in your file path
    




    <pyart.core.radar.Radar at 0x257006722b0>



## Single time corrected PyART compatible NetCDF file with multiple sweep data converted to xarray grid NetCDF file


```python
xg = ir.format_transform.sweeps2gridnc(filenamel2, grid_shape=(31, 501, 501), height=16.313, length=250, save_file=True)
```

    Processing file:  RSSHR_11JUL2019_195339_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSSHR_11JUL2019_195339_L2B_STD.nc done successfully and saved in gridded_RSSHR_11JUL2019_195339_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    


```python
xg
```




<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */

:root {
  --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
  --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
  --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
  --xr-border-color: var(--jp-border-color2, #e0e0e0);
  --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
  --xr-background-color: var(--jp-layout-color0, white);
  --xr-background-color-row-even: var(--jp-layout-color1, white);
  --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
}

html[theme=dark],
body[data-theme=dark],
body.vscode-dark {
  --xr-font-color0: rgba(255, 255, 255, 1);
  --xr-font-color2: rgba(255, 255, 255, 0.54);
  --xr-font-color3: rgba(255, 255, 255, 0.38);
  --xr-border-color: #1F1F1F;
  --xr-disabled-color: #515151;
  --xr-background-color: #111111;
  --xr-background-color-row-even: #111111;
  --xr-background-color-row-odd: #313131;
}

.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}

.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}

.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}

.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}

.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}

.xr-obj-type {
  color: var(--xr-font-color2);
}

.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 20px 20px;
}

.xr-section-item {
  display: contents;
}

.xr-section-item input {
  display: none;
}

.xr-section-item input + label {
  color: var(--xr-disabled-color);
}

.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}

.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}

.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}

.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}

.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}

.xr-section-summary-in + label:before {
  display: inline-block;
  content: '►';
  font-size: 11px;
  width: 15px;
  text-align: center;
}

.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}

.xr-section-summary-in:checked + label:before {
  content: '▼';
}

.xr-section-summary-in:checked + label > span {
  display: none;
}

.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}

.xr-section-inline-details {
  grid-column: 2 / -1;
}

.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}

.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}

.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}

.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}

.xr-preview {
  color: var(--xr-font-color3);
}

.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}

.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}

.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}

.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}

.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}

.xr-dim-list:before {
  content: '(';
}

.xr-dim-list:after {
  content: ')';
}

.xr-dim-list li:not(:last-child):after {
  content: ',';
  padding-right: 5px;
}

.xr-has-index {
  font-weight: bold;
}

.xr-var-list,
.xr-var-item {
  display: contents;
}

.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  margin-bottom: 0;
}

.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}

.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
}

.xr-var-name {
  grid-column: 1;
}

.xr-var-dims {
  grid-column: 2;
}

.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}

.xr-var-preview {
  grid-column: 4;
}

.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}

.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}

.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  background-color: var(--xr-background-color) !important;
  padding-bottom: 5px !important;
}

.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}

.xr-var-data > table {
  float: right;
}

.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}

.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}

dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}

.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}

.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}

.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}

.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt;
Dimensions:  (time: 1, z: 31, y: 501, x: 501)
Coordinates:
  * time     (time) object 2019-07-11 19:53:39.055556
  * z        (z) float64 29.0 571.8 1.115e+03 ... 1.523e+04 1.577e+04 1.631e+04
    lat      (y) float64 11.41 11.42 11.42 11.43 ... 15.87 15.88 15.89 15.9
    lon      (x) float64 77.93 77.94 77.95 77.96 ... 82.49 82.5 82.51 82.52
  * y        (y) float64 -2.5e+05 -2.49e+05 -2.48e+05 ... 2.49e+05 2.5e+05
  * x        (x) float64 -2.5e+05 -2.49e+05 -2.48e+05 ... 2.49e+05 2.5e+05
Data variables:
    DBZ      (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    VEL      (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    WIDTH    (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    ZDR      (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    PHIDP    (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    RHOHV    (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    ROI      (time, z, y, x) float32 9.26e+03 9.241e+03 ... 1.006e+04 1.007e+04</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-3f0ba2bd-220c-4753-8848-b6de41f3f7d7' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-3f0ba2bd-220c-4753-8848-b6de41f3f7d7' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>time</span>: 1</li><li><span class='xr-has-index'>z</span>: 31</li><li><span class='xr-has-index'>y</span>: 501</li><li><span class='xr-has-index'>x</span>: 501</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-79e93e7b-7e5b-43d9-aba7-4c9ac45560a0' class='xr-section-summary-in' type='checkbox'  checked><label for='section-79e93e7b-7e5b-43d9-aba7-4c9ac45560a0' class='xr-section-summary' >Coordinates: <span>(6)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>object</div><div class='xr-var-preview xr-preview'>2019-07-11 19:53:39.055556</div><input id='attrs-4aa9dafe-477d-4574-85cf-db68d1434855' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-4aa9dafe-477d-4574-85cf-db68d1434855' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-fc80ef84-f319-4181-85ea-4b192e90321b' class='xr-var-data-in' type='checkbox'><label for='data-fc80ef84-f319-4181-85ea-4b192e90321b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([cftime.DatetimeGregorian(2019, 7, 11, 19, 53, 39, 55556, has_year_zero=False)],
      dtype=object)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>z</span></div><div class='xr-var-dims'>(z)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>29.0 571.8 ... 1.577e+04 1.631e+04</div><input id='attrs-49108f8d-49a2-4be1-8ea0-5a9b41c2c560' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-49108f8d-49a2-4be1-8ea0-5a9b41c2c560' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-e885eec0-105a-4626-8425-3cb9f50c857a' class='xr-var-data-in' type='checkbox'><label for='data-e885eec0-105a-4626-8425-3cb9f50c857a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>projection_z_coordinate</dd><dt><span>long_name :</span></dt><dd>Z distance on the projection plane from the origin</dd><dt><span>axis :</span></dt><dd>Z</dd><dt><span>units :</span></dt><dd>m</dd><dt><span>positive :</span></dt><dd>up</dd></dl></div><div class='xr-var-data'><pre>array([   29. ,   571.8,  1114.6,  1657.4,  2200.2,  2743. ,  3285.8,  3828.6,
        4371.4,  4914.2,  5457. ,  5999.8,  6542.6,  7085.4,  7628.2,  8171. ,
        8713.8,  9256.6,  9799.4, 10342.2, 10885. , 11427.8, 11970.6, 12513.4,
       13056.2, 13599. , 14141.8, 14684.6, 15227.4, 15770.2, 16313. ])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lat</span></div><div class='xr-var-dims'>(y)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>11.41 11.42 11.42 ... 15.89 15.9</div><input id='attrs-eb085658-d81d-43e3-8e4b-ef101c67c171' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-eb085658-d81d-43e3-8e4b-ef101c67c171' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-99df2049-bb8a-417e-b611-9bc4d523839e' class='xr-var-data-in' type='checkbox'><label for='data-99df2049-bb8a-417e-b611-9bc4d523839e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>long_name :</span></dt><dd>latitude of grid cell center</dd><dt><span>units :</span></dt><dd>degree_N</dd><dt><span>standard_name :</span></dt><dd>Latitude</dd></dl></div><div class='xr-var-data'><pre>array([11.40613983, 11.41513042, 11.42412102, 11.43311161, 11.4421022 ,
       11.45109279, 11.46008338, 11.46907398, 11.47806457, 11.48705516,
       11.49604575, 11.50503634, 11.51402693, 11.52301752, 11.5320081 ,
       11.54099869, 11.54998928, 11.55897987, 11.56797046, 11.57696104,
       11.58595163, 11.59494222, 11.6039328 , 11.61292339, 11.62191397,
       11.63090456, 11.63989514, 11.64888573, 11.65787631, 11.6668669 ,
       11.67585748, 11.68484806, 11.69383864, 11.70282923, 11.71181981,
       11.72081039, 11.72980097, 11.73879155, 11.74778213, 11.75677271,
       11.76576329, 11.77475387, 11.78374445, 11.79273503, 11.80172561,
       11.81071619, 11.81970677, 11.82869734, 11.83768792, 11.8466785 ,
       11.85566907, 11.86465965, 11.87365023, 11.8826408 , 11.89163138,
       11.90062195, 11.90961253, 11.9186031 , 11.92759367, 11.93658425,
       11.94557482, 11.95456539, 11.96355597, 11.97254654, 11.98153711,
       11.99052768, 11.99951825, 12.00850882, 12.01749939, 12.02648996,
       12.03548053, 12.0444711 , 12.05346167, 12.06245224, 12.07144281,
       12.08043337, 12.08942394, 12.09841451, 12.10740508, 12.11639564,
       12.12538621, 12.13437677, 12.14336734, 12.1523579 , 12.16134847,
       12.17033903, 12.1793296 , 12.18832016, 12.19731072, 12.20630129,
       12.21529185, 12.22428241, 12.23327297, 12.24226354, 12.2512541 ,
       12.26024466, 12.26923522, 12.27822578, 12.28721634, 12.2962069 ,
...
       15.04730053, 15.05629097, 15.06528141, 15.07427185, 15.08326229,
       15.09225273, 15.10124317, 15.11023361, 15.11922405, 15.12821449,
       15.13720492, 15.14619536, 15.1551858 , 15.16417623, 15.17316667,
       15.18215711, 15.19114754, 15.20013798, 15.20912841, 15.21811884,
       15.22710928, 15.23609971, 15.24509014, 15.25408058, 15.26307101,
       15.27206144, 15.28105187, 15.2900423 , 15.29903273, 15.30802316,
       15.31701359, 15.32600402, 15.33499445, 15.34398488, 15.3529753 ,
       15.36196573, 15.37095616, 15.37994659, 15.38893701, 15.39792744,
       15.40691786, 15.41590829, 15.42489871, 15.43388913, 15.44287956,
       15.45186998, 15.4608604 , 15.46985083, 15.47884125, 15.48783167,
       15.49682209, 15.50581251, 15.51480293, 15.52379335, 15.53278377,
       15.54177419, 15.55076461, 15.55975503, 15.56874544, 15.57773586,
       15.58672628, 15.59571669, 15.60470711, 15.61369752, 15.62268794,
       15.63167835, 15.64066877, 15.64965918, 15.65864959, 15.66764001,
       15.67663042, 15.68562083, 15.69461124, 15.70360165, 15.71259206,
       15.72158247, 15.73057288, 15.73956329, 15.7485537 , 15.75754411,
       15.76653452, 15.77552493, 15.78451533, 15.79350574, 15.80249615,
       15.81148655, 15.82047696, 15.82946736, 15.83845777, 15.84744817,
       15.85643858, 15.86542898, 15.87441938, 15.88340978, 15.89240019,
       15.90139059])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lon</span></div><div class='xr-var-dims'>(x)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>77.93 77.94 77.95 ... 82.51 82.52</div><input id='attrs-bc6ea833-b71e-4ac5-b238-0b03ec6162b5' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-bc6ea833-b71e-4ac5-b238-0b03ec6162b5' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3ae92457-c068-4ab4-9abc-26fa05b7a14e' class='xr-var-data-in' type='checkbox'><label for='data-3ae92457-c068-4ab4-9abc-26fa05b7a14e' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>long_name :</span></dt><dd>longitude of grid cell center</dd><dt><span>units :</span></dt><dd>degree_E</dd><dt><span>standard_name :</span></dt><dd>Longitude</dd></dl></div><div class='xr-var-data'><pre>array([77.9343612 , 77.9435329 , 77.9527046 , 77.96187631, 77.97104802,
       77.98021974, 77.98939147, 77.9985632 , 78.00773493, 78.01690667,
       78.02607842, 78.03525017, 78.04442193, 78.05359369, 78.06276546,
       78.07193723, 78.081109  , 78.09028079, 78.09945257, 78.10862437,
       78.11779617, 78.12696797, 78.13613978, 78.14531159, 78.15448341,
       78.16365523, 78.17282706, 78.18199889, 78.19117073, 78.20034257,
       78.20951442, 78.21868627, 78.22785813, 78.23702999, 78.24620186,
       78.25537373, 78.26454561, 78.27371749, 78.28288938, 78.29206127,
       78.30123316, 78.31040506, 78.31957697, 78.32874888, 78.33792079,
       78.34709271, 78.35626463, 78.36543656, 78.37460849, 78.38378043,
       78.39295237, 78.40212431, 78.41129626, 78.42046822, 78.42964018,
       78.43881214, 78.44798411, 78.45715608, 78.46632805, 78.47550003,
       78.48467202, 78.49384401, 78.503016  , 78.512188  , 78.52136   ,
       78.530532  , 78.53970401, 78.54887602, 78.55804804, 78.56722006,
       78.57639209, 78.58556412, 78.59473615, 78.60390819, 78.61308023,
       78.62225227, 78.63142432, 78.64059637, 78.64976843, 78.65894049,
       78.66811255, 78.67728462, 78.68645669, 78.69562877, 78.70480085,
       78.71397293, 78.72314502, 78.73231711, 78.7414892 , 78.7506613 ,
       78.7598334 , 78.7690055 , 78.77817761, 78.78734972, 78.79652183,
       78.80569395, 78.81486607, 78.8240382 , 78.83321033, 78.84238246,
...
       81.64910605, 81.65827817, 81.66745028, 81.67662239, 81.6857945 ,
       81.6949666 , 81.7041387 , 81.7133108 , 81.72248289, 81.73165498,
       81.74082707, 81.74999915, 81.75917123, 81.76834331, 81.77751538,
       81.78668745, 81.79585951, 81.80503157, 81.81420363, 81.82337568,
       81.83254773, 81.84171977, 81.85089181, 81.86006385, 81.86923588,
       81.87840791, 81.88757994, 81.89675196, 81.90592398, 81.91509599,
       81.924268  , 81.93344   , 81.942612  , 81.951784  , 81.96095599,
       81.97012798, 81.97929997, 81.98847195, 81.99764392, 82.00681589,
       82.01598786, 82.02515982, 82.03433178, 82.04350374, 82.05267569,
       82.06184763, 82.07101957, 82.08019151, 82.08936344, 82.09853537,
       82.10770729, 82.11687921, 82.12605112, 82.13522303, 82.14439494,
       82.15356684, 82.16273873, 82.17191062, 82.18108251, 82.19025439,
       82.19942627, 82.20859814, 82.21777001, 82.22694187, 82.23611373,
       82.24528558, 82.25445743, 82.26362927, 82.27280111, 82.28197294,
       82.29114477, 82.30031659, 82.30948841, 82.31866022, 82.32783203,
       82.33700383, 82.34617563, 82.35534743, 82.36451921, 82.373691  ,
       82.38286277, 82.39203454, 82.40120631, 82.41037807, 82.41954983,
       82.42872158, 82.43789333, 82.44706507, 82.4562368 , 82.46540853,
       82.47458026, 82.48375198, 82.49292369, 82.5020954 , 82.5112671 ,
       82.5204388 ])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>y</span></div><div class='xr-var-dims'>(y)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-2.5e+05 -2.49e+05 ... 2.5e+05</div><input id='attrs-933f1708-deed-4447-855f-e4e7da28a81b' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-933f1708-deed-4447-855f-e4e7da28a81b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-cd07517a-fccf-4711-b40f-db35f9f0ff51' class='xr-var-data-in' type='checkbox'><label for='data-cd07517a-fccf-4711-b40f-db35f9f0ff51' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>projection_y_coordinate</dd><dt><span>long_name :</span></dt><dd>Y distance on the projection plane from the origin</dd><dt><span>axis :</span></dt><dd>Y</dd><dt><span>units :</span></dt><dd>m</dd></dl></div><div class='xr-var-data'><pre>array([-250000., -249000., -248000., ...,  248000.,  249000.,  250000.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>x</span></div><div class='xr-var-dims'>(x)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-2.5e+05 -2.49e+05 ... 2.5e+05</div><input id='attrs-6e6b8c51-c865-46de-847c-d254fca0cb89' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-6e6b8c51-c865-46de-847c-d254fca0cb89' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8a9901c8-0126-4c2e-929d-a3231539f3c8' class='xr-var-data-in' type='checkbox'><label for='data-8a9901c8-0126-4c2e-929d-a3231539f3c8' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>projection_x_coordinate</dd><dt><span>long_name :</span></dt><dd>X distance on the projection plane from the origin</dd><dt><span>axis :</span></dt><dd>X</dd><dt><span>units :</span></dt><dd>m</dd></dl></div><div class='xr-var-data'><pre>array([-250000., -249000., -248000., ...,  248000.,  249000.,  250000.])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-157fe078-7096-4889-866a-a1f582fb0e13' class='xr-section-summary-in' type='checkbox'  checked><label for='section-157fe078-7096-4889-866a-a1f582fb0e13' class='xr-section-summary' >Data variables: <span>(7)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>DBZ</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-71a1622b-7246-42e6-8494-13cabc6c3470' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-71a1622b-7246-42e6-8494-13cabc6c3470' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-80307bcf-f22e-411d-a0fd-caf22eee1939' class='xr-var-data-in' type='checkbox'><label for='data-80307bcf-f22e-411d-a0fd-caf22eee1939' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>dBZ</dd><dt><span>standard_name :</span></dt><dd>equivalent_reflectivity_factor</dd><dt><span>Polarization :</span></dt><dd>Horizontal</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>VEL</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-53f93b7c-db57-4997-b168-a38848bbd1bb' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-53f93b7c-db57-4997-b168-a38848bbd1bb' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-0a637941-7200-4ae6-bbf4-c404fdd5ae24' class='xr-var-data-in' type='checkbox'><label for='data-0a637941-7200-4ae6-bbf4-c404fdd5ae24' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>m/s</dd><dt><span>standard_name :</span></dt><dd>radial_velocity_of_scatterers_ away_from_instrument</dd><dt><span>Polarization :</span></dt><dd>Horizontal</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>WIDTH</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-c673058f-30f3-4132-8efd-7b8beae4501e' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-c673058f-30f3-4132-8efd-7b8beae4501e' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-3a621d8c-d1ef-41f0-a9cd-06ea12e365ab' class='xr-var-data-in' type='checkbox'><label for='data-3a621d8c-d1ef-41f0-a9cd-06ea12e365ab' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>m/s</dd><dt><span>standard_name :</span></dt><dd>doppler_spectrum_width</dd><dt><span>Polarization :</span></dt><dd>Horizontal</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>ZDR</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-9ee51182-62ee-4602-b828-57848bc2944a' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-9ee51182-62ee-4602-b828-57848bc2944a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d28fcd90-0bd7-4323-a059-80e1abf22850' class='xr-var-data-in' type='checkbox'><label for='data-d28fcd90-0bd7-4323-a059-80e1abf22850' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>dB</dd><dt><span>standard_name :</span></dt><dd>log_differential_reflectivity_hv</dd><dt><span>Polarization :</span></dt><dd>Horizontal and Vertical</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>PHIDP</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-92e0b6c6-f7d4-4bde-a346-adcf3a0406fe' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-92e0b6c6-f7d4-4bde-a346-adcf3a0406fe' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-7d44895e-e795-43c1-b34e-7b144c56f263' class='xr-var-data-in' type='checkbox'><label for='data-7d44895e-e795-43c1-b34e-7b144c56f263' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>degrees</dd><dt><span>standard_name :</span></dt><dd>differential_phase_hv</dd><dt><span>Polarization :</span></dt><dd>Horizontal and Vertical</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>RHOHV</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-7f668c5d-db6b-49aa-8cbf-e0fc87605382' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-7f668c5d-db6b-49aa-8cbf-e0fc87605382' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d4786673-a74f-47a2-9e20-22bcaad29e38' class='xr-var-data-in' type='checkbox'><label for='data-d4786673-a74f-47a2-9e20-22bcaad29e38' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd></dd><dt><span>standard_name :</span></dt><dd>cross_correlation_ratio_hv</dd><dt><span>Polarization :</span></dt><dd>Horizontal and Vertical</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>ROI</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>9.26e+03 9.241e+03 ... 1.007e+04</div><input id='attrs-7008fa09-0637-49fe-8b8e-55e5f6c4644b' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-7008fa09-0637-49fe-8b8e-55e5f6c4644b' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9fc56aff-4da6-4deb-9fcd-f6e0e16ec47b' class='xr-var-data-in' type='checkbox'><label for='data-9fc56aff-4da6-4deb-9fcd-f6e0e16ec47b' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>radius_of_influence</dd><dt><span>long_name :</span></dt><dd>Radius of influence for mapping</dd><dt><span>units :</span></dt><dd>m</dd><dt><span>least_significant_digit :</span></dt><dd>1</dd><dt><span>_FillValue :</span></dt><dd>-9999.0</dd></dl></div><div class='xr-var-data'><pre>array([[[[ 9259.571,  9241.074,  9222.613, ...,  9222.613,  9241.074,
           9259.571],
         [ 9241.074,  9222.539,  9204.042, ...,  9204.042,  9222.539,
           9241.074],
         [ 9222.613,  9204.042,  9185.507, ...,  9185.507,  9204.042,
           9222.613],
         ...,
         [ 9222.613,  9204.042,  9185.507, ...,  9185.507,  9204.042,
           9222.613],
         [ 9241.074,  9222.539,  9204.042, ...,  9204.042,  9222.539,
           9241.074],
         [ 9259.571,  9241.074,  9222.613, ...,  9222.613,  9241.074,
           9259.571]],

        [[ 9286.712,  9268.214,  9249.754, ...,  9249.754,  9268.214,
           9286.712],
         [ 9268.214,  9249.679,  9231.182, ...,  9231.182,  9249.679,
           9268.214],
         [ 9249.754,  9231.182,  9212.646, ...,  9212.646,  9231.182,
           9249.754],
...
         [10009.674,  9991.102,  9972.566, ...,  9972.566,  9991.102,
          10009.674],
         [10028.134, 10009.6  ,  9991.102, ...,  9991.102, 10009.6  ,
          10028.134],
         [10046.632, 10028.134, 10009.674, ..., 10009.674, 10028.134,
          10046.632]],

        [[10073.771, 10055.274, 10036.813, ..., 10036.813, 10055.274,
          10073.771],
         [10055.274, 10036.739, 10018.241, ..., 10018.241, 10036.739,
          10055.274],
         [10036.813, 10018.241,  9999.707, ...,  9999.707, 10018.241,
          10036.813],
         ...,
         [10036.813, 10018.241,  9999.707, ...,  9999.707, 10018.241,
          10036.813],
         [10055.274, 10036.739, 10018.241, ..., 10018.241, 10036.739,
          10055.274],
         [10073.771, 10055.274, 10036.813, ..., 10036.813, 10055.274,
          10073.771]]]], dtype=float32)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-001feff7-b42d-43bd-b5f6-f83642a37073' class='xr-section-summary-in' type='checkbox'  ><label for='section-001feff7-b42d-43bd-b5f6-f83642a37073' class='xr-section-summary' >Indexes: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>time</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-9921f7e1-0f32-4179-a906-a8571c8a04dd' class='xr-index-data-in' type='checkbox'/><label for='index-9921f7e1-0f32-4179-a906-a8571c8a04dd' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(CFTimeIndex([2019-07-11 19:53:39.055556],
            dtype=&#x27;object&#x27;, length=1, calendar=&#x27;standard&#x27;, freq=None))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>z</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-a5c8e2d5-24c5-4d0f-9be0-848019094b34' class='xr-index-data-in' type='checkbox'/><label for='index-a5c8e2d5-24c5-4d0f-9be0-848019094b34' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([              29.0,              571.8,             1114.6,
              1657.3999999999999,             2200.2,             2743.0,
              3285.7999999999997, 3828.5999999999995,             4371.4,
                          4914.2,             5457.0,  5999.799999999999,
               6542.599999999999,             7085.4,  7628.199999999999,
               8170.999999999999,             8713.8,  9256.599999999999,
                          9799.4, 10342.199999999999,            10885.0,
                         11427.8, 11970.599999999999,            12513.4,
              13056.199999999999, 13598.999999999998,            14141.8,
              14684.599999999999, 15227.399999999998, 15770.199999999999,
              16312.999999999998],
             dtype=&#x27;float64&#x27;, name=&#x27;z&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>y</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-8faf1a4f-ea81-432d-a0db-e9c653fabfa1' class='xr-index-data-in' type='checkbox'/><label for='index-8faf1a4f-ea81-432d-a0db-e9c653fabfa1' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([-250000.0, -249000.0, -248000.0, -247000.0, -246000.0, -245000.0,
              -244000.0, -243000.0, -242000.0, -241000.0,
              ...
               241000.0,  242000.0,  243000.0,  244000.0,  245000.0,  246000.0,
               247000.0,  248000.0,  249000.0,  250000.0],
             dtype=&#x27;float64&#x27;, name=&#x27;y&#x27;, length=501))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>x</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-10b0dc86-5253-494a-80ff-06a11a167ec1' class='xr-index-data-in' type='checkbox'/><label for='index-10b0dc86-5253-494a-80ff-06a11a167ec1' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([-250000.0, -249000.0, -248000.0, -247000.0, -246000.0, -245000.0,
              -244000.0, -243000.0, -242000.0, -241000.0,
              ...
               241000.0,  242000.0,  243000.0,  244000.0,  245000.0,  246000.0,
               247000.0,  248000.0,  249000.0,  250000.0],
             dtype=&#x27;float64&#x27;, name=&#x27;x&#x27;, length=501))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-4b1d4da3-ef12-4a5c-8959-b61120f76b40' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-4b1d4da3-ef12-4a5c-8959-b61120f76b40' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>




```python
xg = ir.format_transform.sweeps2gridnc(filenames3, grid_shape=(31, 501, 501), height=16.313, length=250, save_file=False)
xg
```

    Processing file:  RCTLS_03SEP2018_051827_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RCTLS_03SEP2018_051827_L2B_STD.nc done successfully
    




<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */

:root {
  --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
  --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
  --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
  --xr-border-color: var(--jp-border-color2, #e0e0e0);
  --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
  --xr-background-color: var(--jp-layout-color0, white);
  --xr-background-color-row-even: var(--jp-layout-color1, white);
  --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
}

html[theme=dark],
body[data-theme=dark],
body.vscode-dark {
  --xr-font-color0: rgba(255, 255, 255, 1);
  --xr-font-color2: rgba(255, 255, 255, 0.54);
  --xr-font-color3: rgba(255, 255, 255, 0.38);
  --xr-border-color: #1F1F1F;
  --xr-disabled-color: #515151;
  --xr-background-color: #111111;
  --xr-background-color-row-even: #111111;
  --xr-background-color-row-odd: #313131;
}

.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}

.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}

.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}

.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}

.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}

.xr-obj-type {
  color: var(--xr-font-color2);
}

.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 20px 20px;
}

.xr-section-item {
  display: contents;
}

.xr-section-item input {
  display: none;
}

.xr-section-item input + label {
  color: var(--xr-disabled-color);
}

.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}

.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}

.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}

.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}

.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}

.xr-section-summary-in + label:before {
  display: inline-block;
  content: '►';
  font-size: 11px;
  width: 15px;
  text-align: center;
}

.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}

.xr-section-summary-in:checked + label:before {
  content: '▼';
}

.xr-section-summary-in:checked + label > span {
  display: none;
}

.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}

.xr-section-inline-details {
  grid-column: 2 / -1;
}

.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}

.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}

.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}

.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}

.xr-preview {
  color: var(--xr-font-color3);
}

.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}

.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}

.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}

.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}

.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}

.xr-dim-list:before {
  content: '(';
}

.xr-dim-list:after {
  content: ')';
}

.xr-dim-list li:not(:last-child):after {
  content: ',';
  padding-right: 5px;
}

.xr-has-index {
  font-weight: bold;
}

.xr-var-list,
.xr-var-item {
  display: contents;
}

.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  margin-bottom: 0;
}

.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}

.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
}

.xr-var-name {
  grid-column: 1;
}

.xr-var-dims {
  grid-column: 2;
}

.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}

.xr-var-preview {
  grid-column: 4;
}

.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}

.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}

.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  background-color: var(--xr-background-color) !important;
  padding-bottom: 5px !important;
}

.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}

.xr-var-data > table {
  float: right;
}

.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}

.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}

dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}

.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}

.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}

.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}

.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt;
Dimensions:  (time: 1, z: 31, y: 501, x: 501)
Coordinates:
  * time     (time) object 2018-09-03 05:18:27.055556
  * z        (z) float64 27.0 569.9 1.113e+03 ... 1.523e+04 1.577e+04 1.631e+04
    lat      (y) float64 6.283 6.292 6.301 6.31 ... 10.75 10.76 10.77 10.78
    lon      (x) float64 74.6 74.61 74.62 74.63 74.64 ... 79.1 79.11 79.12 79.13
  * y        (y) float64 -2.5e+05 -2.49e+05 -2.48e+05 ... 2.49e+05 2.5e+05
  * x        (x) float64 -2.5e+05 -2.49e+05 -2.48e+05 ... 2.49e+05 2.5e+05
Data variables:
    DBZ      (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    VEL      (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    WIDTH    (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    ZDR      (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    PHIDP    (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    RHOHV    (time, z, y, x) float32 nan nan nan nan nan ... nan nan nan nan nan
    ROI      (time, z, y, x) float32 9.259e+03 9.241e+03 ... 1.006e+04 1.007e+04</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-38ccd303-e953-4bf5-af6f-bb3b5e047f34' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-38ccd303-e953-4bf5-af6f-bb3b5e047f34' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>time</span>: 1</li><li><span class='xr-has-index'>z</span>: 31</li><li><span class='xr-has-index'>y</span>: 501</li><li><span class='xr-has-index'>x</span>: 501</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-017b9c74-52c9-4257-b2da-e673d8f68670' class='xr-section-summary-in' type='checkbox'  checked><label for='section-017b9c74-52c9-4257-b2da-e673d8f68670' class='xr-section-summary' >Coordinates: <span>(6)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>time</span></div><div class='xr-var-dims'>(time)</div><div class='xr-var-dtype'>object</div><div class='xr-var-preview xr-preview'>2018-09-03 05:18:27.055556</div><input id='attrs-b5975e75-30ec-4aa2-ac8f-2a479be33494' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-b5975e75-30ec-4aa2-ac8f-2a479be33494' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-66aedb2b-99eb-4dff-824b-281b59ad2a20' class='xr-var-data-in' type='checkbox'><label for='data-66aedb2b-99eb-4dff-824b-281b59ad2a20' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>array([cftime.DatetimeGregorian(2018, 9, 3, 5, 18, 27, 55556, has_year_zero=False)],
      dtype=object)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>z</span></div><div class='xr-var-dims'>(z)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>27.0 569.9 ... 1.577e+04 1.631e+04</div><input id='attrs-090b2b0e-82c4-42c6-baad-d107f42305b1' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-090b2b0e-82c4-42c6-baad-d107f42305b1' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6f18213d-2661-45c7-81cb-15a9f21bd426' class='xr-var-data-in' type='checkbox'><label for='data-6f18213d-2661-45c7-81cb-15a9f21bd426' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>projection_z_coordinate</dd><dt><span>long_name :</span></dt><dd>Z distance on the projection plane from the origin</dd><dt><span>axis :</span></dt><dd>Z</dd><dt><span>units :</span></dt><dd>m</dd><dt><span>positive :</span></dt><dd>up</dd></dl></div><div class='xr-var-data'><pre>array([   27.      ,   569.866667,  1112.733333,  1655.6     ,  2198.466667,
        2741.333333,  3284.2     ,  3827.066667,  4369.933333,  4912.8     ,
        5455.666667,  5998.533333,  6541.4     ,  7084.266667,  7627.133333,
        8170.      ,  8712.866667,  9255.733333,  9798.6     , 10341.466667,
       10884.333333, 11427.2     , 11970.066667, 12512.933333, 13055.8     ,
       13598.666667, 14141.533333, 14684.4     , 15227.266667, 15770.133333,
       16313.      ])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lat</span></div><div class='xr-var-dims'>(y)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>6.283 6.292 6.301 ... 10.77 10.78</div><input id='attrs-ea73f74d-1e9a-4141-9272-6da641d71bf4' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-ea73f74d-1e9a-4141-9272-6da641d71bf4' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-18955d0a-05b1-4851-adcd-df45cad4df60' class='xr-var-data-in' type='checkbox'><label for='data-18955d0a-05b1-4851-adcd-df45cad4df60' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>long_name :</span></dt><dd>latitude of grid cell center</dd><dt><span>units :</span></dt><dd>degree_N</dd><dt><span>standard_name :</span></dt><dd>Latitude</dd></dl></div><div class='xr-var-data'><pre>array([ 6.28308311,  6.29207391,  6.30106472,  6.31005553,  6.31904634,
        6.32803714,  6.33702795,  6.34601876,  6.35500956,  6.36400037,
        6.37299117,  6.38198198,  6.39097279,  6.39996359,  6.4089544 ,
        6.4179452 ,  6.42693601,  6.43592681,  6.44491762,  6.45390842,
        6.46289923,  6.47189003,  6.48088083,  6.48987164,  6.49886244,
        6.50785324,  6.51684405,  6.52583485,  6.53482565,  6.54381646,
        6.55280726,  6.56179806,  6.57078886,  6.57977966,  6.58877046,
        6.59776127,  6.60675207,  6.61574287,  6.62473367,  6.63372447,
        6.64271527,  6.65170607,  6.66069687,  6.66968767,  6.67867847,
        6.68766927,  6.69666007,  6.70565087,  6.71464167,  6.72363247,
        6.73262326,  6.74161406,  6.75060486,  6.75959566,  6.76858646,
        6.77757725,  6.78656805,  6.79555885,  6.80454964,  6.81354044,
        6.82253124,  6.83152203,  6.84051283,  6.84950363,  6.85849442,
        6.86748522,  6.87647601,  6.88546681,  6.8944576 ,  6.9034484 ,
        6.91243919,  6.92142999,  6.93042078,  6.93941158,  6.94840237,
        6.95739316,  6.96638396,  6.97537475,  6.98436554,  6.99335634,
        7.00234713,  7.01133792,  7.02032871,  7.0293195 ,  7.0383103 ,
        7.04730109,  7.05629188,  7.06528267,  7.07427346,  7.08326425,
        7.09225504,  7.10124583,  7.11023662,  7.11922741,  7.1282182 ,
        7.13720899,  7.14619978,  7.15519057,  7.16418136,  7.17317215,
...
        9.92434334,  9.93333406,  9.94232478,  9.9513155 ,  9.96030622,
        9.96929694,  9.97828765,  9.98727837,  9.99626909, 10.00525981,
       10.01425053, 10.02324124, 10.03223196, 10.04122268, 10.05021339,
       10.05920411, 10.06819482, 10.07718554, 10.08617626, 10.09516697,
       10.10415769, 10.1131484 , 10.12213912, 10.13112983, 10.14012054,
       10.14911126, 10.15810197, 10.16709268, 10.1760834 , 10.18507411,
       10.19406482, 10.20305553, 10.21204625, 10.22103696, 10.23002767,
       10.23901838, 10.24800909, 10.2569998 , 10.26599051, 10.27498122,
       10.28397193, 10.29296264, 10.30195335, 10.31094406, 10.31993477,
       10.32892548, 10.33791618, 10.34690689, 10.3558976 , 10.36488831,
       10.37387901, 10.38286972, 10.39186043, 10.40085113, 10.40984184,
       10.41883255, 10.42782325, 10.43681396, 10.44580466, 10.45479537,
       10.46378607, 10.47277678, 10.48176748, 10.49075819, 10.49974889,
       10.50873959, 10.5177303 , 10.526721  , 10.5357117 , 10.5447024 ,
       10.5536931 , 10.56268381, 10.57167451, 10.58066521, 10.58965591,
       10.59864661, 10.60763731, 10.61662801, 10.62561871, 10.63460941,
       10.64360011, 10.65259081, 10.66158151, 10.67057221, 10.67956291,
       10.6885536 , 10.6975443 , 10.706535  , 10.7155257 , 10.72451639,
       10.73350709, 10.74249779, 10.75148848, 10.76047918, 10.76946987,
       10.77846057])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lon</span></div><div class='xr-var-dims'>(x)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>74.6 74.61 74.62 ... 79.12 79.13</div><input id='attrs-33ec498b-bf2b-4f7d-9bb4-340f5ffac02a' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-33ec498b-bf2b-4f7d-9bb4-340f5ffac02a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-51f8f832-f51b-49bc-bbfe-9d8ff7960c32' class='xr-var-data-in' type='checkbox'><label for='data-51f8f832-f51b-49bc-bbfe-9d8ff7960c32' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>long_name :</span></dt><dd>longitude of grid cell center</dd><dt><span>units :</span></dt><dd>degree_E</dd><dt><span>standard_name :</span></dt><dd>Longitude</dd></dl></div><div class='xr-var-data'><pre>array([74.6043822 , 74.61342732, 74.62247244, 74.63151756, 74.64056268,
       74.64960781, 74.65865293, 74.66769806, 74.67674319, 74.68578832,
       74.69483345, 74.70387859, 74.71292372, 74.72196886, 74.731014  ,
       74.74005914, 74.74910429, 74.75814943, 74.76719458, 74.77623973,
       74.78528488, 74.79433003, 74.80337519, 74.81242034, 74.8214655 ,
       74.83051066, 74.83955582, 74.84860098, 74.85764614, 74.86669131,
       74.87573648, 74.88478165, 74.89382682, 74.90287199, 74.91191716,
       74.92096234, 74.93000752, 74.9390527 , 74.94809788, 74.95714306,
       74.96618824, 74.97523343, 74.98427861, 74.9933238 , 75.00236899,
       75.01141418, 75.02045937, 75.02950457, 75.03854976, 75.04759496,
       75.05664016, 75.06568536, 75.07473056, 75.08377577, 75.09282097,
       75.10186618, 75.11091138, 75.11995659, 75.1290018 , 75.13804702,
       75.14709223, 75.15613744, 75.16518266, 75.17422788, 75.1832731 ,
       75.19231832, 75.20136354, 75.21040876, 75.21945399, 75.22849921,
       75.23754444, 75.24658967, 75.2556349 , 75.26468013, 75.27372536,
       75.2827706 , 75.29181583, 75.30086107, 75.30990631, 75.31895155,
       75.32799679, 75.33704203, 75.34608727, 75.35513252, 75.36417776,
       75.37322301, 75.38226826, 75.3913135 , 75.40035875, 75.40940401,
       75.41844926, 75.42749451, 75.43653977, 75.44558502, 75.45463028,
       75.46367554, 75.4727208 , 75.48176606, 75.49081132, 75.49985659,
...
       78.26772446, 78.27676972, 78.28581498, 78.29486023, 78.30390549,
       78.31295074, 78.32199599, 78.33104125, 78.3400865 , 78.34913174,
       78.35817699, 78.36722224, 78.37626748, 78.38531273, 78.39435797,
       78.40340321, 78.41244845, 78.42149369, 78.43053893, 78.43958417,
       78.4486294 , 78.45767464, 78.46671987, 78.4757651 , 78.48481033,
       78.49385556, 78.50290079, 78.51194601, 78.52099124, 78.53003646,
       78.53908168, 78.5481269 , 78.55717212, 78.56621734, 78.57526256,
       78.58430777, 78.59335298, 78.6023982 , 78.61144341, 78.62048862,
       78.62953382, 78.63857903, 78.64762423, 78.65666944, 78.66571464,
       78.67475984, 78.68380504, 78.69285024, 78.70189543, 78.71094063,
       78.71998582, 78.72903101, 78.7380762 , 78.74712139, 78.75616657,
       78.76521176, 78.77425694, 78.78330212, 78.7923473 , 78.80139248,
       78.81043766, 78.81948284, 78.82852801, 78.83757318, 78.84661835,
       78.85566352, 78.86470869, 78.87375386, 78.88279902, 78.89184418,
       78.90088934, 78.9099345 , 78.91897966, 78.92802481, 78.93706997,
       78.94611512, 78.95516027, 78.96420542, 78.97325057, 78.98229571,
       78.99134086, 79.000386  , 79.00943114, 79.01847628, 79.02752141,
       79.03656655, 79.04561168, 79.05465681, 79.06370194, 79.07274707,
       79.08179219, 79.09083732, 79.09988244, 79.10892756, 79.11797268,
       79.1270178 ])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>y</span></div><div class='xr-var-dims'>(y)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-2.5e+05 -2.49e+05 ... 2.5e+05</div><input id='attrs-297b20e2-1554-4e17-bebd-6083f3130e01' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-297b20e2-1554-4e17-bebd-6083f3130e01' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-b3e0b05b-4658-464d-998e-09f3d88fddd7' class='xr-var-data-in' type='checkbox'><label for='data-b3e0b05b-4658-464d-998e-09f3d88fddd7' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>projection_y_coordinate</dd><dt><span>long_name :</span></dt><dd>Y distance on the projection plane from the origin</dd><dt><span>axis :</span></dt><dd>Y</dd><dt><span>units :</span></dt><dd>m</dd></dl></div><div class='xr-var-data'><pre>array([-250000., -249000., -248000., ...,  248000.,  249000.,  250000.])</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>x</span></div><div class='xr-var-dims'>(x)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>-2.5e+05 -2.49e+05 ... 2.5e+05</div><input id='attrs-e9bef9ba-3062-40f4-900e-9fe1b5062791' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-e9bef9ba-3062-40f4-900e-9fe1b5062791' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-82575eae-2b3c-43ed-b405-357638a81429' class='xr-var-data-in' type='checkbox'><label for='data-82575eae-2b3c-43ed-b405-357638a81429' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>projection_x_coordinate</dd><dt><span>long_name :</span></dt><dd>X distance on the projection plane from the origin</dd><dt><span>axis :</span></dt><dd>X</dd><dt><span>units :</span></dt><dd>m</dd></dl></div><div class='xr-var-data'><pre>array([-250000., -249000., -248000., ...,  248000.,  249000.,  250000.])</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-4c48cd7e-b9a3-4113-9600-66234cc0fce5' class='xr-section-summary-in' type='checkbox'  checked><label for='section-4c48cd7e-b9a3-4113-9600-66234cc0fce5' class='xr-section-summary' >Data variables: <span>(7)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>DBZ</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-fd2e8a1e-fc5d-4554-9a55-5ac82f773085' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-fd2e8a1e-fc5d-4554-9a55-5ac82f773085' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-9ebad9cf-71cb-457a-8fce-240ac9fc7bc5' class='xr-var-data-in' type='checkbox'><label for='data-9ebad9cf-71cb-457a-8fce-240ac9fc7bc5' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>dBZ</dd><dt><span>standard_name :</span></dt><dd>equivalent_reflectivity_factor</dd><dt><span>Polarization :</span></dt><dd>Horizontal</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>VEL</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-9aa5644e-3b37-43ba-ab1a-27200dc5c45f' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-9aa5644e-3b37-43ba-ab1a-27200dc5c45f' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-8cfbf36e-851b-477e-867e-16dbee17abbe' class='xr-var-data-in' type='checkbox'><label for='data-8cfbf36e-851b-477e-867e-16dbee17abbe' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>m/s</dd><dt><span>standard_name :</span></dt><dd>radial_velocity_of_scatterers_ away_from_instrument</dd><dt><span>Polarization :</span></dt><dd>Horizontal</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>WIDTH</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-e78ebb99-29d9-4d80-b0aa-837be617b2db' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-e78ebb99-29d9-4d80-b0aa-837be617b2db' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6cb407d0-f376-4a86-829a-ce53b832c1cc' class='xr-var-data-in' type='checkbox'><label for='data-6cb407d0-f376-4a86-829a-ce53b832c1cc' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>m/s</dd><dt><span>standard_name :</span></dt><dd>doppler_spectrum_width</dd><dt><span>Polarization :</span></dt><dd>Horizontal</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>ZDR</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-dceaddd4-665b-4437-a6c3-f7e384be31e9' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-dceaddd4-665b-4437-a6c3-f7e384be31e9' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-d1e28e18-3af0-45cf-9eaa-0e37988a17ed' class='xr-var-data-in' type='checkbox'><label for='data-d1e28e18-3af0-45cf-9eaa-0e37988a17ed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>dB</dd><dt><span>standard_name :</span></dt><dd>log_differential_reflectivity_hv</dd><dt><span>Polarization :</span></dt><dd>Horizontal and Vertical</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>PHIDP</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-b3250eb8-9d36-47de-ab6c-d1ac736f145c' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-b3250eb8-9d36-47de-ab6c-d1ac736f145c' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6dcb4646-cc65-405a-8fde-02a1b72741ed' class='xr-var-data-in' type='checkbox'><label for='data-6dcb4646-cc65-405a-8fde-02a1b72741ed' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd>degrees</dd><dt><span>standard_name :</span></dt><dd>differential_phase_hv</dd><dt><span>Polarization :</span></dt><dd>Horizontal and Vertical</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>RHOHV</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>nan nan nan nan ... nan nan nan nan</div><input id='attrs-7ae11f31-e114-4075-b983-fa35f6739c22' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-7ae11f31-e114-4075-b983-fa35f6739c22' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-dc8f1e60-1237-403b-b5bb-ae3a89c8c659' class='xr-var-data-in' type='checkbox'><label for='data-dc8f1e60-1237-403b-b5bb-ae3a89c8c659' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>_FillValue :</span></dt><dd>0.0</dd><dt><span>units :</span></dt><dd></dd><dt><span>standard_name :</span></dt><dd>cross_correlation_ratio_hv</dd><dt><span>Polarization :</span></dt><dd>Horizontal and Vertical</dd><dt><span>coordinates :</span></dt><dd>time range</dd></dl></div><div class='xr-var-data'><pre>array([[[[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
...
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]],

        [[nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         ...,
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan],
         [nan, nan, nan, ..., nan, nan, nan]]]], dtype=float32)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>ROI</span></div><div class='xr-var-dims'>(time, z, y, x)</div><div class='xr-var-dtype'>float32</div><div class='xr-var-preview xr-preview'>9.259e+03 9.241e+03 ... 1.007e+04</div><input id='attrs-44ab5485-6fe5-43ed-b9af-beeb1a9430ca' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-44ab5485-6fe5-43ed-b9af-beeb1a9430ca' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-17f0278f-78dc-4497-a2ba-9f1d78029825' class='xr-var-data-in' type='checkbox'><label for='data-17f0278f-78dc-4497-a2ba-9f1d78029825' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>radius_of_influence</dd><dt><span>long_name :</span></dt><dd>Radius of influence for mapping</dd><dt><span>units :</span></dt><dd>m</dd><dt><span>least_significant_digit :</span></dt><dd>1</dd><dt><span>_FillValue :</span></dt><dd>-9999.0</dd></dl></div><div class='xr-var-data'><pre>array([[[[ 9259.472,  9240.974,  9222.514, ...,  9222.514,  9240.974,
           9259.472],
         [ 9240.974,  9222.439,  9203.941, ...,  9203.941,  9222.439,
           9240.974],
         [ 9222.514,  9203.941,  9185.406, ...,  9185.406,  9203.941,
           9222.514],
         ...,
         [ 9222.514,  9203.941,  9185.406, ...,  9185.406,  9203.941,
           9222.514],
         [ 9240.974,  9222.439,  9203.941, ...,  9203.941,  9222.439,
           9240.974],
         [ 9259.472,  9240.974,  9222.514, ...,  9222.514,  9240.974,
           9259.472]],

        [[ 9286.615,  9268.117,  9249.657, ...,  9249.657,  9268.117,
           9286.615],
         [ 9268.117,  9249.582,  9231.085, ...,  9231.085,  9249.582,
           9268.117],
         [ 9249.657,  9231.085,  9212.55 , ...,  9212.55 ,  9231.085,
           9249.657],
...
         [10009.67 ,  9991.099,  9972.563, ...,  9972.563,  9991.099,
          10009.67 ],
         [10028.131, 10009.596,  9991.099, ...,  9991.099, 10009.596,
          10028.131],
         [10046.628, 10028.131, 10009.67 , ..., 10009.67 , 10028.131,
          10046.628]],

        [[10073.771, 10055.273, 10036.813, ..., 10036.813, 10055.273,
          10073.771],
         [10055.273, 10036.739, 10018.241, ..., 10018.241, 10036.739,
          10055.273],
         [10036.813, 10018.241,  9999.707, ...,  9999.707, 10018.241,
          10036.813],
         ...,
         [10036.813, 10018.241,  9999.707, ...,  9999.707, 10018.241,
          10036.813],
         [10055.273, 10036.739, 10018.241, ..., 10018.241, 10036.739,
          10055.273],
         [10073.771, 10055.273, 10036.813, ..., 10036.813, 10055.273,
          10073.771]]]], dtype=float32)</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-7dda368c-7ad0-4bca-8ef1-461a4d96c45d' class='xr-section-summary-in' type='checkbox'  ><label for='section-7dda368c-7ad0-4bca-8ef1-461a4d96c45d' class='xr-section-summary' >Indexes: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>time</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-ef9562d4-66d3-4a86-9ae4-2949d15abe2a' class='xr-index-data-in' type='checkbox'/><label for='index-ef9562d4-66d3-4a86-9ae4-2949d15abe2a' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(CFTimeIndex([2018-09-03 05:18:27.055556],
            dtype=&#x27;object&#x27;, length=1, calendar=&#x27;standard&#x27;, freq=None))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>z</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-d8a977c4-53cf-47b9-b56b-9d7d01e751ec' class='xr-index-data-in' type='checkbox'/><label for='index-d8a977c4-53cf-47b9-b56b-9d7d01e751ec' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([              27.0,  569.8666666666666, 1112.7333333333331,
              1655.5999999999997, 2198.4666666666662,  2741.333333333333,
              3284.1999999999994, 3827.0666666666657, 4369.9333333333325,
               4912.799999999999,  5455.666666666666,  5998.533333333332,
               6541.399999999999, 7084.2666666666655,  7627.133333333331,
               8169.999999999998,  8712.866666666665,  9255.733333333332,
               9798.599999999999, 10341.466666666665, 10884.333333333332,
              11427.199999999997, 11970.066666666664,  12512.93333333333,
              13055.799999999997, 13598.666666666664, 14141.533333333331,
              14684.399999999998, 15227.266666666663,  15770.13333333333,
              16312.999999999998],
             dtype=&#x27;float64&#x27;, name=&#x27;z&#x27;))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>y</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-18c657c5-5135-4af0-9120-0f1b11296687' class='xr-index-data-in' type='checkbox'/><label for='index-18c657c5-5135-4af0-9120-0f1b11296687' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([-250000.0, -249000.0, -248000.0, -247000.0, -246000.0, -245000.0,
              -244000.0, -243000.0, -242000.0, -241000.0,
              ...
               241000.0,  242000.0,  243000.0,  244000.0,  245000.0,  246000.0,
               247000.0,  248000.0,  249000.0,  250000.0],
             dtype=&#x27;float64&#x27;, name=&#x27;y&#x27;, length=501))</pre></div></li><li class='xr-var-item'><div class='xr-index-name'><div>x</div></div><div class='xr-index-preview'>PandasIndex</div><div></div><input id='index-c9234384-b9e8-4c80-b93b-7956baae12fe' class='xr-index-data-in' type='checkbox'/><label for='index-c9234384-b9e8-4c80-b93b-7956baae12fe' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(Float64Index([-250000.0, -249000.0, -248000.0, -247000.0, -246000.0, -245000.0,
              -244000.0, -243000.0, -242000.0, -241000.0,
              ...
               241000.0,  242000.0,  243000.0,  244000.0,  245000.0,  246000.0,
               247000.0,  248000.0,  249000.0,  250000.0],
             dtype=&#x27;float64&#x27;, name=&#x27;x&#x27;, length=501))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-9dfc17fa-93ff-4004-aacd-221ac4df7214' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-9dfc17fa-93ff-4004-aacd-221ac4df7214' class='xr-section-summary'  title='Expand/collapse section'>Attributes: <span>(0)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'></dl></div></li></ul></div></div>



## Multiple time corrected PyART compatible NetCDF file with multiple sweep data converted to xarray grid NetCDF file


```python
file_path_short
file_path_long
```




    'C:\\Users\\dell\\codes\\test_data\\mosdac\\short'






    'C:\\Users\\dell\\codes\\test_data\\mosdac\\long'




```python
# Iterate over the files in the original directory
for filename in os.listdir(file_path_short):
    if filename.endswith('.nc'):
        # Get the full file path
        file_path = os.path.join(file_path_short, filename)
        xg=ir.format_transform.sweeps2gridnc(file_path, grid_shape=(31, 501, 501), height=16.313, length=250, save_file=True)
```

    Processing file:  RCTLS_03SEP2018_051827_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RCTLS_03SEP2018_051827_L2B_STD.nc done successfully and saved in gridded_RCTLS_03SEP2018_051827_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RCTLS_03SEP2018_053343_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RCTLS_03SEP2018_053343_L2B_STD.nc done successfully and saved in gridded_RCTLS_03SEP2018_053343_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSCHR_11JUL2019_071439_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSCHR_11JUL2019_071439_L2B_STD.nc done successfully and saved in gridded_RSCHR_11JUL2019_071439_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSCHR_24MAR2022_173414_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSCHR_24MAR2022_173414_L2B_STD.nc done successfully and saved in gridded_RSCHR_24MAR2022_173414_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSSHR_11JUL2019_193045_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSSHR_11JUL2019_193045_L2B_STD.nc done successfully and saved in gridded_RSSHR_11JUL2019_193045_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSSHR_11JUL2019_195144_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSSHR_11JUL2019_195144_L2B_STD.nc done successfully and saved in gridded_RSSHR_11JUL2019_195144_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    


```python
# Iterate over the files in the original directory
for filename in os.listdir(file_path_long):
    if filename.endswith('.nc'):
        # Get the full file path
        file_path = os.path.join(file_path_long, filename)
        xg=ir.format_transform.sweeps2gridnc(file_path, grid_shape=(31, 501, 501), height=16.313, length=250, save_file=True)
```

    Processing file:  RCTLS_03SEP2018_052448_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RCTLS_03SEP2018_052448_L2B_STD.nc done successfully and saved in gridded_RCTLS_03SEP2018_052448_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSCHR_11JUL2019_023140_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSCHR_11JUL2019_023140_L2B_STD.nc done successfully and saved in gridded_RSCHR_11JUL2019_023140_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSCHR_24MAR2022_004350_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSCHR_24MAR2022_004350_L2B_STD.nc done successfully and saved in gridded_RSCHR_24MAR2022_004350_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSSHR_11JUL2019_193241_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSSHR_11JUL2019_193241_L2B_STD.nc done successfully and saved in gridded_RSSHR_11JUL2019_193241_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    Processing file:  RSSHR_11JUL2019_195339_L2B_STD.nc
    Xarray gridding of volumetric sweeps of radar PPI scan file: RSSHR_11JUL2019_195339_L2B_STD.nc done successfully and saved in gridded_RSSHR_11JUL2019_195339_L2B_ST.nc in the newly added "gridded_radar_ncfiles" folder in your file path
    


```python

```
