from django import forms
from .models import Farm, FarmProfile

class FarmForm(forms.ModelForm):
    '''This form allows create and update a farm'''
    class Meta:
        model=Farm
        fields=('name','address','phone')
        widgets={
            'name':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
            'address':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
            'phone':forms.TextInput(attrs=
                {'class':'form-control','required':'True'})
        }

class FarmProfileForm(forms.ModelForm):
    '''This form allows update the farm profile'''
    class Meta:
        model = FarmProfile
        fields=('slogan','facebook','twitter','banner','latitude','longitude','location', 'web_site')
        widgets={
            'slogan':forms.TextInput(attrs=
                {'class':'form-control'}),
            'facebook':forms.TextInput(attrs=
                {'class':'form-control'}),
            'twitter':forms.TextInput(attrs=
                {'class':'form-control'}),
            'web_site':forms.TextInput(attrs=
                {'class':'form-control'}),
            'latitude':forms.HiddenInput(),
            'longitude':forms.HiddenInput(),
            'location':forms.HiddenInput(),
            }
