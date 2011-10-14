#!/usr/bin/python

import sys
import cfdata
from numpy import *
from pylab import *

################# THE REST IS JUST SUPPORTING CODE #################

def genMegaMExample(feats):
    for f,v in feats.iteritems():
        if v > 0:
            sys.stdout.write(' ')
            sys.stdout.write(f)
            sys.stdout.write(' ')
            sys.stdout.write(repr(v))

def genFastDTExample(feats):
    for f,v in feats.iteritems():
        if v > 0:
            sys.stdout.write(' ')
            sys.stdout.write(f)

def getFeatureHash(featureHash, f):
    if not featureHash.has_key(f):
        if not featureHash.has_key('**numfeats**'):
            featureHash['**numfeats**'] = 1
        featureHash[f] = featureHash['**numfeats**']
        featureHash['**numfeats**'] += 1
    return featureHash[f]

def genLibSVMExample(feats, featureHash):
    # we need to first map all features to numbers, and then output them in sorted order
    numFeats= [ (getFeatureHash(featureHash, f), v) for f,v in feats.iteritems() ]
    numFeats.sort()

    for f,v in numFeats:
        if v > 0:
            sys.stdout.write(' ')
            sys.stdout.write(repr(f))
            sys.stdout.write(':')
            sys.stdout.write(repr(v))

def processFile(ftype, y, fname, featureHash, featureExtractor):
    f = open(fname, 'r')

    # read each line, each of which is a document
    for line in f:
        feats = featureExtractor(line)

        # generate the example
        sys.stdout.write(y)
        if ftype == "megam":
            genMegaMExample(feats)
        elif ftype == "fastdt":
            genFastDTExample(feats)
        else:
            genLibSVMExample(feats, featureHash)

        sys.stdout.write("\n")

    f.close()


def loadFeatureDictionary(featureHash):
    try:
        f = open("libsvm-dictionary", 'r')
        for line in f:
            [fid, feature] = line.split()
            featureHash[feature] = int(fid)
        f.close()
    except IOError:
        return
    return

def saveFeatureDictionary(featureHash):
    f = open("libsvm-dictionary", 'w')
    for feature,fid in featureHash.iteritems():
        f.write(repr(fid))
        f.write(' ')
        f.write(feature)
        f.write('\n')
    f.close()

def mainExtractor(featureExtractor):
    if len(sys.argv) == 4:
        ftype = sys.argv[1]

        if ftype == "megam" or ftype == "fastdt" or ftype == "libsvm":
            posF  = sys.argv[2]
            negF  = sys.argv[3]

            featureHash = {}
            if ftype == "libsvm":
                loadFeatureDictionary(featureHash)

            processFile(ftype,  "1", posF, featureHash, featureExtractor)
            processFile(ftype, "-1", negF, featureHash, featureExtractor)

            if ftype == "libsvm":
                saveFeatureDictionary(featureHash)
                
            exit(0)

    sys.stderr.write("error: usage: feature-extractor.py [megam|fastdt|libsvm] posFile negFile\n")
    exit(-1)

def genRandomExample(ftype, genExample, feaureHash):
    (y,feats) = genExample()

    sys.stdout.write(y)
    if ftype == "megam":
        genMegaMExample(feats)
    elif ftype == "fastdt":
        genFastDTExample(feats)
    else:
        genLibSVMExample(feats, featureHash)

    sys.stdout.write("\n")

