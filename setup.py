#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["arm_pyart", "xarray", "cartopy"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Nitig Singh, Vaibhav Tyagi, Hamid Ali Syed",
    author_email="nitig14rdfsma@gmail.com",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="convert raw ISRO Doppler Weather Radar (DWR) \
        data files and correct MOSDAC radar NetCDF files into \
            Py-ART compatible NetCDF files",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyiwr",
    name="pyiwr",
    packages=find_packages(include=["pyiwr", "pyiwr.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/nitigsingh/pyiwr",
    version="1.0.1",
    zip_safe=False,
)
