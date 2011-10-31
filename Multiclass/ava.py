import sys 
import os

num_of_classes = 4
lambda_value = 0.5

def main():
	Relable("train_multiclass.megam","ava_train_megam")
	# train classifier based on those files
	train()
	BinaryPredict()
	predicts = getMulticlassPrediction()
	results = []
	labels = getTrueLabel()
	# for each data point
	for d in range(len(labels)):
		col = 0
		scores = [0]*6
		for i in range(num_of_classes-1):		
			for j in range(i+1,num_of_classes):
				predict = predicts[col][d]
				if predict == 0:
					predict = -1
				scores[i] = scores[i] + predict
				scores[j] = scores[j] - predict
				col = col +1
		
		max = scores[0]
		maxIdx = 0
		for s in range(1,len(scores)):
			if max < scores[s]:
				max= scores[s]
				maxIdx = s
		# get the multiclass prediction based on maxIdx
		results.append(maxIdx+1)
	compare(results, labels)
				
	
def trainMegam(fin, fout):

    os.system("./megam -fvals -tune -lambda %f binary %s > %s"%(lambda_value,fin, fout))  

def testMegam(fin,test,fout):
    os.system("./megam -fvals -predict %s binary %s > %s"%(fin,test, fout))	
def readDataFromFile(filename):
	f = open(filename,"r")
	D =[]
	for line in f:
		line = line.strip()
		line = line.split()
		D.append(line)
	return D
def BinaryPredict():
	for i in range(num_of_classes-1):		
		for j in range(i+1,num_of_classes):
			fin = "ava_model_megam" + i.__str__()+j.__str__()+".txt"
			fout = "ava_test_megam"+ i.__str__()+j.__str__()+".txt"
			testMegam(fin,"test_multiclass.megam", fout)
def getMulticlassPrediction():
	results = []
	for i in range(num_of_classes-1):		
		for j in range(i+1,num_of_classes):
			fin = "ava_test_megam"+ i.__str__()+j.__str__()+".txt"
			f = open(fin,"r")
			predicts = []
			for line in f:
				# get the first number of each line as predictions
				line = line.strip()
				line = line.split()
				predicts.append(int(line[0]))
			results.append(predicts)
			f.close()			
	return results
def compare(results,labels):
	count=0
	for i in range(len(results)):
		if not results[i] == labels[i]:
			count = count + 1
	error = float(float(count)/float(len(results)))
	sys.stderr.write('done\nError=%f/%f=%f'%(count,len(results),error))

def getTrueLabel():	
	name = "test_multiclass.megam"
	f = open(name,"r")
	labels = []
	for line in f:
		# get the first number of each line as predictions
		line = line.strip()
		line = line.split()
		labels.append(int(line[0]))
	return labels	
					
def train():	
	for i in range(num_of_classes-1):		
		for j in range(i+1,num_of_classes):
			fin = "ava_train_megam" + i.__str__()+j.__str__()+".txt"
			fout = "ava_model_megam" + i.__str__()+j.__str__()+".txt"
			trainMegam(fin,fout)
		
def Relable(dataFile,outputFile):
	D_bin =[]
	# get f_ij where class i is pos and j is neg
	for i in range(num_of_classes-1):		
		for j in range(i+1,num_of_classes):
			D_bin = readDataFromFile(dataFile)
			fname = outputFile + i.__str__()+j.__str__()+".txt"
			writeFile = open(fname,"w")	
			for d in D_bin:				
				if int(d[0]) == i+1: #class label starts from 1
					d[0]  = 1
					output = ""
					for token in d:
						output = output + " "+ token.__str__()
					writeFile.write(output.strip())
					writeFile.write('\n')
				elif int(d[0]) == j + 1:
					d[0] = -1
					output = ""
					for token in d:
						output = output + " "+ token.__str__()
					writeFile.write(output.strip())
					writeFile.write('\n')
			


if __name__ == "__main__":
    main()