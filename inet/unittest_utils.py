"""
motifs_unittest.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Mon Aug 14 20:07:16 CEST 2017

Unittest environment to test the utils of motifs
"""
import unittest

import numpy as np
from utils import chem_squarematrix 
from utils import elec_squarematrix 

class Testchem_squarematrix(unittest.TestCase):
    """
    A major unittest class to test the random generation of
    chemical synapses
    """
        
    def setUp(self):
        """
        Create random matrices objects from global matrices with
        known connections
        """
        # will get an average of 3 connections
        chem_3 = list()
        chem_6 = list()
        chem_10 = list()

        elec_3 = list()

        for _ in range(10000):
            chem_3.append(np.count_nonzero(chem_squarematrix(3, 0.5)))
            chem_6.append(np.count_nonzero(chem_squarematrix(4, 0.5)))
            chem_10.append(np.count_nonzero(chem_squarematrix(5, 0.5)))
            elec_3.append(np.count_nonzero(elec_squarematrix(4, 0.5)))

        self.chem_3 = np.mean(chem_3)
        self.chem_6 = np.mean(chem_6)
        self.chem_10 = np.mean(chem_10)

        self.elec_3 = np.mean(elec_3)

    def test_chem_squarematrix(self):
        """
        Check whether the average number of chemical synapses is close to
        theoretical values for chemical random connections
        """
        #tolerance = lambda x,y: abs(x-y)/x < 0.05
        self.assertAlmostEquals(3, self.chem_3, 1)
        self.assertAlmostEquals(6, self.chem_6, places = 1)
        self.assertAlmostEquals(10, self.chem_10, places = 1)

    def test_elec_squarematrix(self):
        """
        Check whether the average number of electrical synapses is close to
        theoretical values for electrical random connections
        """
        mymsg = 'testing number of electrical synapses'
        self.assertAlmostEquals(3, self.elec_3, 1, msg=mymsg )
        
if __name__ == '__main__':
    unittest.main()
