import sys 
import os
from subprocess import Popen, PIPE
from numpy import *
import pdb
from math import log

GRAPHICS = 'train.comp.graphics.txt'
WINDOWS = 'train.comp.windows.x.txt'
BASEBALL = 'train.rec.sport.baseball.txt'
HOCKEY = 'train.rec.sport.hockey.txt'

GRAPHICS_TEST = 'test.comp.graphics.txt'
WINDOWS_TEST = 'test.comp.windows.x.txt'
BASEBALL_TEST = 'test.rec.sport.baseball.txt'
HOCKEY_TEST = 'test.rec.sport.hockey.txt'

def main():
	bestFirst = (float("-inf"), -100)
	bestSecond = (float("-inf"), -100)
	scoreFirst = []
	scoreSecond = []
	for i in range(-5, 6): # try many lambda, see which one's the best
		lambda_value = 2**i
		print "\n**********first tree using lambda 2^%f**********"%log(lambda_value, 2)
		classifiers = trainFirstTree(lambda_value)
		firstResult = testFirstTree(classifiers[0], classifiers[1], classifiers[2])
		scoreFirst.append(firstResult)
		print "\n********** second tree using lambda 2^%f **********"%log(lambda_value, 2)
		classifiersTwo = trainSecondTree(lambda_value)
		secondResult = testSecondTree(classifiersTwo[0], classifiersTwo[1], classifiersTwo[2])
		scoreSecond.append(secondResult)
		print "first tree: %f, second tree: %f with lambda 2^%f"%(firstResult, secondResult, log(lambda_value, 2))
		if bestFirst[0] < firstResult:
			bestFirst = (firstResult, log(lambda_value, 2))
		if bestSecond[0] < secondResult:
			bestSecond = (secondResult, log(lambda_value, 2))
	
	print "best score for first: %f with lambda 2^%f"%bestFirst
	print "best score for second: %f with lambda 2^%f"%bestSecond
	print scoreFirst
	print scoreSecond
	return (firstResult, secondResult)


def trainFirstTree(lambda_value):
	"""
	Root splits does {graphics,windows} versus {baseball,hockey}. For this data, we only need 3 classifiers, f0, the root, f01, the left leaf, and f10 the right leaf.
	"""	
	# f0: the classifier for root. does {graphics,windows} versus {baseball,hockey}.
	f0 = "tree0_model.megam"
	# generate data so that grachics, windows get +1 and rest get -1
	f0_train = "tree0_train.megam"
	
	if not os.path.exists(f0_train):
		print "make training data for root.."
		# has to be in the order Graphics, Windows, Baseball, Hockey (because ground truth is in that order)
		generateBinaryData(GRAPHICS, WINDOWS, "tmp1")
		generateBinaryData(BASEBALL, HOCKEY, "tmp2")
		makeAllLabel("tmp1", f0_train, "1") #make graphics windows all +1
		makeAllLabel("tmp2", "tmp22", "-1") #make windows-hockey all -1
		appendTwoFiles("tmp22", f0_train) #append baseball-hockey to graphics-windows
	print "train root classifier.."
	trainMegam(f0_train,f0, lambda_value)
	
	# f01: the left child classifier of root. does {graphics}vs{windows}
	fLeft = "treeLeft_model.megam" 
	fLeftTrain = "treeLeft_train.megam"
	if not os.path.exists(fLeftTrain):
		print "make training data for left.."
		generateBinaryData(GRAPHICS, WINDOWS, fLeftTrain)
	print "train left classifier.."
	trainMegam(fLeftTrain,fLeft, lambda_value)
	
	# f02: the right child classifier of root. does {baseball}vs{hockey}
	fRight = "treeRight_model.megam" 
	fRightTrain = "treeRight_train.megam"
	if not os.path.exists(fRightTrain):
		print "make training data for right.."
		generateBinaryData(BASEBALL, HOCKEY, fRightTrain)
	print "train right classifier.."
	trainMegam(fRightTrain,fRight, lambda_value)
	return (f0,fLeft,fRight)

