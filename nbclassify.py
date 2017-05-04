from __future__ import division
import sys
import os
import re
import math

def getFileName():
	if not len(sys.argv) == 2:
		print "Please provide 1 file name - the one that contains test data"
		sys.exit()
	fileName = sys.argv[1]
	return fileName

def readFile(fileName):
	if not os.path.isfile(fileName):
		print "Please check whether test data file exists or not"
		sys.exit()
	global testData, modelData
	inputFile = open(fileName, 'r')
	for line in inputFile:
		lineParts = line.split(' ', 1)
		testData[lineParts[0]] = lineParts[1]
	inputFile.close()

	fileName = "nbmodel.txt"
	if not os.path.isfile(fileName):
		print "Please check whether nbmodel.txt  exists or not"
		sys.exit()
	inputFile = open(fileName, 'r')
	for line in inputFile:
		lineParts = line.split(' ', 1)
		modelData[lineParts[0]] = float(lineParts[1])
	inputFile.close()

def classifyTD_PN(review):
	global modelData
	classOutput = {}
	reviewParts = review.split(' ')
	Tprob = math.log(modelData['PRIOR_truthful'], 2)
	Dprob = math.log(modelData['PRIOR_deceptive'], 2)
	Pprob = math.log(modelData['PRIOR_positive'], 2)
	Nprob = math.log(modelData['PRIOR_negative'], 2)
	for word in reviewParts:
		#if word is there in deceptive/positive then it should be there in truthful/negative as well - due to add-one smoothing.
		#Also, if word is not there in the training data (hence not in the model data), we will ignore it.
		if word+"_deceptive" in modelData or word+"_truthful" in modelData:
			Tprob += math.log(modelData[word+"_truthful"], 2)
			Dprob += math.log(modelData[word+"_deceptive"], 2)
		if word+"_positive" in modelData or word+"_negative" in modelData:
			Pprob += math.log(modelData[word+"_positive"], 2)
			Nprob += math.log(modelData[word+"_negative"], 2)

	if Tprob > Dprob:
		classOutput['TD'] = 'truthful'
	else:
		classOutput['TD'] = 'deceptive'
	if Pprob > Nprob:
		classOutput['PN'] = 'positive'
	else:
		classOutput['PN'] = 'negative'
	return classOutput

def classifyTestData():
	global testData
	outputFile = open('nboutput.txt', 'w')
	for identifier in testData:
		review = testData[identifier]
		review = review.lower()
		review = re.sub(r', ', ',', review)
		review = re.sub(r',', ', ', review)

		review = re.sub(r': ', ':', review)
		review = re.sub(r':', ': ', review)

		review = re.sub(r'; ', ';', review)
		review = re.sub(r';', '; ', review)
	
		review = re.sub(r'\. ', '.', review)
		review = re.sub(r'\.', '. ', review)

		review = re.sub(r'[.\'\"!@#$%^*&\(\)?\/\\,_;:\n\-]', '', review)
		
		classOutput = classifyTD_PN(review)
		outputFile.write(identifier+" "+classOutput['TD']+" "+classOutput['PN']+"\n")
	outputFile.close()

def main():
	fileName = getFileName()
	readFile(fileName)
	classifyTestData()

testData = {}
modelData = {}

main()
