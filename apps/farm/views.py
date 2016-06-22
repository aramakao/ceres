#-*- encoding: utf-8 -*-
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.template.response import TemplateResponse
from apps.account.models import User, LoggedInMixin, Profile, getStateUser, StateUser, StateUserComment
from .models import *
from .forms import *
from apps.ceres.processors import haveFarm, getFarmUser
from apps.account.forms import StateUserForm, StateUserCommentForm
import json
from apps.ceres.processors import getUserFullName
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core import serializers
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

class MyFarm(LoggedInMixin,TemplateView):
    '''This view shows the status and can publish status'''
    template_name='farm/home.html'

    def get_context_data(self, **kwargs):
    	context = super(MyFarm, self).get_context_data(**kwargs)
    	context['farmer_profile']=get_object_or_404(Profile,user=self.request.user)
        context['state_form'] = StateUserForm()
        context['comments_form'] = StateUserCommentForm()
        context['admin']=True
        paginator = Paginator(getStateUser(self.request.user),10)
        context['status']=paginator.page(1)
        if 'page' in self.request.GET:
            page = self.request.GET.get('page')
            try:
                context['status'] = paginator.page(page)
            except PageNotAnInteger:
                context['status'] = paginator.page(1)
            except EmptyPage:
                context['status'] = paginator.page(paginator.num_pages)
    	return context

    def post(self, request, *args, **kwargs):
        '''This function allows create, delete and comment status'''
        for key in request.POST:
            if key.startswith('btn_delete:'):
                delete =  key[11:]
                state=StateUser.objects.get(id=delete)
                state.delete()
                messages.success(self.request, 'Publicación borrada!')
        if 'btn_state' in request.POST:
            text = request.POST['text']
            if 'picture' in request.FILES:
                state = StateUser(user=request.user,text=text,picture=request.FILES['picture'])
            else:
                state = StateUser(user=request.user,text=text)
            state.save()
            messages.success(self.request, 'Publicación exitosa!')
        if 'btn_comments' in request.POST:
            text = request.POST['text']
            state = request.POST['state']
            if 'picture' in request.FILES:
                state = StateUserComment(state_id=state,user=request.user,text=text,picture=request.FILES['picture'])
            else:
                state = StateUserComment(state_id=state,user=request.user,text=text)
            state.save()
            messages.success(self.request, 'Publicación exitosa!')
        return redirect('mi_agro')

@login_required
def farmSuccess(request):
    '''This function shows if the farm was created'''
    if haveFarm(request.user)==True:
		template_name='farm/farm_success.html'
		return TemplateResponse(request,template_name,{})
    else:
        return redirect('register_farm')

class RegisterFarm(LoggedInMixin,CreateView):
    '''This view allows register a farm'''
    template_name ='farm/register_farm.html'
    model = Farm
    form_class = FarmForm
    success_url = reverse_lazy('farm_success')

    def dispatch(self, request, *args, **kwargs):
        '''This function checks if the user have a farm'''
        if haveFarm(self.request.user):
            return redirect('mi_agro')
        else:
            return super(RegisterFarm, self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        '''This function checks if the form is valid before save it'''
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        phone = form.cleaned_data['phone']
        Farm(name=name, address=address, phone=phone, user=self.request.user).save()
        return redirect('farm_success')

class MyFarmUpdateView(LoggedInMixin,TemplateView):
    '''This view allows update the farm information'''
    template_name = 'farm/my_farm.html'

    def get_context_data(self,**kwargs):
        '''This function returns the farm if the user have one'''
        context = super(MyFarmUpdateView,self).get_context_data(**kwargs)
        farm = Farm.objects.get(user=self.request.user)
        profile = FarmProfile.objects.get(farm=farm)
        context['form_farm']=FarmForm(self.request.POST or None,instance=farm)
        context['form_profile']=FarmProfileForm(self.request.POST or None, instance=profile)
        return context

    def post(self,request,*args,**kwargs):
        '''This function save the information'''
        try:
            context = self.get_context_data()
            if context["form_farm"].is_valid() and context["form_profile"].is_valid():
                context["form_farm"].save()
                context["form_profile"].save()
                messages.success(self.request, 'La información de tu granja se ha actualizado!')
            else:
                messages.error(self.request, 'Por favor revisa tu información!')
            return HttpResponseRedirect(reverse_lazy('my_farm'))
        except Exception as e:
            messages.error(self.request, 'Tenemos un problema en el servidor!')
            return HttpResponseRedirect(reverse_lazy('my_farm'))

class DeactivateFarmView(LoggedInMixin,TemplateView):
    '''This view allows deactivate a farm'''
    template_name = 'farm/deactivate_farm.html'
    success_url = reverse_lazy('deactivate_farm')

    def post(self,request):
        '''This function deactive the farm'''
        messages.success(self.request, 'Tu granja ha sido desactivada!')
        farm=getFarmUser(self.request.user)
        farm.is_active=False
        farm.save()
        return redirect('activate_farm')

    def dispatch(self, request, *args, **kwargs):
        '''This function checks if the user have a farm'''
        _haveFarm=haveFarm(self.request.user)
        if _haveFarm:
            farm=getFarmUser(self.request.user)
            if farm.is_active:
                return super(DeactivateFarmView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('activate')
        else:
            return super(RegisterFarm, self).dispatch(request, *args, **kwargs)

class ActivateFarmView(LoggedInMixin,TemplateView):
    '''This view active a farm'''
    template_name = 'farm/activate_farm.html'
    success_url = reverse_lazy('activate_farm')

    def post(self,request):
        '''This function active the farm'''
        messages.success(self.request, 'Tu granja ha sido activada!')
        farm=getFarmUser(self.request.user)
        farm.is_active=True
        farm.save()
        return redirect('activate_farm')

    def dispatch(self, request, *args, **kwargs):
        '''This fucntion checks if the user hava a farm'''
        _haveFarm=haveFarm(self.request.user)
        if _haveFarm:
            farm=getFarmUser(self.request.user)
            if not farm.is_active:
                return super(ActivateFarmView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('deactivate_farm')
        else:
            return super(RegisterFarm, self).dispatch(request, *args, **kwargs)

def changePictureProfile(request):
    '''This function allows change the logo'''
    if request.is_ajax():
        farm=Farm.objects.get(user=request.user)
        farm.logo=request.FILES['file_upload']
        farm.save()
        return HttpResponse(farm.logo.url, content_type="text/plain")
    else:
        raise Http404

def changePictureBanner(request):
    '''This function changes the banner picture'''
    if request.is_ajax():
        farm=FarmProfile.objects.get(farm__user=request.user)
        farm.banner=request.FILES['file_upload']
        farm.save()
        return HttpResponse(farm.banner.url, content_type="text/plain")
    else:
        raise Http404
