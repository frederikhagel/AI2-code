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
    def __init__(self, index, name, params):
        self.name = name
        self.index = index
        self.liste = []#ClassificationDataSet(17, 1, nb_classes=4)        
        self.status_good = True

        self.number_of_moves = 0
        self.number_of_sound_moves = 0

        n = FeedForwardNetwork()
        
        self.inLayer = LinearLayer(17)
        self.hiddenLayer = SigmoidLayer(5)
        self.outLayer = LinearLayer(4)
     
        
        n.addInputModule(self.inLayer)
        n.addModule(self.hiddenLayer)
        n.addOutputModule(self.outLayer)
        
        from pybrain.structure import FullConnection
        in_to_hidden = FullConnection(self.inLayer, self.hiddenLayer)
        hidden_to_out = FullConnection(self.hiddenLayer, self.outLayer)
        
        n.addConnection(in_to_hidden)
        n.addConnection(hidden_to_out)
        
        n.sortModules()
        
        for j, i in enumerate(params[0]):
            n.connections[self.hiddenLayer][0].params[j] = i  
            
        for j, i in enumerate(params[1]):
            n.connections[self.inLayer][0].params[j] = i

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
   
    def get_genes(self):
        return self.n.connections[self.hiddenLayer][0].params, self.n.connections[self.inLayer][0].params  

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
    
#    gene1 = []
#    for i in range(20):
#        gene1.append(random.uniform(-1),, 1))            
#    gene2 = []        
#    for i in range(85):
#        gene2.append(random.uniform(-1, 1))        


    gene1 = [-0.394045 ,-0.42523323 ,1.17425565 ,0.68426058 ,-0.76756122 ,-0.38202486, 
         -0.43251972 ,-0.74743696 , 0.58916094 , 1.15660748 , 0.7687538 ,  0.8833087,
         -0.22013751 ,-0.39497726 , 0.13222979 , 0.31185992 , 0.28467431 , 0.20197958,
         -0.34235231, -0.11735546]
         
    gene2 = [ -5.93125358*10**(-2),  -5.02825777*10**(-1),  -7.43123323*10**(-1),   2.72268216*10**(-1),
          -1.71522019*10**(-2),   4.49586559*10**(-2),   1.17559737*10**(-2),   1.53154475*10**(-3),
          -6.22993917*10**(-3),  -7.56530419*10**(-2),  -1.73336772*10**(-2),   1.10334428*10**(-2),
          -8.05223068*10**(-3),  -4.37961805*10**(-2),   1.62623332*10**(-2),  -1.86651987*10**(-2),
           9.51692820*10**(-3),  -5.39453364*10**(-2),  -5.51716543*10**(-1),  -8.17662363*10**(-1),
           3.64845032*10**(-1),  -1.54216957*10**(-2),   6.24146947*10**(-2),   2.39287392*10**(-2),
           9.99261783*10**(-3),   1.23116647*10**(-3),  -8.71307747*10**(-2),  -1.41028789*10**(-2),
           2.37023711*10**(-2),  -2.33068758*10**(-3),  -4.70443933*10**(-2),   2.10552589*10**(-2),
          -2.07545801*10**(-2),   7.25334769*10**(-3),   8.38463850*10**(-1),   9.42097702*10**(-1),
          -4.32765799*10**(-1),  -3.29289396*10**(-1),  -9.24285162*10**(-3),  -8.09600584*10**(-3),
           5.71904851*10**(-2),   3.25492854*10**(-3),   4.16351565*10**(-2),   6.11670475*10**(-2),
           6.86794772*10**(-2),   8.92152110*10**(-2),  -5.58108661*10**(-3),   7.51694544*10**(-3),
          -8.35058642*10**(-3),   4.74553385*10**(-2),   1.74906838*10**(-2),   9.52153190*10**(-2),
           4.92458372*10**(-1),   7.17829975*10**(-1),  -9.89063886*10**(-2),   1.73650216*10**(-2),
          -1.51111053*10**(-2),   9.15949333*10**(-3),   1.30543832*10**(-2),   2.39234756*10**(-2),
           4.89518013*10**(-2),   2.44439875*10**(-2),   1.17854298*10**(-2),   1.49895838*10**(-2),
           3.78721780*10**(-2),  -2.29043729*10**(-2),   1.84260850*10**(-2),  -4.37034525*10**(-2),
          -8.50535174*10**(-1),  -7.86287339*10**(-1),   7.17083054*10**(-1),   1.23955783*10**(-1),
           2.87609854*10**(-4),  -3.11260368*10**(-2),  -8.61966815*10**(-2),  -2.37089194*10**(-2),
          -5.89151006*10**(-2),  -4.88255709*10**(-2),  -7.91137260*10**(-2),  -1.22454195*10**(-1),
          -1.58646690*10**(-2),  -5.12659972*10**(-3),  -1.89296045*10**(-2),  -4.08347212*10**(-2),
          -4.55205302*10**(-2)]

    #allData = ClassificationDataSet(17, 1, nb_classes=4)

    for count in range(100):
        gplayer = GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2]) 
    
    
        gplayer.get_genes()
        
        
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
    
    
        allData = ClassificationDataSet(17, 1, nb_classes=4)
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

        gene1 = tr_network.connections[gplayer.hiddenLayer][0].params  
            
        gene2 = tr_network.connections[gplayer.inLayer][0].params


#
#
#    print winner_list 
#
#    with open('gene_list_stage4_speed.dat', 'wb') as f:
#        pickle.dump(genes, f)