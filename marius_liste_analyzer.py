# -*- coding: utf-8 -*-
"""
Created on Sat May 24 19:08:33 2014

@author: frederik
"""

""" marius liste analyzer """

import pickle

import numpy as np

with open('marius_liste.dat', 'rb') as f:
    marius_liste = pickle.load(f)
    
print marius_liste
print len(marius_liste)

with open('marius_liste2.dat', 'rb') as f:
    marius_liste2 = pickle.load(f)
    
print marius_liste2
print len(marius_liste2)

with open('marius_liste3.dat', 'rb') as f:
    marius_liste3 = pickle.load(f)
    
print marius_liste3
print len(marius_liste3)

print len(marius_liste + marius_liste2 + marius_liste3)

from pybrain.datasets            import ClassificationDataSet
marius_training_set = ClassificationDataSet(17, 1, nb_classes=4)

for marius in marius_liste + marius_liste2 + marius_liste3:    
    summering = 0
    for ans in marius[1]:
        summering = summering + ans
    if summering != 1:
        print "fejl"
    else :
        index = 0
        for i, ans in enumerate(marius[1]):        
            if ans == 1:
                index = i
#        print "ck", marius[0][0][0][index] , marius[0][0][0][index] , marius[0][1]
        if marius[0][0][0][index] == 57 or (marius[0][0][0][index] == 0 and marius[0][1] != 6):
            print "fejl"
        else :
            marius_training_set.addSample(np.sort( marius[0][0][0][0],
                                          marius[0][0][0][1],
                                          marius[0][0][0][2],
                                          marius[0][0][0][3]),
                                          np.sort(marius[0][0][1][0],
                                          marius[0][0][1][1],
                                          marius[0][0][1][2],
                                          marius[0][0][1][3]),
                                          np.sort(marius[0][0][2][0],
                                          marius[0][0][2][1],
                                          marius[0][0][2][2],
                                          marius[0][0][2][3]),                                          
                                          np.sort(marius[0][0][3][0],
                                          marius[0][0][3][1],
                                          marius[0][0][3][2],
                                          marius[0][0][3][3]),
                                          marius[0][1]],
                                          [index]  )
                                          
with open('training.dat', 'wb') as f:
    pickle.dump( marius_training_set , f)

            