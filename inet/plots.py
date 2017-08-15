"""
plots.py

Jose Guzman, sjm.guzman@gmail.com
Claudia Espinoza, claudia.espinoza@ist.ac.at

Created: Tue Aug 15 01:48:09 CEST 2017

Function to perform basic plotting.

Usage
-----

>>> from iplots import bar_plot
>>> from matplotib.pyplot import figure, show
>>> fig = figure()
>>> ax = fig.add_subplot(111)
>>> bar_plot(simulation, n_found)
>>> ax.set_title('My figure')
"""

import numpy as np
import matplotlib.pyplot as plt

def barplot(simulation, n_found, ax=None):
    """
    Plots a bar of simulated values versus the counts of
    the connections found experimentally and provide a P-Value
    for the null-hypothesis.

    Arguments
    ---------
    
    simulation : list
        a list containing the successes according to the null-hypothese.

    n_found: int
        the number of successes found empirically

    ax : plt.axis
        an axis object to plot it

    Returns
    -------

    an axis object with a bar plot together with standard deviation and
    P-values.
    """
    
    sim = np.array(simulation)
    p_val = len(sim[sim>n_found]) / sim.size

    if ax is None:
        ax = plt.gca() # gets current axis if necessary

    x_pos = (0, 0.4) 
    x_labels = ('Simulation', 'Experiment')

    # bar with SD
    ax.bar(x_pos, [sim.mean(), n_found],  \
        color = ('brown', 'white'), width =0.30, align='center')
    ax.errorbar(x_pos, [sim.mean(), n_found], fmt=' ',\
        yerr=[sim.std(), 0], color='brown', capsize=12, capthick=3)
    ax.text(0, n_found + n_found*0.1,  'P = %2.4f'%p_val,\
        verticalalignment='center', horizontalalignment='center')


    # labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels) 
    ax.set_ylabel('Number of motifs')

    mymax = max(sim.mean(), n_found)
    mymax += mymax*0.2 
    ax.set_ylim(ymax = mymax)

    return( ax )
