from django.conf.urls import url, patterns
from applications import views

urlpatterns = patterns('',
    url(r'^apps/$', views.list, name='app-list'),
    url(r'^apps/(?P<app_id>\d+)/$', views.detail, name='app-detail'),
    url(r'^apps/(?P<app_id>\d+)/claim/$', views.claim, name='app-claim'),

    url(r'^apps/submit/$', views.submit, name='app-submit'),
    url(r'^apps/confirm/$', views.list_confirm, name='list-confirm'),
    url(r'^apps/claim/$', views.list_claim, name='list-claim'),
    url(r'^apps/finish/$', views.list_finish, name='list-finish'),
    #url(r'^apps/review/$', views.review, name='app-review'),
)
