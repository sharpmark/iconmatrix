# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, Form
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _

from app_parser.parser import get_app_from_url
from applications.models import Application

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

CreateFormSetBase = modelformset_factory(Application, extra=0, fields={})

class CreateFormSet(CreateFormSetBase):

    def add_fields(self, form, index):
        super(CreateFormSet, self).add_fields(form, index)
        form.fields['is_checked'] = forms.BooleanField(required=False)
        form.fields['is_checked'].widget.attrs['class'] = 'select-app'
