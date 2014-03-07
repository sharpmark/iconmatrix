from django.conf.urls import url, patterns
from icons import views

urlpatterns = patterns('',
    url(r'^icons/(?P<icon_id>\d+)/rate/(?P<score>[\d\-]+)/$', views.rate, name='icon-rate'),
)
