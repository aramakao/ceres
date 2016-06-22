from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$','apps.comments.views.comment',name='comment'),
    url(r'^getComments$','apps.comments.views.getComments', name='comments'),
    #url(r'^/(?P<user>[-\w]+)$',MessagesList.as_view(),name='message'),
)
