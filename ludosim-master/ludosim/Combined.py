'''
Created on May 10, 2014

@author: leon
'''
import numpy as np

class Player(object):
    '''
    classdocs
    '''


    def __init__(self, index, name, learn_statics=True, learn_dynamics=True, passive=False, max_updates=200, printout=False, optimal_policy=False,random_start_guess=True, learning_rate=0.01):
        '''
        Constructor
        '''
        # Parse constructor parameters
        self.index = index
        self.name = name
        
        self.passive = passive
        self.max_updates = max_updates
        self.printout = printout
        self.optimal_policy = optimal_policy
        self.learn_statics = learn_statics
        self.learn_dynamics = learn_dynamics
        
        
        self.printout = printout
        self.learning_rate = learning_rate
        self.random_start_guess = random_start_guess
        
        self.last_feedback = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.previous_state = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.previous_move = 0
        
        # Settings
        self.input_neurons = 14
        self.output_neurons = 1
        self.offset = 1.0
        
        self.previous_input = [0]*self.input_neurons
        self.previous_linear_output = 0
        
        # Class variables
        self.neurons = np.zeros((self.input_neurons), dtype=np.float64)

        if self.random_start_guess :
            self.weight = np.random.rand(self.output_neurons, self.input_neurons)
            for i in range(len(self.weight)) :
                for j in range(len(self.weight[i])) :
                    self.weight[i][j] -= 0.5
                    
        else :
            # Initialise with values based on probability
            self.weight = np.zeros((self.output_neurons, self.input_neurons), dtype=np.float64)

            self.weight[0][0] = (1.0/6.0)      # -6
            self.weight[0][1] = (1.0/6.0)      # -5
            self.weight[0][2] = (1.0/6.0)      # -4
            self.weight[0][3] = (1.0/6.0)      # -3
            self.weight[0][4] = (1.0/6.0)      # -2
            self.weight[0][5] = (1.0/6.0)      # -1
            self.weight[0][6] = 1              #  0 (center)
            self.weight[0][7] = -(3.0/12.0)     # +1
            self.weight[0][8] = -(3.0/12.0)     # +2
            self.weight[0][9] = -(2.0/12.0)     # +3
            self.weight[0][10] = -(2.0/12.0)    # +4
            self.weight[0][11] = -(1.0/12.0)    # +5
            self.weight[0][12] = -(1.0/12.0)    # +6
            self.weight[0][13] = 1    # Offset weight
            
            
        # Class variables
        self.utility = []
        self.visits = [[0.0]*60]*6
        self.updates = 0
        self.home = 57

        self.initUtility()
        
        
        
    def initUtility(self):
        stars = [6,12,19,25,32,38,45]
        globes = [1,9,14,22,27,35,40,48]
        
        if self.optimal_policy :    
            for roll in range(6):
                tmp = []
                for tile in range(self.home+6):
                    if tile+roll+1 in stars :
                        tmp.append(1.0)
                    elif tile == self.home:
                        tmp.append(1.0)
                    elif tile == 0:
                        tmp.append(-1.0)
                    else :
                        tmp.append(0.0)
                self.utility.append(tmp)
            self.utility[5][0] = -1.0 # Start+roll6 gives star, which is wrong 
        else :
            for tile in range(self.home+6) :
                if tile == 0 :
                    self.utility.append(0.0)
                elif tile == self.home :
                    self.utility.append(1.0)
                elif tile == 1 :
                    self.utility.append(0.0)
                elif tile in globes :
                    self.utility.append(0.0)
                elif tile in stars :
                    self.utility.append(0.0)
                else:
                    self.utility.append(0.0)

            self.utility = [self.utility[:],self.utility[:],self.utility[:],self.utility[:],self.utility[:],self.utility[:]] # Extend state space to cover die roll too                      
                                      

    def decideMove(self, state, roll, possible_moves):
        # Analyse effect of possible moves
        change = []
        for token_index, move in enumerate(possible_moves) :
            change.append(move - state[self.index][token_index])
        
        # Iterate in random order to simulate random selection between moves with equal threat values
        iteration_order = range(len(possible_moves))
        np.random.shuffle(iteration_order)
        
        # Find best move    
        for token_index in iteration_order :
            move = -1
            best = 0
            if self.printout :
                print "  Evaluating move " + str(token_index)
            
            # Evaluate actual moves in possible moves    
            if change[token_index] > 0 : 
                self.updateActivation( self.extractInputFromState( state, possible_moves[token_index]))

                utility = self.getUtility(roll,state[self.index][token_index])
                threat = self.getOutput()                   
                evaluation =  utility - threat 
                    
                if evaluation > best and change > 0:
                    best = evaluation
                    move = token_index
            else :
                if self.printout :
                    print "  Move chances nothing"


        # Make sure a valid move was selected
        if move == -1 :
            while(change[move] == 0):
                move = np.random.randint(0,len(possible_moves))
        
        # Upkeep         
        self.previous_move = move

        self.updateActivation( self.extractInputFromState( state, possible_moves[move]))
        self.visits[roll-1][state[self.index][move]] += 1
        self.update(state[self.index][move], roll, possible_moves[move]) 
        if self.printout :
            print "  Deciding to move token " + str(move) + " to tile " + str(possible_moves[move])
        return move
            
    def getUtility(self, roll, token):
        if self.updates < self.max_updates and self.visits[roll-1][token] < 5 :
            return 1
        else :
            return self.utility[roll-1][token]
                    
    def randomMove(self, state, roll, possible_moves):
        change = []
        for token_index, move in enumerate(possible_moves) :
            change.append(move - state[self.index][token_index])
        move = np.random.randint(0,len(possible_moves))
        while(change[move] == 0):
            move = np.random.randint(0,len(possible_moves))
        return move
        
    
    def update(self, old_tile, roll, new_tile):
        if self.learn_statics :
            self.updates += 1
            if not self.optimal_policy :
                hit_tile = (old_tile + roll)
                learning_rate = (1/(1+(self.visits[roll-1][old_tile])))
                if self.updates > self.max_updates :
                    learning_rate /= self.updates
                reward = 1.0*(new_tile - hit_tile)
                temporal_difference = (reward + self.utility[roll-1][hit_tile] - self.utility[roll-1][old_tile])
                self.utility[roll-1][old_tile] += learning_rate * temporal_difference
                
                if self.printout :
                    print "Updating transition from " + str(old_tile) + " to " + str(hit_tile) + " visited: " + str(self.visits[roll-1][old_tile])
                    print "  Rewards: " + str(self.utility[roll-1][old_tile]) + " and " + str(self.utility[roll-1][hit_tile])
                    print " learning rate: " + str(learning_rate) + " and temporal difference: " + str(temporal_difference)
                    print "   New utility: " +str(self.utility[roll-1][old_tile])  
                
    def extractInputFromState(self, state_vector, center):
        if self.printout :
            print "Testing state " + str(state_vector)
        out = [0.0]*self.input_neurons
        for state_i in range(len(state_vector)) :
            if self.printout :
                print "Checking player " + str(state_i)
            for token_i in range(len(state_vector[state_i])) :
                if self.printout :
                    print "  Checking token " + str(token_i) + " at tile " + str(state_vector[state_i][token_i])
                if state_vector[state_i][token_i] > 0 and state_vector[state_i][token_i] < 52 :
                    if self.printout :
                        print "    tile is between 1 and 51 and offset value is " + str(state_vector[state_i][token_i] - center + 6)
                    if (state_vector[state_i][token_i] - center + 6) < 52 :
                        if self.printout :
                            print "     which is below 51 and thus offset token is " + str((state_vector[state_i][token_i] - center + 6))
                        offset_token = (state_vector[state_i][token_i] - center + 6)
                    else :
                        if self.printout :
                            print "     which is above 51 and thus offset token is " + str((state_vector[state_i][token_i] - center + 6) % 52)
                        offset_token = ((state_vector[state_i][token_i] - center + 6) % 52)
                    if offset_token > 0 and offset_token < 12 :
                        if self.printout :
                            print "         which is between 0 and 12"
                        if state_i == self.index :
                            if self.printout :
                                print "           Registered as friendly token"
                            out[offset_token] = -1.0
                        else :
                            if self.printout :
                                print "           Registered as enemy token"
                            out[offset_token] = 1.0
                    else:
                        if self.printout :
                            print "         which is not between 0 and 12"
                else :
                    if self.printout :
                        print "    tile is not between 1 and 51"
        
        # Flip sign on center value if it is protected
        if center in [1,9,14,22,27,35,40,48]:
            out[6] *= -1.0
        else :    
            for state in state_vector :
                if state.count(center) > 1:
                    out[6] *= -1.0
                    
        if self.printout :
            print "Final output is " + str(out)    
        return out
   
   
    def activationFunction(self, u):
        return np.tanh(u)
    

    def derivativeFunction(self, u):
        return 1 - (self.activationFunction(u)**2)
    
    
    def updateActivation(self, input_synapses):
        input_synapses[-1] = self.offset # append offset
        for synapse_i in range(self.input_neurons):
            for neuron_i in range(self.output_neurons) :
                self.neurons[synapse_i] = input_synapses[synapse_i]*self.weight[neuron_i][synapse_i]
                
        self.previous_input = input_synapses
       
                
    def getOutput(self):
        summation = 0.0
        for neuron_i in range(len(self.neurons)) :
            summation += self.neurons[neuron_i]
        self.previous_linear_output = summation
        return self.activationFunction(summation)
            

    def receiveFeedback(self, feedback):
        difference = [map(int.__sub__,a ,b) for a,b in zip(feedback, self.last_feedback)]
        
        for index in range(len(difference)):
            if index > 6 :
                difference[index] += self.neurons[0][index]*0.6
        
        if self.printout :
            print "Received feedback: " + str(difference)
        for player_i, player in enumerate(difference):
            if 1 in player :
                for token_i, token in enumerate(player) :
                    if token == 1 :
                        self.updateWeights(player_i, token_i)          
        self.last_feedback = feedback

    def updateWeights(self, player, token):
        if self.learn_dynamics :
            error_signal = 0
            
            summation = 0.0
            for neuron_i in range(len(self.neurons)) :
                summation += self.neurons[neuron_i]
            self.previous_linear_output = summation
            
            if player == self.index :
                error_signal = 1 - self.activationFunction(self.previous_linear_output) # I was hit home = desired output 1
                if self.printout :
                    print "I was hit home - error: " + str(error_signal)
                    
            else :
                if self.previous_move == self.previous_state[player][token]:
                    error_signal = (-1) - self.activationFunction(self.previous_linear_output) # I hit someone else home = desired output -1
                    if self.printout :
                        print "I hit someone home - error: " + str(error_signal)
            
            if not error_signal == 0 :
                if self.printout :            
                    print "Old weights"
                    print self.weight      
                    print "New weights"
                for synapse_i in range(self.input_neurons):
                    for neuron_i in range(self.output_neurons) :
                        self.weight[neuron_i][synapse_i] += 2*self.learning_rate*error_signal*self.derivativeFunction(self.previous_linear_output)*self.previous_input[synapse_i]
                        if self.printout :
                            print self.weight[neuron_i][synapse_i]
                
                
                
                
                