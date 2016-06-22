#-*- encoding: utf-8 -*-
from django import forms
from .models import *

class UserRegisterForm(forms.ModelForm):
    '''This form belongs to the user model for the register'''
    class Meta:
        model=User
        fields=('username','email','password')
        widgets={
            'username':forms.TextInput(attrs=
                {'class':'form-control','placeholder':'Usuario','required':'True'}),
            'email':forms.TextInput(attrs=
                {'class':'form-control',
                'type':'email','placeholder':'Correo Electrónico','required':'True'}),
            'password':forms.TextInput(attrs=
                {'class':'form-control password',
                'type':'password','placeholder':'Contraseña','required':'True'}),
        }

class LoginForm(forms.Form):
    '''This form login'''
    username = forms.CharField(max_length=40,widget=forms.TextInput(attrs=
        {'class':'form-control','placeholder':'Usuario','required':'True'}))
    password = forms.CharField(max_length=40,widget=forms.TextInput(attrs=
        {'class':'form-control pass_login',
        'type':'password','placeholder':'Contraseña','required':'True'}))

class ResetPasswordForm(forms.Form):
    '''This form shows an email field for change the password'''
    email = forms.CharField(max_length=40,widget=forms.TextInput(attrs=
        {'class':'form-control','type':'email','placeholder':'Correo Electrónico','required':'True'}))


class UserForm(forms.ModelForm):
    '''This form belongs to the user model'''
    class Meta:
        model = User
        fields=('email','first_name','last_name')
        widgets={
            'email':forms.TextInput(attrs=
                {'class':'form-control','type':'email','required':'True'}),
            'first_name':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
            'last_name':forms.TextInput(attrs=
                {'class':'form-control','required':'True'}),
        }

class UpdatePasswordForm(forms.Form):
    '''This form allows update the password'''
    old_password = forms.CharField(
        max_length = 20,
        widget=forms.TextInput(attrs={
            'type':'password',
            'placeholder':'Antigua contraseña',
            'class' : 'form-control'}))
    new_password1 = forms.CharField(
        max_length = 20,
        widget=forms.TextInput(attrs={
            'type':'password',
            'placeholder':'Nueva contraseña',
            'class' : 'form-control'}))
    new_password2 = forms.CharField(
        max_length = 20,
        widget=forms.TextInput(attrs={
            'type':'password',
            'placeholder':'Confirmar contraseña',
            'class' : 'form-control'}))

    def clean(self):
        '''this function checks the new password with the old password'''
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                raise forms.ValidationError(("Las contraseñas no son iguales."))
        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    '''This form allows change the password'''
    password = forms.CharField(
        max_length = 20,
        widget=forms.TextInput(attrs={
            'type':'password',
            'placeholder':'Contraseña',
            'class' : 'form-control'}))
    re_password = forms.CharField(
        max_length = 20,
        widget=forms.TextInput(attrs={
            'type':'password',
            'placeholder':'Confirmar Contraseña',
            'class' : 'form-control'}))

class ProfileForm(forms.ModelForm):
    '''This form allows update the user profile'''
    class Meta:
        model = Profile
        fields=('occupation','birth_day','gender','phone','mobile','address','twitter',
                'facebook','description','banner')
        widgets={
            'birth_day':forms.TextInput(attrs=
                {'class':'form-control form_date','type':'date','required':'True'}),
            'description':forms.Textarea(attrs=
                {'class':'form-control'}),
            'occupation':forms.Select(attrs=
                {'class':'form-control'}),
            'gender':forms.Select(attrs=
                {'class':'form-control','required':'True'}),
            'phone':forms.TextInput(attrs=
                {'class':'form-control'}),
            'mobile':forms.TextInput(attrs=
               {'class':'form-control'}),
            'address':forms.TextInput(attrs=
                {'class':'form-control'}),
            'twitter':forms.TextInput(attrs=
                {'class':'form-control'}),
            'facebook':forms.TextInput(attrs=
                {'class':'form-control'})
         }

class StateUserForm(forms.ModelForm):
    '''This form allows write a state'''
    class Meta:
        model = StateUser
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

class StateUserCommentForm(forms.ModelForm):
    '''This form allows comment a state'''
    class Meta:
        model = StateUserComment
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

class InivitationFriendForm(forms.ModelForm):
    '''This form allows send a friend request'''
    class Meta:
        model = InivitationFriend
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs=
            {'placeholder':'Escribe un comentario...',
            'class':'form-control',
            'rows':'2',
            'required':'True'})
        }

class FriendDeleteForm(forms.ModelForm):
    '''This form allows delete a friend'''
    class Meta:
        model = Friend
        fields = ('user',)
        widgets = {
            'user':forms.HiddenInput()
        }
