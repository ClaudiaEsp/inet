"""
motifs.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Thu Aug  3 16:26:12 CEST 2017

Contains classes to quantifiy and generate connectivity models based 
on recording synapses between principal cells and interneurons recorded 
with a simultaneous whole-cell patch clamp recording configuration
"""

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

    def __add__(self, MotifCounterObj):
        """
        addition between MotifCounter objects
        """
        pass

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
        """
        super(IIMotifCounter, self).__init__()
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix)

    def __call__(self, matrix = None):
        """
        """
        return IIMotifCounter(matrix)
        
    def read_matrix(self, matrix):
        """
        """
        II_chem_found  = matrix[ np.where(II_matrix==1) ].size
        II_elec_found  = matrix[ np.where(II_matrix==2) ].size
        
    
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
        Counts connectivity motifs between excitatory and inhibitory
        neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            excitatory neurons (pre) and inhibitory neurons (post).
        
        """
        # subclass MotifCounter 
        super(EIMotifCounter, self).__init__(self._MOTIF_TYPES)

# ready-to-use objects
motifcounter = MotifCounter()
iicounter    = IIMotifCounter()
