from django.conf.urls import url, patterns
from applications import views

urlpatterns = patterns('',
    url(r'^apps/$', views.list, name='app-list'),
    url(r'^apps/(?P<app_id>\d+)/$', views.detail, name='app-detail'),
    url(r'^apps/(?P<app_id>\d+)/rate/(?P<score>[\d\-]+)/$', views.rate, name='app-rate'),
)
