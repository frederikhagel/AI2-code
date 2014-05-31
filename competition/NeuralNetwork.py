# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/dimx/.spyder2/.temp.py
"""

import random
import math
import operator

class Neuron:
    def __init__(self):
        random.seed()
        self.weights = []
        #self.bias = random.random() * 2 - 1
        self.bias = 0 # This will be fixed the day after...
        self.lastoutput = 0
        self.deltaoutput = 0
        self.lastinput = []
        self.lastWeightUpdate = []
        
    def activationFunction(self, sum):
        return sum
        #return math.tanh(sum)
        
    def getOutputs(self, inputs):
        self.lastinput = inputs
        # Fix size of weights
        while len(self.weights) < len(inputs):
            self.weights.append(random.random() * 2 - 1)
        
        # Calculate sum and return
        weighted_sum = self.bias
        for w, i in zip(self.weights, inputs):
            weighted_sum += w*i
            
        weighted_sum /= len(self.weights)
        
        if weighted_sum > 1 or weighted_sum < -1:
            raise AssertionError("Something wrong in the neural network! Weights: " + self.weights)
            
        newoutput = self.activationFunction(weighted_sum)
        self.deltaoutput = self.lastoutput - newoutput
        self.lastoutput = newoutput
        
        return self.lastoutput
        
    def learn(self, error, learningRate, alpha):
        errors = [] # errors send to preceding layer
        self.bias += learningRate * error
        weightUpdate = []
        for i in range(len(self.weights)):
            learning = learningRate * error * self.lastinput[i]
            errors.append(self.weights[i] * error)
            if (len(self.lastWeightUpdate) < 1):
                momentum = 0
            else:
                momentum = alpha * self.lastWeightUpdate[i]
            weightUpdate.append(learning + momentum)
            self.weights[i] += weightUpdate[i]
            #print "Error: ", error, " WeightUpdate: ", weightUpdate, " New weight: ", self.weights[i]
        self.lastWeightUpdate = weightUpdate
        return errors

class NeuronLayer:
    def __init__(self, neurons):
        self.neurons = []
        
        while len(self.neurons) < neurons:
            self.neurons.append(Neuron())
    def forward(self, inputs):
        
        # Calculate outputs
        outputs = []
        for n in self.neurons:
            outputs.append(n.getOutputs(inputs))
        
        return outputs
        
    def learn(self, errors, learningRate, alpha):
        input_error = []       
    
        for i in range(len(self.neurons)):
            neuron_input_error = self.neurons[i].learn(errors[i], learningRate, alpha)
            if len(input_error) < 1:
                input_error = neuron_input_error
            else: 
                input_error = map(operator.add, input_error, neuron_input_error)
        return input_error
    def showWeights(self):
        for n in self.neurons:
            print n.weights
            
    def getNumWeights(self):
        weights = 0
        for n in self.neurons:
            weights += len(n.weights)
        return weights
    
    def setWeights(self, weights):
        for n in self.neurons:
            neuronWeightsNum = len(n.weights)
            n.weights = list()
            for i in range(0,neuronWeightsNum):
                newWeight = weights.pop()
                n.weights.append(newWeight)

class NeuralNetwork:
    def __init__(self, layers): # Format: [layer_1_neurons, .. , layer_n_neurons]
        self.neuronLayers = []
        
        # Create layers
        for l in layers:
            self.neuronLayers.append(NeuronLayer(l))
        
    def forward(self, inputs):
        axon = inputs # dendrite
        for l in self.neuronLayers:
            axon = l.forward(axon)
        
        return axon # synapse

    def think(self, inputs):
        return self.forward(inputs)
    
    def learn(self, learningRate, alpha, inputs, desired_outputs):
        # Forward and calculate error
        actual_outputs = self.forward(inputs)        
        error = map(operator.sub, desired_outputs, actual_outputs) #desired_outputs - actual_outputs
        
        # Backward - push errors to layers        
        for forwardPos in range(len(self.neuronLayers)):
            backwardPos = len(self.neuronLayers) - forwardPos - 1
            error = self.neuronLayers[backwardPos].learn(error,learningRate, alpha)
            #print "Layer: ", backwardPos, " error: ", error
        
        return error
    
    def showWeights(self):
        for forwardPos in range(len(self.neuronLayers)):
            print "Layer ", forwardPos
            self.neuronLayers[forwardPos].showWeights()
            
    def getNumWeights(self):
        weights = 0
        for forwardPos in range(len(self.neuronLayers)):
            # Probe each layer     
            weights += self.neuronLayers[forwardPos].getNumWeights()
        return weights
    
    def setWeights(self, newWeights):
        # numWeights is list with all weights of the network
        for forwardPos in range(len(self.neuronLayers)):
            layerWeightsNum = self.neuronLayers[forwardPos].getNumWeights()
            layerWeights = list()
            for i in range(0,layerWeightsNum):
                newWeight = newWeights.pop()
                layerWeights.append(newWeight)
            self.neuronLayers[forwardPos].setWeights(layerWeights)
            
# Neuron test
def neuronTest():
    n = Neuron()
    
    desired_out = 0.5
    print "Desired output: ", desired_out
    for i in range (20):
        out = n.getOutputs([1,1])
        print out
        #error = 0.5*(desired_out - out)*(desired_out - out)
        error = (desired_out - out)
        #error = error * error
        print n.learn( error , 0.3, 0.3)
#neuronTest()

# Neuron layer test
def neuronLayerTest():
    desired_out = [0.5, 1]
    l = NeuronLayer(2)
    for i in range(20):
        out = l.forward([1,1])
        print out
        error = map(operator.sub, desired_out, out)
        l.learn(error, 0.3, 0.3)
#neuronLayerTest()

def neuralNetTest():
    desired_out = [-0.5]
    inp = [1]
    nn = NeuralNetwork([3,3,1])
    for i in range(20):
        print nn.learn(0.3,0.3, inp, desired_out)
    print "Test: ", nn.forward(inp)
    
#neuralNetTest()

def testXor():
    nn = NeuralNetwork([2,2,1])
    
    # Train!!
    for i in range (30000):
        nn.learn(0.2,0.3, [1,1], [-1])
        nn.learn(0.2,0.3, [1,-1], [1])
        nn.learn(0.2,0.3, [-1,1], [1])
        nn.learn(0.2,0.3, [-1,-1], [-1])

    # Test
    t_1_1 = nn.forward([1,1])[0]
    t_1_0 = nn.forward([1,-1])[0]
    t_0_1 = nn.forward([-1,1])[0]
    t_0_0 = nn.forward([1,1])[0]
    
    if (t_1_1 < 0.0 and t_0_0 < 0.0 and t_1_0 > 0.0 and t_0_1 > 0.0):
        print "SUCCESS"
    else:
        print "FAIL"
    
    if True:
        print " 1*1: ", t_1_1
        print " 1*0: ", t_1_0
        print " 0*1: ", t_0_1
        print " 0*0: ", t_0_0

def testAnd():
    nn = NeuralNetwork([2,2,1])
    
    # Train!!
    for i in range (3000):
        nn.learn(0.2,0.3, [1,1], [1])
        nn.learn(0.2,0.3, [1,-1], [-1])
        nn.learn(0.2,0.3, [-1,1], [-1])
        nn.learn(0.2,0.3, [-1,-1], [-1])

    # Test
    t_1_1 = nn.forward([1,1])[0]
    t_1_0 = nn.forward([1,-1])[0]
    t_0_1 = nn.forward([-1,1])[0]
    t_0_0 = nn.forward([1,1])[0]
    
    if (t_1_1 > 0.0 and t_0_0 < 0.0 and t_1_0 < 0.0 and t_0_1 < 0.0):
        print "SUCCESS"
    else:
        print "FAIL"

    if True:
        print " 1*1: ", t_1_1
        print " 1*0: ", t_1_0
        print " 0*1: ", t_0_1
        print " 0*0: ", t_0_0

def testLearning():
    nn = NeuralNetwork([2,2,1])
    print "out: ", nn.forward([1,1])
    nn.showWeights()
    for i in range (10):
        print ""
        nn.learn(0.2,0.3, [1,1], [1])
        nn.showWeights()
        print "out: ", nn.forward([1,1])
    
    print "----"
    
    for i in range (10):
        print ""
        nn.learn(0.2,0.3, [-1,-1], [-1])
        nn.showWeights()
        print "out: ", nn.forward([1,1])

def testSetWeights():
    nn = NeuralNetwork([1])
    print "out: ", nn.forward([1,1])
    nn.showWeights()
    nn.setWeights([-1,1])
    nn.showWeights()

if __name__ == '__main__':
    testSetWeights()

# NeuralNetwork forward test
#nn = NeuralNetwork([3,3,1])
#print nn.forward([1,1,1])

#print nn.learn(0.3 ,0.3,[1,1],[0])