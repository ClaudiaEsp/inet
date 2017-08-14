"""
loader.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Wed Jul 19 01:45:16 CEST 2017

Contains a class to load ASCII files with connectivities and  
distances between neurons recorded in an simultaneous whole-cell
patch clamp recording.

Example:
>>> from loader import DataLoader
>>> mydataset = DataLoader("./data") # load files with *sys extension
>>> mydataset.stats('conf') # report basis configuration statistics
"""

from __future__ import division

import glob, os
import numpy as np

from terminaltables import AsciiTable

import inet.utils as utils
from inet.utils import enum

from motifs import motifcounter
from motifs import iicounter, eicounter, iecounter, eecounter

class DataLoader(object):
    """
    A class to load synaptic type and distances from connectivity
    matrix in ./data folder. Check Readme.md for details
    """

    def __init__(self, path = None):
        """
        Reads all *.syn files contained in path folder

        Argument
        --------
        path : string 
            the path containing the folder to open .syn files. 
            If None (default), reads from current directory.
        """

        # --- Global loader attributes (from the recording) -- #

        # an empty dict with 2 keys, connections found and tested 
		#per each recording configuration (ex: octuple, quintuple)
		
        self.__configuration = utils.configuration() 

        # Total number of recorded cells
        self.__nPV = 0 # total number of recorded PV-positive cells
        self.__nGC = 0 # total number of recorded granule cells

        # all conection motifs are zero at construction
        self.__motif = motifcounter() 

        # --- dict attributes -- #

        # a list of dictionaries whose keys are:
        # filename, matrix and connections
        self.__experiment = list()

        # a list of dictionaries whose indices are the
        # number of PV cells recorded simulatenously
        # (e.g. DataLoader.PV[2] returns a configuration dictionary
        # with the recording configurations containing 2 PV cells
        self.__PV = [utils.configuration() for _ in range(9)]

        cwd = os.getcwd()
        if path is not None:
            os.chdir(path)
            
        PVsyn = glob.glob("*.syn")

        for fname in PVsyn:
            mydict = dict()
            mydict['fname'] = fname
            matrix, motif = self.__loadsyn(fname, int(fname[0]))
            mydict['matrix'] = matrix
            mydict['motif'] = motif 

            self.__experiment.append( mydict )
        
        os.chdir(cwd)

        # prompt number of files loaded
        print("%4d syn  files loaded" %len(PVsyn))

    def __loadsyn(self, filename, nPV):
        """
        Reads the matrix of connectivities from a *syn file and 
        extract basic information about connectivity and cell types.

        Arguments 
        ---------
        filename : string
            filename or path to open  

        nPV : integer
            the number of PV+ cells contained in the matrix

        Returns
        -------
        matrix : 2D Numpy matrix
            connectivity matrix containing <0> if no connection, <1> if
            chemical synapse, <2> if electrical synapse and <3> if both
        
        connections : A connecion dictionary containing the number and
            tested and found connections for every type.
        
        """

        # error if filename is not *.sys
        try:
            if not filename[-3:] == 'syn':
                raise IOError('Filename has no *.syn extension')
        except IOError:
            raise

        matrix = np.loadtxt(filename, dtype=int)
        ncells = matrix.shape[0]

        # UPDATE recording configurationtype
        configurationtype = enum[ncells]
        self.configuration[ configurationtype ] +=1 

        # UPDATE PV dictionary list :
        PVdict = self.PV[nPV]
        PVdict[configurationtype ] +=1

        # UPDATE number of total PV cells
        self.__nPV += nPV

        # UPDATE number of granule cells
        nGC = ncells - nPV
        self.__nGC += nGC 

        # UPDATE connections 
        # count synapses:slice the matrix to get general connection types

        II_matrix = utils.II_slice(matrix, nPV)
        EI_matrix = utils.EI_slice(matrix, nPV)
        IE_matrix = utils.IE_slice(matrix, nPV)
        EE_matrix = utils.EE_slice(matrix, nPV)

        # UPDATE connection
        mymotif = iicounter(II_matrix) + eicounter(EI_matrix) + \
            iecounter(IE_matrix) + eecounter(EE_matrix) 
        # UPDATE connection motif
        self.__motif += mymotif

        return( matrix, mymotif )

    def stats(self, show):
        """
        Print basis statistics from the recorded dataset

        Argument
        --------

        show : string 
            A string with 'conf' to show the configurations or
            'prob' to show the different probabilities.

        Returns
        -------
            An ASCII table with basic statistics
        """

        if show == 'conf':
            info = [
                ['Concept', 'Quantity'],
                ['PV-positive cells', self.nPV],
                ['Granule cells', self.nGC],
                [' ',' '],
                ['Pairs       ', self.configuration[enum[2]]],
                ['Triplets    ', self.configuration[enum[3]]],
                ['Quadruplets ', self.configuration[enum[4]]],
                ['Quintuplets ', self.configuration[enum[5]]],
                ['Sextuplets  ', self.configuration[enum[6]]],
                ['Septuplets  ', self.configuration[enum[7]]],
                ['Octuplets   ', self.configuration[enum[8]]],
            ]
            table = AsciiTable(info)
            print (table.table)

        if show == 'prob':
            
            info = [
                ['Connection type', 'Value'],
                ['PV-PV chemical synapses', self.II_chem_found],
                ['PV-PV electrical synapses', self.II_elec_found],
                ['PV-PV one chemical with electrical', self.II_ce1_found],
                ['PV-PV bidirectional chemical with electrical', self.II_ce2_found],
                [' ',' '],
                ['P(PV-PV) chemical synapse', self.II_chem_found/self.II_chem_tested],
                ['P(PV-PV) electrical synapse', self.II_elec_found/self.II_elec_tested],
                ['P(PV-PV) one chemical with electrical', self.II_ce1_found/self.II_ce1_tested],
                ['P(PV-PV) bidirectional chemical with electrical', self.II_ce2_found/self.II_ce2_tested],
                [' ',' '],
                ['PV-GC chemical synapses', self.IE_found],
                ['GC-PC chemical synapses', self.EI_found],
                [' ',' '],
                ['P(PV-GC) chemical synapse',self.IE_found/self.IE_tested],
                ['P(GC-PC) chemical synapse', self.EI_found/self.EI_tested],
                [' ',' '],
            ]
            table = AsciiTable(info)
            print (table.table)

    def __len__(self):
        """
        Returns the number of experiments in the data set
        """
        return len(self.experiment)



    # only getters for private attributes 
    configuration = property(lambda self: self.__configuration)
    PV = property(lambda self: self.__PV)
    nGC = property(lambda self: self.__nGC)
    nPV = property(lambda self: self.__nPV)
    motif = property(lambda self: self.__motif)
    experiment = property(lambda self: self.__experiment)


    # usefull attributes
    II_chem_found = property(lambda self: self.motif['ii_chem']['found'])
    II_chem_tested = property(lambda self: self.motif['ii_chem']['tested'])

    II_elec_found = property(lambda self: self.motif['ii_elec']['found'])
    II_elec_tested = property(lambda self: self.motif['ii_elec']['tested'])

    II_ce1_found = property(lambda self: self.motif['ii_ce1']['found'])
    II_ce1_tested = property(lambda self: self.motif['ii_ce1']['tested'])

    II_ce2_found = property(lambda self: self.motif['ii_ce2']['found'])
    II_ce2_tested = property(lambda self: self.motif['ii_ce2']['tested'])

    
    IE_found = property(lambda self: self.motif['ie']['found'])
    EI_found = property(lambda self: self.motif['ei']['found'])

    EI_tested = property(lambda self: self.motif['ei']['tested'])
    IE_tested = property(lambda self: self.motif['ei']['tested'])


if __name__ == "__main__":
    # %run in IPython
    mydataset = DataLoader('../data')
    mydataset.stats(show='conf')
    mydataset.stats(show='prob')
    myfilelist = ['./data/1_170302_02.dist', 
        './data/1_170214_03.dist',
        './data/1_170307_02.dist']
            
