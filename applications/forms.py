# -*- coding: utf-8 -*-

from django.forms import ModelForm
from applications.models import Application
from django.utils.translation import ugettext_lazy as _

class SubmitForm(ModelForm):
    class Meta:
        model = Application

        fields = ('wandoujia_url', )

        labels = {
            'wandoujia_url': _(u'豌豆荚链接'),
        }
        help_texts = {
            'wandoujia_url': _(u'豌豆荚的应用详情链接，例如http://www.wandoujia.com/apps/com.taobao.caipiao'),
        }
