"""
utils.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created:  Sun Jul 30 08:34:28 CEST 2017

A collection of utilities to use with the inet module
"""

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

def connection():
    """
    Create a connections dictionary with the number of connections found
    and tested for every type of connection: 

    II_chem : chemical synapse between inhibitory neurons
    II_elec : electrical synapse between inhibitory neurons
    II_both : connection containing both chemical and electrical synapse

    EI : synapse between excitatory and inhibitory neuron
    IE : synapse between inhibitory and excitatory neuron

    For example
    >>> mydict = connections()
    >>> mydict['II_chem']['found']
    >>> # could return a list with the properties of the connections found

    """

    myconnection = dict()
    myconnection['II_chem']=  {'found':0, 'tested':0}
    myconnection['II_elec']=  {'found':0, 'tested':0}
    myconnection['II_both']=  {'found':0, 'tested':0}

    myconnection['EI'] =   {'found':0, 'tested':0}
    myconnection['IE'] =   {'found':0, 'tested':0}

    return( myconnection )
