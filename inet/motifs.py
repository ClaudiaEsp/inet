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

    For example
    >>> mymotifs = MotifCounter() #extended dictionary
    >>> mymotifs['ii_chem']
    >>> {'found': 0, 'tested':0}
    >>> mymotifs['ii_chem']
    """

    def __init__(self, *argv, **kargw):
        """
        """
        # subclass python dictionary without any key
        # key will be added in subclasses later 
        super(MotifCounter, self).__init__(*argv, **kargw)

    def __call__(self, matrix = None):
        """
        Returns a MotifCounter object
        """
        return MotifCounter(matrix) # return a new Connection object

            

    def __radd__(self, MotifCounterObj):
        pass

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

        if matrix is not None:
            self.read_matrix(matrix)
        else:
            for key in self.motiflist:
                self.__setitem__(key, {'tested':0, 'found':0})

    def __call__(self, matrix = None):
        """
        Returns a IIMotifCounter object with counts of motifs
        """
        return IIMotifCounter(matrix)
        
    def __add__(self, MotifCounterObj):
        """
        addition between MotifCounter objects
        """
        mysum = IIMotifCounter()
        for key in self.keys():
            found = self[key]['found'] + MotifCounterObj[key]['found']
            tested = self[key]['tested'] + MotifCounterObj[key]['tested']
            mysum[key]['found'] = found 
            mysum[key]['tested'] = tested 

        return(mysum)

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
        II_ce1 = matrix [ np.where(matrix == 3)].size
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
    _MOTIF_TYPES = dict.fromkeys(motiflist, {'tested':0, 'found':0})

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
        
        if matrix is not None:
            self.read_matrix(matrix)
        else:
            for key in self.motiflist:
                self.__setitem__(key, {'tested':0, 'found':0})

    def __call__(self, matrix = None):
        """
        Returns a EIMotifCounter object with counts of motifs
        """
        return EIMotifCounter(matrix)

    def __add__(self, MotifCounterObj):
        """
        addition between MotifCounter objects
        """
        mysum = EIMotifCounter()
        for key in self.keys():
            found = self[key]['found'] + MotifCounterObj[key]['found']
            tested = self[key]['tested'] + MotifCounterObj[key]['tested']
            mysum[key]['found'] = found 
            mysum[key]['tested'] = tested 

        return(mysum)

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
    _MOTIF_TYPES = dict.fromkeys(motiflist, {'tested':0, 'found':0})

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
        
        if matrix is not None:
            self.read_matrix(matrix)
        else:
            for key in self.motiflist:
                self.__setitem__(key, {'tested':0, 'found':0})

    def __call__(self, matrix = None):
        """
        Returns a EIMotifCounter object with counts of motifs
        """
        return IEMotifCounter(matrix)

    def __add__(self, MotifCounterObj):
        """
        addition between MotifCounter objects
        """
        mysum = IEMotifCounter()
        for key in self.keys():
            found = self[key]['found'] + MotifCounterObj[key]['found']
            tested = self[key]['tested'] + MotifCounterObj[key]['tested']
            mysum[key]['found'] = found 
            mysum[key]['tested'] = tested 

        return(mysum)

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        ecell, icell = matrix.shape

        IE_found = np.count_nonzero(matrix)
        IE_tested = ecell * icell # possible EI connections

        self.__setitem__('ie', {'tested':IE_tested, 'found':IE_found})


# ready-to-use objects
motifcounter = MotifCounter()
iicounter    = IIMotifCounter()
eicounter    = EIMotifCounter()
iecounter    = IEMotifCounter()
