"""
setup.py

Jose Guzmand and Claudia Espinoza
Created: Sun Jul 30 13:42:41 CEST 2017

Installation file required for the PVNet Python module

"""
from setuptools import setup, find_packages

setup(
    name = 'inet', # application name
    version = '0.0.9',# application version
    author ='Jose Guzman and Claudia Espinoza',
    author_email = 'sjm.guzman@gmail.com',
    packages = ['inet'],
    include_package_data = True,# include additional data
    package_data={
        # If any package contains *.txt files, include them:
        '': ['*.txt'],
        # And include any *.syn files found in the 'data' subdirectory
        # of the 'PVNet' package, also:
        'PVNet': ['data/*.syn'],
    },
    url = 'https://github.com/ClaudiaEsp/inet.git',
    license = 'LICENSE',
    description = 'network simulations based on connections of PV neurons',
    long_description = open('README.md').read(),
    install_requires = ['numpy', 'scipy'],
)
