import sys 
import os

num_of_classes = 4
lambda_value = 1

def main():
	classifiers = trainFirstTree()
	testTree(classifiers[0], classifiers[1], classifiers[2])
	

def trainFirstTree():
"""
Root splits does {graphics,windows} versus {baseball,hockey}. For this data, we only need 3 classifiers, f0, the root, f01, the left leaf, and f10 the right leaf.
"""	
	# f0: the classifier for root. does {graphics,windows} versus {baseball,hockey}.
	f0 = "tree0_model.megam"
	# generate data so that grachics, windows get +1 and rest get -1
	generateBinaryData('../../data/train.comp.graphics.txt', '../../data/train.rec.sport.baseball.txt', f0)
	appendBinaryData('../../data/train.comp.windows.x.txt', '../../data/train.rec.sport.hockey.txt', f0)
	f0_train = "tree0_train.megam"
	trainMegam(f0_train,f0)
	
	# f01: the left child classifier of root. does {graphics}vs{windows}
	f01 = "tree01_model.megam" 
	# generate the data like we did in warm up
	# python wordExtractor.py megam data/train.comp.graphics.txt data/train.comp.windows.x.txt > tree01_train.megam
	f01train = "tree01_train.megam"
	generateBinaryData('../data/train.comp.graphics.txt', '../data/train.comp.windows.x.txt', f01train)
	trainMegam(f01_train,f01)

	# f02: the right child classifier of root. does {baseball}vs{hockey}
	f10 = "tree10_model.megam" 
	f10train = "tree10_train.megam"
	generateBinaryData('../data/train.rec.sport.baseball.txt', '../data/train.rec.sport.hockey.txt', f01train)
	trainMegam(f01_train,f01)
	return (f0,f01,f10)

def testFirstTree(f0,f01,f10):
	#so now we have f0, f01, and f10
	testFile0 = "tree0_test.megam"
	# generate test data so that grachics, windows get +1 and rest get -1
	generateBinaryData('../../data/test.comp.graphics.txt', '../../data/test.rec.sport.baseball.txt', testFile0)
	appendBinaryData('../../data/test.comp.windows.x.txt', '../../data/test.rec.sport.hockey.txt', testFile0)

	f0out = "treef0_Y.megam"
	testMegam(fin,testFile0,f0out) # test it, get output
	Y = getLabels(f0out)
	testFile10 = "tree10_test.megam"
	testFile01 = "tree01_test.megam"
	# for all files marked as +1 in f0out, write the corresponding data to testFile10, -1 goes to testFile01
	# Y = open(f0out, "r")
	# f10 = open(testFile10, "w")
	# f01 = open(testFile10, "w")
	# for line in f:
        #         # get the first number of each line as predictions
	# 	line = line.strip()
	# 	line = line.split()
	# 	labels.append(int(line[0]))
		
		
	


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
	return labels		
		
def trainMegam(fin, fout):
    os.system("./megam -fvals -tune -lambda %f binary %s > %s"%(lambda_value,fin, fout))  

def testMegam(fin,test,fout):
    os.system("./megam -fvals -predict %s binary %s > %s"%(fin,test, fout))
# def compare(results,labels):
# 	count=0
# 	for i in range(len(results)):
# 		if not results[i] == labels[i]:
# 			count = count + 1
# 	error = float(float(count)/float(len(results)))
# 	sys.stderr.write('done\nError=%f/%f=%f'%(count,len(results),error))

if __name__ == "__main__":
    main()
