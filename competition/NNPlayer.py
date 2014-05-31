# -*- coding: utf-8 -*-
"""
Created on Sat May 17 19:54:50 2014

@author: dimx
"""
from NeuralNetwork import NeuralNetwork

class NNPlayer(object):
    def __init__(self, index, name, nn_network = [1,2], nn_weights = []):
        self.name = name
        self.index = index
        self.real_index = index
        self.brain = NeuralNetwork(nn_network)
        self.pos_globes = [1,9,14,22,27,35,40,48]
        self.pos_stars = [6,12,19,25,32,38,45,51]
        self.pos_start = 0
        self.pos_home = 57
        self.pos_runway_start = 52
        self.token_outputs = [0.0,0.0,0.0,0.0]
        self.winner_output = 0.0
        self.winner_token = 0
        self.restart_counter = [0]*4
        self.turns = 0
        self.die_roll_sum = 0
        self.initNeuralNetwork()
        nn_weight_length = self.getNumWeights()
        if len(nn_weights) == nn_weight_length:
            self.brain.setWeights(nn_weights)
        elif not len(nn_weights) == 0:
            print "Wrong length of weights %i (%s): " % ( len(nn_weights), name)
        
    def initNeuralNetwork(self):
        state = [[12, 24, 57, 52], [57, 7, 57, 34], [48, 57, 39, 57], [15, 57, 47, 57]]
        roll = 5
        possible_moves = [17, 29, 57, 57]
        self.getBrainOutput(state, roll, possible_moves)      
        
    def new_index(self, index):
        self.index = index     
        
    def getNumWeights(self):
        return self.brain.getNumWeights()
    
    def setWeights(self, newWeights):
        self.brain.setWeights(newWeights)
        
    def showWeights(self):
        return self.brain.showWeights()
    
    
    def getBrainOutput(self, state, roll, possible_moves):   
        athome = self.athome(state)
        atstart = self.atstart(state)
        atrunway = self.atrunway(state)
        #can move to star
        #can move to globus
        #can hit player home
        [opponent_near_front, opponent_near_back] = self.opponent_near(state)
        
        nn_out = [-1]*len(possible_moves)    
        
        move = 0
        max_score = -1
        scores = list()
        nn_roll = self.translate_clamp_val(roll, 1, 6, -1, 1)
        
        for token_id in range(len(possible_moves)):
            if possible_moves[token_id] - state[self.index][token_id] > 0:
                nn_in = list()
                nn_in.append(nn_roll)
                nn_in.append(athome[token_id])
                nn_in.append(atstart[token_id])
                nn_in.append(atrunway[token_id])
                opponent_near_front_token = self.translate_clamp_val(opponent_near_front[token_id], 0, 6, -1, 1)
                opponent_near_back_token = self.translate_clamp_val(opponent_near_front[token_id], -6, 0, -1, 1)
                nn_in.append(opponent_near_front_token)
                nn_in.append(opponent_near_back_token)
                #print self.restart_counter
                my_restarts = self.translate_clamp_val(self.restart_counter[token_id], 0, 5, -1, 1)
                player_restarts = self.translate_clamp_val(sum(self.restart_counter), 0, 10, -1, 1)
                
                nn_in.append(my_restarts)
                nn_in.append(player_restarts)
                                
                # distance to goal
                # distance to globe
                
                nn_in.append(self.token_outputs[token_id])
                nn_in.append(self.winner_output)
                nn_in.append(self.tokenForNN(token_id))
                nn_in.append(self.tokenForNN(self.winner_token))
                
                nn_out[token_id] = score = self.brain.think(nn_in)[0]
                scores.append(score)
                self.token_outputs[token_id] = score
                #print "Token %i has score %f" % (token_id, score)
                if (score > max_score):
                    max_score = score
                    move = token_id                    
        #print scores        
        self.winner_output = max_score
        return move
 
    def decideMove(self, state, roll, possible_moves):
        '''
            We need to provide the following information to the neural network:
                roll - Numerical mapped from [1-6] to [-1-1]
                athome - Binary [-1,1]
                atstart - Binary [-1,1]
                atrunway - Binary [-1,1]
                opponent_front - Numerical mapped from [1-6] to [-1-1]
                opponent_back - Numerical mapped from [1-6] to [-1-1]
                distance_goal - Numerical
                distance_globe - Numerical
                Your last output - Numerical
                Winner last output - Numerical
                Your token id - Numerical
                Winner last token id - Numerical
                -- Your restart counter - Numerical mapped from [0-5] to [-1-1]
                -- Player restart counter - Numerical mapped from [0-10] to [-1-1]
        '''
        self.die_roll_sum += roll
        self.turns += 1
        
        move = self.getBrainOutput(state, roll, possible_moves) 
        #print "State: ", state
        #print "Roll: ", roll
        #print "Possible moves" , possible_moves
        #print "My move: ", move
        return move
    
    def tokenForNN(self, token_id):
        # input 0-3
        # output -1-1
        centered_token = token_id -1.5 # -1.5 - 1.5
        normalized_token = centered_token / 1.5
        
        return normalized_token
 
    def loadWeights(self, filename):
        import pickle
        iput = open(filename, 'r')
        pool = pickle.load(iput)
        breed = pool[len(pool) - 1]
        if len(breed['genes']) == 8150:
            nn_network = [50,50,50,50,1]
            self.brain = NeuralNetwork(nn_network)
            self.setWeights(breed['genes'])
            print "Large genepool loaded with fitness %i" % breed['fitnessvalue']
        elif len(breed['genes']) == 230:
            nn_network = [10,10,1]
            self.brain = NeuralNetwork(nn_network)
            self.setWeights(breed['genes'])
            print "Small genepool loaded with fitness %i" % breed['fitnessvalue']
        else:
            print "Unknown genes"
       
    def atposition(self,state,position):    
        my_state = state[self.index]
        atposition = [0]*len(my_state)
        for token_id in range(len(my_state)):
            if my_state[token_id] == position:
                atposition[token_id] = 1
        return atposition
        
    def athome(self,state):
        return self.atposition(state,self.pos_home)
    
    def atstart(self,state):
        return self.atposition(state,self.pos_start)
    
    def atrunway(self,state):
        my_state = state[self.index]
        atrunway = [0]*len(my_state)
        for token_id in range(len(my_state)):
            if my_state[token_id] > self.pos_runway_start:
                atrunway[token_id] = 1
        return atrunway
    
    def translate_val(self,value, leftMin, leftMax, rightMin, rightMax):
        # Found at : http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
    
        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)
    
        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)    

    def translate_clamp_val(self,value, leftMin, leftMax, rightMin, rightMax):
        val = self.translate_val(value, leftMin, leftMax, rightMin, rightMax)
        if val > rightMax:
            val = rightMax
        if val < rightMin:
            val = rightMin
        return val
    
    def opponent_near(self, state):
        # Find nearest distance to opponent token
        my_state = state[self.index]
        opponent_front = [99]*len(my_state)
        opponent_back = [-99]*len(my_state)
        for opponent_player_id in range(len(state)):
            if not opponent_player_id == self.index:
                opponent_player_state = state[opponent_player_id]
                for opponent_token in opponent_player_state:
                    for my_token_id in range(len(my_state)):
                        distance = opponent_token - my_state[my_token_id]
                        if distance > 0:
                            if (distance < opponent_front[my_token_id]):
                                opponent_front[my_token_id] = distance
                        else:
                            if (distance > opponent_back[my_token_id]):
                                opponent_back[my_token_id] = distance
                                
        return [opponent_front, opponent_back]        
       
    
    def receiveFeedback(self, feedback):
        self.restart_counter = feedback[self.index]
        pass

def testPlayer():
    player = NNPlayer(0, 'Player')
    state = [[12, 24, 57, 52], [57, 7, 57, 34], [48, 57, 39, 57], [15, 57, 47, 57]]
    roll = 5
    possible_moves = [17, 29, 57, 57]
    player.decideMove(state, roll, possible_moves)

def testLoadPlayer():
    player = NNPlayer(0, 'Player')
    player.loadWeights("1401234786.57.pkl")

if __name__ == '__main__':
    print "All your base are belong to us!" 
    #testPlayer()
    testLoadPlayer()