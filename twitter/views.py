from django.shortcuts import redirect, render
from twitter.utils.twitter_sentiment_analysis import findusertweets, pie_chart

def analysis(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username != '':
            summary = findusertweets(user_name=username)
            bt_div = pie_chart('behavioral-traits', summary)
            em_div = pie_chart('emotional-traits', summary)
            return render(request, 'twitter/tweet-results.html', {'bt_div':bt_div, 'em_div':em_div})
    return render(request, 'twitter/tweet-analysis.html')

def tweet_results(request):
    return render(request, 'twitter/tweet-results.html')
