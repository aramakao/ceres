#-*- encoding: utf-8 -*-
from django import forms
from .models import *

class AskForm(forms.ModelForm):
    class Meta:
        model=ProductComments
        fields=('ask',)
        widgets={
            'ask':forms.Textarea(attrs=
                {'class':'form-control  box-comment',
                'placeholder':'Escribe tu pregunta...',
                'rows':3,'required':'True'})
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model=ProductComments
        fields=('reply',)
        widgets={
            'reply':forms.Textarea(attrs=
                {'class':'form-control',
                'placeholder':'Escribe tu respuesta...',
                'rows':3})
        }

class ShippingOptionForm(forms.ModelForm):
    class Meta:
        model = ShippingOption
        fields = ('name','detail','price','porcentage')
        widgets = {
            'name':forms.TextInput(attrs=
                {'class':'form-control',
                'required':'True'}),
            'detail':forms.Textarea(attrs=
                {'class':'form-control',
                'placeholder':'Notas adicionales...',
                'rows':3,
                'required':'True'}),
            'price':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
            'porcentage':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
        }

class PayentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment','description')
        widgets = {
            'payment':forms.Select(attrs=
            {'class':'form-control',
            'required':'True'}),
            'description':forms.Textarea(attrs=
            {'class':'form-control',
            'placeholder':'Escribe una descripción...',
            'rows':3,
            'required':'True'})
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('neighborhood','address','city','phone','description')
        widgets = {
            'neighborhood':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
            'address':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
            'city':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
            'phone':forms.TextInput(attrs=
            {'class':'form-control','required':'True'}),
            'description':forms.Textarea(attrs=
            {'class':'form-control',
            'placeholder':'Notas adicionales...',
            'rows':3,'required':'True'})
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ('state',)
        widgets = {
            'state':forms.Select(attrs=
            {'class':'form-control'})
        }

class FeedbackSellerForm(forms.ModelForm):
    class Meta:
        model = FeedbackSeller
        fields = ('observations','quickness', 'responsibility','communication' )
        widgets ={
            'communication':forms.TextInput(attrs={
            'class':'feedback'}),
            'quickness':forms.TextInput(attrs={
            'class':'feedback'}),
            'responsibility':forms.TextInput(attrs={
            'class':'feedback'}),
            'observations':forms.Textarea(attrs={
            'class':'form-control',
            'placeholder':'Observaciones...',
            'rows':3,
            'required':'True'
            })
        }

class ReplyFeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackSeller
        fields = ('reply',)
        widgets = {
            'reply':forms.Textarea(attrs={
            'class':'form-control',
            'placeholder':'Respuesta...',
            'rows':3,
            'required':'True'
            })
        }
class FeedbackProductForm(forms.ModelForm):
    class Meta:
        model = FeedbackProduct
        fields = ('comment','price', 'description','quality' )
        widgets ={
            'quality':forms.TextInput(attrs={
            'class':'feedback'}),
            'price':forms.TextInput(attrs={
            'class':'feedback'}),
            'description':forms.TextInput(attrs={
            'class':'feedback'}),
            'comment':forms.Textarea(attrs={
            'class':'form-control',
            'placeholder':'Observaciones...',
            'rows':3,
            'required':'True'
            })
        }
