# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:14:11 2015

@author: Navdeep
"""

import os

def loadcorpus():
    """Load the corpus of abstracts and documents."""
    dirname = "cmplg-txt"
    charLengthOfAbstract = 0
    wordLengthOfAbstract = 0
    charLengthOfSentence = 0
    wordLengthOfSentence = 0
    nuOfAbstracts = 0
    nuOfSentences = 0
    for fn in sorted(os.listdir(dirname)):
        #docid = fn.split("-")[0]
        if fn.endswith("abstract.txt"):
            nuOfAbstracts += 1
            abstractWords = 0
            abstractChars = 0
            with open(os.path.join(dirname, fn), 'r') as f:
                for line in f:
                    words = line.split()
                    abstractWords += len(words)
                    abstractChars += len(line)
                    wordLengthOfAbstract += len(words)
                    charLengthOfAbstract += len(line)
            print ('number of chars in abstract ', fn, ' is:: ', abstractChars)
            print ('number of words in abstract ', fn, ' is:: ', abstractWords)
        if fn.endswith("sentences.txt"):
            nuOfSentences += 1
            sentenceWords = 0
            sentenceChars = 0
            with open(os.path.join(dirname, fn), 'r') as f:
                for line in f:
                    words = line.split()
                    sentenceWords += len(words)
                    sentenceChars += len(line)
                    wordLengthOfSentence += len(words)
                    charLengthOfSentence += len(line)
            print ('number of chars in document ', fn, ' is:: ', sentenceChars)
            print ('number of words in document ', fn, ' is:: ', sentenceWords)
    print('average number of chars in abstracts is ::', charLengthOfAbstract/nuOfAbstracts)
    print('average number of words in abstracts is ::', wordLengthOfAbstract/nuOfAbstracts)
    print('average number of chars in documents is ::', charLengthOfSentence/nuOfSentences)
    print('average number of words in documents is ::', wordLengthOfSentence/nuOfSentences)
    recuredPertInChars = ((charLengthOfSentence - charLengthOfAbstract) * 100) / charLengthOfSentence
    recuredPertInWords = ((wordLengthOfSentence - wordLengthOfAbstract) * 100) / wordLengthOfSentence
    print(recuredPertInChars, '% the average abstract reduced the length of document in chars')
    print(recuredPertInWords, '% the average abstract reduced the length of document in words')
    
loadcorpus()