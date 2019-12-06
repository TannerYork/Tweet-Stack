from django.urls import path
from sentiment_analysis.views import SearchView, sentiment_view

app_name = 'sentiment_analysis'
urlpatterns = [
    path('search/', SearchView.as_view(), name="search-view"),
    path('sentiment/', sentiment_view, name="sentiment-view")
]