#!/usr/bin/python

import fileMaker
from numpy import *

def fullKernel(lambda1, lambda2, lambda3, gamma, x1, x2):
    '''
    our kernel function is:
         lambda1 * K_linear(x1,x2)
       + lambda2 * K_quadratic(x1,x2)
       + lambda3 * K_rbf(x1,x2)
    where the linear kernel is just x1*x2, the quadratic
    kernel is (1+x1*x2)^2 and the rbf kernel is
    exp[-gamma * ||x1-x2||^2]

    x1 and x2 are provided as equal-length vectors, 
    just like in P1.
    '''

    ### TODO: YOUR CODE HERE
    util.raiseNotDefined()

def linearKernel(lambda1, lambda2, lambda3, gamma, x1, x2):
    '''
    ignore all the lambdas, etc., and just compute a linear kernel.
    '''

    return dot(x1,x2)

if __name__=="__main__":
    fileMaker.mainKernel(linearKernel)   ### TODO: CHANGE THIS TO fullKernel

    

