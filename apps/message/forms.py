from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    '''This form allows create and update a message'''
    class Meta:
        model = Message
        fields = ('message','file')
        widgets = {
        'message':forms.Textarea(attrs=
            {'class':'form-control',
            'rows':'3',
            'placeholder':'Escribe un mensaje',
            'required':'True'})
        }

class MessageGroupForm(forms.ModelForm):
    '''This form allows create and update a group message'''
    class Meta:
        model = MessageGroup
        fields = ('message','file')
        widgets = {
        'message':forms.Textarea(attrs=
            {'class':'form-control',
            'rows':'3',
            'placeholder':'Escribe un mensaje',
            'required':'True'})
        }
