from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.forms import Form

from tweet_generator.models import Generator
from tweet_generator.static.script.dicto_chain.dicto_chain import DictoChain
import re


class IndexPage(TemplateView):
    template_name = "index.html"

class Generators(TemplateView):
    template_name = 'generators.html'

class CreateGenerator(TemplateView):
    template_name = 'create_generator.html'

def add_generator(request):
    """Add a new generator to the database"""
    if request.method == 'POST':
        generator_name = request.POST['name']
        generator_file = request.FILES['file']
        if Generator.objects.count() < 30 and generator_name and generator_file:
            generator = Generator.objects.create(name=generator_name, data={})
            # generator.save()
            return redirect('generators/')
        else:
            return render(request, 'create_generator.html', { 
                'error_message': f"Sorry, the mas number of generators has been reached {Generator.objects.count()}" })
    else:
        return render(request, 'create_generator.html', { 
                'error_message': "Sorry, a post request was not recieved" })

def generator_display(request):
    with open('tweet_generator/static/data/processed_meditations.txt') as file:
        words_list = file.read().split()
        print(words_list[:5])
        meditations_markov_chain = DictoChain(words_list)
        sentence = meditations_markov_chain.walk(10)
    return render(request, 'generator_display.html', {'sentence': sentence})