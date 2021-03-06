"""
motifs.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Thu Aug  3 16:26:12 CEST 2017

Contains classes to count connectivity motifs based 
on recording synapses between principal cells and interneurons recorded 
with a simultaneous whole-cell patch clamp recording configuration.
"""

import numpy as np
from scipy.misc import comb
from itertools import permutations
from terminaltables import AsciiTable

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

        # dynamically rewrite object attributes
        for key in mysum:
            setattr(mysum, key+'_tested',mysum[key]['tested']) 
            setattr(mysum, key+'_found' ,mysum[key]['found' ]) 

        return(mysum)
        
    def __radd__(self, MotifCounterObj):
        """
        Sum more than two instances of MotifCounterObj
        """
        return self.__add__(MotifCounterObj)

    def __str__(self):
        """
        Show the dictionary with all the values found in a nice
        Ascii table when printing the object
        """
        info = [['Motif', 'found', 'tested'],]
        for key in self.keys():
            info.append([key, self[key]['found'], self[key]['tested']])

        info[1:] = (sorted(info[1:])) # sort keys
        
        table = AsciiTable(info)
        print(table.table) # return a string value
        return('') # has to return a string value
        

class EIMotifCounter(MotifCounter):
    """
    Create a MotifCounter object with the the number of 
    connections found and tested between exfor the following connection 
    types:

    ei : a chemical synapse between excitatory and inhibitory neurons
    e2i: two excitatory cells converging to one inhibitory neuron.
    """
    motiflist = ['ei', 'e2i', 'e3i']

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
        return EIMotifCounter(matrix) # will count motifs and update attr.

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        ecell, icell = matrix.shape

		
        ei_found = np.count_nonzero(matrix)
        ei_tested = ecell * icell # all possible unitary ei connections
 
        e2i_tested, e2i_found = 0, 0
        e3i_tested, e3i_found = 0, 0
		
        if ecell == 1:
            pass # e*i_tested and e*i_found will remain zero
        else:
            for col in range(icell):
                syn = np.count_nonzero(matrix[:,col]) 
                e2i_tested += int( comb(ecell,2) )
                e2i_found  += int( comb(syn,2)    )

                e3i_tested += int( comb(ecell,3) )
                e3i_found  += int( comb(syn,3)   )
			
        self.__setitem__('ei',  {'tested':ei_tested, 'found':ei_found} )
        self.__setitem__('e2i', {'tested':e2i_tested,'found':e2i_found})
        self.__setitem__('e3i', {'tested':e3i_tested,'found':e3i_found})
		
		
        # dynamically create attributes only if matrix is entered
        for key in self:
            setattr(self, key+'_tested', self[key]['tested'])
            setattr(self, key+'_found',  self[key]['found' ])

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
            inhibitory neurons (pre) and excitatory neurons (post).
        
        """
        super(IEMotifCounter, self).__init__()
        
        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix) # requires previous creation of keys

        for key in self:
            setattr(self, key+'_tested', self[key]['tested'])
            setattr(self, key+'_found',  self[key]['found' ])

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

		
        # dynamically create attributes only if matrix is entered
        for key in self:
            setattr(self, key+'_tested', self[key]['tested'])
            setattr(self, key+'_found',  self[key]['found' ])

class IIMotifCounter(MotifCounter):
    """
    Create a MotifCounter type object with connectivity motifs
    between same type of neurons. The motifs measured are the following:

    ii_chem : a chemical synapse between neurons
    ii_elec : an electrical synapse between neurons
    ii_c1e : an alectrical synapse together with ONE chemical
    ii_c2e : an alectrical synapse together with TWO chemical
    ii_c2  : two reciprocally connected chemical synapses
    ii_con : two neurons converging on to a third
    ii_div : one neuron diverging into two neurons 
    ii_lin : one neuron connected to a second one and this last to another
    
    """
    motiflist = ['ii_chem', 'ii_elec', 'ii_c1e', 'ii_c2e', 'ii_c2', \
        'ii_con', 'ii_div', 'ii_lin']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between inhibitory neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            recurrently connected inhibitory neurons
            
        
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

        syn_chem = matrix[ np.where(matrix==1) ].size
        syn_elec = matrix[ np.where(matrix==2) ].size
        syn_c1e =  matrix[ np.where(matrix==3) ].size # ** see below
        syn_chem += syn_c1e
        syn_elec += syn_c1e
        
        # count unidirectional chemical synapses with gap junctions (c1e)
        # or bidirectional chemical synapses with gap junctions (c2e)
        syn_c2e = 0

        if syn_c1e: # only if there are entries ==3 (see **)
            pre, post = np.where(matrix==3)
            mylist = zip(post,pre)
            for x,y in mylist:
                if matrix[ x,y ] == 1:
                    syn_c2e +=1 # add bidirectional chemical to electrical
                    syn_c1e +=1 # add another unidirectional to electrical


        # COUNT ONLY CHEMICAL SYNAPSES
        rows,cols = np.where(matrix==3) 
        A = matrix.copy()
        A[rows,cols] = 1
        A[np.where(matrix==2)] = 0 # remove electrical only

        # transform into matrix type to perform matrix operations (e.g Tr)
        # bidirec motifs are counted from the trace <Tr> of a <A> matrix:
        # n_reciprocal = Tr(A*A)/2, see Zhao et al., 2011
        A = np.matrix(A) 
        syn_c2 = int(np.sum( (A*A).diagonal() )/2) # bidirectional motifs

        J = A*A.T
        syn_con = int( ( J.sum()-A.sum() )/2) # convergent motifs

        J = A.T*A
        syn_div = int(( J.sum()-A.sum() )/2) # divergent motifs

        J = A*A
        syn_lin = int( J.sum() - np.sum(J.diagonal()) )# linear chain motifs

        # possible connections
        n_chem = n*(n-1)
        n_elec = n*(n-1)/2

        n_c1e = n_elec*2
        n_c2e = n_elec

        # see Zhao et al., eq 3
        n_c2 =    n*(n-1)/2
        n_con = ( n*(n-1)*(n-2) ) / 2
        n_div = ( n*(n-1)*(n-2) ) / 2 
        n_lin = ( n*(n-1)*(n-2) ) 
        
        motif = self.motiflist
        self.__setitem__(motif[0], {'tested':n_chem, 'found':syn_chem})
        self.__setitem__(motif[1], {'tested':n_elec, 'found':syn_elec})

        self.__setitem__(motif[2], {'tested':n_c1e , 'found':syn_c1e })
        self.__setitem__(motif[3], {'tested':n_c2e , 'found':syn_c2e })

        self.__setitem__(motif[4], {'tested':n_c2 ,  'found':syn_c2  })
        self.__setitem__(motif[5], {'tested':n_con , 'found':syn_con  })
        self.__setitem__(motif[6], {'tested':n_div , 'found':syn_div  })
        self.__setitem__(motif[7], {'tested':n_lin , 'found':syn_lin  })
        
        # dynamically rewrite object attributes
        for key in self:
            setattr(self, key+'_tested',self[key]['tested']) 
            setattr(self, key+'_found' ,self[key]['found' ]) 
    
    
class IIConMotifCounter(MotifCounter):
    """
    Create a MotifCounter type object with convergent connectivity motifs
    The motifs measured are the following:

    ii_con_e   : an electrical synapse between converging inhibitory neurons
    ii_con_c   : a chemical synapse between converging inhibitory 
    ii_con_c2  : a bidirectional chemical synapse between converging inhibitory neurons 
    ii_con_c1e : an alectrical synapse and chemical synapse between converging inhibitory neurons
    ii_con_c2e : an alectrical synapse and bidirectional chemical synapse between converging inhibitory neurons
    
    """
    motiflist = ['ii_con_elec', 'ii_con_chem', 'ii_con_c2', 'ii_con_c1e', 'ii_con_c2e']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between convergent inhibitory neurons
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
            recurrently connected inhibitory neurons
        
        """
        super(IIConMotifCounter, self).__init__()

        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            self.read_matrix(matrix) # requires previous creation of keys

    def __call__(self, matrix = None):
        """
        Returns a IIConMotifCounter object with counts of motifs
        """

        return IIConMotifCounter(matrix)

    def read_matrix(self, matrix):
        """
        Counts the motifs in the matrix
        """
        try:
            if matrix.shape[0] != matrix.shape[1]:
                raise IOError("matrix must be a square matrix!")
        except IOError:
            raise

        npost = matrix.shape[1] # number of postsynaptic neurons
    
        
        # counts chemical synapses between convergent motifs
        ii_con_chem_found  = 0
        ii_con_chem_tested = 0
        ii_con_elec_found = 0
        ii_con_elec_tested = 0

        mymatrix = matrix.copy()  
        mymatrix[mymatrix==2]=0 # remove gaps

        pre, post = np.nonzero(mymatrix)
        ii_con_elec_tested = 10#ii_con_chem_tested/2

        self.__setitem__('ii_con_chem', {'tested':ii_con_chem_tested, \
            'found': ii_con_chem_found})
        self.__setitem__('ii_con_elec', {'tested':ii_con_elec_tested, \
            'found': ii_con_elec_found})

        # dynamically rewrite object attributes
        for key in self:
            setattr(self, key+'_tested',self[key]['tested']) 
            setattr(self, key+'_found' ,self[key]['found' ]) 
             
        

