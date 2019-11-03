from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

class IndexPage(TemplateView):
    template_name = "index.html"

class Generators(TemplateView):
    template_name = 'generators.html'
