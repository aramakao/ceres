from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

def handler404(request):
    return render(request, '404.html')

class UnauthorizedAccessView(TemplateView):
    template_name = 'extras/unauthorizedAccess.html'

def loaderio(request):
    text='loaderio-5dfd6207ca10eaeb1ad15a1de5fa9482'
    return HttpResponse(text)

def google_site(request):
    text='google-site-verification: google21fafab3e80845e3.html'
    return HttpResponse(text)
