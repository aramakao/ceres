#-*- encoding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from apps.account.models import LoggedInMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import serializers
from apps.ceres.processors import haveFarm, getFarmUser
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
import json
from django.forms.models import model_to_dict
from itertools import chain

class ProductCreateView(LoggedInMixin,CreateView):
	'''This view allows create a product'''
	model = Product
	template_name='product/product_add.html'
	form_class=ProductForm

	def post(self,request,*args,**kwargs):
		'''This function checks if a form is valid before save it'''
		try:
			product_form=ProductForm(request.POST)
			if product_form.is_valid():
				name=product_form.cleaned_data['name']
				summary=product_form.cleaned_data['summary']
				category=product_form.cleaned_data['category']
				description=product_form.cleaned_data['description']
				price=product_form.cleaned_data['price']
				quantity=product_form.cleaned_data['quantity']
				farm=getFarmUser(self.request.user)
				product=Product(name=name, summary=summary, category=category, description=description, price=price, quantity=quantity,farm=farm)
				product.save()
				for image in request.FILES:
					imagen=ProductImage(product=product,image=request.FILES[image])
					imagen.save()
				messages.success(self.request,"Has agreagado {0} a tu lista de productos".format(product.name))
				return HttpResponseRedirect(reverse('product_app:product_list'))
			else:
				return HttpResponseRedirect(reverse('product_app:product_add'))
		except Exception as e:
			print e
			messages.error(self.request,"Tenemos un problema")
			return HttpResponseRedirect(reverse('product_app:product_add'))

