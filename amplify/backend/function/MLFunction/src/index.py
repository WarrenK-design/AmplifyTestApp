import nltk 
nltk.data.path.append("/var/task/nltk_data")
import json
import requests
from bs4 import BeautifulSoup 
from statistics import mean
import csv 
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
from pprint import pprint
import pickle 


import csv


def readWordFile(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        return list(reader)[0]

top100Negative = readWordFile('negativeWords.csv')
top100Neutral = readWordFile('neutralWords.csv')
top100Positive = readWordFile('positiveWords.csv')

def loadClassifier(file):
    classifierFile = open(file,"rb")
    classifier = pickle.load(classifierFile)
    classifierFile.close()
    return classifier

#### Training the model ####
# This is where we train the classifier incoperating the new features 
# First need to extract the features from the text being analysed 
def extract_features(text,top100Positive,top100Negative,top100Neutral):
    '''
    This function will extract features from movie reviews associated with positive reviews
    It returns a dictionary which creates 3 features for every piece of text. 
        1. The average compund score. 
        2. The average positive score. 
        3. The amount of words in the text that are part of the top 100 words list for positive reviews.
    Based upon these featrues we can then train the model more accurately. 
    '''
    features = dict()
    posWordCount = 0
    negWordCount = 0 
    neutralWordCount = 0 
    compound_scores = list()
    positive_scores = list()
    negative_scores = list()
    neutral_scores  = list()
    
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            if word.lower() in top100Negative:
                negWordCount +=1
            if word.lower() in top100Positive:
                posWordCount += 1
            if word.lower() in top100Neutral:
                neutralWordCount += 1
        compound_scores.append(sia.polarity_scores(sentence)["compound"])
        positive_scores.append(sia.polarity_scores(sentence)["pos"])
        negative_scores.append(sia.polarity_scores(sentence)["neg"])
        neutral_scores.append(sia.polarity_scores(sentence)["neu"])
        #print("***************************************")
        #print(sentence)
        #print(f'Postive words count {posWordCount}')
        #print(f'Negative word count {negWordCount}')
        #print(f'Compound {sia.polarity_scores(sentence)["compound"]}')
        #print(f'Pos {sia.polarity_scores(sentence)["pos"]}')
        #print(f'Neg {sia.polarity_scores(sentence)["neg"]}')

    # Adding 1 to the final compound score to always have positive numbers
    # since some classifiers you'll use later don't work with negative numbers.
    features["mean_compound"] = mean(compound_scores) + 1
    features["mean_positive"] = mean(positive_scores)
    features["posWordCount"]  = posWordCount
    features["negWordCount"]  = negWordCount 
    features["neutralWordCount"] = neutralWordCount
    features["mean_negative"] = mean(negative_scores)
    features["mean_neutral"] = mean(neutral_scores)
    #print(features)
    return features




def handler(event, context):
    print('received event:')
    feed = "https://abcnews.go.com/abcnews/moneyheadlines"
    response = requests.get(feed)

    webpage = response.content

    soup = BeautifulSoup(webpage, features='xml')

    # Find all the item tags 
    items = soup.find_all('item')

    # Now get each article URL from item list 
    articles = []
    for item in items:
        headline    = item.find('title').text
        link        = item.find('link').text
        pubDate     = item.find('pubDate').text
        description = item.find('description').text
        image       = item.find('media:thumbnail')
        article = {"Headline":headline,"Link":link,"Description":description,"Image":image,"PubDate":pubDate}
        articles.append(article)

    # load the classifier 
    classifier = loadClassifier('./naivebayes.pickle')

    # For each of the articles need to get the features 
    for article in articles:
        # Extract the features for the given headline
        article['Features'] = extract_features(article['Headline'],top100Positive,top100Negative,top100Neutral)
        # Make predictions 
        prediction = classifier.classify(article['Features'])
        #print(f'{article['Headline']}')
        print("******************************")
        print(f'Headline:{article["Headline"]}\nSentiment Prediction:{prediction}\nDate:{article["PubDate"]}\nLink:{article["Link"]}\nDescription:{article["Description"]}')


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from lambda!!')
    }

handler("BLAH","BLAH")