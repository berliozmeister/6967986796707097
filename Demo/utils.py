'''
Created on 24.05.2012

@author: berlioz

some auxilary functions and classes to be defined here
'''
import math
import networkx.utils as nu
import networkx as nx
import numpy as np

#def is_valid_degree_sequence(sequence):
    

def powerLawArray(n, beta, mean_degree):
    powerLawSequence = nu.powerlaw_sequence(n, beta)
    powerLawArr = np.array(powerLawSequence)
    initialSum = np.sum(powerLawArr)
    expectedSum = mean_degree * n
    for i in xrange(n):
        powerLawArr[i] = powerLawArr[i] * 1.0 * expectedSum / initialSum
    return powerLawArr

def parsum(s):
    count = 0
    yield 0
    for i in s:
        count += i
        yield count

def partSum(arr):
    count = 0
    yield 0
    for i in range(arr.size - 1):
        count += arr[i]
        yield count

def partialSum(arr):
    tmpArray = np.cumsum(arr)
    yield tmpArray
        


