"""
The implementation of the stacking algorithm for collective classification
Using the cora dataset (www.research.whizbang.com/data) That consists of ML papers classified in 7 categories, represented by 1433 unique words.


"""
from numpy import *
from pylab import *
import sys 
import os
from subprocess import Popen, PIPE
import stackFeatures

DATADIR = 'data/'
citeFile = 'cora/cora.cites'

def stackTrain(K,  contentFile):
    """
    implementation stacking algorithm. Takes in k which is the number of stacks
    """
    fIn = map(lambda k: DATADIR+"train%d.megam"%k, range(K))
    fOut =  map(lambda k: DATADIR+"Y_train%d.megam"%k, range(K))
    err = [0]*K 
    classifiers = map(lambda k: DATADIR+"model%d.megam"%k, range(K)) # name of the classifiers
    for k in range(0,K):
       if k == 0: data = stackFeatures.initFeatures(citeFile, contentFile, fIn[k])
       else: stackFeatures.stackFeatures(data, fIn[k-1],fOut[k-1],fIn[k],k)
       # train
       print "********** train stack %d **********"%k
       trainMegam(fIn[k], classifiers[k])
       
       # test, get \hat Y[k], here don't do stackTest but reuse
       err[k] = predict(classifiers[k], fIn[k], fOut[k])

    return (classifiers,err)
       

def stackTest(fModels, K, testFile):
    """
    Implementation of algorithm 21. Takes in k classifiers( fModel ), and fin are strings (filename), k is the level of stack
    """
    fIn = map(lambda k: DATADIR+"test%d.megam"%k, range(K))
    fOut = map(lambda k: DATADIR+"Y_test%d.megam"%k, range(K))
    data = stackFeatures.initFeatures(citeFile, testFile, fIn[0])
    err = [0]*K 
    for k in range(0,K):
        if k!=0: stackFeatures.stackFeatures(data, fIn[k-1], fOut[k-1], fIn[k], k)        
        # test
        print "********** test @ stack %d **********"%k
        err[k] = predict(fModels[k],fIn[k],fOut[k])
    return fOut, err

def predict(fModel, fin, fout):
    """
    predit using megam
    fModel is the classifiert o use, fIn is the name of the file for the features
    fout is where the predictions (Y) are going to be written to
    """
    print "at predict, fin: " + fin + " fout : " + fout
    cmd="megam -predict %s multiclass %s > %s"%(fModel, fin, fout)
    p = Popen(cmd,stderr=PIPE,shell=True)
    stdout, stderr = p.communicate() # get the error rate from stderr
    err = stderr.split(' ')[7] # looks like '0.123456\n'
    print "error:",err
    err = float(err[0:len(err)-1]) # make it into 0.123456

    return err

       
def trainMegam(fin, fout):
    # call: "megam -fvals multiclass fin > fout"
    os.system("megam -fvals multiclass %s > %s"%(fin, fout))

def main():
    K = 1
    trainF = DATADIR+'train.content'
    testF = DATADIR+'test.content'
    # train
    classifiers, trainErrors = stackTrain(K, trainF)
    # test
    Ys, testErrors = stackTest(classifiers, K, testF)

    print trainErrors
    # plot
    # plot(K, testErrors)
    # figure()
    # plot(K, trainErors, 'r.')
    # hold()
    # plot(K, testErrors, 'b.')
    # title('training error vs test error')

   #cross validate
    crossValidate()
    
def crossValidate:
    files = map(lambda k: "train%d.megam"%k, range(K))
    possibleStacks = [1,2,3,4,5]
    DIR = "crossValidate/"
    #this is 3 folds, data was seperated before hand. this list saves tuples of form: (trainContentFileName, tessContentFileName)
    crossFiles = [('d1R.content', 'd3.content'),  ('d2R.content', 'd1.content'), ('d3R.content', 'd2.content'),]
    bestError = float('inf')
    bestK = -1
    for k in possibleStacks: #for all possible hyperparam
        errs = []
        for i in range(0,3): #try on all crossfold sets
           trainContent = crossFiles[i][0]
           testContent = crossFiles[i][1]
           classifiers, trainErrors = stackTrain(k,trainContent)
           errs.append(stackTest(classifiers, K, testContent))
        avgErr = mean(errs)
        print "avgErr of k=% was %\%" %(k, avgErr)
        if avgErr < bestError
          bestError = avgErr
          bestK = k
           

if __name__ == "__main__":
    main()
