# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from applications import views

urlpatterns = patterns('',

    # 应用列表
    url(r'^apps/$', views.list, name='app-list'),
    url(r'^apps/random/$', views.list, name='apps-list'),
    url(r'^apps/page/(?P<page_id>\d+)/$', views.list, name='apps-list'),

    # 应用搜索
    url(r'^apps/search/$', views.search, name='apps-search'),

    # 应用详情
    url(r'^apps/(?P<app_id>\d+)/$', views.detail, name='app-detail'),
    url(r'^apps/(?P<app_id>\d+)/thumb/$', views.thumb, name='app-thumb'),
)
