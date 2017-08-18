"""
unittest_motifs.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created:  Wed Aug  9 17:49:33 CEST 2017

Unittest environment to test the counting of motifs
"""

import unittest

import numpy as np
from motifs import iicounter, eicounter, iecounter, eecounter

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
        self.assertEquals(1, self.a1.ii_c1e_found)
        self.assertEquals(1, self.a2.ii_c1e_found)

        self.assertEquals(2, self.b1.ii_c1e_found)
        self.assertEquals(2, self.b2.ii_c1e_found)

        self.assertEquals(0, self.c1.ii_c1e_found)
        self.assertEquals(0, self.c2.ii_c1e_found)

        self.assertEquals(0, self.d1.ii_c1e_found)
        self.assertEquals(0, self.d2.ii_c1e_found)

        self.assertEquals(0, self.e.ii_c1e_found)
        
        self.assertEquals(0, self.z.ii_c1e_found)

    def test_found_electrical_and_two_chemical(self):
        """
        Test 'ii_c2e' : an alectrical synapse together with TWO chemical
        """
        self.assertEquals(0, self.a1.ii_c2e_found)
        self.assertEquals(0, self.a2.ii_c2e_found)

        self.assertEquals(1, self.b1.ii_c2e_found)
        self.assertEquals(1, self.b2.ii_c2e_found)

        self.assertEquals(0, self.c1.ii_c2e_found)
        self.assertEquals(0, self.c2.ii_c2e_found)

        self.assertEquals(0, self.d1.ii_c2e_found)
        self.assertEquals(0, self.d2.ii_c2e_found)

        self.assertEquals(0, self.e.ii_c2e_found)

        self.assertEquals(0, self.z.ii_c2e_found)

    def test_found_electrical_syn(self):
        """
        Test 'ii_elec' : electrical synapses between interneurons
        """
        self.assertEquals(1, self.a1.ii_elec_found)
        self.assertEquals(1, self.a2.ii_elec_found)

        self.assertEquals(1, self.b1.ii_elec_found)
        self.assertEquals(1, self.b2.ii_elec_found)

        self.assertEquals(1, self.c1.ii_elec_found)
        self.assertEquals(1, self.c2.ii_elec_found)

        self.assertEquals(0, self.d1.ii_elec_found)
        self.assertEquals(0, self.d2.ii_elec_found)

        self.assertEquals(0, self.e.ii_elec_found)

        self.assertEquals(0, self.z.ii_elec_found)

    def test_found_chemical_syn(self):
        """
        Test 'ii_chem' : a chemical synapses between interneurons
        """
        self.assertEquals(1, self.a1.ii_chem_found)
        self.assertEquals(1, self.a2.ii_chem_found)

        self.assertEquals(2, self.b1.ii_chem_found)
        self.assertEquals(2, self.b2.ii_chem_found)

        self.assertEquals(0, self.c1.ii_chem_found)
        self.assertEquals(0, self.c2.ii_chem_found)

        self.assertEquals(1, self.d1.ii_chem_found)
        self.assertEquals(1, self.d2.ii_chem_found)

        self.assertEquals(2, self.e.ii_chem_found)

        self.assertEquals(0, self.z.ii_chem_found)

    def test_found_bidirectional_chemical(self):
        """
        Test 'ii_c2' : a bidirectional chemical synapse
        """
        self.assertEquals(0, self.a1.ii_c2_found)
        self.assertEquals(0, self.a2.ii_c2_found)

        self.assertEquals(1, self.b1.ii_c2_found)
        self.assertEquals(1, self.b2.ii_c2_found)

        self.assertEquals(0, self.c1.ii_c2_found)
        self.assertEquals(0, self.c2.ii_c2_found)

        self.assertEquals(0, self.d1.ii_c2_found)
        self.assertEquals(0, self.d2.ii_c2_found)

        self.assertEquals(1, self.e.ii_c2_found)

        self.assertEquals(0, self.z.ii_c2_found)

    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysuma = self.a1 +  self.a2 

        self.assertEquals(2, mysuma.ii_chem_found)
        self.assertEquals(2, mysuma.ii_elec_found)
        self.assertEquals(2, mysuma.ii_c1e_found)
        self.assertEquals(0, mysuma.ii_c2e_found)

        self.assertEquals(4, mysuma.ii_chem_tested)
        self.assertEquals(2, mysuma.ii_elec_tested)
        self.assertEquals(4, mysuma.ii_c1e_tested)
        self.assertEquals(2, mysuma.ii_c2e_tested)

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
        self.assertEquals(4, self.a.ei_found)
        self.assertEquals(2, self.b.ei_found)
        
    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysum = self.a + self.b 

        self.assertEquals(6, mysum.ei_found)
        self.assertEquals(8, mysum.ei_tested)


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
        self.assertEquals(4, self.a.ie_found)
        self.assertEquals(2, self.b.ie_found)
        
    def test_add_objects(self):
        """
        Test that sum objects is correct
        """
        mysum = self.a + self.b 

        self.assertEquals(6, mysum.ie_found)
        self.assertEquals(8, mysum.ie_tested)
        
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
        self.assertEquals(4, self.ii_sum.ii_chem_found)
        self.assertEquals(2, self.ii_sum.ii_elec_found)
        self.assertEquals(4, self.ii_sum.ii_c1e_found)
        self.assertEquals(2, self.ii_sum.ii_c2e_found)

        self.assertEquals(8, self.ei_sum.ei_found)
        self.assertEquals(8, self.ie_sum.ie_found)

        # test tested
        self.assertEquals(4, self.ii_sum.ii_chem_tested)
        self.assertEquals(2, self.ii_sum.ii_elec_tested)
        self.assertEquals(4, self.ii_sum.ii_c1e_tested)
        self.assertEquals(2, self.ii_sum.ii_c2e_tested)

        self.assertEquals(8, self.ei_sum.ei_tested)
        self.assertEquals(8, self.ie_sum.ie_tested)

    def test_add_diff_objects(self):
        """
        Test the result of different  MotifCounter objects
        will returna a MotifCounter object type
        """
        # test found
        self.assertEquals(2, self.ie_ii.ii_chem_found)
        self.assertEquals(1, self.ie_ii.ii_elec_found)
        self.assertEquals(2, self.ie_ii.ii_c1e_found)
        self.assertEquals(1, self.ie_ii.ii_c2e_found)

        self.assertEquals(4, self.ei_ie.ei_found)
        self.assertEquals(4, self.ei_ie.ie_found)
        
        self.assertEquals(4, self.ie_ei.ei_found)
        self.assertEquals(4, self.ie_ei.ie_found)

        # test tested
        self.assertEquals(2, self.ie_ii.ii_chem_tested)
        self.assertEquals(1, self.ie_ii.ii_elec_tested)
        self.assertEquals(2, self.ie_ii.ii_c1e_tested)
        self.assertEquals(1, self.ie_ii.ii_c2e_tested)

        self.assertEquals(4, self.ei_ie.ei_tested)
        self.assertEquals(4, self.ei_ie.ie_tested)
        
        self.assertEquals(4, self.ie_ei.ei_tested)
        self.assertEquals(4, self.ie_ei.ie_tested)

