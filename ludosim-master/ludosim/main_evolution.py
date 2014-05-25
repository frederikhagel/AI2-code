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

from pybrain.structure import LinearLayer, SigmoidLayer
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
        
        inLayer = LinearLayer(17)
        hiddenLayer = SigmoidLayer(5)
        outLayer = LinearLayer(4)
     
        
        n.addInputModule(inLayer)
        n.addModule(hiddenLayer)
        n.addOutputModule(outLayer)
        
        from pybrain.structure import FullConnection
        in_to_hidden = FullConnection(inLayer, hiddenLayer)
        hidden_to_out = FullConnection(hiddenLayer, outLayer)
        
        n.addConnection(in_to_hidden)
        n.addConnection(hidden_to_out)
        
        n.sortModules()
        
        for i in params[1]:
            n.connections[hiddenLayer][0].params[i] = 0   
        for i in params[0]:
            n.connections[inLayer][0].params[i] = 0  

        self.n = n
#        
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


    return chosen_move


   def receiveFeedback(self, feedback):
       pass
   
import ludosim
from matplotlib import pyplot as plt
import random    
    
if __name__ == '__main__':
    
    # Instantiate players
        
    print "Start"        
    
    genes = []    
    
    for i in range 50::
        gene1 = []
        for i in range(20):
            gene1.append(random.uniform(-1, 1))            
        gene2 = []        
        for i in range(85):
            gene2.append(random.uniform(-1, 1))        
        genes.append(GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2]) )

    for gplayer in genes:
        
        players = [ GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2]),
                ludosim.RandomPlayer(1, 'Random player 1'),                
                ludosim.RandomPlayer(2, 'Random player 1'),                
                ludosim.RandomPlayer(3, 'Random player 2') ]        
    
    
    # Variables to hold results
    winner_vect = []
    wins = [0]*len(players)
    
    great_list = []    
    
    # Run a lot of games
    for i in range(100) :
        if not i % 10:
            print i
            print wins[0]
        sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
        winner = sim.playGame(players).index
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




