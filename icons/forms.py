# -*- coding: utf-8 -*-

from django.forms import ModelForm
from icons.models import Icon

class UploadForm(ModelForm):
    class Meta:
        model = Icon

        fields = ['image_128px', 'image_192px']#, 'image_fullsize', 'image_rawfile']

        labels = {
            'image_128px': '128px尺寸图片',
            'image_192px': '192px尺寸图片',
            #'image_fullsize': '原始尺寸图片（可选）',
            #'image_rawfile': '原始设计稿（可选）',
        }

        help_texts = {
            'image_128px': u'128px X 128px 大小的 .png 格式图片',
            'image_192px': u'192px X 192px 大小的 .png 格式图片',
            #'image_fullsize': u'原始尺寸（例如 1024px 尺寸的 .png 格式图片',
            #'image_rawfile': u'原始文件，格式不限，例如.psd',
        }
