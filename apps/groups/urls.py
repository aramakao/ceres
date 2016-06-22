from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = patterns('',
	url(r'^$', GroupsView.as_view(),name='groups'),
	url(r'^/mis_asociaciones$', MyGroupsList.as_view(), name='my_groups'),
	url(r'^/registrar$', RegisterGroup.as_view(),name='register'),
	url(r'^/(?P<slug>[-\w]+)$', MyGroupView.as_view(), name='my_group'),
	url(r'^/(?P<slug>[-\w]+)/admin$', MyGroupAdminView.as_view(), name='group_admin'),
	url(r'^/(?P<slug>[-\w]+)/mis_productos$', MyProductsGroupView.as_view(), name='my_products'),
	url(r'^/changePictureProfile/', 'apps.groups.views.changePictureProfile', name = 'changePictureProfile'),
	url(r'^/changePictureBanner/', 'apps.groups.views.changePictureBanner', name = 'changePictureBanner'),
	url(r'^/(?P<slug>[-\w]+)/participantes$', MembersGroup.as_view(), name='members')
)
