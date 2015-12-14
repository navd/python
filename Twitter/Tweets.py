# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:38:29 2015

@author: Navdeep
"""
#Imported the needed packages, stopwords is for Question 1a)
import nltk.tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Tweet Data, function to load tweet data in an array for processing
def load_tweets():
    print("Loading Tweets...")
    tweet1=("Matt Harvey didn't attend Mets' mandatory workout - Sun Times National Matt Harvey http://goo.gl/xg3yqy?MattHarvey-plge")
    tweet2=("NewJerseyDotCom ° How will Mets punish Matt Harvey for skipping mandatory workout before NLDS?: Harvey wasn't ... http://bit.ly/1j54uTz")
    tweet3=("'Matt Harvey Apologizes for Missing Mets Workout' by SETH BERKMAN via NYT http://www.nytimes.com/2015/10/07/sports/baseball/matt-harvey-apologizes-for-missing-mets-workout.html")
    tweet4=("Not a good look for Matt Harvey, but the Monday Night Football menu at American Cut in Tribeca does sound delicious. http://www.nydailynews.com/sports/basebal")
    tweet5=("Can't wait till Matt Harvey's a yankee... Can't deal w him anymore")
    tweet6=("Was he with Matt Harvey? RT @truebluela Scott Van Slyke 'not where he needs to be' physically today, per Don Mattingly.")
    tweet7=("Matt Harvey was late for work. The Mets are taking money out of his pocket. This situation SHOULD be resolved ('should' being the key word)")
    tweet8=("Scott Boras says that Matt Harvey's car was on a miles limit, which was why he was late for practice today")
    tweet9=("Terry Collins says Matt Harvey will be fined. Still pitching Game 3 obviously. This isn't college football, TC notes")
    tweet10=("Headed home. Stuck in traffic. The real kind of traffic, not the Matt Harvey kind of traffic")
    return [tweet1, tweet2, tweet3, tweet4, tweet5, tweet6, tweet7, tweet8, tweet9, tweet10]

# function to convert tags to either v or n, for lemmatization (a pre requisite for lemmatization)
def convert_tags(tag):
    if tag == 'vbd' or tag == 'vbg' or tag == 'vbz':
        return 'v'
    else:
        return 'n'


# This function covers the complete preprocessing steps, including stop words removal
def process_tweets(allTweets):
    allLemmatizedTweetDistinctWords = []
    wordsListForWordCloud = ''
    #fetching each tweet from array of tweets
    for eachTweet in allTweets:
        # tokenizing eachh tweet using word_tokenizer
        tokenizedTweet = nltk.word_tokenize(eachTweet)
        # normalizing each tweet
        normalizedTweet = [word.lower() for word in tokenizedTweet]
        #pos-tagging each tweet using nltk's pos_tag 
        posTaggedTweet = nltk.pos_tag(normalizedTweet)
        # array declaration for lemmatized tweet
        # please note this array will not contain stop words
        # as below code handles the stop word removal functionality
        lemmatizedTweet = []
        for item in posTaggedTweet:
            # converting tweet's each word's tag to either verb or noun
            newTag = convert_tags(item[1].lower())
            # lemmatizing the word
            out = wnl.lemmatize(item[0], newTag)
            # checking if word is stop word or not
            # if stop word, then ignoring that word
            if out not in stop:
                # if word is not a stop word, then save this word in lemmatizedTweet array
                lemmatizedTweet.append(out)
                # getting wordsList for wordcloud
                wordsListForWordCloud += out
                wordsListForWordCloud += ' '                
                if out not in allLemmatizedTweetDistinctWords:
                    # getting only distinct word after pre processing the tweets
                    allLemmatizedTweetDistinctWords.append(out)
        # printing the pre processed tweet without stop words
        print(lemmatizedTweet)
        tfScores = []
        for word in allTfWords:
            # fetching term frequency
            tfScores.append(lemmatizedTweet.count(word))
        # printing term frequency
        print(tfScores)
        print("\n")
    print("\n\n")
    print(allLemmatizedTweetDistinctWords)
    print("\n\n")
    print(wordsListForWordCloud)
    
# creating WordNetLemmatizer abd stopwords object
wnl = nltk.WordNetLemmatizer()
stop = stopwords.words('english')
allTfWords = ['matt', 'harvey', 'attend', 'mets', 'mandatory', 'workout', 'sun', 'time', 'national', 'punish', 'skipping', 'nlds', 'apologize', 'miss', 'seth', 'berkman', 'via', 'nyt', 'good', 'look', 'monday', 'night', 'football', 'menu', 'american', 'cut', 'tribeca', 'sound', 'delicious', 'wait', 'till', 'yankee', 'deal', 'anymore', 'truebluela', 'scott', 'van', 'slyke', "'not", 'need', 'physically', 'today', 'per', 'mattingly', 'late', 'work', 'take', 'money', 'pocket', 'situation', 'resolved', 'boras', 'say', 'car', 'mile', 'limit', 'practice', 'terry', 'collins', 'fined', 'still', 'pitch', 'game', 'obviously', 'college', 'note', 'head', 'home', 'stuck', 'traffic', 'real', 'kind']
#Run the program
allTweets = load_tweets()
process_tweets(allTweets)
