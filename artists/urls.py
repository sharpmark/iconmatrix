from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from artists import views

urlpatterns = patterns('',
    url(r'^artists/$', views.list, name='artist-list'),
    url(r'^artists/(?P<artist_id>\d+)/apps/$', views.apps, name='artist-apps'),
)
