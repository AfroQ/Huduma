import tweepy as tw
import os
import pandas as pd

#Get your credentials from dev account 
api_consumer_key = ''
api_consumer_secret = ''
access_token = ''
access_token+secret = ''

authentication = tw.OAuthHandler(api_consumer_key, api_consumer_secret)
authtentication.set_access_token(access_token, api_consumer_secret)
api = tw.API(authentication, wait_on_rate_limit=True)

search_keys = '#hudumanamba'
date_since = '2020-06-01'

tweets = tw.Cursor(
    api.search,
    q=search_keys,
    lan='en',
    since=date_since).items(5)

for tweet in tweets:
    print(tweet.text)

# put into a pandas table
