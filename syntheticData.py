#!/usr/bin/python

import sys
import fileMaker
import pylab

def genForDT():
    ### TODO: YOUR CODE HERE
    util.raiseNotDefined()
    return 0

def genForLR():
    ### TODO: YOUR CODE HERE
    util.raiseNotDefined()
    return 0

def genExampleAxisAligned():
    # first choose a label
    y = ''
    feats = {}
    if pylab.rand() < 0.5:   # negative example
        # from Nor([-1,0], 1)
        y = '-1'
        feats['x'] = pylab.randn() - 1
        feats['y'] = pylab.randn()
    else:
        # from Nor([+1,0], 1)
        y = '1'
        feats['x'] = pylab.randn() + 1
        feats['y'] = pylab.randn()
    return (y, feats)


if __name__=="__main__":
    fileMaker.mainRandom(genExampleAxisAligned)     ### TODO: CHANGE THIS TO genForDT or genForLR
