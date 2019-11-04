from django.urls import path
from tweet_generator.views import IndexPage, Generators, generator_display

app_name = 'tweet_generator'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('generators/', Generators.as_view(), name="generators"),
    path('generators/display', generator_display, name="generator_display")
]

