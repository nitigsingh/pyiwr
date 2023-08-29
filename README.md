

<p align="center">
  <img src="pyiwr.png" alt="pyiwr" width="50%">
</p>






# pyiwr

pyiwr is an advanced open-source library developed by researchers at the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw ISRO Doppler Weather Radar (DWR) data files and Restructure dual-pol radar ISRO-DWR NetCDF files into Py-ART compatible NetCDF files. pyiwr also provides a range of useful tools and visualization functions to facilitate working with and analyzing weather radar data. In addition, for further information, please consult the documentation available at https://nitigsingh.github.io/pyiwr.

## Features

- Converts raw ISRO Doppler Weather Radar (DWR) data files into Py-ART compatible NetCDF files.
- Restructures dual-pol dwr NetCDF files with missing data moments and attributes into Py-ART compatible NetCDF files.
- Converts radial sweeps format data into cartesian gridded data NetCDF files.
- Provides convenient tools for data processing and analysis.
- Offers visualization functions for better understanding and interpretation of radar data.

## Installation

pyiwr can be installed as:
```shell
conda create -n pyiwr python=3.9 jupyter git -c conda-forge
conda activate pyiwr
pip install git+https://github.com/nitigsingh/pyiwr.git
```

## Note:
As an active project, pyiwr seeks contributions from the research community, making it a dynamic and collaborative toolkit for weather radar research and applications. Future work includes implementing advanced data processing algorithms like quality control, precipitation type classifications and radar Quantitative Precipitation Estimation (QPE) etc.

