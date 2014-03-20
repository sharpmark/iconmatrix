# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from applications import views

urlpatterns = patterns('',
    # 已绘应用列表
    url(r'^apps/$', views.list, name='app-list'),
    url(r'^apps/random/$', views.list, name='app-list'),
    url(r'^apps/page/(?P<page_id>\d+)/$', views.list, name='app-list'),

    # 应用操作
    url(r'^apps/submit/$', views.submit, name='apps-submit'),         # 提交应用
    url(r'^apps/create/$', views.list_create, name='apps-create'),    # 审核应用

    # 已确认，待认领
    url(r'^apps/confirm/$', views.list_confirm, name='apps-confirm'),
    url(r'^apps/confirm/page/(?P<page_id>\d+)/$', views.list_confirm, name='apps-confirm'),

    # 应用详情
    url(r'^apps/(?P<app_id>\d+)/$', views.detail, name='app-detail'),
    url(r'^apps/(?P<app_id>\d+)/claim/$', views.detail_claim, name='app-claim'),        # 应用认领
    url(r'^apps/(?P<app_id>\d+)/unclaim/$', views.detail_unclaim, name='app-unclaim'),  # 应用取消认领

    #url(r'^apps/finish/$', views.list_finish, name='list-finish'),
    #url(r'^apps/finish/page/(?P<page_id>\d+)/$', views.list_finish, name='list-finish'),
    #url(r'^apps/review/$', views.review, name='app-review'),
)
