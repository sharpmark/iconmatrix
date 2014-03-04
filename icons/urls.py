from django.conf.urls import url, patterns
from icons import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='index'),
    url(r'^icons/(?P<icon_id>\d+)/$', views.detail, name='icon-detail'),
    url(r'^icons/$', views.list, name='icon-list'),

    url(r'^icons/submit/$', views.submit, name='icon-submit'),
    url(r'^icons/upload/$', views.upload, name='icon-upload'),

    #url(r'^icons/review/$', views.review, name='icon-review'),
)
