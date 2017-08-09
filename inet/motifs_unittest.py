"""
motifs_unittest.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created:  Wed Aug  9 17:49:33 CEST 2017

Unittest environment to test the motif module
"""

import numpy as np

import unittest
from motifs import iicounter

A = np.array(([0,3],[0,0]))
B = np.array(([0,3],[1,0]))


class TestMotifs(unittest.TestCase):
        
    def setUp(self):
        self.a  = iicounter(A)
        self.b  = iicounter(B)

    def test_count_chemical_syn(self):
        self.assertEquals(1, self.a['ii_chem']['found'])

    def test_count_electrical_syn(self):
        self.assertEquals(1, self.a['ii_elec']['found'])
        self.assertEquals(1, self.b['ii_elec']['found'])



if __name__ == '__main__':
    unittest.main()
