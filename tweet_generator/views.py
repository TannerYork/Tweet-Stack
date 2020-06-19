from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView
from django.forms import Form

from tweet_generator.models import MarkovChain
from tweet_generator.static.script.dicto_chain.dicto_chain import DictovChain
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
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
        context['col_two'] = [chains[index] if index < len(chains) else None for index in range(4, 8)]
        context['col_three'] = [chains[index] if index < len(chains) else None for index in range(8, 12)]
        return context

class CreateGenerator(TemplateView):
    template_name = 'tweet_generator/create_generator.html'

def add_generator(request):
    """Add a new generator to the database"""
    if request.method != 'POST':
        return render(request, 'tweet_generator/create_generator.html', { 
                'error_message': "Sorry, a post request was not recieved" })

    generator_name = request.POST['name']
    generator_file = request.FILES['file']
    generator_order = request.POST['order']
    if MarkovChain.objects.count() < 12 and generator_name and generator_file \
        and MarkovChain.objects.filter(name=generator_name).count() == 0:
        # Add start and stop tokens
        sentences = sent_tokenize(generator_file.read().decode())
        tokenized_corpus = ' '.join(f'*START {sent} *STOP' for sent in sentences)

        # Get tokens from the uploded file
        tokens = tokenized_corpus.split()

        # Create the words list from temporary file
        words_list = [re.sub(r'([^A-Za-z|\'|\.|_|-|*])', ' ', token).strip(' ') for token in tokens]
        
        # Create markov chain from words list
        markov_chain = DictovChain(words_list, int(generator_order))

        generator = MarkovChain.objects.create(name=generator_name, data=markov_chain,
                    start_tokens=markov_chain.start_tokens, order=generator_order)
        generator.save()
        return redirect('/generators/')
    elif MarkovChain.objects.count() >= 12:
        return render(request, 'tweet_generator/create_generator.html', { 
            'error_message': f"Sorry, the mas number of generators has been \
                reached. {MarkovChain.objects.count()} is the max." })
    elif MarkovChain.objects.filter(name=generator_name).count() > 0:
        return render(request, 'tweet_generator/create_generator.html', { 
            'error_message': f"Sorry, the name given already exist" })
    else:
        return render(request, 'tweet_generator/create_generator.html', { 
            'error_message': f"Sorry, an error accured while retrieving your data" })

def generator_display(request, chain_slug):
    chain = MarkovChain.objects.get(slug=chain_slug)
    sentence = chain.walk(30)
    return render(request, 'tweet_generator/generator_display.html', {'chain': chain, 'sentence': sentence})