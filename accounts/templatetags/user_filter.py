# -*- coding: utf-8 -*-

from django import template
from applications.models import Application
from django.contrib.auth.models import User, Group
from django.conf import settings

register = template.Library()

@register.filter
def get_claim(value):
    return Application.objects.filter(artist=value).filter(status__in=[Application.CLAIM]).count()

@register.filter
def get_upload(value):
    return Application.objects.filter(artist=value).filter(status__in=[Application.UPLOAD, Application.FINISH]).count()

@register.filter
def is_ui(value):
    if settings.DEBUG:
        return True
    else:
        return value.groups.filter(name='UI设计部').count() != 0

@register.filter
def is_pm(value):
    if settings.DEBUG:
        return True
    else:
        return value.groups.filter(name='产品规划部').count() != 0

@register.filter
def is_admin(value):
    if settings.DEBUG:
        return True
    else:
        return value.groups.filter(name='网站管理员').count() != 0
