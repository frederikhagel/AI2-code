# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:41:56 2014

@author: dimx
"""

from NNPlayer import NNPlayer
from matplotlib import pyplot as plt
import random
import ludosim
import Combined

def plotResult(title, players, vector, xlabel, ylabel):
    plt.figure(title)
    plt.plot(range(len(vector)),vector)
    plt.legend(['{}'.format(player.name) for player in players],loc=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return plt

def competeVsLeonl(train_run, competition_runs):
    winner_vect = []
    
    player0 = NNPlayer(2, "100 gens small network 1")
    player0.loadWeights("1401127755_100.pkl")

    player1 = NNPlayer(3, "1000 gens large network 2")
    player1.loadWeights("1401234786.57.pkl")

#    player2 = NNPlayer(2, "200 gens small network")
#    player2.loadWeights("1401126700_200.pkl")
#    
#    player3 = NNPlayer(3, "100 gens small network")
#    player3.loadWeights("1401127755_100.pkl")
    
    concurrently_trained1 = Combined.Player(0, 'Concurrently trained1', learning_rate=0.6, random_start_guess=False, optimal_policy=True)
    concurrently_trained2 = Combined.Player(1, 'Concurrently trained2', learning_rate=0.6, random_start_guess=False, optimal_policy=True)

    players = [ concurrently_trained1,
                    concurrently_trained2,
                    ludosim.RandomPlayer(2, 'Random'),
                    ludosim.RandomPlayer(3, 'Random')
                    ]
                    
    for i in range(train_run) :
        sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
        winner = sim.playGame(players).index
        print "Training ", i

    players = [concurrently_trained1,concurrently_trained2,player0,player1]

#    sequentially_trained1.learn_dynamics = False
#    sequentially_trained2.learn_dynamics = False
#    sequentially_trained1.learn_statics = False
#    sequentially_trained2.learn_statics = False
    
    wins = [0]*4

    sim = ludosim.LudoSim(printout=False, statics=True, dynamics=True)
    for i in range(competition_runs):
        winner = sim.playGame(players)
        wins[winner.index] += 1
        winner_vect.append(wins[:])     
        print "Winner round %i: %s " % (i, winner.name)
    
    for i in range(4):
        print "Player %i total wins: %i" % (i, wins[i])
        
    plotResult("Game wins against AI with %i runs " % train_run, players, winner_vect, "Game #", "Acc. Wins").show()

if __name__ == '__main__':
    competeVsLeonl(100, 1000)
    
    
"""
Player 0 and 1: 1000 gens large network
Player 2 and 3: Concurrently trained
Player 0 total wins: 593
Player 1 total wins: 382
Player 2 total wins: 12
Player 3 total wins: 13



Player 0 total wins: 9          Concurrently trained1
Player 1 total wins: 15         Concurrently trained2
Player 2 total wins: 363        200 gens small network 1
Player 3 total wins: 613        1000 gens large network 2


Player 0 total wins: 6         Concurrently trained1
Player 1 total wins: 13        Concurrently trained2
Player 2 total wins: 328       100 gens small network 1
Player 3 total wins: 653       1000 gens large network 2

"""    