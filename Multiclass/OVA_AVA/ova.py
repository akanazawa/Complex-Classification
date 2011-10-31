import sys 
import os

num_of_classes = 4
lambda_value = 1

def main():
	D = "train_multiclass.megam"
	
	# write to multiple files where ith class as positive and all others labeled negative
	commonName = "temp_train_megam"
	Relable(D,num_of_classes,commonName)
	
	# train classifier based on those files
	for i in range(1, num_of_classes+1):
		fin = "temp_train_megam" + i.__str__()+".txt"
		fout = "temp_model_megam" + i.__str__()+".txt"
		trainMegam(fin,fout)

	model_files =[]
	for j in range(1, num_of_classes+1):
		model_files.append( "temp_model_megam"+j.__str__()+".txt")
	BinaryPredict(model_files,num_of_classes)
	
	# get the predictions in an N by D array
	predicts = getPredictions()
	results = []
	# for each data point
	for data in range(len(predicts[0])):		
		scores = [0]*num_of_classes
		# for each classes
		for c in range(num_of_classes):
			predict = predicts[c][data]
			if predict == 1:
				# increment score by 1 to this class
				scores[c] = scores[c]+1
			else:
				# for the data that are predicted to be -1, add 1 to all other classes
				for s in range(num_of_classes):
					if s == c:
						continue
					else:
						scores[s] = scores[s] + 1
		# get the max index
		max = scores[0]
		maxIdx = 0
		for s in range(len(scores)):
			if max < scores[s]:
				max= scores[s]
				maxIdx = s
		# 		get the multiclass prediction based on maxIdx
		results.append(maxIdx+1)
	labels = getTrueLabel()
	
	compare(results, labels)
	
def getPredictions():	
	results = []
	for l in range(1,num_of_classes+1):
		name = "temp_test_megam"+l.__str__()+".txt"
		f = open(name,"r")
		predicts = []
		for line in f:
			# get the first number of each line as predictions
			line = line.strip()
			line = line.split()
			predicts.append(int(line[0]))
		results.append(predicts)
		f.close()
	return results
	
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
"""
One versus All Train
write to multiple files as fi
file name: temp_train_megam$i.txt
"""
def Relable(D_multiclass,classes,commonName):

	for i in range(1,classes+1):
		# step1: rewrite all the label to +1/-1
		f = open(D_multiclass,"r")
		D_bin = []
		for line in f:
			line = line.strip()
			words = line.split()
			if int(words[0]) == i:
				words[0] = 1
			else:
				words[0] = -1
			D_bin.append(words)
		filename = commonName + i.__str__() + ".txt"
		writeToFile = open(filename,"w")
		
		for d in D_bin:
			output = ""
			for word in d:
				output = output + " " + word.__str__()
			writeToFile.write(output.strip())
			writeToFile.write("\n")


def BinaryPredict(file_to_predict,classes):
	idx = 1
	for f in file_to_predict:
		fout = "temp_test_megam"+idx.__str__()+".txt"
		# for each binary model file, predict
		testMegam(f,"test_multiclass.megam", fout)
		idx = idx +1
		
def trainMegam(fin, fout):
    os.system("./megam -fvals -tune -lambda %f binary %s > %s"%(lambda_value,fin, fout))  

def testMegam(fin,test,fout):
    os.system("./megam -fvals -predict %s binary %s > %s"%(fin,test, fout))
def compare(results,labels):
	count=0
	for i in range(len(results)):
		if not results[i] == labels[i]:
			count = count + 1
	error = float(float(count)/float(len(results)))
	sys.stderr.write('done\nError=%f/%f=%f'%(count,len(results),error))

if __name__ == "__main__":
    main()
