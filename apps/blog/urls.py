from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
	url(r'^$', EntryList.as_view(),name='agro_blog'),
	url(r'^/categorias$', CategoryList.as_view(),name='categories'),
	url(r'^/categorias/(?P<slug>[-\w]+)$', CategoryBlogView.as_view(), name='category'),
	url(r'^/(?P<slug>[-\w]+)', EntryView.as_view(),name='entry'),

)
