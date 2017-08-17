# inet 

A python module to test connectivity models based on multiple
simulatenous patch-clamp recordings between [Parvalbumin](https://en.wikipedia.org/wiki/Parvalbumin) (PV) positive [interneurons](https://en.wikipedia.org/wiki/Interneuron) and [granule cells](https://en.wikipedia.org/wiki/Granule_cell) in the [dentate gyrus](https://en.wikipedia.org/wiki/Dentate_gyrus) of mice.

It is for personal use only. 

Requirements
============

* Python (tested in 2.7, will not work in Python 3.6)
* NumPy (tested in 1.13)
* Scipy (tested in 0.19)

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
