"""
simulations.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Wed Oct 25 10:22:47 CEST 2017

Contains models to simulate different null hypothesis to be
tested againts the empirical data.

Requires inet
"""

from __future__ import division

import numpy as np
import pickle
from itertools import combinations

from inet.motifs import iicounter

def sigmoid(x, A, C, r):
    """
    solves for the following function:
    f(x; A, C, r ) = ( A  / ( 1 + np.exp((x-C)/r)))
    
    where x is the independent variable,
    A is the maximal amplitude of the curve,
    C is the half point of the sigmoidal function,
    r is rate of maximum population growth.
    """
    return  A  / ( 1 + np.exp((x-C)/r) )

# distance-depedent functions
# param for https://github.com/ClaudiaEsp/inet/Analysis/Sigmoids.ipynb
chem_param = pickle.load( open('chem_syn.p', 'rb') )
elec_param = pickle.load( open('elec_syn.p', 'rb') )

fchem = lambda x: sigmoid(x, *chem_param)
felec = lambda x: sigmoid(x, *elec_param)

def chem_squarematrix(size, prob):
    """
    generates a square random matrix with a probability 'prob'
    of having ones, zero otherwise. It does not take into account
    the diagonal, which is always zero.

    Arguments
    ---------
    size : int
        the size of the square matrix
    prob : float
        the probability of having ones.

    Returns
    -------
    a 2D Numpy matrix.
    """

    n = size
    ntested = n*(n-1)
    A = np.zeros((n,n), dtype = int)

    # take all non-diagonal elements
    x,y = np.where(~np.eye(A.shape[0], dtype = bool))

    myids = zip(x,y) # list with non-diagonal coord

    mymask =  np.random.rand( ntested )<prob  # True when connection

    my_ones = np.ma.array(range(ntested), mask = ~mymask).compressed()
    
    for i in my_ones:
        coor = myids[i]
        A[coor] = 1
    
    return( A )
        

def elec_squarematrix(size, prob):
    """
    generates a square random matrix with a probability 'prob'
    of having values == 2, zero otherwise. It does not take into account
    the diagonal, which is always zero.

    Arguments
    ---------
    size : int
        the size of the square matrix
    prob : float
        the probability of having ones.

    Returns
    -------
    a 2D Numpy matrix.
    """

    n = size
    A = np.zeros((n,n), dtype = int)

    # take a list with  all possible 2-combinations
    pairs = [i for i in combinations(range(n),2)]
    # shuffle the list!
    np.random.shuffle(pairs) 
    
    for i in pairs:
        A[i] = (np.random.rand()<prob)*2
    
    return( A )
        
        
class IIUniformModel(object):
    """
    This is a connectivity model that assumes a constant and uniform
    connection probability between interneurons.
    """        

    def __init__(self, dataset):
        """
        
        Arguments
        ---------
        dataset: DataLoaderObject (see DataLoader in inet module) 
        """

        # get a list with (nPV, nRecord) for nPV>2
        self.__PVconf = list()
        for nPV in range(2,9): # between 2 and 8 simultaneous cells
            nRecord = np.sum( dataset.IN[nPV].values() )
            if nRecord: # larger than zero recordings
                self.PVconf.append((nPV, nRecord))
                print('{:2d} recordings with {} PV-cells'.format(nRecord,nPV ))

        self.__PC = dataset.motif.ii_chem_found/dataset.motif.ii_chem_tested
        self.__PE = dataset.motif.ii_elec_found/dataset.motif.ii_elec_tested

        self.nchem = np.empty(0) # chemical synapse (ii_chem)
        self.nelec = np.empty(0) # electrical synapse (ii_elec) 

        self.nbid = np.empty(0) # bidirectional chemical synapse (ii_c2)
        self.ncon = np.empty(0) # convergent inhibitory motifs (ii_con)
        self.ndiv = np.empty(0) # divergent inhibitory motifs (ii_div)
        self.nlin = np.empty(0) # linear inhibitory motifs (ii_lin)

        self.nc1e = np.empty(0) # electrical and unidirectional chemical (ii_c1e)
        self.nc2e = np.empty(0) # electrical and bidirectional chemical (ii_c2e)

    def __simulate_dataset(self):
        """
        Simulates chemical and electrical synapses with an 
        average connectivity given as arguments. It will automatically
        update the counter of inhibitory motifs (iicounter)

        Returns:
        An IICounter Object

        """ 
        myiicounter = iicounter()

        # simulates the nubmer of PVs and how many recordings
        for nPV, nRecord in self.PVconf:
            for _ in range(nRecord): 
                C = chem_squarematrix(size = nPV, prob = self.PC)
                E = elec_squarematrix(size = nPV, prob = self.PE)
                
                S = C + E
                x,y = np.where(S==2) # eliminate '1' form the opposite pos
                mycoor = zip(y, x)
                for i,j in mycoor:
                    if S[i,j]==1:
                        S[i,j]=3
                        S[j,i]=0

                myiicounter += iicounter(S)

        return( myiicounter )
        
    def run(self, n_iter, seed=None):
        """
        Arguments:
        niter:  n_iter      
            Number of iterations

        Update the number of motifs found in the lists
        """
        np.random.seed(seed)
        self.iicounter = iicounter() # set counter to zero!

        # resize NumPy arrays and set pointers
        self.nchem = np.resize(self.nchem, n_iter)
        self.nelec = np.resize(self.nelec, n_iter) 

        self.nbid = np.resize(self.nbid, n_iter)
        self.ncon = np.resize(self.ncon, n_iter)
        self.ndiv = np.resize(self.ndiv, n_iter)
        self.nlin = np.resize(self.nlin, n_iter)

        self.nc1e = np.resize(self.nc1e, n_iter)
        self.nc2e = np.resize(self.nc2e, n_iter)

        for i in range(n_iter):
            mysim = self.__simulate_dataset()
            self.nchem[i] = mysim['ii_chem']['found']
            self.nelec[i] = mysim['ii_elec']['found']

            self.nbid[i] = mysim['ii_c2']['found'] 
            self.ncon[i] = mysim['ii_con']['found'] 
            self.ndiv[i] = mysim['ii_div']['found'] 
            self.nlin[i] = mysim['ii_lin']['found'] 

            self.nc1e[i] = mysim['ii_c1e']['found'] 
            self.nc2e[i] = mysim['ii_c2e']['found'] 


    # only getters for private attributes 
    PVconf = property(lambda self: self.__PVconf)
    PC = property(lambda self: self.__PC)
    PE = property(lambda self: self.__PE)


class IISigmoidModel(object):
    """
    This is a connectivity model that assumes a sigmoid-like  
    connection probability between interneurons.
    """        


