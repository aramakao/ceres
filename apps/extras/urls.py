from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
	url(r'^/ocupaciones$', OccupationListView.as_view(), name='occupations_list'),
	url(r'^/ocupaciones/agregar$', OccupationCreateView.as_view(), name='occupation_add'),
	url(r'^/ocupaciones/actulizar/(?P<pk>\d+)$', OcupationUpdateView.as_view(), name='occupation_update'),
    url(r'^/ocupaciones/borrar/(?P<pk>\d+)$', OccupationDeleteView.as_view(), name='occupation_delete'),
	)