class ProductUpdateView(LoggedInMixin,UpdateView):
	'''This view update a product'''
	model = Product
	template_name= 'product/product_edit.html'
	form_class = ProductForm
	success_url = reverse_lazy('product_app:product_list')

	def get_object(self,queryset=None):
		'''This function checks if the product belong to user'''
		obj = super(ProductUpdateView, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			return obj
		else:
			raise Http404("farm deactive")

	def post(self,request,*args,**kwargs):
		'''This function checks if the form is valid before save it'''
		try:
			product=Product.objects.get(slug=kwargs['slug'])
			product_form=ProductForm(request.POST)
			if product_form.is_valid():
				product.name=product_form.cleaned_data['name']
				product.summary=product_form.cleaned_data['summary']
				product.category=product_form.cleaned_data['category']
				product.description=product_form.cleaned_data['description']
				product.price=product_form.cleaned_data['price']
				product.quantity=product_form.cleaned_data['quantity']
				product.save()
				messages.success(self.request,"Has actualizado {0} correctamente".format(product.name))
			else:
				messages.error(self.request,"Tenemos un problema!")

			for key in request.POST:
				if key.startswith('btn_img'):
						imagen_id = key[7:]
						ProductImage.objects.get(id=imagen_id,product__farm__user=request.user).delete()
			if request.FILES:
				for image in request.FILES:
					imagen=ProductImage(product=product,image=request.FILES[image])
					imagen.save()
			return HttpResponseRedirect(reverse('product_app:product_list'))

		except Exception as e:
			messages.error(self.request,"Tenemos un problema!")
			return HttpResponseRedirect(reverse('product_app:product_edit', kwargs={'slug':product.slug}))

class ProductDeleteView(LoggedInMixin,DeleteView):
	'''This view delete a product'''
	model = Product
	success_url = reverse_lazy('product_app:product_list')

	def get_object(self,queryset=None):
		'''This function checks if a product belong to user'''
		obj = super(ProductDeleteView, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			return obj
		else:
			raise Http404("farm deactive")

class ProductDetailView(LoggedInMixin,DetailView):
	'''This views allows view a product'''
	model = Product
	context ='product'

	def get_object(self,queryset=None):
		'''This function checks if a product belong to user'''
		obj = super(ProductDetailView, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			else:
				return obj
		else:
			raise Http404("farm deactive")

class ProductListView(LoggedInMixin,ListView):
	'''This views returns a list of products'''
	model = Product
	template_name='product/product_list.html'
	paginate_by = 10
	context_object_name = 'products'

	def get_queryset(self):
		'''This function checks if the farm is active and filter the products by user'''
		if haveFarm(self.request.user)==True:
			farm=getFarmUser(self.request.user)
			if farm.is_active:
				return Product.objects.filter(farm=farm).order_by('name')
			else:
				raise Http404("farm deactive")
		else:
			return redirect('register_farm')

class ProductCategoryListView(LoggedInMixin,ListView):
	'''This view lists the product categories'''
	model = ProductCategory
	template_name = 'product/category_list.html'
	paginate_by = 10
	context_object_name = 'categories'

	def get_queryset(self):
		'''This function checks if the user is superuser'''
		if self.request.user.is_superuser:
			return ProductCategory.objects.order_by('name')
		else:
			raise Http404

class ProductCategoryCreateView(LoggedInMixin,CreateView):
	'''This view allows create a category'''
	model = ProductCategory
	template_name='product/category_add.html'
	form_class=ProductCategoryForm

	def post(self,request,*args,**kwargs):
		'''This function checks if the form is valid before save it'''
		try:
			form=ProductCategoryForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				messages.success(self.request,"Has agreagado una nueva categoría")
				return HttpResponseRedirect(reverse('product_app:category'))
			else:
				messages.error(self.request,"Tenemos un problema")
				return HttpResponseRedirect(reverse('product_app:category_add'))
		except Exception as e:
			messages.error(self.request,"Tenemos un problema")
			return HttpResponseRedirect(reverse('product_app:category_add'))

	def get_form(self,form_class):
		'''This function checks if the user is superuser'''
		if self.request.user.is_superuser:
			return form_class(**self.get_form_kwargs())
		else:
			raise Http404

class ProductCategoryUpdateView(LoggedInMixin,UpdateView):
	'''This views allows update a category'''
	model = ProductCategory
	template_name='product/category_update.html'
	form_class=ProductCategoryForm
	success_url = reverse_lazy('product_app:category')

	def form_valid(self,form):
		'''This function checks if the form is valid before save it'''
		messages.success(self.request,"Categoría Actualizada")
		return super(ProductCategoryUpdateView, self).form_valid(form)

	def get_form(self,form_class):
		'''This function checks if the user is superuser'''
		if self.request.user.is_superuser:
			return form_class(**self.get_form_kwargs())
		else:
			raise Http404

class ProductCategoryDelete(LoggedInMixin,DeleteView):
	'''This view allows delete a category'''
	model = ProductCategory
	success_url = reverse_lazy('product_app:category')
	template_name = 'product/category_delete.html'

	def get_form(self,form_class):
		'''This function checks if the user is superuser'''
		if self.request.user.is_superuser:
			return form_class(**self.get_form_kwargs())
		else:
			raise Http404

def updateMyProductsGroup(request):
	'''This function allows update the products of the group'''
	if request.is_ajax:
		state = request.POST['state']
		product = request.POST['product']
		group = request.POST['group']
		if request.method=='POST':
			if state=='false':
				productGroup=ProductsGroup.objects.get(product_id=product,group_id=group)
				productGroup.delete()
			else:
				productGroup=ProductsGroup(product_id=product,group_id=group)
				productGroup.save()
	else:
		data=False
	return HttpResponse("Producto agreagado con exito!", content_type="text/plain")

def updateActiveProduct(request):
	'''This function allows change the state of the product'''
	if request.is_ajax:
		state = request.POST['state']
		product_id = request.POST['product']
		product=Product.objects.get(id=product_id)
		if request.method=='POST':
			if product.farm.user==request.user:
				if state=='false':
					product.is_active=False
				else:
					product.is_active=True
				product.save()
	else:
		data=False
	return HttpResponse("Producto agreagado con exito!", content_type="text/plain")
