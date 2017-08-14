"""
motifs_unittest.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created:  Wed Aug  9 17:49:33 CEST 2017

Unittest environment to test the counting of motifs
"""

import unittest

import numpy as np
from motifs import iicounter, eicounter, iecounter

class TestIIMotifCounter(unittest.TestCase):
    """
    A major unittest class to test IIMotifCounter 
    """
        
    Z = np.zeros((3,3))
    A = np.array(([0,3],[0,0]))
    B = np.array(([0,3],[1,0]))
    C = np.array(([0,3],[1,0]))
    D = np.array(([0,1],[3,0])) # equal to C

    def setUp(self):
        """
        Create IIMotifCounter objects from global matrices with
        known connections
        """
        self.a  = iicounter(self.A)
        self.b  = iicounter(self.B)
        self.c  = iicounter(self.C)
        self.d  = iicounter(self.C)
        self.z  = iicounter(self.Z)

    def test_found_chemical_syn(self):
        """
        Test 'ii_chem' : a chemical synapses between interneurons
        """
        self.assertEquals(1, self.a['ii_chem']['found'])
        self.assertEquals(2, self.b['ii_chem']['found'])
        self.assertEquals(2, self.c['ii_chem']['found'])
        self.assertEquals(2, self.d['ii_chem']['found'])
        self.assertEquals(0, self.z['ii_chem']['found'])

    def test_found_electrical_syn(self):
        """
        Test 'ii_elec' : electrical synapses between interneurons
        """
        self.assertEquals(1, self.a['ii_elec']['found'])
        self.assertEquals(1, self.b['ii_elec']['found'])
        self.assertEquals(1, self.c['ii_elec']['found'])
        self.assertEquals(1, self.d['ii_elec']['found'])
        self.assertEquals(0, self.z['ii_elec']['found'])

    def test_found_electrical_and_one_chemical(self):
        """
        Test 'ii_ce1' : an alectrical synapse together with ONE chemical
        """
        self.assertEquals(1, self.a['ii_ce1']['found'])
        self.assertEquals(2, self.b['ii_ce1']['found'])
        self.assertEquals(2, self.c['ii_ce1']['found'])
        self.assertEquals(2, self.d['ii_ce1']['found'])
        self.assertEquals(0, self.z['ii_ce1']['found'])

    def test_found_electrical_and_two_chemical(self):
        """
        Test 'ii_ce2' : an alectrical synapse together with TWO chemical
        """
        self.assertEquals(0, self.a['ii_ce2']['found'])
        self.assertEquals(1, self.b['ii_ce2']['found'])
        self.assertEquals(1, self.c['ii_ce2']['found'])
        self.assertEquals(1, self.d['ii_ce2']['found'])
        self.assertEquals(0, self.z['ii_ce2']['found'])

    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysum = self.a +  self.d

        self.assertEquals(3, mysum['ii_chem']['found'])
        self.assertEquals(2, mysum['ii_elec']['found'])
        self.assertEquals(3, mysum['ii_ce1']['found'])
        self.assertEquals(1, mysum['ii_ce2']['found'])

        self.assertEquals(4, mysum['ii_chem']['tested'])
        self.assertEquals(2, mysum['ii_elec']['tested'])
        self.assertEquals(4, mysum['ii_ce1']['tested'])
        self.assertEquals(2, mysum['ii_ce2']['tested'])

class TestEIMotifCounter(unittest.TestCase):
    """
    A major unittest class to test EIMotifCounter 
    """
    A = np.ones((2,2))
    B = np.array(([1,1],[0,0]))

    def setUp(self):
        """
        Create EIMotifCounter objects from global matrices with
        known connections
        """
        self.a = eicounter(self.A)
        self.b = eicounter(self.B)
         

    def test_found_chemical_syn(self):
        """
        Test 'ei' : a chemical synapses between excitatory to inhibitory 
                    neuron.
        """
        self.assertEquals(4, self.a['ei']['found'])
        self.assertEquals(2, self.b['ei']['found'])
        
    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysum = self.a + self.b 

        self.assertEquals(6, mysum['ei']['found'])
        self.assertEquals(8, mysum['ei']['tested'])


