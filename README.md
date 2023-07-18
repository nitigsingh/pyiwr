![SIGMA](SIGMA.png)


# Py-SRT

Py-SRT is an advanced open-source library developed by researchers at SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw Doppler Weather Radar (DWR) files into Py-ART compatible NetCDF files. Py-SRT also provides a range of useful tools and visualization functions to facilitate working with weather radar data.

## Features

- Converts raw Doppler Weather Radar (DWR) files into Py-ART compatible NetCDF files.
- Provides convenient tools for data processing and analysis.
- Offers visualization functions for better understanding and interpretation of radar data.

## Installation

Py-SRT can be installed in different ways depending on your preference. Below are two recommended methods:

### Method 1: Installing via Conda

```shell
conda create -n srt python=3.9 jupyter arm_pyart pandas wradlib git -c conda-forge
conda activate srt
pip install git+https://github.com/Space14Mann/Py_SRT.git


