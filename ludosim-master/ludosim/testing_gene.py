# -*- coding: utf-8 -*-
"""
Created on Mon May 26 08:32:41 2014

@author: frederik
"""

import random     

import main_evolution

def mate(gw1, gw2):
    g11, g12 = gw1.get_genes()
    g21, g22 = gw2.get_genes()
    d1 = random.randint(0,20)
    d2 = random.randint(0,85)
    
    print type(g11[0:d1])    
    
    gn1 = main_evolution.GeneticPlayerSH5(0, 'Genetic Warrior 1', [g11[0:d1].tolist() + g21[d1:20].tolist(), g12[0:d2].tolist() + g22[d2:85].tolist()])
    gn2 = main_evolution.GeneticPlayerSH5(0, 'Genetic Warrior 1', [g21[0:d1].tolist() + g11[d1:20].tolist(), g22[0:d2].tolist() + g12[d2:85].tolist()])
    return gn1, gn2


gene1 = [1,1,1,1] + [0]*16

#print len(gene1)
#print gene1

gene2 = [1]*5 + [1]*80


j = main_evolution.GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2])

e, t = j.get_genes()

print e
print t

print j.decideMove([ [47,-2,-2,-2],[-2,-2,-2,-2],[-2,-2,-2,-2],[-2,-2,-2,-2] ], 1, [ 6,6,6,6] )

j.decideMove([ [-2,-2,-2,-2],[-2,-2,-2,-2],[-2,-2,-2,-2],[-2,-2,-2,-2] ], 1, [ 6,6,6,6] )


gene1 = []
for i in range(20):
    gene1.append(random.uniform(-1, 1))            
gene2 = []        
for i in range(85):
    gene2.append(random.uniform(-1, 1)) 

j1 = main_evolution.GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2])


gene1 = []
for i in range(20):
    gene1.append(random.uniform(-1, 1))            
gene2 = []        
for i in range(85):
    gene2.append(random.uniform(-1, 1)) 

j2 = main_evolution.GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2])

j3, j4 = mate(j2, j1)



print j1.decideMove([ [22,32,43,3],[12,2,4,27],[2,2,2,33],[21,2,23,2] ], 5, [ 45,12,41,41] )
print j2.decideMove([ [22,32,43,3],[12,2,4,27],[2,2,2,33],[21,2,23,2] ], 5, [ 45,12,41,41] )
print j3.decideMove([ [22,32,43,3],[12,2,4,27],[2,2,2,33],[21,2,23,2] ], 5, [ 45,12,41,41] )