def trainSecondTree(lambda_value):
	"""
	Root splits does {graphics,baseball} versus {windows,hockey}. 
	"""	
	# f0: the classifier for root. does {graphics, baseball} versus {windows,hockey}.
	f0 = "treeTwo_0_model.megam"
	# generate data so that grachics, windows get +1 and rest get -1
	f0_train = "treeTwo_0_train.megam"

	if not os.path.exists(f0_train):
		print "make training data for root.."
		generateBinaryData(GRAPHICS, WINDOWS, f0_train) #graphics +1, windows -1
		appendBinaryData(BASEBALL, HOCKEY, f0_train) # baseball +1, hockey -1
	print "train root classifier.."
	trainMegam(f0_train,f0, lambda_value)
		
	# f01: the left child classifier of root. does {graphics}vs{baseball}
	fLeft = "treeTwo_Left_model.megam" 
	fLeftTrain = "treeTwo_Left_train.megam"
	if not os.path.exists(fLeftTrain):
		print "make training data for left.."
		generateBinaryData(GRAPHICS, BASEBALL, fLeftTrain)
	print "train left classifier.."
	trainMegam(fLeftTrain,fLeft, lambda_value)

	# f02: the right child classifier of root. does {windows}vs{hockey}
	fRight = "treeTwo_Right_model.megam" 
	fRightTrain = "treeTwo_Right_train.megam"
	if not os.path.exists(fRightTrain):
		print "make training data for right.."
		generateBinaryData(WINDOWS, HOCKEY, fRightTrain)

	print "train right classifier.."
	trainMegam(fRightTrain,fRight, lambda_value)
	return (f0,fLeft,fRight)

def testFirstTree(f0,fLeft,fRight):
	#so now we have f0, fRight, and fLeft
	testFile0 = "tree0_test.megam"
	# generate test data so that grachics, windows get +1 and rest get -1
	if not os.path.exists(testFile0):
		print "make test data for root.."
		generateBinaryData(GRAPHICS_TEST, WINDOWS_TEST, "tmp1")
		generateBinaryData(BASEBALL_TEST, HOCKEY_TEST, "tmp2")
		makeAllLabel("tmp1", testFile0, "1") #make graphics windows all +1
		makeAllLabel("tmp2", "tmp3", "-1") #make windows-hockey all -1
		appendTwoFiles("tmp3", testFile0) #append baseball-hockey to graphics-windows
	
	f0out = "treef0_Y.megam"
	print "---------- test at root ----------"
	testMegam(f0,testFile0,f0out) # test it, output is written to f0out
	Y = getLabels(f0out)
	testFileLeft = "treeLeft_test.megam"
	testFileRight = "treeRight_test.megam"
	wrongAlready = makeTestCases(Y,testFile0, testFileLeft, testFileRight, 1,2,3,4)
	print "---------- test at left ----------"
	testLeftOut = "treeLeft_Y.megam"
	testRightOut = "treeRight_Y.megam"
	numLeftWrong = testMegam(fLeft,testFileLeft,testLeftOut) # test it, get output
	print "---------- test at right ----------"
	numRightWrong = testMegam(fRight,testFileRight,testRightOut) # test it, get output
	totalerr = (numLeftWrong+numRightWrong+wrongAlready)/len(Y)
	accuracy = 1-totalerr
	print "total error %f/%d = %f, accuracy %f"%((numRightWrong+numLeftWrong+wrongAlready), len(Y), totalerr,accuracy*100)
	return accuracy

def testSecondTree(f0,fLeft,fRight):
	#so now we have f0, f01, and f10
	testFile0 = "treeTwo_0_test.megam"
	# generate test data so that grachics, windows get +1 and rest get -1
	if not os.path.exists(testFile0):
		print "make test data for root.."
		generateBinaryData(GRAPHICS_TEST, WINDOWS_TEST, testFile0)
		appendBinaryData(BASEBALL_TEST, HOCKEY_TEST, testFile0)

	f0out = "treeTwo_f0_Y.megam"
	print "---------- test at root ----------"
	testMegam(f0,testFile0,f0out) # test it, output is written to f0out
	Y = getLabels(f0out)
	testFileLeft = "treeTwo_Left_test.megam"
	testFileRight = "treeTwo_Right_test.megam"
	wrongAlready = makeTestCases(Y,testFile0, testFileLeft, testFileRight, 1,3,2,4)
	print "---------- test at left ----------"
	testLeftOut = "treeTwo_Left_Y.megam"
	testRightOut = "treeTwo_Right_Y.megam"
	numLeftWrong = testMegam(fLeft,testFileLeft,testLeftOut) # test it, get output
	numRightWrong = testMegam(fRight,testFileRight,testRightOut) # test it, get output
	totalerr = (numLeftWrong+numRightWrong+wrongAlready)/len(Y)
	accuracy = 1-totalerr
	print "total error %f/%d = %f, accuracy %f"%((numRightWrong+numLeftWrong+wrongAlready), len(Y), totalerr,accuracy*100)
	return accuracy
	

