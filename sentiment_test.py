import tweepy as tw
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import cred
plt.style.use('fivethirtyeight')

api_consumer_key = ''
api_consumer_secret = ''
access_token = ''
access_token_secret = ''

authentication = tw.OAuthHandler(api_consumer_key, api_consumer_secret)
authentication.set_access_token(access_token, access_token_secret)
api = tw.API(authentication, wait_on_rate_limit=True)

posts = api.user_timeline(screen_name ="BillGates", count= 100, lang =  "en", tweet_mode="extended")

#print last five tweets
print("show the 5 recent tweets: \n")
i = 1
for tweet in posts[0:5]:
    print(str(i) + ') ' + tweet.full_text + '\n')
    i = i + 1

#create a dataframe with a column with column  called Tweets
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
df.head()

#clean data
#create a function to clean tweets

def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #removes @ mentions
    text = re.sub(r'#', '', text) #remove the # symbol
    text = re.sub(r'RT[\s]+', '', text) #remove RT
    text = re.sub(r'http?:\/\/\S+', '', text) #remove hyperlink

    return text
df['Tweets']= df['Tweets'].apply(cleanTxt)
print(df)

#create function to get subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

#create a function to get polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

#create two new columns
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

#show new dataframe with new columns
print(df)

#plot word cloud
allWords = ' '.join([twts for twts in df['Tweets']])
WordCloud = WordCloud(width = 500, height = 300, random_state = 21, max_font_size = 119).generate(allWords)
plt.imshow(WordCloud, interpolation = "bilinear")
plt.axis('off')
plt.show()

#create a function to compute negative, nuetral and positive analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)
print(df)

#print all positive tweets
j = 1
sortedDF = df.sort_values(by=['Polarity'])
for i in range(0, sortedDF.shape[0]):
    if(sortedDF['Analysis'][i] == 'Positive'):
        print(str(j) + ') ' + sortedDF['Tweets'][i])
        print()
        j = j+1

#print negative tweets
j = 1
sortedDF = df.sort_values(by=['Polarity'], ascending='False')
for i in range(0, sortedDF.shape[0]):
    if(sortedDF['Analysis'][i] == 'Negative'):
        print(str(j) + ') ' + sortedDF['Tweets'][i])
        print()
        j = j+1

#Plot polarity

plt.figure(figsize=(8,6))
for i in range(0, df.shape[0]):
    plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color = 'Blue')
plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

#get the percentage of positive tweets
ptweets = df[df.Analysis == 'Positive']
ptweets = ptweets['Tweets']
round(ptweets.shape[0] / df.shape[0] * 100, 1)
ptweets

#get the percentage of positive tweets
ntweets = df[df.Analysis == 'Positive']
ntweets = ntweets['Tweets']
round(ntweets.shape[0] / df.shape[0] * 100, 1)
ntweets

#show value counts
df['Analysis'].value_counts()
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()
    
