from expertai.nlapi.cloud.client import ExpertAiClient
from google_play_scraper import app
import re
import plotly.graph_objects as go
from plotly.io import to_html
import numpy as np

def clean_review(review):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", review).split())


def fetchreviews(applink):  
  result = app(applink,lang='en', country='us')
  return result

def Review_pie(cleaned_reviews):
  Sentiment = {'Positive':int(0),'Negative':int(0)}
  for review in cleaned_reviews:  
    client = ExpertAiClient()
    document = client.specific_resource_analysis(
    body={"document": {"text": review}}, 
    params={'language': 'en', 'resource': 'sentiment'})
    if document.sentiment.overall>0:
      Sentiment['Positive'] += 1
    else:
      Sentiment['Negative'] += 1
  val = list(Sentiment.values())
  values = ((val[0]*100)/(val[0]+val[1])),((val[1]*100)/(val[0]+val[1]))  
  fig = go.Figure(data=[go.Pie(labels=list(Sentiment.keys()), values=values, textinfo='label',hole=0,marker= dict(colors=['#16c928','#fc0000']),title='Reviews')])
  div = to_html(fig)
  return div

def histo_graph(result):
  sizes = np.divide(result, 700)
  fig = go.Figure(data=go.Scatter(x=[1,2,3,4,5],y=result, 
  mode="markers",
  marker=dict(
        color=list(sizes),
        showscale=False,
  size=list(sizes))
  ))
  fig.update_layout(xaxis_title='Ratings',yaxis_title='No.of.Users')
  div = to_html(fig)
  return div

def pie_chart(taxonomy,summary):
  client = ExpertAiClient()
  language= 'en'
  output = client.classification(body={"document": {"text": summary}}, params={'taxonomy': taxonomy, 'language': language})
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
  return div