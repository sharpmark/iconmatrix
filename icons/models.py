# -*- coding: utf-8 -*-
import os
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from applications.models import Application

def image_192px_name(instance, filename):
    f, ext = os.path.splitext(filename)
    imagename = '/'.join(['icons/192px', instance.application.package_name + ext])
    fullname = os.path.join(settings.MEDIA_ROOT, imagename)
    if os.path.exists(fullname):
        instance.application.last_icon.image_192px = imagename[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + imagename[-4:]
        instance.application.last_icon.save()
        os.rename(fullname, fullname[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + fullname[-4:])
    return imagename

def image_128px_name(instance, filename):
    f, ext = os.path.splitext(filename)
    imagename = '/'.join(['icons/128px', instance.application.package_name + ext])
    fullname = os.path.join(settings.MEDIA_ROOT, imagename)
    if os.path.exists(fullname):
        instance.application.last_icon.image_128px = imagename[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + imagename[-4:]
        instance.application.last_icon.save()
        os.rename(fullname, fullname[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + fullname[-4:])
    return imagename

def image_fullsize_name(instance, filename):
    f, ext = os.path.splitext(filename)
    imagename = '/'.join(['icons/fullsize', instance.application.package_name + ext])
    fullname = os.path.join(settings.MEDIA_ROOT, imagename)
    if os.path.exists(fullname):
        instance.application.last_icon.image_fullsize = imagename[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + imagename[-4:]
        instance.application.last_icon.save()
        os.rename(fullname, fullname[:-3] + datetime.datetime.now().strftime('%Y-%m%d-%H%M%S') + fullname[-4:])
    return imagename

class Icon(models.Model):

    application = models.ForeignKey(Application)

    # 绘制数据
    image_192px = models.ImageField(upload_to=image_192px_name)
    image_128px = models.ImageField(upload_to=image_128px_name)
    image_fullsize = models.ImageField(upload_to=image_fullsize_name)
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
