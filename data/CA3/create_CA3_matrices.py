"""
create_CA3_matrices.py

Jose Guzman, sjm.guzman@gmail.com

Dummy script to fill CA3 recording configurations and connections. Motif
will be added manually according to the experiments
"""
import numpy as np

enum = {2: 'pair', 3: 'triplet', 4: 'quadruplet', 5: 'quintuplet', 
        6: 'sextuplet', 7: 'septuplet', 8: 'octuple'}

myrecording = dict()
myrecording['pair']       = {'tested': 495, 'found':  4} # OK
myrecording['triplet']    = {'tested':  96, 'found':  6} # OK
myrecording['quadruplet'] = {'tested': 135, 'found': 18} # 2L, 16 U OK
myrecording['quintuplet'] = {'tested': 120, 'found': 27} # OK
myrecording['sextuplet']  = {'tested': 118, 'found': 39} # OK
myrecording['septuplet']  = {'tested':  66, 'found': 25} # OK
myrecording['octuple']    = {'tested':  72, 'found': 27}

# create empty matrices
for conf in range(2,9):
    tested = myrecording[enum[conf]]['tested']
    found = 0
    for x in range(tested):
        fname = '0_{}{:03}.syn'.format(enum[conf],x) 
        mymatrix = np.zeros((conf,conf), dtype=int)
        if found < myrecording[enum[conf]]['found']:
            mymatrix[0][1] = 1
            found +=1
            print('Adding syn{} to {}'.format(found, fname))

        np.savetxt(fname, mymatrix, fmt='%d')
    
