"""
setup.py

Jose Guzmand and Claudia Espinoza
Created: Sun Jul 30 13:42:41 CEST 2017

Installation file for the PVNet Python module

"""
from setuptools import setup

setup(
    name = 'PVNet', # application number
    version = '0.0.1',# application version
    author ='Jose Guzman and Claudia Espinoza',
    author_email = 'sjm.guzman@gmail.com',
    packages = ['PVNet'],
    include_package_data = True,# include additional data
    url = 'https://github.com/ClaudiaEsp/Dentate/',
    license = 'LICENSE',
    description = 'network simulations based on connections of PV neurons',
    long_description = open('README').read(),
    install_requires=['numpy', 'scipy', 'teminaltables'],
)
