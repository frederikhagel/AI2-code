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

with open('training.dat', 'rb') as f:
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

fnn = buildNetwork( trndata.indim, 20, trndata.outdim, outclass=SoftmaxLayer )

trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.01, verbose=True, weightdecay=0.01)


#ticks = arange(-3.,6.,0.2)
#X, Y = meshgrid(ticks, ticks)
# need column vectors in dataset, not arrays
#griddata = ClassificationDataSet(2,1, nb_classes=4)
#for i in xrange(X.size):
#    griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
#griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy


for i in range(40):
    trainer.trainEpochs( 1 )
    trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult

#out = fnn.activate(trndata['input'][0])


fileObject = open('fnn', 'w')
pickle.dump(fnn, fileObject)
fileObject.close()



print tstdata['input'][0],  fnn.activate(tstdata['input'][0])
print tstdata['input'][20],  fnn.activate(tstdata['input'][20])
print tstdata['input'][40],  fnn.activate(tstdata['input'][40])
print tstdata['input'][25],  fnn.activate(tstdata['input'][25])


#print fnn([ 35.,   0.,  19.,   4.,  11.,   0.,   0.,  57.,  33.,   0.,  51.,   0.,  57.,  57.,  26.,   0.,   2.])

#out = out.argmax(axis=1)  # the highest output activation gives the class
#out = out.reshape(X.shape)
#figure(1)
#ioff()  # interactive graphics off
#clf()   # clear the plot
#hold(True) # overplot on
#for c in [0,1,2,3]:
#    here, _ = where(tstdata['class']==c)
#    plot(tstdata['input'][here,0],tstdata['input'][here,1],'o')
#if out.max()!=out.min():  # safety check against flat field
#    contourf(X, Y, out)   # plot the contour
#ion()   # interactive graphics on
#draw()  # update the plot
#    
#ioff()
#show()