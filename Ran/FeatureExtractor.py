f = open("uniquewords.txt",'r')
c = 0
feats = {}
for word in f:
	word = word.strip()
	feats[word] = c
	c = c + 1
keys = feats.keys()

# keys = sorted(keys)

X = []
files=("graphics-windows-train.megam","train.basebal.hockey.megam")
for fl in files:
	f2 = open(fl,'r')
	for words in f2:
		row = []
		for j in range(len(keys)):
			row.append( 0)
	
		words = words.split()
		for i in range(1,len(words),2):
			if words[i] in keys:
				idx =int( feats[words[i]])
				row[idx] =int( words[i+1])
		X.append(row)

print X