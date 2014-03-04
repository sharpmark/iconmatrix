from django.conf.urls import url
from icons import views

urlpatterns = patterns('',
    url(r'^artists/$', views.list, name='artist-list'),
    url(r'^artists/(?P<artist_id>\d+)/$', views.detail, name='artist-detail'),
)
