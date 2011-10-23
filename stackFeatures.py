#!/usr/bin/python

import sys
import cfdata
from numpy import *
from pylab import *

def stackFeatures(coraData, featureFile, predictFile, outputFile, xVersion):
	# citing is a dictionary which maps a 
	# paper ID to the IDs of papers it cited
	cited = coraData[0]
	# citing is a dictionary which maps a
	# paper ID to the IDs of papers citing it
	citing = coraData[1]
	# IDs in the order they appear in the documents
	entryIDs = coraData[2]

	# X_{k-1} features
    featureF = open(featureFile, 'r')
	# Y_{k-1} predictions
    predictF = open(predictFile, 'r')
	# outpu file 
    outputF = open(outputFile, 'w')

	# A dictionary which maps entryIDs to their labelled classes
	predictions = {}

	index = 0
    for line in predictF:
		toks = line.split()
		# map entryID to its labelled class
		predictions[entryIDs[index]] = toks[0]
		# increment to next entryID
		index += 1

	index = 0
    # read each line, each of which is a document
    for line in contentF:
		preCT = [0] * 10

		# tally the labels of your neighbors
		# TODO weight them by something? (number of citations they have)
		for neighbor in cited[entryIDs[index]]:
			preCT[predictions[neighbor]] = preCT[predictions[neighbor]] + 1

		# normalize and add to feature vector
		total = sum(t)
		if total > 0
		for label in range(len(preCT)):
			preCT[label] = preCT[label] / total
			if preCT[label] > 0:
				line = line + ' L' + label + 'X' + xVersion + ' ' + repr(preCT[label])

		# write this feature to a file
		outputF.write(line)
		outputF.write('\n')

    featureF.close()
    predictF.close()
	outputF.close()



def initFeatures(citeFile, contentFile, outputFile):
	# citing is a dictionary which maps a 
	# paper ID to the IDs of papers it cited
	cited = {} 
	# citing is a dictionary which maps a
	# paper ID to the IDs of papers citing it
	citing = {}

	# read in the links
    citeF = open(citeFile, 'r')
    for line in citeF:
    	toks = line.split()
		
		if citing.has_key(toks[1]):
			citing[toks[1]] = citing[toks[1]].append(toks[2])
		else:
			citing[toks[1]] = [toks[2]]

		if cited.has_key(toks[2]):
			cited[toks[2]] = cited[toks[2]].append(toks[1])
		else:
			cited[toks[2]] = toks[1]
	
    contentF = open(contentFile, 'r')
    outputF = open(outputFile, 'w')
	entryIDs = []

    # read each line, each of which is a document
    for line in contentF:
		# Each line is in the format:
		# <paper_id> <word_attributes>+ <class_label>
	    # first split the line
		toks = line.split()

		# save the entry ID
		entryIDs.append(toks[1])

		# prefix the feature with the <class_label>
		features = repr(toks[len(toks)-1])

		# isolate the <word_attributes>+
		# and then add them to our feature
		toks = toks[1:len(toks)-1]
	    for i in range(len(toks)):
			# if the word appeared in the document then
			# add Fi 1.0
			if toks[i] != 0
				features += ' F' + i + ' ' + toks[i] + '.0'

		# write this feature to a file
		outputF.write(features)
		outputF.write('\n')

    citeF.close()
    contentF.close()
	outputF.close()

	coraData = (cited, citing, entryIDs)
	return coraData
