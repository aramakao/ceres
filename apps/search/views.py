from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

class Search(TemplateView):
    '''This view returns the search results'''
    template_name = 'search/index.html'

    def get(self, request, *args, **kwargs):
        '''This function get the word search and returns results'''
        context = self.get_context_data(**kwargs)
        if 'query' in request.GET:
            context['word']=request.GET['query']
            context['results']=Index.objects.search(word=request.GET['query'])
        return self.render_to_response(context)
