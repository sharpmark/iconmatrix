# -*- coding: utf-8 -*-

from django.forms import ModelForm
from icons.models import Icon

class IconForm(ModelForm):
    class Meta:
        model = Icon

        fields = ['wandoujia_url']

        labels = {
            'wandoujia_url': '豌豆荚链接',
        }
        help_texts = {
            'wandoujia_url': '豌豆荚的应用详情链接',
        }
