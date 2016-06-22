#-*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from apps.account.models import LoggedInMixin
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse

class OccupationListView(LoggedInMixin,ListView):
	'''This class lists the occupations'''
	model = Occupation
	template_name = 'extras/occupation_list.html'
	paginate_by = 10
	context_object_name = 'occupations'

	def get_queryset(self):
		if self.request.user.is_superuser:
			return Occupation.objects.order_by('name')
		else:
			raise Http404

class OccupationCreateView(LoggedInMixin,CreateView):
	'''This class allows create an occupation'''
	model = Occupation
	template_name='extras/occupation_add.html'
	form_class=OccupationForm

	def post(self,request,*args,**kwargs):
		'''This function allows save an ocupation'''
		try:
			form=OccupationForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(self.request,"Has agreagado una nueva occupación")
				return HttpResponseRedirect(reverse('extras_app:occupations_list'))
			else:
				messages.error(self.request,"Tenemos un problema")
				return HttpResponseRedirect(reverse('extras_app:occupations_list'))
		except Exception as e:
			messages.error(self.request,"Tenemos un problema")
			return HttpResponseRedirect(reverse('extras_app:occupations_list'))

class OcupationUpdateView(LoggedInMixin,UpdateView):
	'''This class update an occupation'''
	model = Occupation
	template_name='extras/occupation_update.html'
	form_class=OccupationForm
	success_url = reverse_lazy('extras_app:occupations_list')

	def form_valid(self,form):
		messages.success(self.request,"Ocupación Actualizada")
		return super(OcupationUpdateView, self).form_valid(form)

	def get_form(self,form_class):
		if self.request.user.is_superuser:
			return form_class(**self.get_form_kwargs())
		else:
			raise Http404

class OccupationDeleteView(LoggedInMixin,DeleteView):
	'''This class allows delete an occupation'''
	model = Occupation
	success_url = reverse_lazy('extras_app:occupations_list')
	template_name = 'extras/occupation_delete.html'

    	def get_form(self,form_class):
            if self.request.user.is_superuser:
                return form_class(**self.get_form_kwargs())
            else:
                raise Http404
