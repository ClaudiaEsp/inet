Installation from the repository
================================

You can simply download the lastest version from the repository:

``` git clone https://github.com/ClaudiaEsp/Dentate```

then enter the directory /src and type:
``` python setup.py install --prefix=~/.local/

Installation from the tar.gz file 
================================
Download the PV.x.x.x.tar.gz file from http://github.com/ClaudiaEsp/Dentate/src/dist/

untar the file and find the directory where setup.py is located. Once there, simply type:

```python setup.py install --prefix=~/.local/```

Create a tar file from repository version
=========================================

in /src type:
>>> python setup.py sdist

This will create a tar file in the directory src/dist

Installing with pip
===================

>>> pip install --user $USER PV.x.x.x.tar.gz
>>> pip install --user $USER https://github.com/ClaudiaEsp/Dentate.git
