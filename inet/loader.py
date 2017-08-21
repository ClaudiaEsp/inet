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

import inet.utils as utils
from inet.utils import enum

from motifs import motifcounter
from motifs import iicounter, eicounter, iecounter, eecounter

class DataLoader(object):
    """
    A class to load synaptic type and distances from connectivity
    matrices. Check README.md for details
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
        self.__nIN = 0 # total number of recorded interneurons 
        self.__nPC = 0 # total number of recorded granule cells

        # all conection motifs are zero at construction
        self.__motif = motifcounter() 

        # --- dict attributes -- #

        # a list of dictionaries whose keys are:
        # filename, matrix and connections
        self.__experiment = list()

        # a list of dictionaries whose indices are the
        # number of interneurons recorded simulatenously
        # (e.g. DataLoader.IN[2] returns a configuration dictionary
        # with the recording configurations containing 2 interneurons
        self.__IN = [utils.configuration() for _ in range(9)]

        cwd = os.getcwd()
        if path is not None:
            os.chdir(path)
            
        filelist = glob.glob("*.syn")

        for fname in filelist:
            mydict = dict()
            mydict['fname'] = fname
            matrix, motif = self.__loadsyn(fname, int(fname[0]))
            mydict['matrix'] = matrix
            mydict['motif'] = motif 

            self.__experiment.append( mydict )
        
        os.chdir(cwd)

        # prompt number of files loaded
        print("%4d syn  files loaded" %len(filelist))

    def __loadsyn(self, filename, nIN):
        """
        Reads the matrix of connectivities from a *syn file and 
        extract basic information about connectivity and cell types.

        Arguments 
        ---------
        filename : string
            filename or path to open  

        nIN : integer
            the number of interneurons contained in the matrix

        Returns
        -------
        matrix : 2D Numpy matrix
            connectivity matrix containing <0> if no connection, <1> if
            chemical synapse, <2> if electrical synapse and <3> if both
        
        motifcounter : motifcounter
            A motif counter object containing the number of 
            tested and found connections for every type (see inet.motifs
            for details)
        
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

        # UPDATE IN dictionary list :
        INdict = self.IN[nIN]
        INdict[configurationtype ] +=1

        # UPDATE number of total IN cells
        self.__nIN += nIN

        # UPDATE number of granule cells
        nPC = ncells - nIN
        self.__nPC += nPC

        # UPDATE connections 
        # count synapses:slice the matrix to get general connection types

        if nIN==0:
            mymotif = eecounter(matrix)

        else:
            II_matrix = utils.II_slice(matrix, nIN)
            EI_matrix = utils.EI_slice(matrix, nIN)
            IE_matrix = utils.IE_slice(matrix, nIN)
            EE_matrix = utils.EE_slice(matrix, nIN)

            # UPDATE motif counters
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

        info : list
            An 2x2 list table with basic counting of cells and
            recording configurations. It can be plotted nicely
            with the terminal tables module.
        
        Example
        -------
        
        >>> from terminaltables import AsciiTable 
        >>> print Asciitable(info).table
        """

        if show == 'conf':
            info = [
                ['Concept', 'Quantity'],
                ['Principal cells', self.nPC],
                ['Interneurons', self.nIN],
                [' ',' '],
                ['Pairs       ', self.configuration[enum[2]]],
                ['Triplets    ', self.configuration[enum[3]]],
                ['Quadruplets ', self.configuration[enum[4]]],
                ['Quintuplets ', self.configuration[enum[5]]],
                ['Sextuplets  ', self.configuration[enum[6]]],
                ['Septuplets  ', self.configuration[enum[7]]],
                ['Octuplets   ', self.configuration[enum[8]]],
            ]

        return(info)

    def __len__(self):
        """
        Returns the number of experiments in the data set
        """
        return len(self.experiment)

    # only getters for private attributes 
    IN = property(lambda self: self.__IN)
    nPC = property(lambda self: self.__nPC)
    nIN = property(lambda self: self.__nIN)
    motif = property(lambda self: self.__motif)
    experiment = property(lambda self: self.__experiment)
    configuration = property(lambda self: self.__configuration)

if __name__ == "__main__":
    # %run in IPython
    mydataset = DataLoader('../data')
    mydataset.stats(show='conf')
    mydataset.stats(show='prob')
    myfilelist = ['./data/1_170302_02.dist', 
        './data/1_170214_03.dist',
        './data/1_170307_02.dist']
            
