# -*- coding: utf-8 -*-

from django import template
from applications.models import Application
from django.contrib.auth.models import User, Group
from django.conf import settings

register = template.Library()

@register.filter
def is_ui(value):
    if settings.DEBUG:
        return False
    else:
        return False #TODO
