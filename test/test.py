'''
Created on 05.06.2012

@author: berlioz
'''
import utils
import networkx as nx
import numpy as np
import random as rnd
import time

def RGG(n, beta, mean_degree):
    G = nx.empty_graph(n)
    powerLawArray = utils.powerLawArray(n, beta, mean_degree)
    powerLawDegreeArray = np.array(powerLawArray, dtype = np.longlong)
    sumOfDegrees = powerLawDegreeArray.sum()
    delimiterArray = np.cumsum(powerLawDegreeArray)
    delimiterArray = np.insert(delimiterArray, 0, 0)
    delimiterArray = np.delete(delimiterArray, n)
    someCounter = 0
    while someCounter < sumOfDegrees/2:
        G.add_edge(np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)),
               np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)))
        someCounter += 1
    txtname = "test/adj-%s-%s-%s-.txt" % (str(n), str(beta), str(mean_degree))
    nx.write_adjlist(G, txtname)
    
f = open('test.txt', 'r+')
#f.write('a')

def output(i):
    for k in range(10000, i, 10000):
        t0 = time.time()
        RGG(k, 1.7, 100)
        t1 = time.time() - t0
        print str(i) + " " + t1

output(30000)