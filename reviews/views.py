import dashboard
from django.shortcuts import render
from reviews.utils.app_review_sentiment_analysis import *
from twitter.utils.twitter_sentiment_analysis import sentiment_gauge
def analysis(request):
    if request.method == 'POST':
        applink = request.POST.get('applink')
        data = {}
        if applink != '':
            applink = applink[applink.index('=')+1:]
            result = fetchreviews(applink)
            cleaned_reviews = [clean_review(review) for review in result['comments']]
            summary = '. '.join(cleaned_reviews)
            review_pie_div = sentiment_gauge(summary[:10000])
            histo_div = histo_graph(result['histogram'])
            bt_div = pie_chart('behavioral-traits',summary[:10000])
            em_div = pie_chart('emotional-traits',summary[:10000])
            data = {
                'rev_div':review_pie_div,
                'histo_div':histo_div,
                'bt_div':bt_div,
                'em_div':em_div,
                'appname':result['title'], 
                'downloads':result['installs'],
                'genre':result['genre']
            }
            return render(request, 'reviews/app-results.html', data)
    return render(request, 'reviews/app-analysis.html')