class TestIEMotifCounter(unittest.TestCase):
    """
    A major unittest class to test IEMotifCounter 
    """
    A = np.ones((2,2))
    B = np.array(([1,1],[0,0]))

    def setUp(self):
        """
        Create IEMotifCounter objects from global matrices with
        known connections
        """
        self.a = iecounter(self.A)
        self.b = iecounter(self.B)

    def test_found_chemical_syn(self):
        """
        Test 'ie' : a chemical synapses between excitatory to inhibitory 
                    neuron.
        """
        self.assertEquals(4, self.a['ie']['found'])
        self.assertEquals(2, self.b['ie']['found'])
        
    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysum = self.a + self.b 

        self.assertEquals(6, mysum['ie']['found'])
        self.assertEquals(8, mysum['ie']['tested'])
        
class TestAddingObjects(unittest.TestCase):
    """
    Unittesting for adding two different MotifObject types
    """
     
    def setUp(self):
        ii = iicounter(np.array(([0,3],[1,0])))
        ie = iecounter(np.ones((2,2)))
        ei = eicounter(np.ones((2,2)))

        self.ii_sum = ii + ii
        self.ie_sum = ie + ie
        self.ei_sum = ei + ei

        self.ie_ii = ie + ii
        self.ii_ie = ii + ei
        self.ei_ie = ei + ie
        self.ie_ei = ie + ei

    def test_add_same_objects(self):
        """
        Test the result of summing same  MotifCounter inherited objects
        """
        # test found
        self.assertEquals(4, self.ii_sum['ii_chem']['found'])
        self.assertEquals(2, self.ii_sum['ii_elec']['found'])
        self.assertEquals(4, self.ii_sum['ii_ce1']['found'])
        self.assertEquals(2, self.ii_sum['ii_ce2']['found'])

        self.assertEquals(8, self.ei_sum['ei']['found'])
        self.assertEquals(8, self.ie_sum['ie']['found'])

        # test tested
        self.assertEquals(4, self.ii_sum['ii_chem']['tested'])
        self.assertEquals(2, self.ii_sum['ii_elec']['tested'])
        self.assertEquals(4, self.ii_sum['ii_ce1']['tested'])
        self.assertEquals(2, self.ii_sum['ii_ce2']['tested'])

        self.assertEquals(8, self.ei_sum['ei']['tested'])
        self.assertEquals(8, self.ie_sum['ie']['tested'])

    def test_add_diff_objects(self):
        """
        Test the result of different  MotifCounter objects
        will returna a MotifCounter object type
        """
        # test found
        self.assertEquals(2, self.ie_ii['ii_chem']['found'])
        self.assertEquals(1, self.ie_ii['ii_elec']['found'])
        self.assertEquals(2, self.ie_ii['ii_ce1']['found'])
        self.assertEquals(1, self.ie_ii['ii_ce2']['found'])

        self.assertEquals(4, self.ei_ie['ei']['found'])
        self.assertEquals(4, self.ei_ie['ie']['found'])
        
        self.assertEquals(4, self.ie_ei['ei']['found'])
        self.assertEquals(4, self.ie_ei['ie']['found'])

        # test tested
        self.assertEquals(2, self.ie_ii['ii_chem']['tested'])
        self.assertEquals(1, self.ie_ii['ii_elec']['tested'])
        self.assertEquals(2, self.ie_ii['ii_ce1']['tested'])
        self.assertEquals(1, self.ie_ii['ii_ce2']['tested'])

        self.assertEquals(4, self.ei_ie['ei']['tested'])
        self.assertEquals(4, self.ei_ie['ie']['tested'])
        
        self.assertEquals(4, self.ie_ei['ei']['tested'])
        self.assertEquals(4, self.ie_ei['ie']['tested'])

if __name__ == '__main__':
    unittest.main()
