from django.shortcuts import redirect, render
from twitter.utils.twitter_sentiment_analysis import findusertweets, pie_chart
import tweepy

def analysis(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username != '':
            try:
                summary = findusertweets(user_name=username)
                bt_div, bt_status = pie_chart('behavioral-traits', summary)
                em_div, em_status = pie_chart('emotional-traits', summary)
                if bt_status == 'ERROR' or em_status == 'ERROR':
                    return render(request, 'twitter/tweet-results.html', {'error': 'Sorry :( We don\'t have enough information to run the prediction for this username'})
                else:
                    return render(request, 'twitter/tweet-results.html', {'bt_div':bt_div, 'em_div':em_div})
            except tweepy.TweepError as e:
                return render(request, 'twitter/tweet-results.html', {'error': 'Sorry :( We don\'t have enough information to run the prediction for this username'})        
                
    return render(request, 'twitter/tweet-analysis.html')

def tweet_results(request):
    return render(request, 'twitter/tweet-results.html')
