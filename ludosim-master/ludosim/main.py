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

class MariusPlayer(object):

   '''
        Simple player choosing at random which move to take.
   '''
   def __init__(self, index, name):
        self.name = name
        self.index = index
        fileObject = open('fnn','r')
        self.fnn = pickle.load(fileObject)

       
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

    output = self.fnn.activate([state[0][0],state[0][1],state[0][2],state[0][3],state[1][0],state[1][1],state[1][2],state[1][3],state[2][0],state[2][1],state[2][2],state[2][3],state[3][0],state[3][1],state[3][2],state[3][3],roll])


    
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


class QuickPlayer(object):

   '''
        Simple player choosing at random which move to take.
   '''
   def __init__(self, index, name):
        self.name = name
        self.index = index  
       
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


    best = possible_moves[0]
    chosen_move = 0
    
    for  index, move in enumerate(possible_moves):
	    if(change[index] != 0) and move >= best:
                chosen_move = index
                best = move      

    return chosen_move


   def receiveFeedback(self, feedback):
       pass
   
class SafePlayer(object):
   '''
        Simple player choosing at random which move to take.
   '''
   def __init__(self, index, name):
        self.name = name
        self.index = index  
       
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
    danger = []    
    change = []
    for token_index, move in enumerate(possible_moves) :
         change.append(move - state[self.index][token_index])

    import copy

    possible_states = []
    for token_index, move in enumerate(possible_moves) :
        k = copy.copy(state[self.index])
        k[token_index] = move
        possible_states.append(k)        
        
#    print possible_states        
        
#        inherent_danger = 0
#
    for tested_state in possible_states:
        inherent_danger = 0         
        if token_index != self.index:
            for pos in tested_state:
                if tested_state.count( pos ) > 1:
                    pass
                else:                    
                    for enemy_index, enemys in enumerate(state):    
                        if enemy_index != self.index:
                            for enemy in enemys:
                                if pos - enemy < 7 and pos - enemy > 0:
                                    inherent_danger = inherent_danger + 1
        danger.append(inherent_danger) 

  

    move = np.random.randint(0,len(possible_moves))
    while(change[move] == 0):
        move = np.random.randint(0,len(possible_moves))  

    chosen_move = move
    best = danger[move]
   
    for  index, inherent_danger in enumerate(danger):
        if(change[index] != 0) and inherent_danger < best:
                chosen_move = index
                best = inherent_danger      

#    print possible_states
#    print danger  
#    print chosen_move

#	print chosen_move
    return chosen_move

   def receiveFeedback(self, feedback):
        '''
            Method for receiving feedback from the simulator in the form of counters showing
            how many times each token on the board has restarted. If the player was hit home 
            or managed to hit home another players token, the knowledge can be extracted from
            the received list.
            
            Arguments:
                feedback: List in the format [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
                representing for each token of each player how many times that token has 
                restarted.
                
            Output: none
        '''
        pass
    
   def give_list(self):
        return self.chosen_states

class FrederikPlayer(object):
   '''
        Simple player choosing at random which move to take.
   '''
   def __init__(self, index, name):
        self.name = name
        self.index = index
        self.chosen_states = []
#        self.temp_index = 0

#    def changeTempIndex(self, index):
#        self.temp_index = index       
       
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

    summation = 0
    for c in change:
        if c > 0:
            summation = summation + 1
#
#    print change
#    print summation            
            
    import copy            
            
    if summation > 2: 
        if np.random.randint(0,150) == 0:
            print change
            print summation
            print [ state, roll ] 
            self.chosen_states.append( [ copy.deepcopy(state), copy.copy(roll) ] )
               

    move = np.random.randint(0,len(possible_moves))
    while(change[move] == 0):
        move = np.random.randint(0,len(possible_moves))        
        
	
#	print "possible", possible_moves
    #print [ state, roll ]
#    best = possible_moves[0]
#    chosen_move = 0
#    for  index, move in enumerate(possible_moves):
#	    if(change[index] != 0) and move >= best:
#                chosen_move = index
#                best = move      

#	print chosen_move
    return move

   def receiveFeedback(self, feedback):
        '''
            Method for receiving feedback from the simulator in the form of counters showing
            how many times each token on the board has restarted. If the player was hit home 
            or managed to hit home another players token, the knowledge can be extracted from
            the received list.
            
            Arguments:
                feedback: List in the format [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
                representing for each token of each player how many times that token has 
                restarted.
                
            Output: none
        '''
        pass
    
   def give_list(self):
        return self.chosen_states

class GroupPlayer(object):
    '''
        Simple player choosing at random which move to take.
    '''
    def __init__(self, index, name):
        self.name = name
        self.index = index
        
    def changeTempIndex(self, index):
        self.index = index       
       
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

#        move = np.random.randint(0,len(possible_moves))
#        while(change[move] == 0):
#            move = np.random.randint(0,len(possible_moves))        
        
	
#	print "possible", possible_moves
        best = 100
        #print [ state, move ]
        for  index, move in enumerate(possible_moves):
            if(change[index] != 0) and move < best:
                chosen_move = index
                best = move      

#	print chosen_move
        return chosen_move

    def receiveFeedback(self, feedback):
        '''
            Method for receiving feedback from the simulator in the form of counters showing
            how many times each token on the board has restarted. If the player was hit home 
            or managed to hit home another players token, the knowledge can be extracted from
            the received list.
            
            Arguments:
                feedback: List in the format [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
                representing for each token of each player how many times that token has 
                restarted.
                
            Output: none
        '''
        pass


import ludosim
from matplotlib import pyplot as plt
import random    
    
if __name__ == '__main__':
    
    # Instantiate players
        
    print "Start"        
        
    players = [ MariusPlayer(0, 'Marius player 0'),
                ludosim.RandomPlayer(1, 'Random player 1'),                
                ludosim.RandomPlayer(2, 'Random player 2'),
                ludosim.RandomPlayer(3, 'Random player 3') ]        
    
    
    # Variables to hold results
    winner_vect = []
    wins = [0]*len(players)
    
    # Run a lot of games
    for i in range(100) :
        sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
        winner = sim.playGame(players).index
        wins[winner] = wins[winner]+1
        winner_vect.append(wins[:]) 


#    print "antal", len(players[0].give_list())
#
#    import pickle
#    with open('state_liste.dat', 'wb') as f:
#        pickle.dump(players[0].give_list(), f)

   
    # Plot the winnings
    plt.figure("Winnings")
    plt.plot(range(len(winner_vect)),winner_vect)
    plt.legend(['{}'.format(player.name) for player in players],loc=2)
    plt.xlabel("games played")
    plt.ylabel("games won")   
    plt.show()




