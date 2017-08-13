Installing with pip
===================

This is the default mode, and it is what we recommend. simply use the latest version from the repository to install as superuser:

``` pip install git+https://github.com/ClaudiaEsp/inet.git```

or as user:

``` pip install --user git+https://github.com/ClaudiaEsp/inet.git```

Alternatively, you can download the tar.gz file for the directory /inet/dist and then install it: 

``` pip install inet.x.x.x.tar.gz```

Upgrade
=======

To upgrade to the latest version of the module just type:

``` pip install upgrade git+https://github.com/ClaudiaEsp/inet.git```

Installing with setuptools
==========================

You can simply download the lastest version from the repository:

``` git clone https://github.com/ClaudiaEsp/inet.git```

then enter the directory /inet and type:

``` python setup.py install --prefix=~/.local/ ```

Installation from the tar.gz file 
=================================

Download *.tar.gz file from http://github.com/ClaudiaEsp/inet/PVNet/dist/

untar the file and find the directory where setup.py is located. Once there, simply type:

```python setup.py install --prefix=~/.local/```

Create a tar file from repository version
=========================================

in /inet type:

``` python setup.py sdist ```

This will create a tar file in the directory src/dist

