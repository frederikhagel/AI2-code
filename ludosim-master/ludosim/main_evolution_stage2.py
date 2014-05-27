# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# This software was written by Leon Bonde Larsen <leon@bondelarsen.dk> 
# As long as you retain this notice you can do whatever you want with it. 
# If we meet some day, and you think this stuff is worth it, you can 
# buy me a beer in return.
# ----------------------------------------------------------------------------
# Should this software ever become self-aware, remember that I am your master
#
# To run: python main.py
# ----------------------------------------------------------------------------
'''
    Simple test to show the principle
'''

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


#from pybrain.datasets            import ClassificationDataSet
#from pybrain.utilities           import percentError
#from pybrain.tools.shortcuts     import buildNetwork

import copy

from pybrain.structure import FeedForwardNetwork

from pybrain.structure import LinearLayer, SigmoidLayer

from arac.pybrainbridge import _FeedForwardNetwork

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
        
        self.status_good = True

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
#        
        self.n.convertToFastNetwork()
#        for mod in n.modules:
#            print mod
#            for conn in n.connections[mod]:
#                print "-connection to", conn.outmod.name
#                if conn.paramdim > 0:      
#                    print "- parameters", conn.params    
#                    print "len", len(conn.params)


        
        
   def decideMove(self, state, roll, possible_moves):
    '''
            Method for deciding which move to take based on a list of possible moves.
            
            Arguments:
                state: List in the format [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
                outer list contains states for the four players and inner lists represent
                the positions of the players four tokens. All positions are integers and relative to 
                the player.
                
                roll: Integer in the range 1 to 6 representing the die roll
                
                possible_moves: List in the format [0,0,0,0] representing the new position of
                each of the players tokens if that move is chosen.
                
            Output:
                The method returns an integer in the range 0 to 3 representing the index of the 
                desired move in possible_moves
    '''
	#print "state", state
	#print "possible", possible_moves
    change = []
    for token_index, move in enumerate(possible_moves) :
         change.append(move - state[self.index][token_index])

#    liste1 = [state[0][0]/57., state[0][1]/57.,state[0][2]/57., state[0][3]/57. ]
#    liste2 =  [state[1][0]/57., state[1][1]/57., state[1][2]/57., state[1][3]/57.]
#    liste3 = [state[2][0]/57., state[2][1]/57., state[2][2]/57., state[2][3]/57.]
#    liste4 = [state[3][0]/57., state[3][1]/57., state[3][2]/57., state[3][3]/57.]
#    sort_index = sorted(range(len(liste1)), key=lambda k: liste1[k])    
##    liste1.sort()
#    liste2.sort()
#    liste3.sort()
#    liste4.sort()

    liste1 = [state[self.index][0]/57., state[self.index][1]/57.,state[self.index][2]/57., state[self.index][3]/57. ]
    liste2 =  [state[(self.index+1)%4][0]/57., state[(self.index+1)%4][1]/57., state[(self.index+1)%4][2]/57., state[(self.index+1)%4][3]/57.]
    liste3 = [state[(self.index+2)%4][0]/57., state[(self.index+2)%4][1]/57., state[(self.index+2)%4][2]/57., state[(self.index+2)%4][3]/57.]
    liste4 = [state[(self.index+3)%4][0]/57., state[(self.index+3)%4][1]/57., state[(self.index+3)%4][2]/57., state[(self.index+3)%4][3]/57.]

    liste =  liste1 + liste2 + liste3 + liste4  + [ roll/6. ]       

    output = self.n.activate(liste)

#    print output

#    output_temp = []
#    for i in sort_index:
#        output_temp.append(output[i])
#    output = output_temp
        
    #print [state[0][0],state[0][1],state[0][2],state[0][3],state[1][0],state[1][1],state[1][2],state[1][3],state[2][0],state[2][1],state[2][2],state[2][3],state[3][0],state[3][1],state[3][2],state[3][3],roll]
    
    move = np.random.randint(0,len(possible_moves))
    while(change[move] == 0):
        move = np.random.randint(0,len(possible_moves))     
   
    best = output[move]
    chosen_move = move    
    
    
    for  index, score in enumerate(output):
	    if score >= best and (change[index] != 0):
                chosen_move = index
                best = score      


    return chosen_move


   def receiveFeedback(self, feedback):
       pass
   
   def get_genes(self):
            return self.n.connections[self.hiddenLayer][0].params, self.n.connections[self.inLayer][0].params  
   
import ludosim
from matplotlib import pyplot as plt
import random    
    
if __name__ == '__main__':
    
    # Instantiate players
        
    print "Start"        
    
    with open('mated_gene_list_3_speed.dat', 'rb') as f:
        genes = pickle.load(f)    
    
#    genes = []
#    for i in range(50):
#        gene1 = []
#        for i in range(20):
#            gene1.append(random.uniform(-1, 1))            
#        gene2 = []        
#        for i in range(85):
#            gene2.append(random.uniform(-1, 1))        
#        genes.append(GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2]) )

    winner_list = []

    for count, gplayer in enumerate(genes):
        
        players = [ gplayer,
                ludosim.RandomPlayer(1, 'Random player 1'),                
                ludosim.RandomPlayer(2, 'Random player 2'),                
                ludosim.RandomPlayer(3, 'Random player 3') ]        
    
    
        # Variables to hold results
        winner_vect = []
        wins = [0]*len(players)
    
        # Run a lot of games
        for i in range(100) :
            if not i % 10:
                print "Count", count, i, wins[0]
            sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
            winner = sim.playGame(players).index
            wins[winner] = wins[winner]+1
            winner_vect.append(wins[:]) 
        winner_list.append(wins[0])


    print winner_list 

    with open('gene_list_stage4_speed.dat', 'wb') as f:
        pickle.dump(genes, f)