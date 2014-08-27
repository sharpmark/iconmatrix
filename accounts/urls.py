from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from accounts import views

#TODO:
urlpatterns = patterns('',
    url(r'^accounts/login/$', views.login, name='auth-login'),
    url(r'^accounts/logout/$', views.logout, name='auth-logout'),
    url(r'^callback/$', views.callback, name='callback'),
)
