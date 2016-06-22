from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models.loading import get_model

def comment(request):
    '''This function allows comment'''
    if request.is_ajax():
        message = request.POST['comment']
        id_object =  request.POST['id']
        model_name = request.POST['object']
        label = request.POST['label']
        model = get_model(label,model_name)
        ctype = ContentType.objects.get_for_model(model)
        Comment(sender=request.user, message=message, content_type=ctype, object_id=id_object).save()
        comments=Comment.objects.getComments(content_type=ctype, object_id=id_object)
        return HttpResponse(comments,content_type="application/json")
    else:
        return HttpResponse(':(', content_type="text/plain")

def getComments(request):
    '''This function returns comments'''
    if request.is_ajax():
        id_object =  request.GET['id']
        model_name = request.GET['object']
        label = request.GET['label']
        model = get_model(label,model_name)
        ctype = ContentType.objects.get_for_model(model)
        comments=Comment.objects.getComments(content_type=ctype, object_id=id_object)
        return HttpResponse(comments,content_type="application/json")
    else:
        return HttpResponse(':(noo', content_type="text/plain")
