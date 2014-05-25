# -*- coding: utf-8 -*-
"""
Created on Sun May 25 17:19:58 2014

@author: frederik """

""" second_pybrain_example """

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal

#means = [(-1,0),(2,4),(3,1),(1,2)]
#cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7]), diag([0.5,0.5])]
#alldata = ClassificationDataSet(2, 1, nb_classes=4)
#print alldata
#for n in xrange(400):
#    for klass in range(4):
#        input = multivariate_normal(means[klass],cov[klass])
#        print input
#        alldata.addSample(input, [klass])
#print alldata      

import pickle

with open('new_list_unscaled.dat', 'rb') as f:
    alldata = pickle.load(f)
  
tstdata, trndata = alldata.splitWithProportion( 0.25 )  
  
#tstdata, _ = tstdata.splitWithProportion( 0.5 )
  


#tstdata = trndata

trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )

print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]
print trndata['input'][1], trndata['target'][1], trndata['class'][1]

#fnn = buildNetwork( trndata.indim, 150, trndata.outdim, outclass=SoftmaxLayer )


wanna_plot = []

# [2, 4, 6, 8, 10, 15, 20, 30, 50 , 100]

for hidden_neurons in [2, 4, 6, 8, 10, 15, 20, 30, 50 , 100]:
    
    from pybrain.structure import FeedForwardNetwork
    from pybrain.structure import LinearLayer, SigmoidLayer
    from pybrain.structure import FullConnection
    
    n = FeedForwardNetwork()
    
    
    inLayer = LinearLayer(17)
    hiddenLayer = SigmoidLayer(hidden_neurons)
    outLayer = LinearLayer(4)
    
    n.addInputModule(inLayer)
    n.addModule(hiddenLayer)
    n.addOutputModule(outLayer)
    
    
    in_to_hidden = FullConnection(inLayer, hiddenLayer)
    hidden_to_out = FullConnection(hiddenLayer, outLayer)
    
    n.addConnection(in_to_hidden)
    n.addConnection(hidden_to_out)
    
    n.sortModules()
    
    trainer = BackpropTrainer( n, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)
    
        
    
    for i in range(15):
        trainer.trainEpochs( 1 )
        trnresult = percentError( trainer.testOnClassData(),
                                  trndata['class'] )
        tstresult = percentError( trainer.testOnClassData(
               dataset=tstdata ), tstdata['class'] )
    
        print "epoch: %4d" % trainer.totalepochs, \
              "  train error: %5.2f%%" % trnresult, \
              "  test error: %5.2f%%" % tstresult

        wanna_plot.append(tstresult)

#out = fnn.activate(trndata['input'][0])


fileObject = open('n_new', 'w')
pickle.dump(n, fileObject)
fileObject.close()