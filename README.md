# inet 

A python module to test connectivity models based on multiple
simulatenous patch-clamp recordings between [Parvalbumin](https://en.wikipedia.org/wiki/Parvalbumin) (PV) positive [interneurons](https://en.wikipedia.org/wiki/Interneuron) and [granule cells](https://en.wikipedia.org/wiki/Granule_cell) in the [dentate gyrus](https://en.wikipedia.org/wiki/Dentate_gyrus) of mice.

It is for personal use only. 

Requirements
============

* Python (tested in 2.7, will not work in Python 3.6)
* NumPy (tested in 1.13)
* Scipy (tested in 0.19)
* terminaltables (tested in 3.1.0)

How to install it
=================

`pip install git+https://github.com/ClaudiaEsp/inet.git`

Basic usage
=================
In python:

```python
from inet import DataLoader
mydataset = Dataloader('./data') # load connectivity matrices
```

Matrices of synaptic connections
================================
<img src="./images/Guzman_2016.png" alt="Drawing" height="350px"/>

The folder *./data* contains the number and types of connections between
PV-positive interneurons and granule cells recorded by up to eight 
simulatenous patch-clamp recordings. Connections are represented as
nxn size matrices of pre-post connections where every element is,

* <0> if no connection, 
* <1> if chemical synapse alone, 
* <2> if electrical synapse alone and 
* <3> if both synapses together (i.e. chemical and electrical). 

A triple recording containing the connections:
* <1> chemical synapses alone: 1->2, 2->1 and 3->1
* <2> electrical synapses alone: 2=3 
* <3> both synapses: 1->3

would be represented as:

```
[ 0, 1, 3 ]
[ 1, 0, 2 ]
[ 1, 0, 0 ]
```

Note that the electrical synapse is only marked once in the matrix (element (2,3) because electrical synapses lack directionality. Thus the matrix above could be also represented as:

```
[ 0, 1, 3 ]
[ 1, 0, 1 ]
[ 1, 2, 0 ]
```

The element (1,3) is an electrical synapse and a chemical synapse from cell1
to cell3. Due to the lack of directionality of the electrical synapse, the matrix could be also represented as:

```
[ 0, 1, 1 ]
[ 1, 0, 1 ]
[ 3, 2, 0 ]
```

Matrices are stored as ASCII files of the form `<filename>.syn`. The 
filename is represented as `N_date_set.syn`, where  __N__ is the number of PV-positive interneurons. For example, a file called *1_160324_01.syn* contains connections where the first row is a PV-positive interneuron.

Matrices of synaptic distances
==============================
The inter-somatic distances between connections are stored as in *.syn* files,but with an extension *.dist*. For example, a file called *1_160341_01.dist* is given, that could contain

```
[   0.000, -53.623,  61.854 ]
[  53.623,  0.0000, 110.419 ]
[ -61.854, -110.419,  0.000 ]

```
