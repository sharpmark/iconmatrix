from django.conf.urls import patterns, include, url
from icons import views

urlpatterns = patterns('',
    url(r'^upload$', views.upload, name='upload'),
    url(r'^icons/(?P<icon_id>\d+)/$', views.detail, name='detail'),
    url(r'^matrix$', views.matrix, name='matrix'),
    url(r'^artist$', views.artist, name='artist'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^review$', views.review, name='review'),
)
