# -*- coding: utf-8 -*-
"""
Created on Mon May 26 10:09:21 2014

@author: frederik
"""


import random     
from main_evolution import GeneticPlayerSH5

import os
import subprocess
import sys

os.environ['LD_LIBRARY_PATH'] = "my_path"
subprocess.check_call(['sqsub', '-np', sys.argv[1], '/path/to/executable'],
                      env=os.environ)

export LD_LIBRARY_PATH=/home/frederik/installed_packages/arac:$LD_LIBRARY_PATH

#import arac
#
#from arac.pybrainbridge import _FeedForwardNetwork, _RecurrentNetwork

def mate(gw1, gw2):
    g11, g12 = gw1.get_genes()
    g21, g22 = gw2.get_genes()
    d1 = random.randint(0,20)
    d2 = random.randint(0,85)
    
    print type(g11[0:d1])    
    
    gn1 = GeneticPlayerSH5(0, 'Genetic Warrior 1', [g11[0:d1].tolist() + g21[d1:20].tolist(), g12[0:d2].tolist() + g22[d2:85].tolist()])
    gn2 = GeneticPlayerSH5(0, 'Genetic Warrior 1', [g21[0:d1].tolist() + g11[d1:20].tolist(), g22[0:d2].tolist() + g12[d2:85].tolist()])
    return gn1, gn2
    
def mutate(gene):
    g1, g2 = gene.get_genes()
    ng1 = []  
    ng2 = []
    for g in g1:
        if random.randint(0,50) == 0:
            ng1.append( random.uniform(-1, 1) )
        else  :
            ng1.append( g )
    for g in g2:
        if random.randint(0,50) == 0:
            ng2.append( random.uniform(-1, 1) )
        else  :
            ng2.append( g )

    gn2 = GeneticPlayerSH5(0, 'Genetic Warrior 1', [ng1, ng2])
    return gn2        
    
    
gene_scores = [45, 42, 48, 50, 37, 36, 40, 36, 50, 44, 39, 49, 42, 37, 36, 46, 44, 33, 26, 44, 45, 42, 39, 30, 40, 35, 47, 40, 48, 31, 44, 42, 39, 36, 22, 42, 49, 37, 34, 43, 40, 47, 41, 44, 44, 38, 35, 41, 35, 32]

sort_index = sorted(range(len(gene_scores)), key=lambda k: gene_scores[k])    

print sort_index

import pickle

gn1 = GeneticPlayerSH5(0, 'Genetic Warrior 1', [[0]*20, [0]*85 ])
    

with open('gene_list.dat', 'rb') as f:
    gene_list = pickle.load(f)

children =  []
   
for winner in sort_index[30:]:
    c1, c2 = mate(gene_list[winner], gene_list[random.randint(30,49)]) 
    c1 = mutate(c1)
    c2 = mutate(c2)
    children.append(c1)
    children.append(c2)
       
for i in range(10):
    gene1 = []
    for i in range(20):
        gene1.append(random.uniform(-1, 1))            
    gene2 = []        
    for i in range(85):
        gene2.append(random.uniform(-1, 1))
    gene_to_optimize = GeneticPlayerSH5(0, 'Genetic Warrior 1', [gene1, gene2] )       
#    gene_to_optimize.convertToFastNetwork()   
    children.append( gene_to_optimize )

with open('mated_gene_list.dat', 'wb') as f:
    pickle.dump(children, f)