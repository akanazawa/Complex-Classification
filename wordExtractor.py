#!/usr/bin/python

import re
import fileMaker

def wordExtractor(line):
    # first lowercase it
    line = line.lower()

    # next, remove all non [a-z ] characters; [^a-z ] is a regular
    # expression for everything except a-z and space.
    line = re.sub("[^a-z ]", " ", line)

    # split out all words, since word == feature
    words = line.split()

    # compute the features
    feats = {}
    for word in words:
        if feats.has_key(word):
            feats[word] += 1
        else:
            feats[word] = 1

    return feats


if __name__=="__main__":
    fileMaker.mainExtractor(wordExtractor)
