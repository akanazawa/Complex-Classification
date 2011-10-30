"""
The implementation of the stacking algorithm for collective classification
Using the cora dataset (www.research.whizbang.com/data) That consists of ML papers classified in 7 categories, represented by 1433 unique words.


"""
from numpy import *
from pylab import *
import sys 
import os
from subprocess import Popen, PIPE
import stackFeatures, pdb
import time


citeFile = 'cora/cora.cites'

def stackTrain(K,  contentFile, DIR):
    """
    implementation stacking algorithm. Takes in k which is the number of stacks
    """
    fIn = map(lambda k: DIR+"train%d.megam"%k, range(K))
    fOut =  map(lambda k: DIR+"Y_train%d.megam"%k, range(K))
    err = [0]*K 
    classifiers = map(lambda k: DIR+"model%d.megam"%k, range(K)) # name of the classifiers
    for k in range(0,K):
       if k == 0: data = stackFeatures.initFeatures(citeFile, contentFile, fIn[k])
       else: stackFeatures.stackFeatures(data, fIn[k-1],fOut[k-1],fIn[k],k)
       # train
       print "********** train stack %d **********"%k
       trainMegam(fIn[k], classifiers[k])
       
       # test, get \hat Y[k], here don't do stackTest but reuse
       err[k] = predict(classifiers[k], fIn[k], fOut[k])

    return (classifiers,err)
       

def stackTest(fModels, K, testFile, DIR):
    """
    Implementation of algorithm 21. Takes in k classifiers( fModel ), and fin are strings (filename), k is the level of stack
    """
    fIn = map(lambda k:DIR+"test%d.megam"%k, range(K))
    fOut = map(lambda k: DIR+"Y_test%d.megam"%k, range(K))
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
    print stderr
    err = stderr.split(' ')[7] # looks like '0.123456\n'
    print "error:",err
    err = float(err[0:len(err)-1]) # make it into 0.123456

    return err

       
def trainMegam(fin, fout):
    # call: "megam -fvals multiclass fin > fout"
    # if not os.path.exists(fout):
    os.system("megam -fvals multiclass %s > %s"%(fin, fout))  
        
        
def main():
    # DATADIR = 'data/'
    # K = 6
    # trainF = 'crossValidate/d2R.content'#DATADIR+'train.content'
    # testF = 'crossValidate/d2.content'#DATADIR+'test.content'
    # # train
    # classifiers, trainErrors = stackTrain(K, trainF, DATADIR)
    # # test
    # Ys, testErrors = stackTest(classifiers, K, testF, DATADIR)

    # print "training errors: " + repr(trainErrors)
    # print "test errors: " + repr(testErrors) 
    # pdb.set_trace()
    # plot(range(1,K+1), trainErrors, 'r*-')
    # hold(True)
    # plot(range(1,K+1), testErrors, 'b*-')
    # title('training error vs test error')
    # ylabel('error')
    # xlabel('K, number of layers')
    # legend(('training error', 'test error'))
    # show()
#   cross validate
    print "**********start cross validation ****"
    tic = time.clock()
    blah =  crossValidate()
    toc = time.clock()
    print " took " + repr(toc-tic)
    return blah

def crossValidate():
    possibleStacks = [1,2,3,4,5,6,7]
    DIR = "crossValidate/"
    #this is 3 folds, data was seperated before hand. this list saves tuples of form: (trainContentFileName, tessContentFileName)
    crossFiles = [(DIR+'d1R.content', DIR+'d1.content'),  (DIR+'d2R.content', DIR+'d2.content'), (DIR+'d3R.content', DIR+'d3.content')]
    bestErrorAndK = (float('inf'), -1)
    allTestErr = []
    allTrainErr = []
    for k in possibleStacks: #for all possible hyperparam
        errs = []
        trainErrs = []
        for i in range(0,3): #try on all crossfold sets
           trainContent = crossFiles[i][0]
           testContent = crossFiles[i][1]
           classifiers, trainErrors = stackTrain(k,trainContent, DIR)
           foo, err = stackTest(classifiers, k, testContent, DIR)
           errs.append(err)
           trainErrs.append(trainErrors)
        # pdb.set_trace()
        avgErr = mean(errs)
        allTestErr.append(avgErr)
        allTrainErr.append(mean(trainErrs))
        print "avgErr of k=%d on holdout %d was %f" %(k, i, avgErr)
        if avgErr < bestErrorAndK[0]:
          bestErrorAndK = (avgErr,k) #update if better
           
    print "bestError was %f with K %d"% bestErrorAndK

    plot(possibleStacks, allTestErr, 'r*-')
    hold(True)
    plot(possibleStacks, allTrainErr, 'b*-')
    title('training error vs test error')
    show()

    return bestErrorAndK
if __name__ == "__main__":
    main()
