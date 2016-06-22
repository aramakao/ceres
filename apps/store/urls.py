from django.conf.urls import patterns, include, url
from .views import *
from apps.account.views import ProfileView
from apps.groups.views import GroupsView, GroupProfileView
from apps.search.views import Search

urlpatterns = patterns('',
	url(r'^$', AboutView.as_view(),name='about'),
	url(r'^inicio$', HomePageView.as_view(),name='home'),
	url(r'^reply/(?P<pk>\d+)', UpdateAskView.as_view(), name='reply'),
    url(r'^producto/(?P<slug>[-\w]+)', ProductView.as_view(), name='product'),
    url(r'^granja/(?P<farm>[-\w]+)$', FarmView.as_view(), name='farm'),
	url(r'^granja/(?P<farm>[-\w]+)/opiniones$', FarmFeedbackView.as_view(), name='feedback_farm'),
    url(r'^granja/(?P<farm>[-\w]+)/producto/(?P<product>[-\w]+)', ProductFarmView.as_view(), name='product_farm'),
    url(r'^granja/(?P<farm>[-\w]+)/productos', ProductsFarmView.as_view(), name='products_list'),
    url(r'^granja/(?P<farm>[-\w]+)/categoria/(?P<category>[-\w]+)', FarmCategoryProductsView.as_view(), name='category_product_farm'),
    url(r'^granja/(?P<farm>[-\w]+)/categorias', FarmCategoryView.as_view(), name='category_farm'),
	url(r'^buscar$', Search.as_view(), name='search'),
    url(r'^granjas$', FarmsView.as_view(), name='farms'),
	url(r'^publicaciones$', StatusList.as_view(), name='status'),
	url(r'^geo-granjas$', GeoFarmView.as_view(), name='geo-farms'),
	url(r'^usuarios/(?P<slug>[-\w]+)$', ProfileView.as_view(), name='user_profile'),
	url(r'^usuarios$', UsersView.as_view(), name='users'),
	url(r'^asociaciones$', GroupsView.as_view(), name='groups'),
	url(r'^productos$', ProductList.as_view(), name='products'),
	url(r'^asociacion/(?P<group>[-\w]+)$', GroupProfileView.as_view(), name='group_profile'),
    url(r'^categorias$', CategoriesView.as_view(), name='category_list'),
    url(r'^carro_compras$', ShoppingCarView.as_view(), name='shopping_cart'),
	url(r'^compra-exitosa$', ShopSuccessView.as_view(), name='shop_success'),
	url(r'^envio$', ShippingAddressView.as_view(), name='shipping'),
	url(r'^shoppingCart$', 'apps.store.views.shoppingCart', name='shopping_cart_update'),
	url(r'^addProductCart$', 'apps.store.views.addProductCart'),
	url(r'^delProductCart$', 'apps.store.views.delProductCart'),
	url(r'^getShoppingCart$', 'apps.store.views.getShoppingCart'),
	url(r'^mailbox$', 'apps.store.views.sendMailbox'),
	url(r'^categoria/(?P<slug>[-\w]+)', CategoryProductsView.as_view(), name='category'),

)
