"""
loader.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Wed Jul 19 01:45:16 CEST 2017
Last change: Thu Jul 20 21:06:53 CEST 2017

Contains a class to load ASCII files with connectivities and  
distances between neurons recorded in an simultaneous whole-cell
patch clamp recording.

Example:
>>> mydataset = DataLoader("./data")
>>> mydataset.stats
"""

import glob, os
import numpy as np

from terminaltables import AsciiTable

enum = {2: 'pairs', 3: 'triplets', 4: 'quadruplets', 5: 'quintuplets', 
        6: 'sextuplets', 7: 'septuplets', 8: 'octuples'}

class DataLoader(object):
    """
    A class to load synaptic type and distances from connectivity
    matrix in ./data folder. Check Readme.txt for details
    """

    def __init__(self, path = None):
        """
        Reads all *.syn and *.dist files contained in path folder

        Arguments:
        path        -- a string containing the folder of the files. If
                       None, then reads from current directory.
        """

        # set recording configurations at zero
        self.__myconfiguration = dict()
        for label in enum.values():
            self.__myconfiguration[label] = 0

        self.__nGC = 0 # number of granule cells
        self.__nPV = 0 # number of PV-positive cells

        # conections found are zero at construction
        self.__II, self.__IE, self.__EI = 0, 0, 0

        # conections tested are zero at construction
        self.__II_tested, self.__IE_tested, self.__EI_tested = 0, 0, 0

        cwd = os.getcwd()
        if path is not None:
            os.chdir(path)
            
        PVsyn = glob.glob("*.syn")
        PVdist = glob.glob("*.dist")# TODO: read distances

        for fname in PVsyn:
            self.__readsyn(filename = fname, nPV = int(fname[0]))
        
        os.chdir(cwd)

        # prompt number of files loaded
        print("%4d syn  files found" %len(PVsyn))
        print("%4d dist files found\n" %len(PVdist))

    def __readsyn(self, filename, nPV):
        """
        Arguments: 
        filename    -- a string containing the file to open
        nPV         -- (int) the number of PV cells that contains
        """
        matrix = np.loadtxt(filename, dtype=int)

        ncells = matrix.shape[0]
        # update recording configuration
        self.myconfiguration[ enum[ncells] ] +=1 

        nGC = ncells - nPV # number of granule cels

        self.__nGC += nGC
        self.__nPV += nPV

        self.__II_tested += nPV * (nPV - 1)
        self.__IE_tested += nPV * nGC
        self.__EI_tested += nGC * nPV

        # read non-zero values from slicing the matrix 
        II_found = np.count_nonzero( matrix[ :nPV][ :,range(0, nPV)] )
        IE_found = np.count_nonzero( matrix[ :nPV][ :,range(nPV, ncells)] )
        EI_found = np.count_nonzero( matrix[nPV: ][ :,range(0, nPV)] )

        self.__II += II_found
        self.__IE += IE_found
        self.__EI += EI_found

    def __stats(self):
        """
        print basis statistics from the recorded dataset
        """

        data = [
                ['Concept', 'Quantity'],
                ['PV-positive cells', self.nPV],
                ['Granule cells', self.nGC],
                [' ',' '],
                ['Pairs       ', self.myconfiguration[enum[2]]],
                ['Triplets    ', self.myconfiguration[enum[3]]],
                ['Quadruplets ', self.myconfiguration[enum[4]]],
                ['Quintuplets ', self.myconfiguration[enum[5]]],
                ['Sextuplets  ', self.myconfiguration[enum[6]]],
                ['Septuplets  ', self.myconfiguration[enum[7]]],
                ['Octuplets   ', self.myconfiguration[enum[8]]],
                [' ',' '],
                ['PV-PV connections', self.II],
                ['PV-GC connections', self.IE],
                ['GC-PC connections', self.EI],
                [' ',' '],
                ['P(PV-PV) connection', float(self.II)/self.II_tested],
                ['P(PV-GC) connection', float(self.IE)/self.IE_tested],
                ['P(GC-PC) connection', float(self.EI)/self.EI_tested]
        ]
        table = AsciiTable(data)
        print (table.table)

    # only getters for private attributes and methods 
    myconfiguration = property(lambda self: self.__myconfiguration)
    nGC = property(lambda self: self.__nGC)
    nPV = property(lambda self: self.__nPV)
    
    IE = property(lambda self: self.__IE)
    EI = property(lambda self: self.__EI)
    II = property(lambda self: self.__II)

    IE_tested = property(lambda self: self.__IE_tested)
    EI_tested = property(lambda self: self.__EI_tested)
    II_tested = property(lambda self: self.__II_tested)

    # only getter for private methods
    stats = property(lambda self: self.__stats())


if __name__ == "__main__":
    # %run in IPython
    mydataset = DataLoader('./data')
    mydataset.stats
        
            
