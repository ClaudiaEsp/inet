"""
loader.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Wed Jul 19 01:45:16 CEST 2017

Contains a class to load ASCII files with connectivities and  
distances between neurons recorded in an simultaneous whole-cell
patch clamp recording.

Example:
>>> mydataset = DataLoader("./data")
>>> mydataset.stats # report basis connectivity statistics
"""

import glob, os
import numpy as np

from terminaltables import AsciiTable

enum = {2: 'pairs', 3: 'triplets', 4: 'quadruplets', 5: 'quintuplets', 
        6: 'sextuplets', 7: 'septuplets', 8: 'octuples'}

#-------------------------------------------------------------------------
# Auxiliary functions for slicing matrices according to number of PV cells
# for example II_matrix(matrix=2DNumPy, nPV=nPV) will return a 2D NumPy 
# array with inhibitory-to-inhibitory connections only
#-------------------------------------------------------------------------

II_slice = lambda matrix, nPV: matrix[:nPV][ :,range(nPV)]
IE_slice = lambda matrix, nPV: matrix[:nPV][ :,range(nPV, matrix.shape[0])]
EI_slice = lambda matrix, nPV: matrix[nPV: ][ :,range(nPV)]

class DataLoader(object):
    """
    A class to load synaptic type and distances from connectivity
    matrix in ./data folder. Check Readme.md for details
    """

    def __init__(self, path = None):
        """
        Reads all *.syn files contained in path folder

        Argument:
        ---------
        path : string 
            the path containing the folder to open .syn files. 
            If None (default), reads from current directory.
        """

        # set recording configurations at zero
        self.__myconfiguration = dict()
        for label in enum.values():
            self.__myconfiguration[label] = 0

        # Total number of recorded cells
        self.__nGC = 0 # number of granule cells
        self.__nPV = 0 # number of PV-positive cells

        # conections found are zero at construction
        self.__II, self.__IE, self.__EI = 0, 0, 0
        self.__II_chem = 0
        self.__II_elec = 0
        self.__II_both = 0

        # conections tested are zero at construction
        self.__II_tested, self.__IE_tested, self.__EI_tested = 0, 0, 0
        self.__II_chem_tested = 0
        self.__II_elec_tested = 0

        cwd = os.getcwd()
        if path is not None:
            os.chdir(path)
            
        PVsyn = glob.glob("*.syn")

        self.__experiment = list()
        for fname in PVsyn:
            mydict = dict()
            mydict['fname'] = fname
            mydict['matrix'] = self.__readsyn(fname, int(fname[0]))
            self.__experiment.append( mydict )
        
        os.chdir(cwd)

        # prompt number of files loaded
        print("%4d syn  files loaded" %len(PVsyn))

    def __readsyn(self, filename, nPV):
        """
        Reads the matrix of connectivities from a *syn file.

        Arguments 
        ---------
        filename : string
            filename or path to open  

        nPV : integer
            the number of PV+ cells contained in the matrix

        Returns
        -------
        matrix : 2D Numpy matrix
            connectivity matrix containing 0 if no connection, 1 if
            chemical synapse, 2 if electrical synapse and 3 if both
        
        """

        # error if filename is not *.sys
        try:
            if not filename[-3:] == 'syn':
                raise IOError('Filename has no *.syn extension')
        except IOError:
            raise

        matrix = np.loadtxt(filename, dtype=int)

        ncells = matrix.shape[0]
        # update recording configuration
        self.myconfiguration[ enum[ncells] ] +=1 

        nGC = ncells - nPV # number of granule cels

        self.__nGC += nGC
        self.__nPV += nPV

        # tested connections
        self.__II_tested += nPV * (nPV - 1)
        self.__IE_tested += nPV * nGC
        self.__EI_tested += nGC * nPV

        # slice the matrix to get general connection types
        II_matrix = II_slice(matrix, nPV)
        IE_matrix = IE_slice(matrix, nPV)
        EI_matrix = EI_slice(matrix, nPV)

        # found connections
        II_found = np.count_nonzero( II_matrix )
        IE_found = np.count_nonzero( IE_matrix )
        EI_found = np.count_nonzero( EI_matrix )
    
        # test II chemical and electrical synapes
        II_chem_tested = II_matrix.shape[0] * (II_matrix.shape[0] - 1) 
        II_elec_tested = II_chem_tested/2

        II_found_chem = II_matrix[ np.where(II_matrix==1) ].size
        II_found_elec = II_matrix[ np.where(II_matrix==2) ].size
        II_found_both = II_matrix[ np.where(II_matrix==3) ].size

        self.__II_chem_tested += II_chem_tested
        self.__II_elec_tested += II_elec_tested

        self.__II += II_found
        self.__IE += IE_found
        self.__EI += EI_found
        self.__II_chem += II_found_chem
        self.__II_elec += II_found_elec
        self.__II_both += II_found_both

        return( matrix )

    def readmatrixdist(self, filelist):
        """
        Read matrices from a list of files that correspond to the 
        experiments loaded in the dataset.

        Arguments: 
        filelist    -- a list of filenames containing matrices to open
        """
        
        # load all matrices from filelist in data
        data = list()
        for filename in filelist:
            data.append( np.loadtxt(filename, dtype = float) )

        # remove extension and take the last 11 chars
        flist = [os.path.splitext(i)[0][-11:] for i in filelist]

        # look for index of an experiment containing that filename
        id_files = list()
        for i, fname in enumerate(flist):
            for o, experiment in enumerate(self.experiment): #
                if fname in experiment['fname']:
                    
                    print(fname, i, o)
                    break # if found, 

            
                    
                    #mymatrix = data[i]
                    #II_syn(mymatrix)

        mydict = dict()
        mydict['II_tested'] = 0
        mydict['IE_tested'] = 0
        mydict['EI_tested'] = 0
        mydict['II_found'] = 0
        mydict['IE_found'] = 0
        mydict['EI_found'] = 0

        return( mydict )
        

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
                ['P(GC-PC) connection', float(self.EI)/self.EI_tested],
                [' ',' '],
                ['PV-PV chemical synapses only', self.II_chem],
                ['PV-PV electrical synapses only', self.II_elec],
                ['PV-PV both synapses together', self.II_both],
                [' ',' '],
                ['P(PV-PV) chemical only', float(self.II_chem)/self.II_chem_tested],
                ['P(PV-PV) electrical only', float(self.II_elec)/self.II_elec_tested],
        ]
        table = AsciiTable(data)
        print (table.table)


    # only getters for private attributes and methods 
    experiment = property(lambda self: self.__experiment) 
    
    myconfiguration = property(lambda self: self.__myconfiguration)
    nGC = property(lambda self: self.__nGC)
    nPV = property(lambda self: self.__nPV)
    
    IE = property(lambda self: self.__IE)
    EI = property(lambda self: self.__EI)
    II = property(lambda self: self.__II)
    II_chem = property(lambda self: self.__II_chem)
    II_elec = property(lambda self: self.__II_elec)
    II_both = property(lambda self: self.__II_both)

    IE_tested = property(lambda self: self.__IE_tested)
    EI_tested = property(lambda self: self.__EI_tested)
    II_tested = property(lambda self: self.__II_tested)
    II_chem_tested = property(lambda self: self.__II_chem_tested)
    II_elec_tested = property(lambda self: self.__II_elec_tested)

    # only getter for private methods
    stats = property(lambda self: self.__stats())


if __name__ == "__main__":
    # %run in IPython
    mydataset = DataLoader('./data')
    mydataset.stats
    myfilelist = ['./data/1_170302_02.dist', 
        './data/1_170214_03.dist',
        './data/1_170307_02.syn']
            
