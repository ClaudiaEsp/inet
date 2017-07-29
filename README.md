# Dentate Connectivity

This is a repository to test connectivity models based on multiple
simulatenous patch-clamp recordings between PV+ interneurons and granule cells in 
mice.

It is for personal use only. 

Matrices of synaptic connections
================================

The folder *./data* contains the number and types of connections between
PV-positive interneurons and granule cells recorded by up to eight 
simulatenous patch-clamp recordings. Connections are represented as
nxn size matrices of pre-post connections where every element is,

* <0> if no connection, 
* <1> if chemical synapse, 
* <2> if electrical synapse and 
* <3> if both (chemical and electrical). 

A triple recording containing the connections:
* <1> chemical synapses: 1->2, 1->3 and 2->1 
* <2> electrical synapses: 1->2, 2->3 and 3->1 
* <3> both synapses: 1->2

would be represented as:

```
[ 0, 3, 1 ]
[ 1, 0, 2 ]
[ 2, 0, 0 ]
```

Every matrix is stored in as ASCII of the form `<filename>.syn`, where
filename is coded as `N_date_set.syn` being <N> is the number of PV-positive
interneurons. For example, a file called *1_160324_01.syn* contains
synaptic connections where the first row is a PV-positive interneuron.

Matrices of synaptic distances
==============================
The inter-somatic distances between connections are stored as in *.syn* files,but with an extension *.dist*. For example, a file called *1_160341_01.dist* is given, that could contain

```
[   0.000, -53.623,  61.854 ]
[  53.623,  0.0000, 110.419 ]
[ -61.854, -110.419,  0.000 ]

```
