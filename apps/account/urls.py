from django.conf.urls import patterns, include, url
from .views import Login,ForgetSucces,Register

urlpatterns = patterns('',
    url(r'^salir/$','django.contrib.auth.views.logout', {'next_page': 'home'},name='logout'),
    url(r'^ingresar/','apps.account.views.Login', name='login'),
    url(r'^registro/','apps.account.views.Register',name='register'),
    url(r'^recordar/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            'apps.account.views.reset_confirm', name='reset_confirm'),
    url(r'^recordar/$', 'apps.account.views.Reset', name='reset'),
    url(r'^changePictureProfile/$', 'apps.account.views.changePictureProfile'),
    url(r'^changePictureBanner/$', 'apps.account.views.changePictureBanner'),
    url(r'^recordar/exitoso$',ForgetSucces.as_view(), name='forget_succes'),
)
