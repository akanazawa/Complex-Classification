f = open("graphics-windows-train.megam",'r')
Y = []
for line in f:
	word = line.split()
	label = int(word[0])
	if label == 1:
		Y.append(1)
	else :
		Y.append(2)
		
f2 = open("train.basebal.hockey.megam",'r')
for line in f2:
	word = line.split()
	label = int(word[0])
	if label == 1:
		Y.append(3)
	else:
		Y.append(4)
		
print Y