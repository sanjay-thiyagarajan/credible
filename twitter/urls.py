from django.urls import path
from twitter import views
urlpatterns = [
    path('', views.analysis, name="analysis"),
    path('results/', views.tweet_results, name="tweet_results")
]
