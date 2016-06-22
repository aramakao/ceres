#-*- encoding: utf-8 -*-
from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    '''This form allows update and create products'''
    class Meta:
        model=Product
        fields=('category','name','summary','description','price','quantity')
        widgets={
        'name':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
        'summary':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
        'description':forms.Textarea(attrs=
            {'class':'form-control'}),
        'category':forms.Select(attrs=
            {'class':'form-control','required':'True'}),
        'price':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
        'quantity':forms.TextInput(attrs=
            {'class':'form-control','required':'True'})
        }

class ProductCategoryForm(forms.ModelForm):
    '''This form allows update and create product categories'''
    class Meta:
        model = ProductCategory
        fields = ('name','image','icon','icon_color')
        widgets = {
            'name':forms.TextInput(attrs=
            {'class':'form-control','required':'True'})
        }
