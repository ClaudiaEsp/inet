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
        
    A1 = np.array(([0,3],[0,0]))
    A2 = np.array(([0,0],[3,0]))

    B1 = np.array(([0,3],[1,0]))
    B2 = np.array(([0,1],[3,0]))

    C1 = np.array(([0,2],[0,0]))
    C2 = np.array(([0,0],[2,0]))

    D1 = np.array(([0,1],[0,0]))
    D2 = np.array(([0,0],[1,0]))

    E  = np.array(([0,1],[1,0]))

    Z = np.zeros((3,3))

    def setUp(self):
        """
        Create IIMotifCounter objects from global matrices with
        known connections
        """
        self.a1  = iicounter(self.A1)
        self.a2  = iicounter(self.A2)

        self.b1  = iicounter(self.B1)
        self.b2  = iicounter(self.B2)

        self.c1  = iicounter(self.C1)
        self.c2  = iicounter(self.C2)
            
        self.d1  = iicounter(self.D1)
        self.d2  = iicounter(self.D2)

        self.e   = iicounter(self.E)

        self.z   = iicounter(self.Z)

    def test_found_electrical_and_one_chemical(self):
        """
        Test 'ii_c1e' : an alectrical synapse together with ONE chemical
        """
        self.assertEquals(1, self.a1['ii_c1e']['found'])
        self.assertEquals(1, self.a2['ii_c1e']['found'])

        self.assertEquals(2, self.b1['ii_c1e']['found'])
        self.assertEquals(2, self.b2['ii_c1e']['found'])

        self.assertEquals(0, self.c1['ii_c1e']['found'])
        self.assertEquals(0, self.c2['ii_c1e']['found'])

        self.assertEquals(0, self.d1['ii_c1e']['found'])
        self.assertEquals(0, self.d2['ii_c1e']['found'])

        self.assertEquals(0, self.e['ii_c1e']['found'])
        
        self.assertEquals(0, self.z['ii_c1e']['found'])

    def test_found_electrical_and_two_chemical(self):
        """
        Test 'ii_c2e' : an alectrical synapse together with TWO chemical
        """
        self.assertEquals(0, self.a1['ii_c2e']['found'])
        self.assertEquals(0, self.a2['ii_c2e']['found'])

        self.assertEquals(1, self.b1['ii_c2e']['found'])
        self.assertEquals(1, self.b2['ii_c2e']['found'])

        self.assertEquals(0, self.c1['ii_c2e']['found'])
        self.assertEquals(0, self.c2['ii_c2e']['found'])

        self.assertEquals(0, self.d1['ii_c2e']['found'])
        self.assertEquals(0, self.d2['ii_c2e']['found'])

        self.assertEquals(0, self.e['ii_c2e']['found'])

        self.assertEquals(0, self.z['ii_c2e']['found'])

    def test_found_electrical_syn(self):
        """
        Test 'ii_elec' : electrical synapses between interneurons
        """
        self.assertEquals(1, self.a1['ii_elec']['found'])
        self.assertEquals(1, self.a2['ii_elec']['found'])

        self.assertEquals(1, self.b1['ii_elec']['found'])
        self.assertEquals(1, self.b2['ii_elec']['found'])

        self.assertEquals(1, self.c1['ii_elec']['found'])
        self.assertEquals(1, self.c2['ii_elec']['found'])

        self.assertEquals(0, self.d1['ii_elec']['found'])
        self.assertEquals(0, self.d2['ii_elec']['found'])

        self.assertEquals(0, self.e['ii_elec']['found'])

        self.assertEquals(0, self.z['ii_elec']['found'])

    def test_found_chemical_syn(self):
        """
        Test 'ii_chem' : a chemical synapses between interneurons
        """
        self.assertEquals(1, self.a1['ii_chem']['found'])
        self.assertEquals(1, self.a2['ii_chem']['found'])

        self.assertEquals(2, self.b1['ii_chem']['found'])
        self.assertEquals(2, self.b2['ii_chem']['found'])

        self.assertEquals(0, self.c1['ii_chem']['found'])
        self.assertEquals(0, self.c2['ii_chem']['found'])

        self.assertEquals(1, self.d1['ii_chem']['found'])
        self.assertEquals(1, self.d2['ii_chem']['found'])

        self.assertEquals(2, self.e['ii_chem']['found'])

        self.assertEquals(0, self.z['ii_chem']['found'])

    def test_found_bidirectional_chemical(self):
        """
        Test 'ii_c2' : a bidirectional chemical synapse
        """
        self.assertEquals(0, self.a1['ii_c2']['found'])
        self.assertEquals(0, self.a2['ii_c2']['found'])

        self.assertEquals(1, self.b1['ii_c2']['found'])
        self.assertEquals(1, self.b2['ii_c2']['found'])

        self.assertEquals(0, self.c1['ii_c2']['found'])
        self.assertEquals(0, self.c2['ii_c2']['found'])

        self.assertEquals(0, self.d1['ii_c2']['found'])
        self.assertEquals(0, self.d2['ii_c2']['found'])

        self.assertEquals(1, self.e['ii_c2']['found'])

        self.assertEquals(0, self.z['ii_c2']['found'])

    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysuma = self.a1 +  self.a2 

        self.assertEquals(2, mysuma['ii_chem']['found'])
        self.assertEquals(2, mysuma['ii_elec']['found'])
        self.assertEquals(2, mysuma['ii_c1e']['found'])
        self.assertEquals(0, mysuma['ii_c2e']['found'])

        self.assertEquals(4, mysuma['ii_chem']['tested'])
        self.assertEquals(2, mysuma['ii_elec']['tested'])
        self.assertEquals(4, mysuma['ii_c1e']['tested'])
        self.assertEquals(2, mysuma['ii_c2e']['tested'])

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
        self.assertEquals(4, self.ii_sum['ii_c1e']['found'])
        self.assertEquals(2, self.ii_sum['ii_c2e']['found'])

        self.assertEquals(8, self.ei_sum['ei']['found'])
        self.assertEquals(8, self.ie_sum['ie']['found'])

        # test tested
        self.assertEquals(4, self.ii_sum['ii_chem']['tested'])
        self.assertEquals(2, self.ii_sum['ii_elec']['tested'])
        self.assertEquals(4, self.ii_sum['ii_c1e']['tested'])
        self.assertEquals(2, self.ii_sum['ii_c2e']['tested'])

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
        self.assertEquals(2, self.ie_ii['ii_c1e']['found'])
        self.assertEquals(1, self.ie_ii['ii_c2e']['found'])

        self.assertEquals(4, self.ei_ie['ei']['found'])
        self.assertEquals(4, self.ei_ie['ie']['found'])
        
        self.assertEquals(4, self.ie_ei['ei']['found'])
        self.assertEquals(4, self.ie_ei['ie']['found'])

        # test tested
        self.assertEquals(2, self.ie_ii['ii_chem']['tested'])
        self.assertEquals(1, self.ie_ii['ii_elec']['tested'])
        self.assertEquals(2, self.ie_ii['ii_c1e']['tested'])
        self.assertEquals(1, self.ie_ii['ii_c2e']['tested'])

        self.assertEquals(4, self.ei_ie['ei']['tested'])
        self.assertEquals(4, self.ei_ie['ie']['tested'])
        
        self.assertEquals(4, self.ie_ei['ei']['tested'])
        self.assertEquals(4, self.ie_ei['ie']['tested'])

if __name__ == '__main__':
    unittest.main()
