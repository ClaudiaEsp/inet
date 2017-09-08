"""
patterns.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: 

Auxiliary functions to calculate operations on pairs of patterns
"""

import numpy as np
import matplotlib.pyplot as plt
 
def similarity(a, b):
    """
    Compute cosine similarity between samples in a and b.

    Cosine similarity, or the cosine kernel, computes similarity as the
    normalized dot product of A and B:

     K(a, b) = <a, b> / (||a||*||b||)

    Parameters
    ----------
    a : 1-D ndarray .

    b : 1-D ndarray.

    """
    # dot product is scalar product
    return np.dot( a/np.linalg.norm(a), b/np.linalg.norm(b))

def randpattern(size, prob):
    """
    Creates a pattern of activities (ones) with a given probability. 
    Activity is 1 if the cell is active, zero otherwise.
    
    Parameters
    ----------
    size : int 
           the size of the resulting random vector
    prob : float
            probability of having ones

    Returns:
    --------

    A 1-D Numpy Array containing zeros and ones at a given probability.
    """
    z = np.zeros(size, dtype=int)
    n_ones = int(size*prob) # number of ones in the vector

    # introduce ones without replacement. Thank you Clau!!!!
    z[np.random.choice(a = size, size = n_ones, replace=False)]=1 
    
    return(z)

class Separation(object):
    """
    A major class to quantify the degree of pattern separation between
    pairs of random patterns containing zeros and ones.
    """

    def __init__(self, inputpatterns = None, outputpatterns = None):
        """
        
        Parameters:
        -----------

        inpatterns:  a tuple with pairs of input patterns
        outpatterns: a tuple with pairs of input patterns
        """
    
        self.inputpatterns = inputpatterns
        self.outputpatterns = outputpatterns

        if inputpatterns is not None:
            self.insimilarity = self.__sim(inputpatterns)
        else:
            self.insimilarity = None

        if outputpatterns is not None:
            self.outsimilarity = self.__sim(outputpatterns)
        else:
            self.outsimilarity = None

    def __call__(self, inputpatterns, outputpatterns):
        """
        Parameters:
        -----------

        inpatterns:  a tuple with pairs of input patterns
        outpatterns: a tuple with pairs of input patterns
        """
        self.inputpatterns = inputpatterns
        self.outputpatterns = inputpatterns
        self.insimilarity = self.__sim(inputpatterns)
        self.outsimilarity = self.__sim(outputpatterns)

        mydict = dict()
        mydict['proportion'] = self.proportion()
        mydict['magnitude']  = self.magnitude()

        return( mydict ) 

    def __sim(self, pattern):
        """
        Returns a list of similarities between pairs of patterns
        """
        mysim = np.array([similarity(i,j) for i,j in pattern])
        return( mysim )

    def proportion(self):
        """
        Computes the proportion of patterns properly separated. These
        are the patterns whose output similiarity is larger than
        the input similarity.

        """
        supra = self.outsimilarity[self.outsimilarity>self.insimilarity]
        return( len(supra)/len(self.inputpatterns) )

    def magnitude(self):
        """
        Computes the magnitude of separation between two sets of patterns
        by analizing the average distance of the separated patterns from
        the identity line. To calculate the distance from a point to a
        line use:
        http://www.fundza.com/vectors/point2line/index.html
        """
        return(0) #TODO
        
        
    def plot(self, ax = None):
        """
        Plots a pattern separation figure containing a similiarty between
        input patterns versus the similarity between output patterns
        
        """
        if ax is None:
            ax = plt.gca()

        # plot
        iline = np.linspace(0,1,100) # identity line
        ax.scatter(self.insimilarity, self.outsimilarity, color = 'gray')
        ax.plot(iline, iline, '--', color = 'brown', alpha=.6)
        ax.fill_between(iline, 1, iline, color='yellow', alpha=.1)

        ax.set_xlim(0,1), ax.set_ylim(0,1)
        ax.set_xticklabels(fontsize = 20) 
            
        ax.set_ylabel('Input similarity  ($\cos(x_i,y_i)$)', fontsize=20)
        ax.set_xlabel('Output similarity ($\cos(x_o,y_o)$)', fontsize=20)

        return(ax)
        
separation = Separation()
