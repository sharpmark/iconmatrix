# -*- coding: utf-8 -*-
import os
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from applications.models import Application

def large_image_name(instance, filename):
    return upload_image_name(instance, filename, 'large')

def small_image_name(instance, filename):
    return upload_image_name(instance, filename, 'small')

def upload_image_name(instance, filename, image_type):
    f, ext = os.path.splitext(filename)
    imagename = '/'.join(['icons/' + image_type, instance.package_name + ext])
    fullname = os.path.join(settings.MEDIA_ROOT, imagename)
    if os.path.exists(fullname):
        os.rename(fullname,
            fullname[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + fullname[-4:])
    return imagename

class Icon(models.Model):

    application = models.ForeignKey(Application)

    # 绘制数据
    large_icon_image = models.ImageField(upload_to=large_image_name)
    small_icon_image = models.ImageField(upload_to=small_image_name)
    artist = models.ForeignKey(User)

    timestamp_upload = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    icon = models.ForeignKey(Icon)
    content = models.CharField(max_length=5000)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

class Like(models.Model):
    icon = models.ForeignKey(Icon)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
