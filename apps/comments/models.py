from django.db import models
from apps.account.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.timesince import timesince
import json

class CommentManager(models.Manager):
    '''This manager allows extend de comment model'''

    def getComments(self,content_type,object_id):
        '''This function returns all comments'''
        comments = self.filter(content_type=content_type, object_id=object_id).order_by('-date')
        comments_list=[]
        comment={}
        for c in comments:
            comment['fullName']=c.sender.fullName()
            comment['slug']=c.sender.username
            comment['avatar']=c.sender.avatar.url
            comment['date']=timesince(c.date)
            comment['message']=c.message
            comments_list.append(comment.copy())
        return json.dumps(comments_list)

class Comment(models.Model):
    '''This model allows save comments'''
    sender = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = CommentManager()

    def __unicode__(self):
        return self.message
