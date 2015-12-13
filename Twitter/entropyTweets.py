# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:38:29 2015

@author: Navdeep
"""
#Imported the needed packages, stopwords is for Question 1a)
import nltk.tokenize
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Tweet Data, function to load tweet data in an array for processing
def load_tweets():
    print("Loading Tweets...")
    # tweet no 1 to 10 are random tweets
    tweet1=("One of the drugs behind this year’s Nobel Prize in Medicine started out as a heartworm pill for dogs")
    tweet2=("80% of people in Bihar feel taking money for vote is not wrong, says survey http://toi.in/rJ7TbY")
    tweet3=("Putin is denying sending ground troops to Syria. They are, apparently, just “volunteers.” http://slate.me/1QXhcig")
    tweet4=("#FIFA president #SeppBlatter provisionally suspended for 90 days after an investigation by ethics committee: reports")
    tweet5=("Maharashtra CM @Dev_Fadnavis snubs Shiv Sena, says Ghulam Ali's show will go on. Can't mix culture with politics")
    tweet6=("Why we need to build a world that works for introverts too: http://t.ted.com/hHSNOJa")
    tweet7=("How did a Texas textbook end up describing slaves as workers from Africa? http://slate.me/1LhSFnS")
    tweet8=("A Biden presidency would be grim news for feminism: http://slate.me/1hqtDXP")
    tweet9=("What lessons do Girl Scouts learn selling cookies?  http://slate.me/1Zb9yqy via @Quora")
    tweet10=("The only way the Democratic race will become exciting: Joe Biden. http://slate.me/1FSHVw0")
    # tweet no 11 to 20 are spam tweets
    tweet11=("Last chance to loose your weight 8 lbs in 2 weeks http://womenshealth.com-june30.us/garcini123/")
    tweet12=("Want to reduce weight 8 lbs in 1 week come to http://womenshealth.com-june30.us/garcinia/")
    tweet13=("Limited offer really works, reduce 8 lbs in 2 weeks http://womenshealth.com-jun.us/garcinia/")
    tweet14=("#offer #offer #offer loose weight 8 lbs in http://womenshealth.com-jun.us/garcini/")
    tweet15=("http://womenshealth.com-jun.us/garcini123/ is the best way to loose weight #looseweight")
    tweet16=("If you are health conscious, down 10 lbs! http://womenshealth.com-jun.us/garcini/")
    tweet17=("Loose your weight upto 8 lbs in 2 weeks! http://womenshealth.com-june30.us/garcinia/")
    tweet18=("Interesting in loosing weight click on http://womenshealth.com-june5.us/garcinia/")
    tweet19=("I've lost 8 lbs in 3 weeks! http://womenshealth.com-jun.us/garcinia/")
    tweet20=("This really works, down 5 more lbs! http://womenshealth.com-june6.us/garcinia/")
    return [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6, tweet7, tweet8, tweet9, tweet10, tweet11, tweet12, tweet13, tweet14, tweet15, tweet16, tweet17, tweet18, tweet19, tweet20]
# end function load_tweets


# function to convert tags to either v or n, for lemmatization (a pre requisite for lemmatization)
def convert_tags(tag):
    if tag == 'vbd' or tag == 'vbg' or tag == 'vbz':
        return 'v'
    else:
        return 'n'
#end function convert_tags


# formula to compute entropy
import math
def entropy(labels):
    freqdist = nltk.FreqDist(labels)
    probs = [freqdist.freq(l) for l in freqdist]
    return -sum(p * math.log(p,2) for p in probs)
# end function entropy

    
# This function covers the complete preprocessing steps, including stop words removal
def process_tweets(allTweets):
    #fetching each tweet from array of tweets
    index = 0
    for eachTweet in allTweets:
        #removing url's
        eachTweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',eachTweet)
        #removing username
        eachTweet = re.sub('@[^\s]+',' ',eachTweet)
        #Remove additional white spaces
        eachTweet = re.sub('[\s]+', ' ', eachTweet)
        #Replace #word with word
        eachTweet = re.sub(r'#([^\s]+)', r'\1', eachTweet)
        #trim
        eachTweet = eachTweet.strip('\'"')
        # tokenizing eachh tweet using word_tokenizer
        tokenizedTweet = nltk.word_tokenize(eachTweet)
        # normalizing each tweet
        normalizedTweet = [word.lower() for word in tokenizedTweet]
        #pos-tagging each tweet using nltk's pos_tag 
        posTaggedTweet = nltk.pos_tag(normalizedTweet)

        # looping through each word of pos tagged tweets
        for item in posTaggedTweet:
            # converting tweet's each word's tag to either verb or noun
            newTag = convert_tags(item[1].lower())
            # lemmatizing the word
            out = wnl.lemmatize(item[0], newTag)
            # checking if word is stop word or not
            # if stop word, then ignoring that word
            if out not in stop:
                # if word is not a stop word, then save this word for entropy array
                allTweetsfeatureList.append(out)
                if index < 10:
                    randomTweetsFeatureList.append(out)
                else:
                    spamTweetsFeatureList.append(out)
                #endif
            #endif
        #endfor
        index += 1
    #end for
# end function process_tweets
    

# creating WordNetLemmatizer abd stopwords object
wnl = nltk.WordNetLemmatizer()
stop = stopwords.words('english')

#
randomTweetsFeatureList = []
spamTweetsFeatureList = []
allTweetsfeatureList = []

#Run the program
allTweets = load_tweets()
process_tweets(allTweets)

#calculating entropy
print("Entropy of random tweets :: ")
print(entropy(randomTweetsFeatureList))
print("\n")
print("Entropy of spam tweets :: ")
print(entropy(spamTweetsFeatureList))
print("\n")
print("Entropy of all tweets :: ")
print(entropy(allTweetsfeatureList))
print("\n")
