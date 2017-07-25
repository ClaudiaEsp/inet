"""
mymath.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Tue Jul 25 07:41:36 CEST 2017
Last change:

Auxiliary functions to perform basic math
"""

import numpy as np

from scipy.stats import t as T
from scipy.stats import norm

def binomial_CI(trials, p_success, confident=0.975):
    """
    Computes confident interval from a binomial process based on a 
    normal approximation. It is given by the following
    expression:

    p +/- Z*sqrt( p*(1-p)/n ),

    where p is the proportion of successes, Z is the z-value for a 
    given value of confidence, and n is the number of binomial trials.

    For details check:
    https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval

    Arguments:
    ----------
    trials      -- (int) number of samples or trials
    p_success   -- (float) proportion of successes
    confident   -- (float) value of confidence e.g. 0.95 for 95%. For a
                    two-tailed 95% confident interval confidence is 0.975
                    (default).

    Returns:
    --------
    The confident interval for the binomial process
    """
    
    n = trials
    p = p_success

    # test if number of trials is integer
    try:
        if not isinstance(n, int):
            raise TypeError("Trials argument is not an integer")
    except TypeError:
        raise

    # test proportions between 0 and 1
    try:
        if p < 0.0 or p > 1.0:
            raise ValueError('Proportion must be between zero and one')
    except ValueError:
        raise

    z = norm.ppf(confident) # normal approximation

    return z * np.sqrt( (p * (1-p))/n )

def linear_CI(fit, data, confident=0.975):
    """
    Computes the upper and lower confident intervals for the 
    linear regression to the data

    https://tomholderness.wordpress.com/2013/01/10/confidence_intervals/

    Arguments:
    ----------

    confident   -- (float) value of confidence e.g. 0.95 for 95%. For a
                    two-tailed 95% confident interval confidence is 0.975
                    (default).
    Returns:
    --------
    A tuple with the lower and the upper confident intervals
    """


    t = T.ppf(confident, n-1)
    pass # TODO finish...
