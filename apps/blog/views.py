from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import *
from .forms import *
from apps.account.models import LoggedInMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy

class EntryView(DetailView):
    '''This class allows view an entry'''
    model = Blog
    template_name = 'blog/entry.html'

class EntryList(ListView):
    '''This class list the entries'''
    model = Blog
    template_name = 'blog/index.html'
    paginate_by = 10
    context_object_name = 'entries'
    queryset = Blog.objects.all().order_by('-posted')

class BlogList(LoggedInMixin,ListView):
    '''This class list the entries for the administrator'''
    model = Blog
    template_name = 'blog/blog_list.httml'
    paginate_by = 10
    context_object_name = 'entries'

    def get_queryset(self):
        '''This function verified if the user is administrator'''
        if self.request.user.is_superuser:
            return Blog.objects.all().order_by('-posted')
        else:
            raise Http404

    def post(self,request,*args,**kwargs):
        '''This function allows delete an entry'''
        if 'delete' in request.POST:
            blog_id=request.POST['delete'][7:]
            Blog.objects.get(id=blog_id).delete()
            messages.success(self.request,"Entrada borrada!")
        return HttpResponseRedirect(reverse('blog'))

class BlogAddView(LoggedInMixin,CreateView):
    '''This class allows create an entry'''
    model = Blog
    template_name = 'blog/blog_add.html'
    form_class = BlogForm
    success_url=reverse_lazy('blog')

    def get_form(self, form_class):
        if self.request.user.is_superuser:
            return form_class(**self.get_form_kwargs())
        else:
            raise Http404

    def form_valid(self,form):
        '''This function checks if the form is valid'''
        messages.success(self.request, 'Entrada agregada exitosamente!')
        return super(BlogAddView, self).form_valid(form)

class BlogView(LoggedInMixin,DetailView):
    '''This class allows view an entry'''
    model = Blog
    context = 'entry'
    template_name = 'blog/entry_view.html'

class BlogUpdateView(LoggedInMixin,UpdateView):
    '''This class allows update an entry'''
    model = Blog
    template_name = 'blog/blog_update.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog')

    def get_form(self,form_class):
        if self.request.user.is_superuser:
            return form_class(**self.get_form_kwargs())
        else:
            raise Http404

    def form_valid(self,form):
        messages.success(self.request, 'Entrada actualizada exitosamente!')
        return super(BlogUpdateView, self).form_valid(form)

class CategoryList(ListView):
    '''This class list all categories'''
    model = Category
    template_name = 'blog/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all().order_by('name')

class CategoryBlogView(ListView):
    '''This class returns an entries list filter by categories'''
    model = Blog
    template_name='blog/category.html'
    paginate_by=10
    context_object_name= 'entries'

    def get_queryset(self):
        object_list = self.model.objects.filter(category__slug = self.kwargs['slug'])
        return object_list

    def get_context_data(self, **kwargs):
        category=get_object_or_404(Category,slug=self.kwargs['slug'])
        context = super(CategoryBlogView, self).get_context_data(**kwargs)
        context['category'] = category
        return context
