from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from artists import views

urlpatterns = patterns('',
    url(r'^artists/$', views.list, name='artist-list'),
    url(r'^artists/my/apps/claim/$', views.claim, name='artist-my-claim'),
    url(r'^artists/my/apps/upload/$', views.upload, name='artist-my-upload'),
    url(r'^artists/my/apps/finish/$', views.finish, name='artist-my-finish'),
    url(r'^artists/(?P<artist_id>\d+)/apps/claim/$', views.claim, name='artist-claim'),
    url(r'^artists/(?P<artist_id>\d+)/apps/upload/$', views.upload, name='artist-upload'),
    url(r'^artists/(?P<artist_id>\d+)/apps/finish/$', views.finish, name='artist-finish'),
)
