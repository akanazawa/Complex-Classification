"""
Goes through each file and makes a set of unique words
Write it down to file
"""
import Stemmer

# get stop words
stopWords = open('stopwords.txt', 'r').read().split()
# files to go through
texts = ['graphics-windows-test.fastdt', 'graphics-windows-train.fastdt', 'train.basebal.hockey.fastdt'];
# the dictionary
uniqueWords = dict()
stem = Stemmer.Stemmer('english')
for f in texts:
    print "looking at " + f
    possibleWords = open(f, 'r').read().split()
    for w in possibleWords:
        if w not in stopWords or not w.isdigit():
            w = stem.stemWord(w)
            if w in uniqueWords.keys():
                uniqueWords[w] +=1 # add count
            else:
                uniqueWords[w] = 1

for word, count in uniqueWords:
    if count < 4:
        print "delete: " + word
        del uniqueWords[word]
        
output = open('uniqueWords.txt', 'w')
for w in uniqueWords:
    output.write(w+'\n')

output.close()
