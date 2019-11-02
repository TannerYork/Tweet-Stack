from django.urls import path
from tweet_generator.views import GeneratorOptions

app_name = 'tweet_generator'
urlpatterns = [
    path('', GeneratorOptions.as_view(), name='index')
]

