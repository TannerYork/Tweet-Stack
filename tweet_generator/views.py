from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView
from django.forms import Form

from tweet_generator.models import MarkovChain
from tweet_generator.static.script.dicto_chain.dicto_chain import DictoChain
import re


class IndexPage(TemplateView):
    template_name = "tweeter/index.html"

class Generators(ListView):
    model = MarkovChain
    template_name = 'tweet_generator/generators.html'
    queryset = MarkovChain.objects.all()
    context_object_name = 'chain'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chains = MarkovChain.objects.all()
        context['col_one'] = [chains[index] if index < len(chains) else None for index in range(0, 4)]
        context['col_two'] = [chains[index] if index < len(chains) else None for index in range(5, 9)]
        context['col_three'] = [chains[index] if index < len(chains) else None for index in range(10, 14)]
        return context

class CreateGenerator(TemplateView):
    template_name = 'tweet_generator/create_generator.html'

def add_generator(request):
    """Add a new generator to the database"""
    if request.method == 'POST':
        generator_name = request.POST['name']
        generator_file = request.FILES['file']
        if MarkovChain.objects.count() < 15 and generator_name and generator_file \
            and MarkovChain.objects.filter(name=generator_name).count() == 0:
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

            dictogram = {}
            for word in words_list:
                if word in dictogram:
                    dictogram[word] += 1
                else:
                    dictogram[word] = 1

            generator = MarkovChain.objects.create(name=generator_name, data=data, dictogram=dictogram)
            generator.save()
            return redirect('/generators/')
        elif MarkovChain.objects.count() > 15:
            return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': f"Sorry, the mas number of generators has been \
                 reached {MarkovChain.objects.count()}" })
        elif MarkovChain.objects.filter(name=generator_name).count() > 0:
            return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': f"Sorry, the name given already exist" })
        else:
            return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': f"Sorry, an error accured while retrieving your data" })
    else:
        return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': "Sorry, a post request was not recieved" })

def generator_display(request, chain_slug):
    chain = MarkovChain.objects.get(slug=chain_slug)
    sentence = chain.walk(10)
    return render(request, 'tweet_generator/generator_display.html', {'chain': chain, 'sentence': sentence})