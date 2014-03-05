from django.conf.urls import url, patterns
from icons import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='index'),
    url(r'^icons/$', views.list, name='icon-list'),
    url(r'^icons/(?P<icon_id>\d+)/$', views.detail, name='icon-detail'),
    url(r'^icons/(?P<icon_id>\d+)/claim$', views.claim, name='icon-claim'),

    url(r'^icons/submit/$', views.submit, name='icon-submit'),

    #url(r'^icons/review/$', views.review, name='icon-review'),
)
