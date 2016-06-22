from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^factura/(?P<order_id>[-\w]+)$',InvoiceView.as_view(),name='invoice'),
)
