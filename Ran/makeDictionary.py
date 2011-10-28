"""
Goes through each file and makes a set of unique words
Write it down to file
"""

stopwords = open('stopwords.txt', 'r').read().split()

texts = ['graphics-windows-test.fastdt', 'graphics-windows-train.fastdt'];
possibleWords = open('
