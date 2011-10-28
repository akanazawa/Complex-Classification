"""
Goes through each file and makes a set of unique words
Write it down to file
"""
from sets import Set
# get stop words
stopWords = open('stopwords.txt', 'r').read().split()
# files to go through
texts = ['graphics-windows-test.fastdt', 'graphics-windows-train.fastdt'];
# the set
uniqueWords = Set()
for f in texts:
    possibleWords = open(f, 'r').read().split()
    for w in possibleWords:
        if w not in stopWords or not w.isdigit():
            uniqueWords.add(w)

output = open('uniqueWords.txt', 'w')
for w in uniqueWords:
    output.write(w+'\n')

output.close()
