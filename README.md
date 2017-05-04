# hotel_reviews_classification #
An implementation of Naive Bayes method to build a Naive Bayes model and use it to classify unseen reviews as positive, negative, truthful or deceptive

## Problem Statement: ##
You will write two programs: *nblearn.py* will learn a naive Bayes model from the training data, and
*nbclassify.py* will use the model to classify new data. The learning program will be invoked in the
following way:

*python nblearn.py /path/to/text/file /path/to/label/file*


The arguments are the two training files; the program will learn a naive Bayes model, and write the
model parameters to a file called *nbmodel.txt*. The format of the model is up to you, but it should
contain the model parameters (that is, the various probabilities) in a way that can be visually
inspected (so no binary files). You may use ordinary probabilities or log probabilities.

The classification program will be invoked in the following way:

*python nbclassify.py /path/to/text/file*

The argument is the test data file, which has the same format as the training text file. The program will
read the parameters of a naive Bayes model from the file nbmodel.txt, classify each entry in the
test data, and write the results to a text file called nboutput.txt in the same format as the label file
from the training data.

### Training files ###

The data will consist of two files, plus readme and license files. The data files are in the following format:

* A text file train-text.txt with a single training instance (hotel review) per line. The first token in the each line is a unique 20-character alphanumeric identifier, which is followed by the text of the review.

* A label file train-labels.txt with labels for the corresponding reviews. Each line consists of three tokens: a unique 20-character alphanumeric identifier corresponding to a review, a label truthful or deceptive, and a label positive or negative.

Each data file contains 1280 lines, corresponding to 1280 reviews.
