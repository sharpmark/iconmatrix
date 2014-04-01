from django.conf.urls import url, patterns
from icons import views

urlpatterns = patterns('',
    url(r'^apps/(?P<app_id>\d+)/icons/$', views.list, name='icon-list'),
    url(r'^apps/(?P<app_id>\d+)/icons/(?P<icon_id>)$', views.detail, name='icon-detail'),
)
