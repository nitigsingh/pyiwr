from setuptools import setup, find_packages

setup(
    name='Py_SRT',
    version='1.0',
    description='Py-SRT is a helpful open-source library developed by the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw DWR (Doppler Weather Radar) files into Py-ART compatible NetCDF files. Furthermore, Py-SRT provides useful tools and visualisation functions to make working with the data easier and more enjoyable.',
    author='Nitig Singh & Vaibhav Tyagi',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    author_email='nitig14rdfsma@gmail.com, phd2201121012@iiti.ac.in and vaibhavtyagi7191@gmail.com',
    long_description=open('README.txt').read(),
    packages=['Py_SRT',],
    install_requires=['arm_pyart', 'numpy', 'xarray'],
    classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Console"
    ],
    url='https://github.com/Space14Mann/Py-SRT.git'
)
