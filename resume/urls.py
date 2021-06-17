from resume import views
from django.urls import path

urlpatterns = [
    path('', views.resume_analysis, name="resume_analysis")
]
