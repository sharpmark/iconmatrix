# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from applications import views

urlpatterns = patterns('',
    # 已绘应用列表
    url(r'^apps/$', views.list_launcher, name='apps-launcher'),
    url(r'^apps/random/$', views.list_launcher, name='apps-launcher'),
    url(r'^apps/page/(?P<page_id>\d+)/$', views.list_launcher, name='apps-launcher'),

    # 应用操作
    url(r'^apps/submit/$', views.submit, name='apps-submit'),         # 提交应用
    url(r'^apps/search/$', views.search, name='apps-search'),         # 搜索应用

    # 分状态的应用列表
    url(r'^apps/create/$', views.list_create, name='apps-create'),    # 审核应用
    url(r'^apps/confirm/$', views.list_confirm, name='apps-confirm'),

    # 应用详情
    url(r'^apps/(?P<app_id>\d+)/$', views.detail, name='app-detail'),
)
