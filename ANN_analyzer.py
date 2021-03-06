# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:52:29 2014

@author: frederik
"""

import pickle

from pybrain.structure import FeedForwardNetwork
n = FeedForwardNetwork()

from pybrain.structure import LinearLayer, SigmoidLayer

fileObject = open('n_marius_for_testing_simple','r')
n = pickle.load(fileObject)



#print n
#
#print n.activate([ 0, 0, 0, 1 ] + [ 0 ]*12 + [6] )
#
#print len(n.params)
#
#print n.params[1] 
#
#n.params[1] = 1


print " --- Module time --- "
for mod in n.modules:
  print "Module:", mod.name
  if mod.paramdim:
    print "--parameters:", mod.params
  for conn in n.connections[mod]:
    print "-connection to", conn.outmod.name
    if conn.paramdim > 0:      
       print "- parameters", conn.params    
       print "len", len(conn.params)
  if hasattr(n, "recurrentConns"):
    print "Recurrent connections"
    for conn in n.recurrentConns:             
       print "-", conn.inmod.name, " to", conn.outmod.name
       if conn.paramdim > 0:
          print "- parameters", conn.params

import random
for i in range(1000):
    para = []
    for i in range(17):
        para.append(random.uniform(0, 1) )

    print n.activate( para )
#
#print n.activate([ 0, 0.1, 1, 1 ] + [0.1]*12 + [0.2] )
#
#print n.activate([ 0, 0.1, 1, 1 ] + [0.1]*12 + [0.2] )