from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.forms import Form

from tweet_generator.models import MarkovChain
from tweet_generator.static.script.dicto_chain.dicto_chain import DictoChain
import re


class IndexPage(TemplateView):
    template_name = "tweeter/index.html"

class Generators(TemplateView):
    template_name = 'tweet_generator/generators.html'

class CreateGenerator(TemplateView):
    template_name = 'tweet_generator/create_generator.html'

def add_generator(request):
    """Add a new generator to the database"""
    if request.method == 'POST':
        generator_name = request.POST['name']
        generator_file = request.FILES['file']
        if MarkovChain.objects.count() < 30 and generator_name and generator_file \
            and MarkovChain.objects.get(name=generator_name) == None:
            # Get tokens from the uploded file
            tokens = generator_file.read().decode('ascii').split()

            # Create the words list from temporary file
            words_list = [re.sub(r'([^a-z])', ' ', token.lower()) for token in tokens if token != '  ']

            # Create markov chain from words list
            data = {}
            for index, word in enumerate(words_list):
                # Check if its at the last word of the list
                if index+1 < len(words_list):
                    next_word = words_list[index+1]
                else:
                    next_word = None

                # If not add the next word to the chain
                if next_word is None:
                    pass
                elif word not in data:
                    data[word] = {next_word:1}
                elif next_word not in data[word]:
                    data[word][next_word] = 1
                elif next_word in data[word]:
                    data[word][next_word] += 1

            generator = MarkovChain.objects.create(name=generator_name, data=data)
            # generator.save()
            return redirect('/generators/')
        elif MarkovChain.objects.count() > 30:
            return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': f"Sorry, the mas number of generators has been \
                 reached {MarkovChain.objects.count()}" })
        elif MarkovChain.objects.get(name=generator_name):
            return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': f"Sorry, the name given already exist" })
        else:
            return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': f"Sorry, an error accured while retrieving your data" })
    else:
        return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': "Sorry, a post request was not recieved" })

def generator_display(request):
    with open('tweet_generator/static/data/processed_meditations.txt') as file:
        words_list = file.read().split()
        print(words_list[:5])
        meditations_markov_chain = DictoChain(words_list)
        sentence = meditations_markov_chain.walk(10)
    return render(request, 'tweet_generator/generator_display.html', {'sentence': sentence})