#-*- encoding: utf-8 -*-
from django.db import models
from autoslug import AutoSlugField
from django.utils import formats

class CategoryManager(models.Manager):
    '''This class allows manager the category model'''
    def menuCategory(self):
        '''This function returns the menu for categories'''
        categories = self.all().order_by('name')
        categories_list=[]
        category={}
        for cat in categories:
            category['name']=cat.name
            category['slug']=cat.slug
            category['svg']=cat.svg
            category['count']=cat.countEntries()
            categories_list.append(category.copy())
        return categories_list

    def countEntries(self):
        '''This function counts the entries'''
        count = self.filter(category=self).count()
        return count

class Category(models.Model):
    '''This model allows save the categories'''
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique_with='name', always_update=True)
    image = models.ImageField(upload_to='blog', default='blog/no_image.png')
    icon = models.ImageField(upload_to='blog', default='blog/no_image.png')
    svg = models.TextField(default='none')
    objects = CategoryManager()

    def __unicode__(self):
        return self.name

    def countEntries(self):
        '''This function counts the entries for categories'''
        count = Blog.objects.filter(category=self).count()
        return count

class BlogManager(models.Manager):
    '''This manager extends from blog model'''
    def getBanners(self):
        banners = self.values('image','slug','title').filter(in_banner=True)
        return banners

class Blog(models.Model):
    '''This model allows save a blog'''
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique_with='title',always_update=True)
    content = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    image = models.ImageField(upload_to='blog', default='blog/no_image.png')
    in_banner = models.BooleanField(default=True)
    objects = BlogManager()

    def __unicode__(self):
        return self.title

    def minContent(self):
        '''This function returns a minimum content of the entry'''
        return self.content[0:100]+'...'

    def date_post(self):
        '''This function returns the publication date'''
        return formats.date_format(self.posted, "SHORT_DATE_FORMAT")
