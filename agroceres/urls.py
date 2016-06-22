from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.account.views import Login
from django.conf import settings
from django.conf.urls.static import static
from apps.store.views import HomePageView
from .views import *
from .sitemap import *
import notifications
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'farms': FarmSitemap,
    'products': ProductSitemap,
    'users':UserSitemap,
    'groups':GroupSitemap,
}

urlpatterns = patterns('',
    url(r'', include('apps.store.urls')),
    url(r'^mi-agro/',include('apps.farm.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reportes/', include('apps.reports.urls', namespace='reports_app')),
    url('',include('social.apps.django_app.urls', namespace='social')),
    url(r'^cuenta/', include('apps.account.urls',namespace='account')),
    url(r'^comentarios/', include('apps.comments.urls'), name='comments'),
    url(r'^api/',include('apps.api.urls')),
    url(r'^agro-blog', include('apps.blog.urls', namespace='blog_app', app_name='blog')),
    url('^acceso-no-autorizado/', UnauthorizedAccessView.as_view(), name='UnauthorizedAccess'),
    url(r'^loaderio-5dfd6207ca10eaeb1ad15a1de5fa9482',loaderio),
    url(r'^google21fafab3e80845e3.html',google_site),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'agroceres.views.handler404'
handler500 = 'agroceres.views.handler404'
