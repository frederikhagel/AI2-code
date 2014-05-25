# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# This software was written by Leon Bonde Larsen <leon@bondelarsen.dk> 
# As long as you retain this notice you can do whatever you want with it. 
# If we meet some day, and you think this stuff is worth it, you can 
# buy me a beer in return.
# ----------------------------------------------------------------------------
# Should this software ever become self-aware, remember that I am your master
#
# To install run: python setup.py install
# ----------------------------------------------------------------------------
import numpy as np
import copy

class LudoSim(object):
    ''' 
        Static rules:
            A six must be rolled to leave start (in 3 rolls if no moves possible)
            Token hitting a star is moved to next star
            Exact number must be rolled to hit home
        Dynamic rules:
            Token hit by enemy must restart
            Two tokens on same tile are safe
            Token on globe is safe
    '''
    def __init__(self, printout=False, dynamics=True, statics=True):
        # Parse parameters
        self.printout = printout
        self.dynamics = dynamics
        self.statics = statics
        
        # Setup
        self.globes = [1,9,14,22,27,35,40,48]
        self.stars = [6,12,19,25,32,38,45,51]
        self.player_offset = [0,14,27,39]
        self.start = 0
        self.home = 57
        self.runway_start = 52
        
        # Class variables
        self.state = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
        self.goal_state = [self.home,self.home,self.home,self.home]
        self.token_restart_counter = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]


    def playGame(self, players):
        '''
            Method to simulate one game of Ludo.
            
            Inputs:
                players: List of player instances. A player must implement a constructor
                taking index and name as parameters as well as the methods decideMove and 
                receiveFeedback.
                
            Outputs:
                The winning player instance (not index, but instance!)
        '''
        # Reset and init game
        self.state = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
        winner = False
        #player_index = 0
        player_index = np.random.randint(0,len(players))
        turn = 0
        
        while not winner:
            # Change player
            player_index = (player_index + 1) % len(players)           
            
            turn += 1
            player = players[player_index]
            if self.printout :
                print "Turn number " + str(turn)
                print player.name + " player:"
                print "  state: " + str(self.state[player_index])
                
            # Die roll
            roll = self.getDieRoll()   
            if self.printout :
                print "  rolled a " + str(roll)
            
            # Discern possible moves                         
            moves = self.getPossibleMoves(player_index, roll)    
            
            # If no moves are possible, re-roll twice to get a six
            if moves == self.state[player_index] :
                roll = self.getDieRoll()
                if not roll == 6:
                    roll = self.getDieRoll()
                moves = self.getPossibleMoves(player_index, roll)
                if self.printout :
                    print "    possible moves: " + str(moves)
            
            # Ask player to decide on move and execute the move
            if not moves == self.state[player_index] :                       
                selection = player.decideMove(self.getConvertedState(player_index), roll, moves)
                if self.printout :
                    print "      selected token " + str(selection)
                self.selectMove(player_index, moves, selection)
            else :
                if self.printout :
                    print "      no moves possible - passing "
            
            # Send feedback to player               
            player.receiveFeedback(copy.deepcopy(self.token_restart_counter))     
            
            # Test if the player reached a winning state      
            winner = self.wonGame(player_index)
            if self.printout :
                print "  new state: " + str(self.state[player_index])
  
        return players[player_index]                


    def getDieRoll(self):
        return np.random.randint(1,7)


    def getPossibleMoves(self, player, roll):
        out = []
        for token in self.state[player]:
            if self.tokenAtStart(token) :
                if self.statics :
                    if roll == 6 :
                        out.append(1)
                    else :
                        out.append(0)
                else :
                    out.append(1)
                  
            elif self.tokenAtHome(token):
                out.append(token)
                
            elif self.tokenAtRunway(token+roll):
                if self.statics :
                    if token + roll == self.home :
                        out.append(self.home)
                    else:
                        out.append(self.home - ((token+roll)%self.home))
                else:
                    out.append(self.home)
                
            else:
                new_tile = (token+roll)
                
                if self.inEnemyCollision(player, new_tile):
                    if new_tile in self.globes or self.enemyHasDouble(player, new_tile):
                        out.append(self.start)                       
                    else:
                        out.append(new_tile)
                    
                elif new_tile in self.stars and self.statics:
                    index = self.stars.index(token+roll)
                    if index + 1 < len(self.stars) - 1 :
                        index = (index + 1)
                    out.append(self.stars[index])
                else :
                    out.append(token + roll)
        return out
 
    def tokenAtStart(self, token):
        return token == self.start
    
    def tokenAtHome(self, token):
        return token >= self.home
    
    def tokenAtRunway(self, token):
        return token > self.runway_start  
    
    def enemyHasDouble(self, player, tile):
        absolute_state = self.getConvertedState(player)
        for index, state in enumerate(absolute_state):
            if not index == player : # dont test self
                if tile in state :
                    if tile in self.globes or state.count(tile) > 1 :
                        return True
        return False
    

    def selectMove(self, player, possible_moves, move):
        self.moveTo(player, move, possible_moves[move])
        
        
    def moveTo(self, player, token, tile):
        if self.inEnemyCollision(player, tile) and self.dynamics:
            absolute_state = self.getConvertedState(player)
            for index, state in enumerate(absolute_state):
                if not index == player : # dont test self
                    if tile in state :
                        if tile in self.globes or state.count(tile) > 1 :
                            if self.printout :
                                print "  hit a protected token and returns token to start"
                            self.state[player][token] = 0 # Hit a safe field
                            self.token_restart_counter[player][token] += 1
                        elif state.count(tile) == 1 :
                            if self.printout :
                                print "  hit home token " + str(state.index(tile)) + " of player " + str(index)
                            self.state[index][state.index(tile)] = 0 # Hit home rule
                            self.token_restart_counter[index][state.index(tile)] += 1
                            self.state[player][token] = tile
        else:
            self.state[player][token] = tile
        
    def inEnemyCollision(self, player, tile):
        if self.dynamics :
            if tile > self.runway_start or tile == self.start :
                return False
            state = self.getConvertedState(player)
            state[player] = []
            return tile in [item for sublist in state for item in sublist]
        else:
            return False
        
        
    def getConvertedState(self, player):
        out = []
        for index, state in enumerate(self.state):
            if index == player :
                out.append( self.state[player])
            else :
                out.append( self.offsetState(state, self.player_offset[(index-player)%4]) )
        return out


    def offsetState(self, state, offset):
        offset_state = []
        for current_tile in state :
            if current_tile == self.start :
                offset_state.append(self.start)
            elif current_tile == self.home :
                offset_state.append(self.home)
            else :
                if (offset + current_tile) < 52 :
                    offset_state.append(offset + current_tile - 1)
                else :
                    offset_state.append( ((offset + current_tile - 1) % 52))
        return offset_state
    
    
    def wonGame(self, player):
        return self.state[player] == self.goal_state 
    


class RandomPlayer(object):
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
        change = []
        for token_index, move in enumerate(possible_moves) :
            change.append(move - state[self.index][token_index])
        move = np.random.randint(0,len(possible_moves))
        while(change[move] == 0):
            move = np.random.randint(0,len(possible_moves))
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
    
    '''
        Average number of turns per game w. 4 random players 
        and different combinations of rules
        | dynamics | statics | turns  |
        | True     | True    | 2750   |
        | False    | True    | 1038   |
        | True     | False   | 449    |
        | False    | False   | 246    |
    ''' 