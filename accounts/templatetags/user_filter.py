# -*- coding: utf-8 -*-

from django import template
from applications.models import Application
from django.contrib.auth.models import User, Group

register = template.Library()

@register.filter
def get_claim(value):
    return Application.objects.filter(artist=value).filter(status__in=[Application.CLAIM]).count()

@register.filter
def get_upload(value):
    return Application.objects.filter(artist=value).filter(status__in=[Application.UPLOAD, Application.FINISH]).count()

@register.filter
def is_ui(value):
    return value.groups.filter(name='UI设计部').count() != 0

@register.filter
def is_pm(value):
    return value.groups.filter(name='产品规划部').count() != 0
