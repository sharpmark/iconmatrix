# -*- coding: utf-8 -*-

from django import template
from applications.models import Application

register = template.Library()

@register.filter
def get_claim(value):
    return Application.objects.filter(artist=value).filter(status__in=[Application.CLAIM]).count()

@register.filter
def get_upload(value):
    return Application.objects.filter(artist=value).filter(status__in=[Application.UPLOAD, Application.FINISH]).count()
