from personality import views
from django.urls import path

urlpatterns = [
    path('', views.analysis, name='personality_analysis')
]
