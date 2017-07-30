Installing with pip
===================

This is the default mode, and it is what we recommend. There are two ways
to install the module. You can downloaded the tar.gz file for the directory /PVNet/dist and then use: 

``` pip install --user $USER PV.x.x.x.tar.gz```

Otherwise, you can simply use the latest version from the repository:

``` pip install --user git+https://github.com/ClaudiaEsp/Dentate.git```

Installing with setuptools
==========================

You can simply download the lastest version from the repository:

``` git clone https://github.com/ClaudiaEsp/Dentate.git```

then enter the directory /PVNet and type:

``` python setup.py install --prefix=~/.local/ ```

Installation from the tar.gz file 
=================================

Download *.tar.gz file from http://github.com/ClaudiaEsp/Dentate/PVNet/dist/

untar the file and find the directory where setup.py is located. Once there, simply type:

```python setup.py install --prefix=~/.local/```

Create a tar file from repository version
=========================================

in /PVNet type:
``` python setup.py sdist ```

This will create a tar file in the directory src/dist

