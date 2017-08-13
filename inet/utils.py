"""
utils.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created:  Sun Jul 30 08:34:28 CEST 2017

A collection of utilities to use with the inet module
"""
import numpy as np

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
EE_slice = lambda matrix, nPV: matrix[nPV: ][ :,range(nPV,matrix.shape[0])]

def configuration():
    """
    Returns an dictionary whose keys are the values of
    the enum dictionary:

    enum = {2: 'pairs', 3: 'triplets', 4: 'quadruplets', 5: 'quintuplets', 
        6: 'sextuplets', 7: 'septuplets', 8: 'octuples'}

    It allows to call the dictionary like dict[enum(8)] in stead of 
    having to write the whole string (e.g. dict['octuples'])
    """

    mydict = dict()
    for label in enum.values():
            mydict[label] = 0
        
    return( mydict )

def rand_squarematrix(size, prob):
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
    nconn = n*(n-1)
    A = np.zeros((n,n), dtype = int)

    # take all non-diagonal elements
    x,y = np.where(~np.eye(A.shape[0], dtype=bool))

    myids = zip(x,y) # list with non-diagonal coord

    mymask =  np.random.rand( nconn )<prob  # True when connection

    my_ones = np.ma.array(range(nconn), mask = ~mymask).compressed()
    
    for i in my_ones:
        coor = myids[i]
        A[coor] = 1
    
    return( A )
        
        
        

