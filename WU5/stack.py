"""
The implementation of the stacking algorithm for collective classification
Using the cora dataset (www.research.whizbang.com/data) That consists of ML papers classified in 7 categories, represented by 1433 unique words.


"""

from numpy import *
import sys 
import util
import os

def stack(K):
    """
    driver of the stacking algorithm. Takes in k which is the number of stacks
    """
    # first do the initial classifier f_0
    # get the location of text file with features to feed to megam
    fIn = ['']*K # make K empty list
    fOut = ['']*K # make K empty list
    classifiers = map(lambda k: "model%d.megam"%k, range(K)) # name of the classifiers
    for k in range(0,K):
       if k == 0:
           fIn[k] = initFeatures()
       else:
           fIn[k] = stackFeatures(fIn[k-1],fOut[k-1])
       # train
       trainMegam(fin, classifiers[k])
       
       # test, get \hat Y[k]
       fOut[k] = stackTest(classifiers[k], fIn[k-1], k);

    return classifiers
       
def initFeatures():
    return "train.megam"

def stackTest(fModel, fin, k):
    """
    Implementation of algorithm 21. Takes in up to k classifiers
    unlike the pseudocode in the text, this function accepts fIn[k-1], 
    which has all of the k-1th prediction stacked on as a feature..    
    fModel and fin are strings (filename), k is the level of stack
    """
    fout = "Y%d.megam"%k
    os.system("megam -predict %s multiclass %s > %s", (fModel%k, fin, fout))
    return fout
       
       
def trainMegam(fin, fout):
    # call: "megam -fvals multiclass fin > fout"
    os.system("megam -fvals multiclass %s > %s", (fin, fout))

def main():
    stack(1)

if __name__ == "__main__":
    main()
