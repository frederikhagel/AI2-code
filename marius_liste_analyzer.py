# -*- coding: utf-8 -*-
"""
Created on Sat May 24 19:08:33 2014

@author: frederik
"""

""" marius liste analyzer """

import pickle

import numpy as np
#
#with open('marius_liste.dat', 'rb') as f:
#    marius_liste = pickle.load(f)
##    
##print marius_liste
##print len(marius_liste)
##
#with open('marius_liste2.dat', 'rb') as f:
#    marius_liste2 = pickle.load(f)
##    
##print marius_liste2
##print len(marius_liste2)
##
#with open('marius_liste3.dat', 'rb') as f:
#    marius_liste3 = pickle.load(f)
##    
#print marius_liste3

#print len(marius_liste3)
#
#print len(marius_liste + marius_liste2 + marius_liste3)

with open('new_test_liste.dat', 'rb') as f:
    test_liste = pickle.load(f)

print len(test_liste)

llist = []


for l in test_liste:
    llist = llist + l

#llist = marius_liste + marius_liste2 + marius_liste3

print llist[0]

print len(llist)

#print llist

from pybrain.datasets            import ClassificationDataSet
marius_training_set = ClassificationDataSet(17, 1, nb_classes=4)

for marius in llist:    
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
#            liste1 = [marius[0][0][0][0]/57., marius[0][0][0][1]/57.,marius[0][0][0][2]/57., marius[0][0][0][3]/57. ]
#            liste2 =  [marius[0][0][1][0]/57., marius[0][0][1][1]/57., marius[0][0][1][2]/57., marius[0][0][1][3]/57.]
#            liste3 = [marius[0][0][2][0]/57., marius[0][0][2][1]/57., marius[0][0][2][2]/57., marius[0][0][2][3]/57.]
#            liste4 = [marius[0][0][3][0]/57., marius[0][0][3][1]/57., marius[0][0][3][2]/57., marius[0][0][3][3]/57.]
#            liste1.sort()
#            liste2.sort()
#            liste3.sort()
#            liste4.sort()
#            liste =  liste1 + liste2 + liste3 + liste4  + [ marius[0][1]/6. ]  
            liste1 = [marius[0][0][0][0], marius[0][0][0][1],marius[0][0][0][2], marius[0][0][0][3] ]
            liste2 =  [marius[0][0][1][0], marius[0][0][1][1], marius[0][0][1][2], marius[0][0][1][3]]
            liste3 = [marius[0][0][2][0], marius[0][0][2][1], marius[0][0][2][2], marius[0][0][2][3]]
            liste4 = [marius[0][0][3][0], marius[0][0][3][1], marius[0][0][3][2], marius[0][0][3][3]]


            
            liste =  liste1 + liste2 + liste3 + liste4  + [ marius[0][1] ]                
            #print liste
                                              
                                          
            marius_training_set.addSample(liste , [index]  )
                                          
with open('new_list_unscaled.dat', 'wb') as f:
    pickle.dump( marius_training_set , f)

            