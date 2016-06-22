from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$',ConversationsList.as_view(),name='conversations'),
    url(r'^/(?P<username>[-\w]+)$',MessagesList.as_view(),name='message'),
)
