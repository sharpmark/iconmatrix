from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from django.contrib.auth import views as auth_views

from accounts import views

#TODO:
urlpatterns = patterns('',
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='auth-login'),
    url(r'^accounts/logout/$', auth_views.logout, {'template_name': 'accounts/logout.html'}, name='auth-logout'),
)
