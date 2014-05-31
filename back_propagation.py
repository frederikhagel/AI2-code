""" second_pybrain_example """

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.structure.modules   import BiasUnit

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

data_loc = 'ludosim-master/ludosim/fast_states.dat'

data_loc = 'marius_list_scaled.dat'

with open(data_loc, 'rb') as f:
    alldata = pickle.load(f)
 
print "Length of data: ", len(alldata)
 
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

#print trndata['input'][0][0]

#fnn = buildNetwork( trndata.indim, 150, trndata.outdim, outclass=SoftmaxLayer )


from pybrain.structure import FeedForwardNetwork
n = FeedForwardNetwork()

from pybrain.structure import LinearLayer, SigmoidLayer

#inLayer = LinearLayer(17)
#hiddenLayer1 = SigmoidLayer(30)
#hiddenLayer2 = SigmoidLayer(20)
#outLayer = LinearLayer(4)
#
#n.addInputModule(inLayer)
#n.addModule(hiddenLayer1)
#n.addModule(hiddenLayer2)
#n.addOutputModule(outLayer)

inLayer = LinearLayer(17, name='in')
hiddenLayer1 = SigmoidLayer(25, name='h1')
hiddenLayer2 = SigmoidLayer(25, name='h2')
#hiddenLayer3 = SigmoidLayer(25, name='h3')
#hiddenLayer4 = SigmoidLayer(25, name='h4')
#hiddenLayer5 = SigmoidLayer(50, name='h5')
#hiddenLayer6 = SigmoidLayer(25, name='h6')
#hiddenLayer7 = SigmoidLayer(50, name='h7')
#hiddenLayer8 = SigmoidLayer(25, name='h8')
#hiddenLayer9 = SigmoidLayer(25, name='h9')
outLayer = LinearLayer(4, name='out')

n.addInputModule(inLayer)
n.addModule(hiddenLayer1)
n.addModule(hiddenLayer2)
#n.addModule(hiddenLayer3)
#n.addModule(hiddenLayer4)
#n.addModule(hiddenLayer5)
#n.addModule(hiddenLayer6)
#n.addModule(hiddenLayer7)
#n.addModule(hiddenLayer8)
#n.addModule(hiddenLayer9)
n.addOutputModule(outLayer)

from pybrain.structure import FullConnection

n.addModule(BiasUnit(name='bias'))

n.addConnection(FullConnection(n['bias'], n['out']))

for i in range(1,3):
    layername = 'h%i' % i
    n.addConnection(FullConnection(n['bias'], n[layername]))

#n.addInputModule(LinearLayer(17, name='in'))
#n.addModule(SigmoidLayer(20, name='hidden'))
#n.addOutputModule(LinearLayer(4, name='out'))

in_to_hidden = FullConnection(inLayer, hiddenLayer1)
hidden_to_hidden1 = FullConnection(hiddenLayer1, hiddenLayer2)
#hidden_to_hidden2 = FullConnection(hiddenLayer2, hiddenLayer3)
#hidden_to_hidden3 = FullConnection(hiddenLayer3, hiddenLayer4)
#hidden_to_hidden4 = FullConnection(hiddenLayer4, hiddenLayer5)
#hidden_to_hidden5 = FullConnection(hiddenLayer5, hiddenLayer6)
#hidden_to_hidden6 = FullConnection(hiddenLayer6, hiddenLayer7)
#hidden_to_hidden7 = FullConnection(hiddenLayer7, hiddenLayer8)
#hidden_to_hidden8 = FullConnection(hiddenLayer8, hiddenLayer9)
hidden_to_out = FullConnection(hiddenLayer2, outLayer)

#extra_1_4 = FullConnection(hiddenLayer1, hiddenLayer4)
#extra_3_8 = FullConnection(hiddenLayer3, hiddenLayer8)
#extra_4_7 = FullConnection(hiddenLayer4, hiddenLayer7)
#extra_1_3 = FullConnection(hiddenLayer1, hiddenLayer3)
#in_to_hidden = FullConnection(inLayer, hiddenLayer)
#hidden_to_out = FullConnection(hiddenLayer, outLayer)


n.addConnection(in_to_hidden)
#n.addConnection(hidden_to_hidden1)
#n.addConnection(hidden_to_hidden2)
#n.addConnection(hidden_to_hidden3)
#n.addConnection(hidden_to_hidden4)
#n.addConnection(hidden_to_hidden5)
#n.addConnection(hidden_to_hidden6)
#n.addConnection(hidden_to_hidden7)
#n.addConnection(hidden_to_hidden8)
n.addConnection(hidden_to_out)

#n.addConnection(extra_1_3)
#n.addConnection(extra_1_4)
#n.addConnection(extra_3_8)
#n.addConnection(extra_4_7)


n.sortModules()

trainer = BackpropTrainer( n, dataset=trndata, momentum=0.00000001, verbose=True, weightdecay=0.01)


#ticks = arange(-3.,6.,0.2)
#X, Y = meshgrid(ticks, ticks)
# need column vectors in dataset, not arrays
#griddata = ClassificationDataSet(2,1, nb_classes=4)
#for i in xrange(X.size):
#    griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
#griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy


for i in range(1):
    trainer.trainUntilConvergence( )
    trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
    tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult

#out = fnn.activate(trndata['input'][0])


#fileObject = open('n_fast_with_no_bias_simple', 'w')
#pickle.dump(n, fileObject)
#fileObject.close()



print tstdata['input'][0],  n.activate(tstdata['input'][0])
print tstdata['input'][20],  n.activate(tstdata['input'][20])
print tstdata['input'][40],  n.activate(tstdata['input'][40])
print tstdata['input'][25],  n.activate(tstdata['input'][25])


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