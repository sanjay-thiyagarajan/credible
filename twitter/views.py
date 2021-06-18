from django.shortcuts import render
from twitter.utils.twitter_sentiment_analysis import findusertweets, pie_chart, no_of_tweets_graph, highest_likes_on_a_day
import tweepy

def analysis(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username != '':
            try:
                df = findusertweets(user_name=username)
                summary = '. '.join(df['tweets'])
                bt_div, bt_status = pie_chart('behavioral-traits', summary)
                em_div, em_status = pie_chart('emotional-traits', summary)
                if bt_status == 'ERROR' or em_status == 'ERROR':
                    return render(request, 'twitter/tweet-results.html', {'error': 'Sorry :( We don\'t have enough information to run the prediction for this username'})
                else:
                    return render(request, 'twitter/tweet-results.html', {'bt_div':bt_div, 'em_div':em_div})
            except tweepy.TweepError as e:
                return render(request, 'twitter/tweet-results.html', {'error': 'Sorry :( The provided username doesn\'t exist. Please check and reach back'})        
                
    return render(request, 'twitter/tweet-analysis.html')

def tweet_results(request):
    return render(request, 'twitter/tweet-results.html')
