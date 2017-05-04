from __future__ import division
import sys
import os
import re

def getFileName():
	if not len(sys.argv) == 3:
		print "Please provide 2 file names - one for training data and one for labels"
		sys.exit()
	fileName = {}
	fileName['trainingDataFile'] = sys.argv[1]
	fileName['labelFile'] = sys.argv[2]
	return fileName

def fillStopWords():
	global stopWords
	stopWords = ["a","able","about","above","abst","accordance","according","accordingly","across","act","actually","added","affected","affecting","affects","ah","all","almost","alone","along","already","also","although","always","am","an","and","any","anyhow","anymore","anything","anyway","anyways","anywhere","apparently","approximately","are","aren","arent","arise","around","as","aside","ask","asking","at","auth","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","begin","beginning","beginnings","begins","behind","being","believe","below","beside","besides","between","beyond","biol","both","brief","briefly","but","by","came","can","cause","causes","certain","certainly","com","come","comes","contain","containing","contains","could","couldnt","date","did","didn't","do","does","doesn't","doing","done","don't","down","downwards","due","during","each","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","et-al","etc","even","ever","every","ex","except","far","few","fifth","first","five","fix","followed","following","follows","for","former","formerly","forth","found","four","from","further","furthermore","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","had","happens","hardly","has","hasn't","have","haven't","having","he","hed","hence","her","here","hereafter","hereby","herein","heres","hereupon","hers","herself","hes","hi","hid","him","himself","his","hither","home","how","howbeit","however","hundred","i","id","ie","if","i'll","im","immediate","immediately","importance","important","in","inc","indeed","index","information","instead","into","invention","inward","is","isn't","it","itd","it'll","its","itself","i've","just","keep","keeps","kept","kg","km","know","known","knows","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","line","little","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","me","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","more","moreover","most","mostly","mr","mrs","much","mug","must","my","myself","na","name","namely","nay","nd","near","necessarily","need","needs","nevertheless","nine","ninety","normally","nos","obtain","obtained","obviously","of","often","oh","omitted","on","one","ones","only","onto","or","ord","other","others","ought","our","ours","ourselves","out","outside","over","owing","own","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","que","quickly","quite","qv","ran","rather","rd","re","readily","really","ref","refs","regarding","regardless","regards","research","respectively","resulted","resulting","results","run","said","same","saw","say","saying","says","sec","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","she","shed","she'll","shes","should","shouldn't","show","showed","shown","showns","shows","similar","similarly","since","six","slightly","so","some","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","such","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","than","that","that'll","thats","that've","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","these","they","theyd","they'll","theyre","they've","think","this","those","thou","though","thoughh","throug","through","throughout","thru","thus","til","tip","to","together","too","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","un","under","unless","until","unto","up","upon","ups","us","use","used","uses","using","various","'ve","via","viz","vol","vols","vs","want","wants","was","wasnt","way","we","wed","welcome","we'll","went","were","werent","we've","what","whatever","what'll","whats","when","whence","whenever","where","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","which","while","whim","whither","who","whod","whoever","whole","who'll","whom","whomever","whos","whose","why","widely","willing","wish","with","within","without","wont","words","world","would","wouldnt","www","you","youd","you'll","your","youre","yours","yourself","yourselves","you've"]
	for word in stopWords:
		stopWords.remove(word)
		word = re.sub(r'[.\'\"!@#$%^*&\(\)?\/\\,_;:\n]', '', word)
		stopWords.append(word)

def readFile(fileNames):
	trainingDataFile = fileNames['trainingDataFile']
	labelFile = fileNames['labelFile']

	if not os.path.isfile(trainingDataFile):
		print "Please check whether training file exists or not"
		sys.exit()
	global trainingData, labelData
	inputFile = open(trainingDataFile, 'r')
	for line in inputFile:
		lineParts = line.split(' ', 1)
		trainingData[lineParts[0]] = lineParts[1]
	inputFile.close()

	if not os.path.isfile(labelFile):
		print "Please check whether label file exists or not"
		sys.exit()
	inputFile = open(labelFile, 'r')
	for line in inputFile:
		lineParts = line.split(' ', 1)
		labelData[lineParts[0]] = lineParts[1]
	inputFile.close()

def filterReview(review):
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
	return review

def deceptiveCounter(review):
	global deceptiveFeatureCount, deceptiveWords, stopWords
	reviewParts = review.split(' ')
	for word in reviewParts:
		if word in stopWords or word == '\n' or word == '\r' or word == '':
			continue
		if word in deceptiveWords:
			deceptiveWords[word] += 1
		else:
			deceptiveWords[word] = 1
		deceptiveFeatureCount += 1

def truthfulCounter(review):
	global truthfulFeatureCount, truthfulWords, stopWords
	reviewParts = review.split(' ')
	for word in reviewParts:
		if word in stopWords or word == '\n' or word == '\r' or word == '':
			continue
		if word in truthfulWords:
			truthfulWords[word] += 1
		else:
			truthfulWords[word] = 1
		truthfulFeatureCount += 1

def positiveCounter(review):
	global positiveFeatureCount, positiveWords, stopWords
	reviewParts = review.split(' ')
	for word in reviewParts:
		if word in stopWords or word == '\n' or word == '\r' or word == '':
			continue
		if word in positiveWords:
			positiveWords[word] += 1
		else:
			positiveWords[word] = 1
		positiveFeatureCount += 1

