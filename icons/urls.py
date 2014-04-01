from django.conf.urls import url, patterns
from icons import views

urlpatterns = patterns('',
    url(r'^apps/(?P<app_id>\d+)/icons/$', views.list, name='icon-list'),
    url(r'^icons/(?P<icon_id>\d+)/$', views.detail, name='icon-detail'),
)
