from django.urls import path
from reviews import views
urlpatterns = [
    path('', views.analysis, name='app_analysis')
]