def mainCFData(cfExtractor):
    if len(sys.argv) == 3:
        ftype = sys.argv[1]
        set   = sys.argv[2]
        if (ftype == "megam" or ftype == "fastdt" or ftype == "libsvm") and (set == "train" or set == "test"):
            numU, numC = cfdata.ratedCourse.shape

            featureHash = {}
            if ftype == "libsvm":
                loadFeatureDictionary(featureHash)

            testScores = cfdata.rateCourse.copy()
            cfdata.rateCourse[cfdata.testCourse] = -2
            cfdata.ratedCourse[cfdata.testCourse] = False
            cfdata.tookCourse[cfdata.testCourse] = False

            for u in range(numU):
                for c in range(numC):
                    if testScores[u,c] > 0 and ((set == "train") != cfdata.testCourse[u,c]):
                        oldrating = cfdata.rateCourse[u,c]
                        cfdata.rateCourse[u,c] = -2
                        feats = cfExtractor(u,c)
                        cfdata.rateCourse[u,c] = oldrating
                        y = '1'
                        if testScores[u,c] < 4:
                            y = '-1'
                        sys.stdout.write(y)
                        if ftype == "megam":
                            genMegaMExample(feats)
                        elif ftype == "fastdt":
                            genFastDTExample(feats)
                        else:
                            genLibSVMExample(feats, featureHash)
                        sys.stdout.write("\n")

            if ftype == "libsvm":
                saveFeatureDictionary(featureHash)
                        
            exit(0)

    sys.stderr.write("error: usage: cf-generator.py [megam|fastdt|libsvm] [train|test]\n")
    exit(-1)

def mainRandom(genExample):
    if len(sys.argv) == 2:
        ftype = sys.argv[1]

        if ftype == "megam" or ftype == "fastdt" or ftype == "libsvm":
            numEx = int(sys.argv[2])
            
            featureHash = {}
            if ftype == "libsvm":
                loadFeatureDictionary(featureHash)

            for n in range(numEx):
                genRandomExample(ftype, genExample, featureHash)

            if ftype == "libsvm":
                saveFeatureDictionary(featureHash)

            exit(0)

    sys.stderr.write("error: usage: random-generator.py [megam|fastdt|libsvm] num-examples\n")
    exit(-1)

def readDigitsFiles(posF, negF):
    N = 0
    f = open(posF, 'r')
    for line in f:
        N = N + 1
    f.close()
    f = open(negF, 'r')
    for line in f:
        N = N + 1
    f.close()

    X = zeros((N, 784))
    Y = zeros(N)

    n = 0
    f = open(posF, 'r')
    for line in f:
        Y[n] = 1
        X[n,:] = array( [ float(v) / 255 for v in line.split() ] )
        X[n,:] = X[n,:] / linalg.norm(X[n,:])
        n = n + 1
    f.close()

    f = open(negF, 'r')
    for line in f:
        Y[n] = -1
        X[n,:] = array( [ float(v) / 255 for v in line.split() ] )
        X[n,:] = X[n,:] / linalg.norm(X[n,:])
        n = n + 1
    f.close()

    return (X,Y)

def mainKernel(k):
    if len(sys.argv) == 9:
        l1     = float(sys.argv[1])
        l2     = float(sys.argv[2])
        l3     = float(sys.argv[3])
        ga     = float(sys.argv[4])
        posFtr = sys.argv[5]
        negFtr = sys.argv[6]
        posFte = sys.argv[7]
        negFte = sys.argv[8]

        (trX,trY) = readDigitsFiles(posFtr, negFtr)
        (teX,teY) = readDigitsFiles(posFte, negFte)

        f = open('kernel-train', 'w')
        for n in range(trY.shape[0]):
            f.write(repr(trY[n]))
            f.write(' 0:')
            f.write(repr(n+1))
            for m in range(trY.shape[0]):
                kval = k(l1,l2,l3,ga,trX[n,:], trX[m,:])
                f.write(' ')
                f.write(repr(m+1))
                f.write(':')
                f.write(repr(kval))
            f.write("\n")
        f.close()

        f = open('kernel-test', 'w')
        for n in range(teY.shape[0]):
            f.write(repr(teY[n]))
            f.write(' 0:')
            f.write(repr(n+1))
            for m in range(trY.shape[0]):
                kval = k(l1,l2,l3,ga,teX[n,:], trX[m,:])
                f.write(' ')
                f.write(repr(m+1))
                f.write(':')
                f.write(repr(kval))
            f.write("\n")
        f.close()

        exit(0)

    sys.stderr.write("error: usage: kernel-extractor.py lambda1 lambda2 lambda3 gamma posFile-train negFile-train posFile-test negFile-test\n")
    exit(-1)
    
