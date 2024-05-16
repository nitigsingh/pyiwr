=====
pyiwr
=====


.. image:: https://img.shields.io/pypi/v/pyiwr.svg
        :target: https://pypi.python.org/pypi/pyiwr

.. image:: https://img.shields.io/travis/nitigsingh/pyiwr.svg
        :target: https://travis-ci.com/nitigsingh/pyiwr

.. image:: https://readthedocs.org/projects/pyiwr/badge/?version=latest
        :target: https://pyiwr.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



.. raw:: html

   <p align="center">

.. raw:: html

   </p>

pyiwr
=====

pyiwr is an advanced open-source library
developed by researchers at the SIGMA Research
Lab at IIT Indore. This powerful tool is
designed to effortlessly read, analyze, and 
visualize Indian Doppler Weather Radar (DWR) data.
pyiwr also provides a range of useful tools and visualization
functions to facilitate Gridding data for Constant Altitude Plan Position Indicator (CAPPI), 
Radar Reflectivity correction, Radar Quantitative Precipitation estimation (QPE) 
using Polarimetric products, Radar Reflectivity 
Contour Frequency by Altitude Diagram 
and Time Series Analysis both spatially and at a given location.

Features
--------

-  Converts raw Indian Doppler Weather Radar (DWR) data files into radar/gridded objects NetCDF files.
-  Restructure and format correct the DWR NetCDF files with missing data moments and
   attributes.
-  Converts radial sweeps format data into cartesian gridded data NetCDF
   files.
-  Capable of merging multiple sweep files into a single volumetric CFradial file,
   with the facility of saving the files into gridded or CFradial format data after format correction.
-  Provides convenient tools for data processing and analysis.
-  Offers visualization functions for better understanding and
   interpretation of radar data.

Installation
------------

pyiwr can be installed as:

.. code:: shell

   conda create -n pyiwr python=3.9 jupyter git -c conda-forge
   conda activate pyiwr
   pip install git+https://github.com/nitigsingh/pyiwr.git

Note:
-----

As an active project, pyiwr seeks contributions from the research
community, making it a dynamic and collaborative toolkit for weather
radar research and applications. Future work includes implementing
advanced data processing algorithms like quality control, precipitation
type classifications and radar Quantitative Precipitation Estimation
(QPE) etc.

* Free software: MIT license
* Documentation: https://pyiwr.readthedocs.io.
