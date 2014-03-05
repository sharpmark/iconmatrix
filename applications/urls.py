from django.conf.urls import url, patterns
from applications import views

urlpatterns = patterns('',
    url(r'^apps/$', views.list, name='app-list'),
    url(r'^apps/(?P<app_id>\d+)/$', views.detail, name='app-detail'),
    url(r'^apps/(?P<app_id>\d+)/claim/$', views.claim, name='app-claim'),

    url(r'^apps/submit/$', views.submit, name='app-submit'),
    #url(r'^apps/review/$', views.review, name='app-review'),
)
