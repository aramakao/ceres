from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
	url(r'^$', ProductListView.as_view(), name='product_list'),
	url(r'^/categorias$', ProductCategoryListView.as_view(), name='category'),
	url(r'^/categorias/agregar$', ProductCategoryCreateView.as_view(), name='category_add'),
	url(r'^/categorias/actulizar/(?P<slug>[-\w]+)$', ProductCategoryUpdateView.as_view(), name='category_update'),
	url(r'^/categorias/borrar/(?P<slug>[-\w]+)$', ProductCategoryDelete.as_view(), name='category_delete'),
    url(r'^/ver/(?P<slug>[-\w]+)$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^/borrar/(?P<slug>[-\w]+)$', ProductDeleteView.as_view(), name='product_delete'),
    url(r'^/agregar', ProductCreateView.as_view(), name='product_add'),
    url(r'^/editar/(?P<slug>[-\w]+)$', ProductUpdateView.as_view(), name='product_edit'),
	url(r'^/update_products_group/$','apps.product.views.updateMyProductsGroup', name='update_products_group'),
	url(r'^/update_active/$','apps.product.views.updateActiveProduct', name='update_active'),

)
