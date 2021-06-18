from django.shortcuts import render
from twitter.utils.twitter_sentiment_analysis import pie_chart, sentiment_gauge


def analysis(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        if input_text != '':
            gauge_div = sentiment_gauge(input_text)
            bt_div = pie_chart('behavioral-traits', input_text)
            em_div = pie_chart('emotional-traits', input_text)
            ip_div = pie_chart('iptc', input_text)
            return render(request, 'personality/sentiment-results.html', {'gauge_div':gauge_div, 'bt_div':bt_div,
            'em_div':em_div, 'ip_div':ip_div})

    return render(request, 'personality/sentiment-analysis.html')
