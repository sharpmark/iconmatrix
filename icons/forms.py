# -*- coding: utf-8 -*-

from django.forms import ModelForm
from icons.models import Icon

class UploadForm(ModelForm):
    class Meta:
        model = Icon

        fields = ['image']

        labels = {
            'image': '192px尺寸图片',
        }

        help_texts = {
            'image': u'192px X 192px 大小的 .png 格式图片',
        }
