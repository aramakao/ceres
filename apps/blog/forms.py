from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    '''This form allows edit and create a blog entry'''
    class Meta:
        model = Blog
        fields = ('title','content','category','image','in_banner')
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'required':'True'}),
            'content':forms.Textarea(attrs={
                'class':'form-control',
                'rows':'10',
                'placeholder':'Escribe tu noticia...',
                'required':'True'
                }),
            'category':forms.Select(attrs=
                {'class':'form-control','required':'True'}),
        }
