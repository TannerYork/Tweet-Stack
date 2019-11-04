from django.urls import path
from tweet_generator.views import IndexPage, Generators, CreateGenerator, add_generator, generator_display

app_name = 'tweet_generator'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('generators/', Generators.as_view(), name="generators"),
    path('generators/new', CreateGenerator.as_view(), name="create_generator"),
    path('generators/new/create', add_generator, name="add_generator"),
    path('generators/display', generator_display, name="generator_display")
]