def negativeCounter(review):
	global negativeFeatureCount, negativeWords, stopWords
	reviewParts = review.split(' ')
	for word in reviewParts:
		if word in stopWords or word == '\n' or word == '\r' or word == '':
			continue
		if word in negativeWords:
			negativeWords[word] += 1
		else:
			negativeWords[word] = 1
		negativeFeatureCount += 1

def getCounts():
	global trainingData, labelData, numNegativeReviews, numPositiveReviews, numTruthfulReviews, numDeceptiveReviews
	for identifier in trainingData:
		review = filterReview(trainingData[identifier])
		if 'deceptive' in labelData[identifier]:
			deceptiveCounter(review)
			numDeceptiveReviews += 1
		elif 'truthful' in labelData[identifier]:
			truthfulCounter(review)
			numTruthfulReviews += 1
		if 'positive' in labelData[identifier]:
			positiveCounter(review)
			numPositiveReviews += 1
		elif 'negative' in labelData[identifier]:
			negativeCounter(review)
			numNegativeReviews += 1

def writeDeceptiveClassParameters(modelFile):
	global deceptiveWords, deceptiveFeatureCount, numDeceptiveReviews, numTruthfulReviews, TDvocabCount
	priorDeceptiveClass = numDeceptiveReviews/(numDeceptiveReviews + numTruthfulReviews)
	modelFile.write("PRIOR_deceptive "+str(priorDeceptiveClass)+"\n")
	for word in deceptiveWords:
		likelihoodDeceptive = (deceptiveWords[word]+1)/(deceptiveFeatureCount+TDvocabCount)
		modelFile.write(word+"_deceptive "+str(likelihoodDeceptive)+"\n")

def writeTruthfulClassParameters(modelFile):
	global truthfulWords, truthfulFeatureCount, numDeceptiveReviews, numTruthfulReviews, TDvocabCount
	priorTruthfulClass = numTruthfulReviews/(numDeceptiveReviews + numTruthfulReviews)
	modelFile.write("PRIOR_truthful "+str(priorTruthfulClass)+"\n")
	for word in truthfulWords:
		likelihoodTruthful = (truthfulWords[word]+1)/(truthfulFeatureCount+TDvocabCount)
		modelFile.write(word+"_truthful "+str(likelihoodTruthful)+"\n")

def writePositiveCLassParameters(modelFile):
	global positiveWords, positiveFeatureCount, numPositiveReviews, numNegativeReviews, PNvocabCount
	priorPositiveClass = numPositiveReviews/(numNegativeReviews + numPositiveReviews)
	modelFile.write("PRIOR_positive "+str(priorPositiveClass)+"\n")
	for word in positiveWords:
		likelihoodPositive = (positiveWords[word]+1)/(positiveFeatureCount+PNvocabCount)
		modelFile.write(word+"_positive "+str(likelihoodPositive)+"\n")

def writeNegativeClassParameters(modelFile):
	global negativeWords, negativeFeatureCount, numPositiveReviews, numNegativeReviews, PNvocabCount
	priorNegativeClass = numNegativeReviews/(numNegativeReviews + numPositiveReviews)
	modelFile.write("PRIOR_negative "+str(priorNegativeClass)+"\n")
	for word in negativeWords:
		likelihoodNegative = (negativeWords[word]+1)/(negativeFeatureCount+PNvocabCount)
		modelFile.write(word+"_negative "+str(likelihoodNegative)+"\n")

def buildModel():
	modelFile = open('nbmodel.txt', 'w')
	writeDeceptiveClassParameters(modelFile)
	writeTruthfulClassParameters(modelFile)
	writePositiveCLassParameters(modelFile)
	writeNegativeClassParameters(modelFile)
	modelFile.close()

def diff(first, second):
	second = set(second)
	return [item for item in first if item not in second]

#Function to add missing words to both TD classes and PN classes
def addMissingWords():
	global deceptiveWords, truthfulWords, TDvocabCount
	Dwords = deceptiveWords.keys()
	Twords = truthfulWords.keys()
	DminusT = diff(Dwords, Twords)
	TminusD = diff(Twords, Dwords)
	for word in DminusT:
		truthfulWords[word] = 0
	for word in TminusD:
		deceptiveWords[word] = 0
	if len(deceptiveWords) == len(truthfulWords):
		print "Good Job"
	TDvocabCount = len(truthfulWords)

	global positiveWords, negativeWords, PNvocabCount
	Pwords = positiveWords.keys()
	Nwords = negativeWords.keys()
	PminusN = diff(Pwords, Nwords)
	NminusP = diff(Nwords, Pwords)
	for word in PminusN:
		negativeWords[word] = 0
	for word in NminusP:
		positiveWords[word] = 0
	if len(positiveWords) == len(negativeWords):
		print "Good Job again!!"
	PNvocabCount = len(positiveWords)

def main():
	fileNames = getFileName()
	readFile(fileNames)
	fillStopWords()
	getCounts()
	addMissingWords()
	buildModel()

trainingData = {}
labelData = {}
stopWords = []
deceptiveWords = {}
truthfulWords = {}
positiveWords = {}
negativeWords = {}
deceptiveFeatureCount = 0
truthfulFeatureCount = 0
positiveFeatureCount = 0
negativeFeatureCount = 0
numDeceptiveReviews = 0
numTruthfulReviews = 0
numPositiveReviews = 0
numNegativeReviews = 0
PNvocabCount = 0
TDvocabCount = 0

main()
