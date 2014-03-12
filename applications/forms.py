# -*- coding: utf-8 -*-

from django.forms import ModelForm
from applications.models import Application
from django.utils.translation import ugettext_lazy as _

class SubmitForm(ModelForm):
    class Meta:
        model = Application

        fields = ('source_url', )

        labels = {
            'source_url': _(u'应用链接'),
        }
        help_texts = {
            'source_url': _(u'目前只支持豌豆荚的应用详情链接，例如http://www.wandoujia.com/apps/com.taobao.caipiao'),
        }