def makeTestCases(Y,testFile0, testFileLeft, testFileRight, leftPositiveClass, leftNegativeClass,rightPositiveClass,rightNegativeClass):
	"""
	Makes test cases for left and right tree to test, (re-writes appropriate labels)
	if a class goes into a wrong leaf, say if document of hockey goes into leaf that test between graphics and windows, don't use it as a test but just count it as wrong. 
	Returns the total number of mis-classified example at this level
	"""
	print "making test cases for left and right leaves.."
	f0test = open(testFile0, "r")
	fLeft = open(testFileLeft, "w")
	fRight = open(testFileRight, "w")	
	# for all files marked as +1 in f0out, write the corresponding data to testFileLeft, -1 goes to testFile01
	trueLabel = getTrueLabel() #truelabel, (1,2,3,or,4) of this data
	print "make test data for left and right tree"
	ind = 0
	numleft=0
	numright=0
	numWrongLeft = 0
	numWrongRight = 0
	for line in f0test:
		line = line.strip()
		line = line.split()		
		# print "Y:%d, trueLabel:%d"%(Y[ind], trueLabel[ind])
                if Y[ind] == 1: # write to left			
			if (trueLabel[ind] == leftNegativeClass): # if windows, set the label to -1
				line[0] = '-1'
			# wrong alraedy. can't classify because these shouldn't be in this leaf
			if (trueLabel[ind] != leftNegativeClass and trueLabel[ind] != leftPositiveClass): 
				numWrongLeft+=1
			#append to left test file
			else: 
				fLeft.write(" ".join(line)+"\n")
				numleft+=1
		else:
			if (trueLabel[ind] == rightNegativeClass): # if hockey, set the label to -1
				line[0] = '-1'
			elif (trueLabel[ind] == rightPositiveClass):
				line[0] = '1' # from 0 to 1
			# don't add if neither class
			if (trueLabel[ind] != rightNegativeClass and trueLabel[ind] != rightPositiveClass):
				numWrongRight+=1
			else:			#append to right test file
				fRight.write(" ".join(line)+"\n")
				numright+=1
		ind+=1 #increment line..
	numpos = len(where(Y==1)[0].tolist())
	print "num pos in test0 %d, num 0 in test 0 %d"%(numpos, len(Y)-numpos)
	print "num in left %d num in right %d"%(numleft, numright)
	print "num wrong already left:%d right:%d"%(numWrongLeft, numWrongRight)
	fLeft.close()
	fRight.close()
	f0test.close()
	return numWrongRight + numWrongLeft

def generateBinaryData(fdata1, fdata2, fout):
	""" generates data like we did in warmup i.e.
	runs "python wordExtractor.py megam fdata1 fdata2 > fout"
	"""
        os.system("python ../../wordExtractor.py megam %s %s > %s"%(fdata1, fdata2, fout))

def appendBinaryData(fdata1, fdata2, fout):
	""" same as above but does >> instead of >
	runs "python wordExtractor.py megam fdata1 fdata2 >> fout"
	"""
        os.system("python ../../wordExtractor.py megam %s %s >> %s"%(fdata1, fdata2, fout))
	
def getLabels(fname):
	"""
	opens the fname, (predictions from megam) and returns an array of the predictions
	"""
	f = open(fname,"r")
	labels = []
	for line in f:
		# get the first number of each line as predictions
		line = line.strip()
		line = line.split()
		labels.append(int(line[0]))
	return array(labels) # make it in numpy array

def getTrueLabel():
	"""
	the true ground truth, graphics == 1, windows ==2, baseball = 3, hockey ==4
	This returns the list of real labels
	"""
	print "getting true labels.."
	graphicsWindowsTest = "graphics-windows-test.megam"
	baseHockeyTest = "baseball-hockey-test.megam"
	if not os.path.exists(graphicsWindowsTest):	
		generateBinaryData(GRAPHICS_TEST, WINDOWS_TEST, graphicsWindowsTest)
		generateBinaryData( BASEBALL_TEST,HOCKEY_TEST, baseHockeyTest)
	f = open(graphicsWindowsTest,'r')
	Y = []
	for line in f:
		word = line.split()
		label = int(word[0])
		if label == 1:
			Y.append(1)
		else :
			Y.append(2)
			
	f2 = open(baseHockeyTest,'r')
	for line in f2:
		word = line.split()
		label = int(word[0])
		if label == 1:
			Y.append(3)
		else:
			Y.append(4)		
	f.close()
	f2.close()
	return Y

def makeAllLabel(fname, fOutName, label):
	f = open(fname,'r')
	fOut = open(fOutName, 'w')
	Y = []
	for line in f:
		line = line.split()
		line[0] = label
		fOut.write(" ".join(line)+"\n")
	f.close()
	fOut.close()

def appendTwoFiles(new, orig):
	os.system("cat %s  >> %s"%(new,orig))
		
def trainMegam(fin, fout, lambda_value):
    os.system("megam -fvals -tune -lambda %f binary %s > %s"%(lambda_value,fin, fout))  

def testMegam(fModel,ftest,fout):
    cmd = "megam -fvals -predict %s binary %s > %s"%(fModel,ftest, fout)
    p = Popen(cmd,stderr=PIPE,shell=True)
    stdout, stderr = p.communicate() # get the error rate from stderr
    print stderr
    err = float(stderr.split(' ')[3]) # num of incorrect classifications
    print "num error:",err
    return err

if __name__ == "__main__":
    main()
