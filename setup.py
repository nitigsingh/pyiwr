from setuptools import setup, find_packages

setup(
    name='pyiwr',
    version='1.0.0',
    description='pyiwr is a helpful open-source library developed by the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw ISRO DWR (Doppler Weather Radar) data files into Py-ART compatible NetCDF files. Furthermore, Py-SRT provides useful tools and visualisation functions to make working with the data easier and more enjoyable.',
    author='Nitig Singh & Vaibhav Tyagi',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    author_email='nitig14rdfsma@gmail.com, phd2201121012@iiti.ac.in and vaibhavtyagi7191@gmail.com',
    long_description=open('README.txt').read(),
    packages=['pyiwr',],
    install_requires=['arm_pyart', 'numpy', 'xarray', 'datetime', 'matplotlib', 'mpl_toolkits'],
    url='https://github.com/nitigsingh/pyiwr.git', 
)

