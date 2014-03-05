# -*- coding: utf-8 -*-

from django.forms import ModelForm
from icons.models import Icon

class UploadForm(ModelForm):
    class Meta:
        model = Icon

        fields = ['large_icon_image', 'small_icon_image']