class EEMotifCounter(IIMotifCounter):
    """
    Create a MotifCounter type object with connectivity motifs
    between same type of neurons. The motifs measured are the following:

    ee_chem : a chemical synapse between neurons
    ee_elec : an electrical synapse between neurons
    ee_c1e : an alectrical synapse together with ONE chemical
    ee_c2e : an alectrical synapse together with TWO chemical
    ee_c2  : two reciprocally connected chemical synapses
    ee_con : two neurons converging on to a third
    ee_div : one neuron diverging into two neurons 
    ee_lin : one neuron connected to a second one and this last to another
    
    It's algorithmically identical to IIMotifcounter
    """
    motiflist = ['ee_chem', 'ee_elec', 'ee_c1e', 'ee_c2e', 'ee_c2', \
        'ee_con', 'ee_div', 'ee_lin']

    def __init__(self, matrix = None):
        """
        Counts connectivity motifs between excitatory neurons 
        
        Argument
        --------
        matrix: 2D NumpyArray
            a connectivity matrix of pre-post dimension between 
        
        """
        super(EEMotifCounter, self).__init__()

        # keys zero at construction
        for key in self.motiflist:
            self.__setitem__(key, {'tested':0, 'found':0})

        if matrix is not None:
            super(EEMotifCounter, self).read_matrix(matrix)

    def __call__(self, matrix = None):
        """
        Returns a EEMotifCounter object with counts of motifs
        """
        return EEMotifCounter(matrix) # will count motifs

# ready-to-use objects
motifcounter = MotifCounter()
iicounter    = IIMotifCounter()
iiconcounter = IIConMotifCounter()
eecounter    = EEMotifCounter()
eicounter    = EIMotifCounter()
iecounter    = IEMotifCounter()
