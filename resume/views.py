from django.shortcuts import render
import requests
from pdfminer.high_level import extract_text
from twitter.utils.twitter_sentiment_analysis import pie_chart
import io
def resume_analysis(request):
    if request.method == 'POST':
        url_input = request.POST.get('url_input')
        file_input = request.FILES.get('file_input')
        if (url_input == '') and (file_input == ''):
            return render(request, 'resume/select.html', {'error': 'Please choose the image in either of the two formats'})
        else:
            input_file = None
            extracted_text = None
            if url_input:
                input_file = requests.get(url_input, stream=True)
                extracted_text = extract_text(io.BytesIO(input_file.content))
            elif file_input:
                input_file = file_input
                extracted_text = extract_text(io.BytesIO(input_file.read()))
            resume_pie_div = pie_chart('iptc', extracted_text)
            bt_pie_div = pie_chart('behavioral-traits', extracted_text)
            return render(request, 'resume/resume-results.html', {'bt_div':bt_pie_div, 'res_div':resume_pie_div})
                
    return render(request, 'resume/select.html') 
