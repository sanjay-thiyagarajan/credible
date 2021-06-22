from django.shortcuts import render
from twitter.utils.twitter_sentiment_analysis import findusertweets, pie_chart, no_of_tweets_graph, highest_likes_on_a_day, sentiment_gauge
import tweepy

def analysis(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username != '':
            try:
                df = findusertweets(user_name=username)
                summary = '. '.join(df['tweets'])
                g1_div = no_of_tweets_graph(df['date'])
                g2_div = highest_likes_on_a_day(df['date'],df['likes'])
                bt_div, bt_status, bt_dict, bt_ids = pie_chart('behavioral-traits', summary[:10000])
                em_div, em_status = pie_chart('emotional-traits', summary[:10000])
                iptc_div, iptc_status = pie_chart('iptc', summary[:10000])
                sent_div = sentiment_gauge(summary[:10000])
                if bt_status == 'ERROR' or em_status == 'ERROR' or iptc_status == 'ERROR':
                    return render(request, 'twitter/tweet-results.html', {'error': 'Sorry :( We don\'t have enough information to run the prediction for this username.'})
                else:
                    return render(request, 'twitter/tweet-results.html', {'bt_div':bt_div, 'em_div':em_div, 'g1_div':g1_div, 'g2_div':g2_div, 'iptc_div':iptc_div, 'sent_div':sent_div, 'username':username, 'bt_dict':bt_dict, 'bt_ids':bt_ids})
            except tweepy.TweepError as e:
                return render(request, 'twitter/tweet-results.html', {'error': 'Sorry :( The provided username doesn\'t exist. Please check and reach back.'})        
                
    return render(request, 'twitter/tweet-analysis.html')

def tweet_results(request):
    return render(request, 'twitter/tweet-results.html')
