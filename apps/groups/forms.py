#-*- encoding: utf-8 -*-
from django import forms
from .models import *
from django.forms.models import inlineformset_factory

class GroupForm(forms.ModelForm):
    '''This form allows create and update a group'''
    class Meta:
        model=Group
        fields=('name','phone','address')
        widgets={
            'name':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
            'phone':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
            'address':forms.TextInput(attrs=
                {'class':'form-control','required':'True'})
        }

class GroupProfileForm(forms.ModelForm):
    '''This form allows create and update a group profile'''
    class Meta:
        model = GroupProfile
        fields = ('slogan','latitude','longitude','location')
        widgets ={
            'slogan':forms.TextInput(attrs=
            {'class':'form-control'}),
            'latitude':forms.HiddenInput(),
            'longitude':forms.HiddenInput(),
            'location':forms.HiddenInput()
        }

class StateGroupForm(forms.ModelForm):
    '''This form allows create status'''
    class Meta:
        model = StateGroup
        fields = ('text','picture')
        widgets = {
            'text':forms.Textarea(attrs=
            {'placeholder':'Qué estás haciendo?',
            'class':'form-control',
            'rows':'2',
            'required':'True'}),
            'picture':forms.FileInput(attrs=
            {'accept':'image/*'})
        }

class StateGroupCommentForm(forms.ModelForm):
    '''This form allows create comments'''
    class Meta:
        model = StateGroupComment
        fields = ('text','picture','state')
        widgets = {
            'text':forms.Textarea(attrs=
            {'placeholder':'Escribe un comentario...',
            'class':'form-control',
            'rows':'2',
            'required':'True'}),
            'state':forms.HiddenInput(),
            'picture':forms.FileInput(attrs=
            {'accept':'image/*'})
        }

class InivitationGroupForm(forms.ModelForm):
    '''This form allows send invitations'''
    class Meta:
        model = InivitationGroup
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs=
            {'placeholder':'Escribe un comentario...',
            'class':'form-control',
            'rows':'2',
            'required':'True'})
        }
