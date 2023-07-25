from setuptools import setup, find_packages

setup(
    name='pyiwr',
    version='1.0.0',
    description='pyiwr is an advanced open-source library developed by researchers at the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw ISRO Doppler Weather Radar (DWR) data files and correct MOSDAC radar NetCDF files into Py-ART compatible NetCDF files. pyiwr also provides a range of useful tools and visualization functions to facilitate working with and analyzing weather radar data.',
    author='Nitig Singh & Vaibhav Tyagi',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    author_email='nitig14rdfsma@gmail.com, phd2201121012@iiti.ac.in and vaibhavtyagi7191@gmail.com',
    long_description=open('README.txt').read(),
    packages=['pyiwr',],
    install_requires=['arm_pyart', 'numpy', 'xarray', 'matplotlib'],
    url='https://github.com/nitigsingh/pyiwr.git', 
)