class TestCA3MotifCounter(unittest.TestCase):
    """
    Test the number of motifs found in CA3 neurons
    according to the data in Guzman et al., 2016
    """
    def setUp(self): 
        """
        Load all CA3 connectivity motifs
        """
        self.a = eecounter(np.loadtxt('../data/CA3/0_100218_1.syn'))
        self.b = eecounter(np.loadtxt('../data/CA3/0_110113_0.syn'))
        self.c = eecounter(np.loadtxt('../data/CA3/0_110127_1.syn'))
        self.d = eecounter(np.loadtxt('../data/CA3/0_120305_1.syn'))
        self.e = eecounter(np.loadtxt('../data/CA3/0_130424_0.syn'))
        self.f = eecounter(np.loadtxt('../data/CA3/0_130621_0.syn'))
        self.g = eecounter(np.loadtxt('../data/CA3/0_130705_0.syn'))
        self.h = eecounter(np.loadtxt('../data/CA3/0_130722_3.syn'))
        self.i = eecounter(np.loadtxt('../data/CA3/0_140205_3.syn'))
        self.j = eecounter(np.loadtxt('../data/CA3/0_140218_0.syn'))
        self.k = eecounter(np.loadtxt('../data/CA3/0_140519_2.syn'))
        self.l = eecounter(np.loadtxt('../data/CA3/0_141006_0.syn'))
        self.m = eecounter(np.loadtxt('../data/CA3/0_141202_0.syn'))
    
    def test_CA3bidirectional_connections(self):
        """
        Test for correct number found in bidirectional connections 
        """
        self.assertEquals(1, self.d.ii_c2_found)
        self.assertEquals(1, self.h.ii_c2_found)
        self.assertEquals(2, self.i.ii_c2_found)
        self.assertEquals(2, self.l.ii_c2_found)

    def test_CA3convergent_connections(self):
        """
        Test for correct number found in divergent connectons 
        """
        self.assertEquals(1, self.e.ii_con_found)
        self.assertEquals(1, self.f.ii_con_found)
        self.assertEquals(1, self.h.ii_con_found)
        self.assertEquals(2, self.i.ii_con_found)
        self.assertEquals(5, self.l.ii_con_found)

    def test_CA3divergent_connections(self):
        """
        Test for correct number found in convergent connectons 
        """
        self.assertEquals(1, self.c.ii_div_found)
        self.assertEquals(1, self.d.ii_div_found)
        self.assertEquals(1, self.g.ii_div_found)
        self.assertEquals(6, self.i.ii_div_found)
        self.assertEquals(1, self.k.ii_div_found)
        self.assertEquals(10, self.l.ii_div_found)
        self.assertEquals(3, self.m.ii_div_found)

    def test_CA3linear_connections(self):
        """
        Test for correct number found in convergent connectons 
        """
        self.assertEquals(1, self.a.ii_chain_found)
        self.assertEquals(1, self.b.ii_chain_found)
        self.assertEquals(1, self.d.ii_chain_found)
        self.assertEquals(1, self.h.ii_chain_found)
        self.assertEquals(7, self.i.ii_chain_found)
        self.assertEquals(1, self.j.ii_chain_found)
        self.assertEquals(12, self.l.ii_chain_found)
        self.assertEquals(1, self.m.ii_chain_found)


if __name__ == '__main__':
    unittest.main()
