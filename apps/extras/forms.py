#-*- encoding: utf-8 -*-
from django import forms
from .models import *

class OccupationForm(forms.ModelForm):
    '''This form allows save and edit an occupation'''
    class Meta:
        model = Occupation
        fields = ('name',)
        widgets = {
            'name':forms.TextInput(attrs=
            {'class':'form-control','required':'True'})
        }
