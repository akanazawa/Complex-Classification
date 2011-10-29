import pdb

f = open("uniqueWords.txt",'r')
c = 0
feats = {}
for word in f:
	word = word.strip()
	feats[word] = c
	c = c + 1
keys = feats.keys()

# keys = sorted(keys)

X = ""
files=("graphics-windows-test.megam","test.baseball.hockey.megam")
for fl in files:
	f2 = open(fl,'r')
	for words in f2:
		row = ""
		# for j in range(len(keys)):
		# 	row.append( 0)
	
		words = words.split()
		# pdb.set_trace()
		for i in range(1,len(words),2):
			if words[i] in keys: #words[i+1] is the freq
				# want to write "idx freq"
				idx = int( feats[words[i]])
				row += " " + str(idx) + " " + words[i+1]
				
				# row[idx] =int( words[i+1])
		X += row + "\n"


print X
