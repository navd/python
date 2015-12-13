# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 14:04:36 2015

@author: Navdeep
"""

import re, math, collections, itertools, sys, os
from nltk.classify import PositiveNaiveBayesClassifier
from nltk.corpus import stopwords

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
cachedStopWords = stopwords.words("english")

negSentences = open(os.path.join(__location__, 'XLect10.Progs\\rt-polarity-neg.txt'), encoding='utf8')
posSentences = open(os.path.join(__location__, 'XLect10.Progs\\rt-polarity-pos.txt'), encoding='utf8')
negSentences = re.split(r'\n', negSentences.read())
posSentences = re.split(r'\n', posSentences.read())

posCutoff = int(math.floor(len(posSentences)*3/4))
negCutoff = int(math.floor(len(negSentences)*3/4))
posTrainFeatures = posSentences[:posCutoff]
negTrainFeatures = negSentences[:negCutoff]
posTestFeatures = posSentences[posCutoff:]
negTestFeatures = negSentences[negCutoff:]

sports_sentences = ['The team dominated the game',
                    'They lost the ball',
                    'The game was intense',
                    'The goalkeeper catched the ball',
                    'The other team controlled the ball'
                    ]
                    
various_sentences = ['The President did not comment',
                     'I lost the keys',
                     'The team won the game',
                     'Sara has two kids',
                     'The ball went off the court',
                     'They had the ball for the whole game',
                     'The show is over'
                     ]
                    
def features(sentence):
    sentence = ' '.join([word for word in sentence.split() if word.lower() not in cachedStopWords])
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)
    
positive_featuresets = list(map(features, sports_sentences))
unlabeled_featuresets = list(map(features, various_sentences))
classifier = PositiveNaiveBayesClassifier.train(positive_featuresets, unlabeled_featuresets)

positive_sentiments = list(map(features, posTrainFeatures))
negative_sentiments = list(map(features, negTrainFeatures))
sentimentClassifier = PositiveNaiveBayesClassifier.train(positive_sentiments, negative_sentiments)

#print (classifier.classify(features('The cat is on the table')))
#print (classifier.classify(features('My team lost the game')))

referenceSets = collections.defaultdict(set)
testSets = collections.defaultdict(set)
positives = 0
negatives = 0
tp = 0
tn = 0
fp = 0
fn = 0
for sentence in posTestFeatures: # enumerate adds number-count to each item\
    positives += 1
    referenceSets[True].add(sentence)               # recorded polarity for these test sentences
    predicted = sentimentClassifier.classify(features(sentence)) # classifiers' proposed polarity for tests
    if(predicted == True):
        tp += 1
    else:
        fn += 1
    testSets[predicted].add(sentence)
for sentence in negTestFeatures: # enumerate adds number-count to each item\
    negatives += 1
    referenceSets[False].add(sentence)               # recorded polarity for these test sentences
    predicted = sentimentClassifier.classify(features(sentence)) # classifiers' proposed polarity for tests
    if(predicted == False):
        tn += 1
    else:
        fp += 1
    testSets[predicted].add(sentence)

print (positives)
print (negatives)
print (tp)
print (tn)
print (fp)
print (fn)

print ('Accuracy: ', (tp + tn) / (positives + negatives))
#Outputs
#print('train on %s instances, test on %s instances'% (len(trainFeatures), len(testFeatures)))
#print('accuracy:', nltk.classify.util.accuracy(sentimentClassifier, posTestFeatures))
