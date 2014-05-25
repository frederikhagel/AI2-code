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

import numpy as np

import pickle


from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork

import copy

from pybrain.structure import FeedForwardNetwork
n = FeedForwardNetwork()

from pybrain.structure import LinearLayer, SigmoidLayer
#
#inLayer = LinearLayer(17)
#hiddenLayer = SigmoidLayer(20)
#outLayer = LinearLayer(4)
#
#n.addInputModule(inLayer)
#n.addModule(hiddenLayer)
#n.addOutputModule(outLayer)
#
#from pybrain.structure import FullConnection
#in_to_hidden = FullConnection(inLayer, hiddenLayer)
#hidden_to_out = FullConnection(hiddenLayer, outLayer)
#
#n.addConnection(in_to_hidden)
#n.addConnection(hidden_to_out)
#
#n.sortModules()
#
#print n.activate([0, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 39, 0, 6])

class GeneticPlayer(object):

   '''
        Simple player choosing at random which move to take.
   '''
   def __init__(self, index, name):
        self.name = name
        self.index = index
        fileObject = open('../../n_marius','r')
        self.fnn = pickle.load(fileObject)
        
        self.status_good = True
        self.last_state = [0,0,0,0]

        self.chosen_states = []
        self.liste = []
       
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

    liste1 = [state[0][0], state[0][1],state[0][2], state[0][3] ]
    liste2 =  [state[1][0], state[1][1], state[1][2], state[1][3]]
    liste3 = [state[2][0], state[2][1], state[2][2], state[2][3]]
    liste4 = [state[3][0], state[3][1], state[3][2], state[3][3]]

    
    liste =  liste1 + liste2 + liste3 + liste4  + [ roll ]       

    output = self.fnn.activate(liste)

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
	    if(change[index] != 0) and score >= best:
                chosen_move = index
                best = score      

    outer = [0,0,0,0]
    outer[chosen_move] = 1

    if state[self.index] == [0,0,0,0]:
        self.liste = []            
        self.liste.append( [[ copy.deepcopy(state), copy.copy(roll) ], outer] )
    elif self.status_good :
        self.liste.append( [[ copy.deepcopy(state), copy.copy(roll) ], outer] )



    return chosen_move


   def receiveFeedback(self, feedback):
      if self.last_state[self.index] == feedback[self.index] :
            self.status_good = True
      else:
            self.status_good = False
      self.last_state = feedback        


   def give_list(self):
        return self.chosen_states

import ludosim
from matplotlib import pyplot as plt
import random    
    
if __name__ == '__main__':
    
    # Instantiate players
        
    print "Start"        
        
    players = [ GeneticPlayer(0, 'Genetic Warrior 0'),
                ludosim.RandomPlayer(1, 'Random player 1'),                
                ludosim.RandomPlayer(2, 'Random player 2'),
                ludosim.RandomPlayer(3, 'Random player 3') ]        
    
    
    # Variables to hold results
    winner_vect = []
    wins = [0]*len(players)
    
    great_list = []    
    
    # Run a lot of games
    for i in range(1000) :
        if not i % 10:
            print i
            print wins[0]
        sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
        winner = sim.playGame(players).index
        if winner == 0:
            #print players[0].liste
            great_list.append( players[0].liste  )        
        wins[winner] = wins[winner]+1
        winner_vect.append(wins[:]) 


    print "antal", len(great_list)
#
    with open('new2_test_liste.dat', 'wb') as f:
        pickle.dump(great_list, f)

   
    # Plot the winnings
    plt.figure("Winnings")
    plt.plot(range(len(winner_vect)),winner_vect)
    plt.legend(['{}'.format(player.name) for player in players],loc=2)
    plt.xlabel("games played")
    plt.ylabel("games won")   
    plt.show()




