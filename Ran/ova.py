import runClassifier
import linear

def main():
	X = []
	Xte = []
	#5485 is the number of unique words -1
	featureNo = 5485
	
	# step 1: processing the data.
	populateData(X,"trainingData.txt",featureNo)
	populateData(Xte,"testingData.txt",featureNo)
	Y =[]
	Yte = []
	# get the labels for the data
	getLabel(Y,"graphics-windows-train.megam","train.basebal.hockey.megam")
	getLabel(Yte,"graphics-windows-test.megam","test.baseball.hockey.megam")
	
	# test
	h = linear.LinearClassifier({'lossFunction': linear.SquaredLoss(), 'lambda': 0, 'numIter': 100, 'stepSize': 0.5})
	runClassifier.trainTest(h, X, Y, Xte, Yte)
	print h
	
"""
populate testing and training data from files

there are only the non-zero features in the files with a format of "index value"
"""
def populateData(X,fileName,fNo):
	openFile = open(fileName,"r")
	for line in openFile:
		line=line.strip()
		values = line.split()
		x = [0] * fNo 
		for i in range(0,len(values),2):
			pos = int(values[i])
			# find the position by 1st number, and the value by 2nd number
			x[pos] = int(values[i+1])
		# add one row in the data array
		X.append(x)
		
		
"""
read Y from megam files and label as 4 classes:1,2,3,4
graphics : 1
windows : 2
baseball : 3
hockey : 4
"""
def getLabel(Y,fn1,fn2):
	f1 = open(fn1,"r")
	f2 = open(fn2,"r")
	for line in f1:
		line = line.strip()
		word = line.split()
		label = int(word[0])
		if label == 1:
			Y.append(1)
		else :
			Y.append(2)
			

	for line in f2:
		line = line.strip()
		word = line.split()
		label = int(word[0])
		if label == 1:
			Y.append(3)
		else:
			Y.append(4)

# step 2: ova train
# step 3: ova test


if __name__ == "__main__":
    main()