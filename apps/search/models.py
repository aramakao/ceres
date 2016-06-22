#-*- encoding: utf-8 -*-
from django.db import models
from apps.account.models import *
from apps.product.models import *
from apps.groups.models import *
from apps.farm.models import *
from apps.blog.models import *
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.loading import get_model
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class IndexManager(models.Manager):
    '''This manager allows extends the index model'''
    def search(self,word):
        '''This function allows search into the index model'''
        word = slugify(word)
        results = self.filter(text__contains=word)
        data ={}
        data_list = []
        for result in results:
            if result.content_type.name=='user':
                user = User.objects.get(id=result.object_id)
                url = reverse("user_profile",args=(user.username,))
                data['text']=user.fullName()
                data['url']=url
                data['image']=user.avatar
                data['source']="Usuario"
                data_list.append(data.copy())
            if result.content_type.name=='product':
                product = Product.objects.get(id=result.object_id)
                url = reverse("product",args=(product.slug,))
                data['text']=product.name
                data['url']=url
                data['image']=product.getPicture
                data['source']="Producto - %s"%(product.category.name)
                data_list.append(data.copy())
            if result.content_type.name=='group profile':
                group = GroupProfile.objects.get(id=result.object_id)
                url = reverse("group_profile",args=(group.group.slug,))
                data['text']=group.group.name
                data['url']=url
                data['image']=group.group.logo
                data['source']="Asociación - %s"%(group.slogan)
                data_list.append(data.copy())
            if result.content_type.name=='blog':
                blog = Blog.objects.get(id=result.object_id)
                url = reverse("blog_app:entry",args=(blog.slug,))
                data['text']=blog.title
                data['url']=url
                data['image']=blog.image
                data['source']="AgroBlog - %s"%(blog.category.name)
                data_list.append(data.copy())
            if result.content_type.name=='farm profile':
                profile = FarmProfile.objects.get(id=result.object_id)
                url = reverse("farm",args=(profile.farm.slug,))
                data['text']=profile.farm.name
                data['url']=url
                data['image']=profile.farm.logo
                data['source']="Granja - %s"%(profile.farm.name)
                data_list.append(data.copy())
        return data_list

    def min_search(self,word):
        '''This function returns a minimal query'''
        word = slugify(word)
        results = self.filter(text__contains=word)[:10]
        data ={}
        data_list = []
        try:
            for result in results:
                if result.content_type.name=='user':
                    user = User.objects.get(id=result.object_id)
                    url = reverse("user_profile",args=(user.username,))
                    data['text']=user.fullName()
                    data['url']=url
                    data['image']=user.avatar
                    data['source']="Usuario"
                    data['slug']=user.username
                    data_list.append(data.copy())
                if result.content_type.name=='product':
                    product = Product.objects.get(id=result.object_id)
                    url = reverse("product",args=(product.slug,))
                    data['text']=product.name
                    data['url']=url
                    data['slug']=product.slug
                    data['image']=product.getPicture
                    data['source']="Producto - %s"%(product.category.name)
                    data_list.append(data.copy())
                if result.content_type.name=='group profile':
                    group = GroupProfile.objects.get(id=result.object_id)
                    url = reverse("group_profile",args=(group.group.slug,))
                    data['text']=group.group.name
                    data['url']=url
                    data['slug']=group.group.slug
                    data['image']=group.group.logo
                    data['source']="Asociación - %s"%(group.slogan)
                    data_list.append(data.copy())
                if result.content_type.name=='blog':
                    blog = Blog.objects.get(id=result.object_id)
                    url = reverse("blog_app:entry",args=(blog.slug,))
                    data['text']=blog.title
                    data['url']=url
                    data['slug']=blog.slug
                    data['image']=blog.image
                    data['source']="AgroBlog - %s"%(blog.category.name)
                    data_list.append(data.copy())
                if result.content_type.name=='farm profile':
                    profile = FarmProfile.objects.get(id=result.object_id)
                    url = reverse("farm",args=(profile.farm.slug,))
                    data['text']=profile.farm.name
                    data['url']=url
                    data['slug']=profile.farm.slug
                    data['image']=profile.farm.logo
                    data['source']="Granja - %s"%(profile.farm.name)
                    data_list.append(data.copy())
            return data_list
        except Exception as e:
            return data_list

    def create(self,instance,text):
        '''This function index data'''
        model = instance.__class__.__name__
        ctype = ContentType.objects.get_for_model(instance)
        try:
            index = self.get(object_id=instance.id, content_type=ctype)
            index.text = text.lower()
            index.save()
        except Index.DoesNotExist:
            Index(text=text, content_type=ctype, object_id=instance.id).save()

class Index(models.Model):
    '''This model allows index information'''
    text = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = IndexManager()

    class Meta:
        unique_together=(('content_type','object_id'),)

    def __unicode__(self):
        return self.text
