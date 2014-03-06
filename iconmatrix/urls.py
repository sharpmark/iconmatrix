from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from applications import views as app_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', app_views.list, name='index'),
    url(r'', include('icons.urls')),
    url(r'', include('accounts.urls')),
    url(r'', include('applications.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
