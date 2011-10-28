"""
The implementation of the stacking algorithm for collective classification
Using the cora dataset (www.research.whizbang.com/data) That consists of ML papers classified in 7 categories, represented by 1433 unique words.


"""

from numpy import *
from pylab import *
import sys 
import os
from subprocess import Popen, PIPE

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
       if k == 0: data = initFeatures(citeFile, contentFile, fIn[k])
       else: stackFeatures(data, fIn[k-1],fOut[k-1],fIn[k],k)
       # train
       print "********** train stack %d **********"%k
       trainMegam(fIn[k], classifiers[k])
       
       # test, get \hat Y[k], here don't do stackTest but reuse
       fOut[k],err[k] = predict(classifiers[k], fIn[k-1], DATADIR+"Y%d.megam"%k)

    return (classifiers,err)
       
def initFeatures(citeFile, contentFile, outputFile):
    """
    returns a tuple
    """
    return outputFile

def stackTest(fModels, testData, K):
    """
    Implementation of algorithm 21. Takes in up to k classifiers
    unlike the pseudocode in the text, this function accepts fIn[k-1], 
    which has all of the k-1th prediction stacked on as a feature..    
    fModel and fin are strings (filename), k is the level of stack
    """
    fIn = ['']*K 
    fOut = ['']*K 
    err = [0]*K 
    for k in range(0,K):
        fIn[k] = testData if k==0 else stackFeatures(fIn[k-1], fOut[k-1])        
        # test
        print "********** test @ stack %d **********"%k
        fOut[k], err[k] = predict(fModels[k],fIn,fOut)
    return fOut, err

def predict(fModel, fin, fout):
    """
    predit using megam
    """
    cmd="megam -predict %s multiclass %s > %s"%(fModel, fin, fout)
    p = Popen(cmd,stderr=PIPE,shell=True)
    stdout, stderr = p.communicate() # get the error rate from stderr
    err = stderr.split(' ')[7] # looks like '0.123456\n'
    err = float(err[0:len(err)-1]) # make it into 0.123456
    print "error:",err
    return (fout,err)

       
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
    testIn = initFeatures(citeFile, testF, DATADIR+'test.megam')
    Ys, testErrors = stackTest(classifiers, testIn, K)

    print trainErrors
    # plot
    # plot(K, testErrors)
    # figure()
    # plot(K, trainErors, 'r.')
    # hold()
    # plot(K, testErrors, 'b.')
    # title('training error vs test error')

    #cross validate
#    crossValidate()
    
# def crossValidate:
#     files = map(lambda k: "train%d.megam"%k, range(K))
#     make3Files('train1.cite', 'train.content', 'test.content', 'test.cite');
#     files = [('data1.cite', 'data1.content'), ('data1.cite', 'data1.content'), ('data1.cite', 'data1.content')]
#     for i in range(0,3):
#         for k in range(1, 5): # num of stack
#         combineFiles(files[1], files[2], fCite, fContent)
#         classifiers, trainErrors =  trainStack(k, fCite, fContent)
#         testIn = initFeatures('test.cite', 'test.content', 'test0.megam')
#         Ys, testErrors = stackTest(classifiers, testIn, K)
        


if __name__ == "__main__":
    main()
