# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:31:41 2014

@author: frederik
"""

""" Lets Develop """
""" Write your victories in stone, and your failures in sand """

import os
import subprocess
import sys

sys.path = sys.path + ['/home/frederik/installed_packages/arac/src/python']
#os.environ['LD_LIBRARY_PATH'] = "/home/frederik/installed_packages/arac"
##subprocess.check_call(['sqsub', '-np', sys.argv[0], '/AI2/ludosim-master/ludosim'],
##                      env=os.environ)

#export LD_LIBRARY_PATH=/home/frederik/installed_packages/arac:$LD_LIBRARY_PATH

import numpy as np

import pickle
import copy

#from pybrain.datasets            import ClassificationDataSet
#from pybrain.utilities           import percentError
#from pybrain.tools.shortcuts     import buildNetwork



from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
from arac.pybrainbridge import _FeedForwardNetwork


from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.supervised.trainers import BackpropTrainer


#
#
#print n.activate([0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 39, 0, 6])

class GeneticPlayerSH5(object):

    '''
        Simple player choosing at random which move to take.
    '''
    def __init__(self, index, name, param):
        self.name = name
        self.index = index
        self.liste = []#ClassificationDataSet(17, 1, nb_classes=4)        
        self.status_good = True

        self.number_of_moves = 0
        self.number_of_sound_moves = 0

        n = FeedForwardNetwork()
        
#        self.inLayer = LinearLayer(17)
#        self.hiddenLayer = SigmoidLayer(5)
#        self.outLayer = LinearLayer(4)
#     
#        
#        n.addInputModule(self.inLayer)
#        n.addModule(self.hiddenLayer)
#        n.addOutputModule(self.outLayer)
        
        self.inLayer = LinearLayer(17)
        self.hiddenLayer1 = SigmoidLayer(15)
        self.hiddenLayer2 = SigmoidLayer(15)
        self.hiddenLayer3 = SigmoidLayer(15)
        self.hiddenLayer4 = SigmoidLayer(15)
        self.hiddenLayer5 = SigmoidLayer(15)
        self.hiddenLayer6 = SigmoidLayer(15)
        self.outLayer = LinearLayer(4)
        
        n.addInputModule(self.inLayer)
        n.addModule(self.hiddenLayer1)
        n.addModule(self.hiddenLayer2)
        n.addModule(self.hiddenLayer3)
        n.addModule(self.hiddenLayer4)
        n.addModule(self.hiddenLayer5)
        n.addModule(self.hiddenLayer6)
        n.addOutputModule(self.outLayer)        
        
        
        
        from pybrain.structure import FullConnection
        
        in_to_hidden = FullConnection(self.inLayer, self.hiddenLayer1)
        hidden_to_hidden1 = FullConnection(self.hiddenLayer1, self.hiddenLayer2)
        hidden_to_hidden2 = FullConnection(self.hiddenLayer2, self.hiddenLayer3)
        hidden_to_hidden3 = FullConnection(self.hiddenLayer3, self.hiddenLayer4)
        hidden_to_hidden4 = FullConnection(self.hiddenLayer4, self.hiddenLayer5)
        hidden_to_hidden5 = FullConnection(self.hiddenLayer5, self.hiddenLayer6)
        hidden_to_out = FullConnection(self.hiddenLayer6, self.outLayer)        
        
        n.addConnection(in_to_hidden)
        n.addConnection(hidden_to_hidden1)
        n.addConnection(hidden_to_hidden2)
        n.addConnection(hidden_to_hidden3)
        n.addConnection(hidden_to_hidden4)
        n.addConnection(hidden_to_hidden5)
        n.addConnection(hidden_to_out)        
        
#        in_to_hidden = FullConnection(self.inLayer, self.hiddenLayer)
#        hidden_to_out = FullConnection(self.hiddenLayer, self.outLayer)
        
#        n.addConnection(in_to_hidden)
#        n.addConnection(hidden_to_out)
        
        n.sortModules()
        
        print len(n.connections[self.inLayer][0].params)
        print len(n.connections[self.hiddenLayer1][0].params )
        print len(n.connections[self.hiddenLayer2][0].params)
        print len(n.connections[self.hiddenLayer3][0].params)
        print len(n.connections[self.hiddenLayer4][0].params)
        print len(n.connections[self.hiddenLayer5][0].params)
        print len(n.connections[self.hiddenLayer6][0].params)

        for j, i in enumerate(param[0]):
            n.connections[self.inLayer][0].params[j] = i        
        for j, i in enumerate(param[1]):
            n.connections[self.hiddenLayer1][0].params[j] = i        
        for j, i in enumerate(param[2]):
            n.connections[self.hiddenLayer2][0].params[j] = i
        for j, i in enumerate(param[3]):
            n.connections[self.hiddenLayer3][0].params[j] = i
        for j, i in enumerate(param[4]):
            n.connections[self.hiddenLayer4][0].params[j] = i        
        for j, i in enumerate(param[5]):
            n.connections[self.hiddenLayer5][0].params[j] = i        
        for j, i in enumerate(param[6]):
            n.connections[self.hiddenLayer6][0].params[j] = i

        n.convertToFastNetwork()

        self.n = n        
        self.n.convertToFastNetwork()
        
        
    def decideMove(self, state, roll, possible_moves):

        change = []
        for token_index, move in enumerate(possible_moves) :
            change.append(move - state[self.index][token_index])


        liste1 = [state[self.index][0]/57., state[self.index][1]/57.,state[self.index][2]/57., state[self.index][3]/57. ]
        liste2 = [state[(self.index+1)%4][0]/57., state[(self.index+1)%4][1]/57., state[(self.index+1)%4][2]/57., state[(self.index+1)%4][3]/57.]
        liste3 = [state[(self.index+2)%4][0]/57., state[(self.index+2)%4][1]/57., state[(self.index+2)%4][2]/57., state[(self.index+2)%4][3]/57.]
        liste4 = [state[(self.index+3)%4][0]/57., state[(self.index+3)%4][1]/57., state[(self.index+3)%4][2]/57., state[(self.index+3)%4][3]/57.]

        liste =  liste1 + liste2 + liste3 + liste4  + [ roll/6. ]       

        output = self.n.activate(liste)

        move = np.random.randint(0,len(possible_moves))
        while(change[move] == 0):
            move = np.random.randint(0,len(possible_moves))     
   
        best = output[move]
        chosen_move = move    
    
    
        for  index, score in enumerate(output):
            if score >= best and (change[index] != 0):
                chosen_move = index
                best = score      


        if state[self.index] == [0,0,0,0]:
            self.liste = []#ClassificationDataSet(17, 1, nb_classes=4)
            self.liste.append( [liste , [chosen_move] ]  )
        else :
            self.liste.append( [ liste , [chosen_move] ]  )


        self.number_of_moves += 1
        
        if output[chosen_move] == max(output):
            self.number_of_sound_moves += 1

        return chosen_move


    def receiveFeedback(self, feedback):
        pass
   
#    def get_genes(self):
#        return self.n.connections[self.hiddenLayer][0].params, self.n.connections[self.inLayer][0].params  

    def get_n(self):
        return self.n

    def training_set(self):
        return self.liste

import ludosim
from matplotlib import pyplot as plt
import random    
    
if __name__ == '__main__':
    
    # Instantiate players
        
    print "Start the development"        
    
#    with open('mated_gene_list_3_speed.dat', 'rb') as f:
#        genes = pickle.load(f)    
   
    gene1 = []        
    for i in range(17*15):
        gene1.append(random.uniform(-1, 1))     
    gene2 = []
    for i in range(15*15):
        gene2.append(random.uniform(-1, 1))             
    gene3 = []
    for i in range(15*15):
        gene3.append(random.uniform(-1, 1))                  
    gene4 = []
    for i in range(15*15):
        gene4.append(random.uniform(-1, 1))          
    gene5 = []
    for i in range(15*15):
        gene5.append(random.uniform(-1, 1))                  
    gene6 = []
    for i in range(15*15):
        gene6.append(random.uniform(-1, 1))          
      
    gene7 = []
    for i in range(15*4):
        gene7.append(random.uniform(-1, 1))            
        
    allData = ClassificationDataSet(17, 1, nb_classes=4)

    for count in range(100):
        gplayer = GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2, gene3, gene4, gene5, gene6, gene7]) 
    
        #gplayer.get_genes()
        
        
        players = [ gplayer,
                    ludosim.RandomPlayer(1, 'Random player 1'),                
                    ludosim.RandomPlayer(2, 'Random player 2'),                
                    ludosim.RandomPlayer(3, 'Random player 3') ]        
        
        win_sets = []
     
       
        
            # Variables to hold results
        winner_vect = []
        wins = [0]*len(players)
        
            # Run a lot of games
        for i in range(100) :
            if not i % 10:
                print "Victories", i, wins[0]
            sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
            winner = sim.playGame(players).index
            if winner == 0:
                win_sets = win_sets + players[0].training_set()
            wins[winner] = wins[winner]+1
            winner_vect.append(wins[:]) 
            
        print "Victories", i, wins[0]
        print "sound move %", 100*float(gplayer.number_of_sound_moves)/float(gplayer.number_of_moves)
    
    
        #allData = ClassificationDataSet(17, 1, nb_classes=4)
        for win_sample in win_sets:
            allData.addSample(win_sample[0], win_sample[1])
    
        tstdata, trndata = allData.splitWithProportion( 0.25 )  
      
        trndata._convertToOneOfMany( )
        tstdata._convertToOneOfMany( )
    
        tr_network = gplayer.get_n()
    
        trainer = BackpropTrainer( tr_network, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)
    
        trainer.trainEpochs( 1 )
        trnresult = percentError( trainer.testOnClassData(),
                                  trndata['class'] )
        tstresult = percentError( trainer.testOnClassData(
               dataset=tstdata ), tstdata['class'] )
    
        print "epoch: %4d" % trainer.totalepochs, \
              "  train error: %5.2f%%" % trnresult, \
              "  test error: %5.2f%%" % tstresult

        gene1 = tr_network.connections[gplayer.inLayer][0].params  
        gene2 = tr_network.connections[gplayer.hiddenLayer1][0].params
        gene3 = tr_network.connections[gplayer.hiddenLayer2][0].params
        gene4 = tr_network.connections[gplayer.hiddenLayer3][0].params
        gene5 = tr_network.connections[gplayer.hiddenLayer4][0].params
        gene6 = tr_network.connections[gplayer.hiddenLayer5][0].params
        gene7 = tr_network.connections[gplayer.hiddenLayer6][0].params



#
#
#    print winner_list 
#
#    with open('gene_list_stage4_speed.dat', 'wb') as f:
#        pickle.dump(genes, f)