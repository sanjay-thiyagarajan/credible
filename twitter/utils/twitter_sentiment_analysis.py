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
from expertai.nlapi.cloud.client import ExpertAiClient
from plotly.io import to_html
from collections import Counter
import collections



class TwitterCredentials():
  
  def __init__(self):
    self.app_key="PDz1fZLoCEHcOx035TtLsrcWS"
    self.app_secret="Ok1aJBP4nM6g87F3hFiPFY0R0a7qnUNsdIoKZteaAuzYF2yTuF" 
    self.oauth_token="1292034807057149952-3Mlqa59ZAoqRdACgnW6z4goXUy3vUs" 
    self.oauth_token_secret="ZZlu7jF3mymeapDxwj19MkqCYF3osQjp48xYEuIL4wRM1"

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
    

def findusertweets(user_name):

    api = TwitterClient().get_twitter_client_api()
    tweets = api.user_timeline(screen_name=user_name, count=30, exclude_replies=False, include_retweets=True)
    tweet_analyzer = TweetAnalyzer()
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    return df

def pie_chart(taxonomy,summarized_tweet):
    client = ExpertAiClient()
    language= 'en'
    output = client.classification(body={"document": {"text": summarized_tweet}}, params={'taxonomy': taxonomy, 'language': language})
    pie_values =  {}
    for category in output.categories:
      pie_values[category.hierarchy[-1]] = category.frequency
    labels = list(pie_values.keys())
    values = list(pie_values.values())
    pull_values = [0 for i in values]
    if len(values) != 0:
        pull_values[values.index(max(values))] = 0.2
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label',hole=0.35,pull = pull_values)])
    div = to_html(fig)
    if len(labels) == 0:
        status = 'ERROR'
    else:
        status = 'SUCCESS'
    behavioral_collection = {}
    behavioral_ids = []
    if taxonomy == 'behavioral-traits':
        for category in output.categories:
            behavioral_collection[category.id_] = [str(category.hierarchy[-1]),str(category.hierarchy[0]+'/'+category.hierarchy[1]+'/'+category.hierarchy[-1]),str(category.frequency)]
            behavioral_ids.append(str(category.id_))
        return div, status, behavioral_collection, behavioral_ids
    return div, status

def sentiment_gauge(input_text, width=None,height=None):
    client = ExpertAiClient()
    language= 'en'
    output = client.specific_resource_analysis(
        body={"document": {"text": input_text}}, 
        params={'language': language, 'resource': 'sentiment'}
    )
    value = output.sentiment.overall
    fig = go.Figure(go.Indicator(
        #domain = {'x': [0, 1], 'y': [0, 1]},
        value = value,
        mode = "gauge+number+delta",
        title = {'text': "Overall sentiment"},
        delta = {'reference': 0},
        gauge = {'axis': {'range': [-100, 100]},
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0}
                }
        )
    )
    if width != None and height != None:
        fig.update_layout(width=width, height=height)
    div = to_html(fig)
    return div

def no_of_tweets_graph(dates):
    dates_list = []
    for i in dates:
      a,b = str(i).split(' ')
      dates_list.append(a)
    dates_list.sort()
    date_list = []
    for i in dates_list:
      a,b,c = i.split('-')
      date_list.append(c+'-'+b+'-'+a)
    c = Counter(date_list)
    y = [int(i) for i in list(c.values())]
    x = list(c.keys())
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.update_layout(xaxis_title='Tweet Date',yaxis_title='No.of.Tweets')
    div = to_html(fig)
    return div

def highest_likes_on_a_day(dates,likes_cnt):
    likes = {}
    for i in range(len(dates)):
      a,b = str(dates[i]).split(' ')
      if a not in likes.keys():
        likes[a] = likes_cnt[i]
      else:
        if likes[a] < likes_cnt[i]:
          likes[a] = likes_cnt[i]
    sorted_likes = collections.OrderedDict(sorted(likes.items()))
    fig = go.Figure(data=go.Scatter(x=list(sorted_likes.keys()),y=list(sorted_likes.values())))
    fig.update_layout(xaxis_title='Tweet Date',yaxis_title='No.of.Likes')
    div = to_html(fig)
    return div



