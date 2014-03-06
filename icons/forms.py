# -*- coding: utf-8 -*-

from django.forms import ModelForm
from icons.models import Icon

class UploadForm(ModelForm):
    class Meta:
        model = Icon

        fields = ['image_fullsize', 'image_192px', 'image_128px']
