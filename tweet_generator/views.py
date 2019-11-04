from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.forms import Form

from tweet_generator.static.script.dictogram import Dictogram
import re


class IndexPage(TemplateView):
    template_name = "index.html"

class Generators(TemplateView):
    template_name = 'generators.html'

def generator_display(request):
    with open('tweet_generator/static/data/meditations-hist.txt') as file:
        meditations_dict = {}
        for line in file.readlines():
            data = line.split(':')
            num = re.sub('\n', '', data[1])
            meditations_dict[data[0]] = int(num)
        histogram = Dictogram(words_dict=meditations_dict)
        sentence = ' '.join([histogram.sample() for _ in range(0, 20)])
    return render(request, 'generator_display.html', {'sentence': sentence})