# -*- coding: utf-8 -*-

from django.forms import ModelForm
from applications.models import Application

class SubmitForm(ModelForm):
    class Meta:
        model = Application

        fields = ['wandoujia_url']

        labels = {
            'wandoujia_url': '豌豆荚链接',
        }
        help_texts = {
            'wandoujia_url': '豌豆荚的应用详情链接',
        }
