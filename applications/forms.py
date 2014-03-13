# -*- coding: utf-8 -*-

from django.forms import Form
from applications.models import Application
from django.utils.translation import ugettext_lazy as _
from django import forms

from app_parser.parser import get_app_from_url

class SubmitForm(Form):

    source_url = forms.CharField(max_length=100,label=u'应用链接',\
    help_text=u'目前只支持豌豆荚的应用详情链接，例如http://www.wandoujia.com/apps/com.taobao.caipiao',\
    widget=forms.TextInput())

    def clean_source_url(self):
        raw_url = self.cleaned_data['source_url']

        if 'http://' in raw_url:
            pass
        else:
            raw_url = 'http://' + raw_url

        if get_app_from_url(raw_url) is None:
            # todo
            raise forms.ValidationError('输入的网址中没有应用信息。')

        return raw_url
