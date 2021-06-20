from django.shortcuts import render
import requests
from pdfminer.high_level import extract_text
from twitter.utils.twitter_sentiment_analysis import pie_chart, sentiment_gauge
from resume.utils.resume_parser import extract_education, extract_email, extract_name, extract_skills, extract_mobile_number
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
            education = "na"
            email = "na"
            skills = "na"
            mobile_number = "na"
            if url_input:
                input_file = requests.get(url_input, stream=True)
                extracted_text = extract_text(io.BytesIO(input_file.content))
            elif file_input:
                input_file = file_input
                extracted_text = extract_text(io.BytesIO(input_file.read()))
            name = extract_name(extracted_text)
            education = extract_education(extracted_text)
            email = extract_email(extracted_text)
            skills = extract_skills(extracted_text)
            mobile_number = extract_mobile_number(extracted_text)
            resume_pie_div = pie_chart('iptc', extracted_text)
            bt_pie_div = pie_chart('behavioral-traits', extracted_text)
            em_div = pie_chart('emotional-traits', extracted_text)
            sent_div = sentiment_gauge(extracted_text, width=620, height=620)
            data = {
                'Name': name,
                'Education':education,
                'Email':email,
                'Skills':skills,
                'Mobile_number':mobile_number,
            }
            div_data = {
                'bt_div':bt_pie_div, 
                'res_div': resume_pie_div,
                'em_div': em_div,
                'sent_div':sent_div
                }
            return render(request, 'resume/resume-results.html',{'data':data, 'div_data': div_data})
                
    return render(request, 'resume/select.html') 
