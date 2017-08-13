"""
motifs.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Thu Aug  3 16:26:12 CEST 2017

Contains classes to quantifiy and generate connectivity models based 
on recording synapses between principal cells and interneurons recorded 
with a simultaneous whole-cell patch clamp recording configuration
"""
import numpy as np

class MotifCounter(dict):
    """
    General porpose class that involves an extended dictionary 
    with the number of connections found and tested for different types 
    of connections. Different classes will inherit from this class
    to perform basic arithmetic operations between objects (like adition
    or sum)

    Example
    -------
    >>> mymotifs = MotifCounter(data = 1) #extended dictionary class
    >>> {data: 1}
    """
    def __init__(self, *argv, **kargw):
        """
        Create an extended dictionay with values and keys as arguments
        this method will be overwritten in daugther motif classes
        """
        # subclass python dictionary without any key
        # key with motifs will be added in subclasses construction later 
        super(MotifCounter, self).__init__(*argv, **kargw)

    def __call__(self, *argv, **kargw):
        """
        Returns a new instance of the entended dictionary class 
        """
        return MotifCounter(*argv, **kargw) 

    def __add__(self, MotifCounterObj):
        """
        addition between two MotifCounter objects creates a new object
        with the intersection of the respective keys and the sum of
        the two objects that have common keys.
        """

        mysum = MotifCounter() # casting the result to MotifCounter

        # 1) add common keys
        # the same MotifCounter object may have different keys!!!
        common = set(self.keys()).intersection(MotifCounterObj.keys())
        commonkeys = list(common)
        if commonkeys: # if not empty

            for key in commonkeys:
                found =  self[key]['found']  + MotifCounterObj[key]['found']
                tested = self[key]['tested'] + MotifCounterObj[key]['tested']
                mysum.__setitem__(key , {'tested':tested, 'found':found})
       
        # 2) add different keys 
        diff1 = set(self.keys()).difference(mysum.keys()) 
        diff1keys = list(diff1)

        if diff1keys: # if not empty
            for key in diff1keys:
                mysum.__setitem__(key, self[key])

        diff2 = set(MotifCounterObj.keys()).difference(mysum.keys()) 
        diff2keys = list(diff2)

        if diff2keys: # if not empty
            for key in diff2keys:
                mysum.__setitem__(key, MotifCounterObj[key])

        return(mysum)
        
    def __radd__(self, MotifCounterObj):
        """
        Sum more than two instances of MotifCounterObj
        """
        return self.__add__(MotifCounterObj)

class IIMotifCounter(MotifCounter):
    """
    Create a MotifCounter type object with connectivity motifs
    between interneurons. The motifs measured are the following:

    ii_chem : a chemical synapse between interneurons
    ii_elec : an electrical synapse between interneurons
    ii_ce1 : an alectrical synapse together with ONE chemical
    ii_ce2 : an alectrical synapse together with TWO chemical
    
    """
    motiflist = ['ii_chem', 'ii_elec', 'ii_ce1', 'ii_ce2']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between inhibitory neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            excitatory neurons (pre) and inhibitory neurons (post).
        
        """
        super(IIMotifCounter, self).__init__()

        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix) # requires previous creation of keys

    def __call__(self, matrix = None):
        """
        Returns a IIMotifCounter object with counts of motifs
        """
        return IIMotifCounter(matrix) # will count motifs

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        try:
            if matrix.shape[0] != matrix.shape[1]:
                raise IOError("matrix must be a square matrix!")
        except IOError:
            raise

        n = matrix.shape[0] # number of presynaptic neurons

        II_chem = matrix[ np.where(matrix==1) ].size
        II_elec = matrix[ np.where(matrix==2) ].size
        II_ce1 = matrix [ np.where(matrix==3)].size
        II_chem += II_ce1
        II_elec += II_ce1
        
        # count unidirectional chemical synapses with gap junctions (ce1)
        # or bidirectional chemical synapses with gap junctions (ce2)
        II_ce2 = 0
        pre,post = np.where(matrix==3)
        if matrix[ (post,pre) ] == 1:
            II_ce2 +=1 # add bidirectional chemical to electrical
            II_ce1 +=1 # add another unidirectional to electrical

        # possible connections
        n_chem = n*(n-1)
        n_elec = n*(n-1)/2
        n_ce1 = n_elec*2
        n_ce2 = n_elec
        
        self.__setitem__('ii_chem', {'tested':n_chem, 'found':II_chem})
        self.__setitem__('ii_elec', {'tested':n_elec, 'found':II_elec})
        self.__setitem__('ii_ce1' , {'tested':n_ce1 , 'found':II_ce1 })
        self.__setitem__('ii_ce2' , {'tested':n_ce2 , 'found':II_ce2 })
        
    
class EIMotifCounter(MotifCounter):
    """
    Create a MotifCounter object with the the number of 
    connections found and tested between exfor the following connection 
    types:

    ei : a chemical synapse between excitatory and inhibitory neurons
    """
    motiflist = ['ei']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between inhibitory and excitatory
        neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            excitatory neurons (pre) and inhibitory neurons (post).
        
        """
        super(EIMotifCounter, self).__init__()
        
        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix) # requires previous creation of keys

    def __call__(self, matrix = None):
        """
        Returns a EIMotifCounter object with counts of motifs
        """
        return EIMotifCounter(matrix) # will count motifs

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        ecell, icell = matrix.shape

        EI_found = np.count_nonzero(matrix)
        EI_tested = ecell * icell # possible EI connections

        self.__setitem__('ei', {'tested':EI_tested, 'found':EI_found})

class IEMotifCounter(MotifCounter):
    """
    Create a MotifCounter object with the the number of 
    connections found and tested between exfor the following connection 
    types:

    ie : a chemical synapse between excitatory and inhibitory neurons
    """
    motiflist = ['ie']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between excitatory and inhibitory
        neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            excitatory neurons (pre) and inhibitory neurons (post).
        
        """
        super(IEMotifCounter, self).__init__()
        
        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix) # requires previous creation of keys

    def __call__(self, matrix = None):
        """
        Returns a EIMotifCounter object with counts of motifs
        """

        return IEMotifCounter(matrix) # will count motifs

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        ecell, icell = matrix.shape

        IE_found = np.count_nonzero(matrix)
        IE_tested = ecell * icell # possible EI connections

        self.__setitem__('ie', {'tested':IE_tested, 'found':IE_found})

class EEMotifCounter(MotifCounter):
    """
    Create a MotifCounter object with the the number of 
    connections found and tested between exfor the following connection 
    types:

    ee : a chemical synapse between excitatory neurons
    """
    motiflist = ['ee']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between excitatory and inhibitory
        neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            excitatory neurons (pre) and inhibitory neurons (post).
        
        """
        super(EEMotifCounter, self).__init__()
        
        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix) # requires previous creation of keys

    def __call__(self, matrix = None):
        """
        Returns a EIMotifCounter object with counts of motifs
        """

        return EEMotifCounter(matrix) # will count motifs

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        ncells = matrix.shape[0]

        EE_found = np.count_nonzero(matrix)
        EE_tested = ncells * (ncells-1) # possible EE connections

        self.__setitem__('ee', {'tested':EE_tested, 'found':EE_found})



# ready-to-use objects
motifcounter = MotifCounter()
iicounter    = IIMotifCounter()
eicounter    = EIMotifCounter()
iecounter    = IEMotifCounter()
eecounter    = EEMotifCounter()
