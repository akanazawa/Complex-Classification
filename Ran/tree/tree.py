import sys 
import os
from subprocess import Popen, PIPE
from numpy import *
num_of_classes = 4
lambda_value = 1

def main():
	classifiers = trainFirstTree()
	testFirstTree(classifiers[0], classifiers[1], classifiers[2])
	

def trainFirstTree():
	"""
	Root splits does {graphics,windows} versus {baseball,hockey}. For this data, we only need 3 classifiers, f0, the root, f01, the left leaf, and f10 the right leaf.
	"""	
	# f0: the classifier for root. does {graphics,windows} versus {baseball,hockey}.
	f0 = "tree0_model.megam"
	# generate data so that grachics, windows get +1 and rest get -1
	f0_train = "tree0_train.megam"
	print "make training data for root.."
	generateBinaryData('../../data/train.comp.graphics.txt', '../../data/train.rec.sport.baseball.txt', f0_train)
	appendBinaryData('../../data/train.comp.windows.x.txt', '../../data/train.rec.sport.hockey.txt', f0_train)
	trainMegam(f0_train,f0)
	
	# f01: the left child classifier of root. does {graphics}vs{windows}
	f01 = "tree01_model.megam" 
	# generate the data like we did in warm up
	# python wordExtractor.py megam data/train.comp.graphics.txt data/train.comp.windows.x.txt > tree01_train.megam
	f01train = "tree01_train.megam"
	print "make training data for left.."
	generateBinaryData('../../data/train.comp.graphics.txt', '../../data/train.comp.windows.x.txt', f01train)
	trainMegam(f01train,f01)

	# f02: the right child classifier of root. does {baseball}vs{hockey}
	f10 = "tree10_model.megam" 
	f10train = "tree10_train.megam"
	print "make training data for right.."
	generateBinaryData('../../data/train.rec.sport.baseball.txt', '../../data/train.rec.sport.hockey.txt', f10train)
	trainMegam(f10train,f10)
	return (f0,f01,f10)

def testFirstTree(f0,f01,f10):
	#so now we have f0, f01, and f10
	testFile0 = "tree0_test.megam"
	# generate test data so that grachics, windows get +1 and rest get -1
	generateBinaryData('../../data/test.comp.graphics.txt', '../../data/test.rec.sport.baseball.txt', testFile0)
	appendBinaryData('../../data/test.comp.windows.x.txt', '../../data/test.rec.sport.hockey.txt', testFile0)
	f0out = "treef0_Y.megam"
	testMegam(f0,testFile0,f0out) # test it, get output
	Y = getLabels(f0out)
	testFile10 = "tree10_test.megam"
	testFile01 = "tree01_test.megam"
	makeTestCases(Y,testFile0, testFile10, testFile01, 1,2,3,4)

def makeTestCases(Y,testFile0, testFile10, testFile01, leftPositiveClass, leftNegativeClass,rightPositiveClass,rightNegativeClass):
	"""
	Makes test cases for left and right tree to test, (re-writes appropriate labels)
	"""
	f0test = open(testFile0, "r")
	f10 = open(testFile10, "w")
	f01 = open(testFile01, "w")	
	# for all files marked as +1 in f0out, write the corresponding data to testFile10, -1 goes to testFile01

	trueLabel = getTrueLabel() #truelabel, (1,2,3,or,4) of this data
	print "make test data for left and right tree"
	ind = 0
	for line in f0test:
		line = line.strip()
		line = line.split()
                if Y[ind] > 1: # write to left
			if (trueLabel[ind] == leftNegativeClass): # if windows, set the label to -1
				line[0] = -1
			# set it to class it can't classify because these shouldn't be in this leaf
			elif (trueLabel[ind] != leftNegativeClass or trueLabel[ind] != leftPositiveClass): 
				line[0] = 5
			#append to left test file
			f10.write("\n".join(line))
		else:
			if (trueLabel[ind] == rightNegativeClass): # if hockey, set the label to -1
				line[0] = -1
			elif (trueLabel[ind] == rightNegativeClass or trueLabel[ind] == rightPositiveClass):
				line[0] = 5
			#append to right test file
			f01.write("\n".join(line))
		ind+=1 #increment line..

	f10.close()
	f01.close()
	f0test.close()

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
	f = open("../graphics-windows-test.megam",'r')
	Y = []
	for line in f:
		word = line.split()
		label = int(word[0])
		if label == 1:
			Y.append(1)
		else :
			Y.append(2)
			
			f2 = open("../test.baseball.hockey.megam",'r')
			for line in f2:
				word = line.split()
				label = int(word[0])
				if label == 1:
					Y.append(3)
				else:
					Y.append(4)		
	return Y

def trainMegam(fin, fout):
     if not os.path.exists(fout):
	     os.system("megam -fvals -tune -lambda %f binary %s > %s"%(lambda_value,fin, fout))  

def testMegam(fModel,ftest,fout):
    cmd = "megam -fvals -predict %s binary %s > %s"%(fModel,ftest, fout)
    p = Popen(cmd,stderr=PIPE,shell=True)
    stdout, stderr = p.communicate() # get the error rate from stderr
    print stderr
    err = stderr.split(' ')[7] # looks like '0.123456\n'
    print "error:",err
    err = float(err[0:len(err)-1]) # make it into 0.123456
    return err

# def compare(results,labels):
# 	count=0
# 	for i in range(len(results)):
# 		if not results[i] == labels[i]:
# 			count = count + 1
# 	error = float(float(count)/float(len(results)))
# 	sys.stderr.write('done\nError=%f/%f=%f'%(count,len(results),error))

if __name__ == "__main__":
    main()
