from tweepy import API 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy.streaming import StreamListener
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import plotly.graph_objects as go
from textblob import TextBlob
from expertai.nlapi.cloud.client import ExpertAiClient
from plotly.io import to_html



class TwitterCredentials():
  
  def __init__(self):
    self.app_key="PDz1fZLoCEHcOx035TtLsrcWS"
    self.app_secret="Ok1aJBP4nM6g87F3hFiPFY0R0a7qnUNsdIoKZteaAuzYF2yTuF" 
    self.oauth_token="1292034807057149952-3Mlqa59ZAoqRdACgnW6z4goXUy3vUs" 
    self.oauth_token_secret="ZZlu7jF3mymeapDxwj19MkqCYF3osQjp48xYEuIL4wRM1"

import os
os.environ["EAI_USERNAME"] = 'nk2indian@gmail.com'
os.environ["EAI_PASSWORD"] = 'Nareshnk2#'

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        twitter_credentials = TwitterCredentials()
        auth = OAuthHandler(twitter_credentials.app_key, twitter_credentials.app_secret)
        auth.set_access_token(twitter_credentials.oauth_token, twitter_credentials.oauth_token_secret)
        return auth


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    

class TweetAnalyzer():

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[self.clean_tweet(tweet.text) for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['lang'] = np.array([tweet.lang for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        
        return df

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    

def findusertweets(user_name):

    api = TwitterClient().get_twitter_client_api()
    tweets = api.user_timeline(screen_name=user_name, count=10, exclude_replies=False, include_retweets=True)
    tweet_analyzer = TweetAnalyzer()
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    df.to_csv(user_name+'_tweets.csv')
    tweets_list = df['tweets']
    summarized_tweet = '. '.join(tweets_list)
    client = ExpertAiClient()
    document = client.specific_resource_analysis(
    body={"document": {"text": summarized_tweet}}, 
    params={'language': 'en', 'resource': 'sentiment'})
    print("sentiment:", document.sentiment.overall)
    return summarized_tweet

def pie_chart(taxonomy,summarized_tweet):
    client = ExpertAiClient()
    language= 'en'
    output = client.classification(body={"document": {"text": summarized_tweet}}, params={'taxonomy': taxonomy, 'language': language})
    print("Tab separated list of categories:")
    pie_values =  {}
    for category in output.categories:
      pie_values[category.hierarchy[-1]] = category.frequency
    print(pie_values)
    labels = list(pie_values.keys())
    values = list(pie_values.values())
    pull_values = [0 for i in values]
    pull_values[values.index(max(values))] = 0.2
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label',hole=0.45,pull = pull_values, title  = taxonomy.upper())])
    fig.update_layout(width=650, height=650)
    div = to_html(fig)
    return div