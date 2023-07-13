from setuptools import setup, find_packages

setup(
    name='PySRT',
    version='0.1',
    description='Py-SRT is a helpful open-source library developed by the SIGMA Research Lab at IIT Indore. This powerful tool is designed to effortlessly convert raw DWR (Doppler Weather Radar) files into Py-ART compatible NetCDF files. Furthermore, Py-SRT provides useful tools and visualisation functions to make working with the data easier and more enjoyable.',
    author='Nitig Singh and Vaibhav Tyagi',
    author_email='nitig14rdfsma@gmail.com, phd2201121012@iiti.ac.in and vaibhavtyagi7191@gmail.com',
    packages=find_packages(),
    install_requires=['arm_pyart', 'numpy'],
)
