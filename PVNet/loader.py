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

import glob, os
import numpy as np

from terminaltables import AsciiTable

import utils
from utils import enum

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

        # --- simple attributes -- #

        # all configurations
        self.__configuration = utils.configuration()

        # Total number of recorded cells
        self.__nPV = 0 # total number of recorded PV-positive cells
        self.__nGC = 0 # total number of recorded granule cells

        # all conections are zero at construction
        self.__connection = utils.connection() 

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
            matrix, connect = self.__loadsyn(fname, int(fname[0]))
            mydict['matrix'] = matrix
            mydict['connection'] = connect

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
        # slice the matrix to get general connection types
        EI_matrix = utils.EI_slice(matrix, nPV)

        # load connections type

        II_matrix = utils.II_slice(matrix, nPV)
        II_chem_found  = II_matrix[ np.where(II_matrix==1) ].size
        II_chem_found += II_matrix[ np.where(II_matrix==3) ].size

        II_elec_found  = II_matrix[ np.where(II_matrix==2) ].size
        II_elec_found += II_matrix[ np.where(II_matrix==3) ].size

        II_both_found = II_matrix[ np.where(II_matrix==3) ].size
        II_chem_tested = nPV * (nPV - 1)
        II_elec_tested = int(II_chem_tested/2)
        II_both_tested = II_elec_tested 

        EI_matrix = utils.EI_slice(matrix, nPV)
        EI_tested = nGC * nPV
        EI_found = np.count_nonzero(EI_matrix)

        IE_matrix = utils.IE_slice(matrix, nPV)
        IE_tested = nPV * nGC
        IE_found = np.count_nonzero(IE_matrix)

        mydict = utils.connection()
        mydict['II_chem']['found']  = II_chem_found
        mydict['II_chem']['tested'] = II_chem_tested
        mydict['II_elec']['found']  = II_elec_found
        mydict['II_elec']['tested']= II_elec_tested
        mydict['II_both']['found']  = II_both_found
        mydict['II_both']['tested'] = II_both_tested

        mydict['EI']['found'] = EI_found
        mydict['EI']['tested'] = EI_tested

        mydict['IE']['found'] = IE_found
        mydict['IE']['tested'] = IE_tested

        # UPDATE connection
        self.add_connection(mydict)

        return( matrix, mydict )

    def add_connection(self, mydict):
        """
        Adds the value of a connection dictionary to the 
        connection attribute of the object
        """
        for key in mydict:
            self.connection[key]['found']  += mydict[key]['found']
            self.connection[key]['tested'] += mydict[key]['tested']
        

    def readmatrix(self, filelist):
        """
        Read matrices from a list of files that correspond to the 
        experiments loaded in the dataset.

        Arguments 
        ---------
        filelist    -- a list of filenames containing matrices to open
        """
        
        # load all matrices from filelist in data
        target = list()
        for filename in filelist:
            target.append( np.loadtxt(filename, dtype = float) )

        # remove extension and take the last 11 chars
        flist = [os.path.splitext(i)[0][-11:] for i in filelist]

        # look for index of an experiment containing that filename
        match = list()
        for i, fname in enumerate(flist):
            for o, experiment in enumerate(self.experiment): #
                if fname in experiment['fname']:
                    
                    print(fname, i, o)
                    match.append(o)
                    break # if found, 
        
        print("list of colected indices",match)
                    
        #target[0][np.where(matrix == 1)]
        
        mydict = dict()
        mydict['II_chem'] = 0
        mydict['II_elec'] = 0
        mydict['IE'] = 0
        mydict['EI'] = 0

        for j, idx in enumerate(match):
            destiny = target[j]
            dataset = self.experiment[idx]['matrix']
            data = destiny[ np.where(dataset==1) ].tolist()
            print(data)

            
        return( mydict )
        

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

            PInhibition = (self.II_chem_found + self.II_elec_found)/(self.II_chem_tested + self.II_elec_tested)
            
            info = [
                ['Connection type', 'Value'],
                ['PV-PV chemical synapses', self.II_chem_found],
                ['PV-PV electrical synapses', self.II_elec_found],
                ['PV-PV both synapses together', self.II_both_found],
                ['PV-GC synapses', self.IE_found],
                ['GC-PC synapses', self.EI_found],
                [' ',' '],
                ['P(PV-PV) connection', PInhibition],
                ['P(PV-GC) connection',self.IE_found/self.IE_tested],
                ['P(GC-PC) connection', self.EI_found/self.EI_tested],
                [' ',' '],
                ['P(PV-PV) chemical synapse', self.II_chem_found/self.II_chem_tested],
                ['P(PV-PV) electrical synapse', self.II_elec_found/self.II_elec_tested],
                ['P(PV-PV) both synapse', self.II_both_found/self.II_both_tested],
            ]
            table = AsciiTable(info)
            print (table.table)



    # only getters for private attributes 
    configuration = property(lambda self: self.__configuration)
    PV = property(lambda self: self.__PV)
    nGC = property(lambda self: self.__nGC)
    nPV = property(lambda self: self.__nPV)
    connection = property(lambda self: self.__connection)
    experiment = property(lambda self: self.__experiment)


    # usefull attributes
    II_chem_found = property(lambda self: self.connection['II_chem']['found'])
    II_chem_tested = property(lambda self: self.connection['II_chem']['tested'])

    II_elec_found = property(lambda self: self.connection['II_elec']['found'])
    II_elec_tested = property(lambda self: self.connection['II_elec']['tested'])

    II_both_found = property(lambda self: self.connection['II_both']['found'])
    II_both_tested = property(lambda self: self.connection['II_both']['tested'])

    
    IE_found = property(lambda self: self.connection['IE']['found'])
    EI_found = property(lambda self: self.connection['EI']['found'])

    EI_tested = property(lambda self: self.connection['EI']['tested'])
    IE_tested = property(lambda self: self.connection['IE']['tested'])


if __name__ == "__main__":
    # %run in IPython
    mydataset = DataLoader('../data')
    mydataset.stats(show='conf')
    mydataset.stats(show='prob')
    myfilelist = ['./data/1_170302_02.dist', 
        './data/1_170214_03.dist',
        './data/1_170307_02.dist']
            
