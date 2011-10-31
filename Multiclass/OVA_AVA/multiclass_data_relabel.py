def main():
	# get the labels for the data
	Y =[]
	# setLabel(Y,"graphics-windows-train.megam","train.basebal.hockey.megam")
	setLabel(Y,"graphics-windows-test.megam","test.baseball.hockey.megam")
	for y in Y:
		output = ""
		for word in y:
			output = output + " " + word.__str__()
		print output.strip()



"""
read Y from megam files and label as 4 classes:1,2,3,4
graphics : 1
windows : 2
baseball : 3
hockey : 4
"""
def setLabel(Y,fn1,fn2):
	f1 = open(fn1,"r")
	f2 = open(fn2,"r")
	for line in f1:
		line = line.strip()
		word = line.split()
		label = int(word[0])
		if label != 1:
			word[0] = 2
		Y.append(word)	

	for line in f2:
		line = line.strip()
		word = line.split()
		label = int(word[0])
		if label == 1:
			word[0] = 3
		else:
			word[0] = 4
		Y.append(word)


if __name__ == "__main__":
    main()