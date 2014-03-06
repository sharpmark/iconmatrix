# -*- coding: utf-8 -*-
import os
import datetime
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from applications.models import Application


def image_192px_name(instance, filename):
    return upload_image_name(instance, filename, '192px')

def image_128px_name(instance, filename):
    return upload_image_name(instance, filename, '128px')

def image_fullsize_name(instance, filename):
    return upload_image_name(instance, filename, 'fullsize')

def image_rawfile_name(instance, filename):
    return upload_image_name(instance, filename, 'rawfile')

def upload_image_name(instance, filename, image_type):
    f, ext = os.path.splitext(filename)

    image_name = 'icons/' + instance.application.package_name + '.' + image_type
    field_name = image_name + datetime.datetime.now().strftime('.%Y-%m%d-%H%M%S') + ext
    return field_name


class Icon(models.Model):

    application = models.ForeignKey(Application)

    # 绘制数据
    image_192px = models.ImageField(upload_to=image_192px_name)
    image_128px = models.ImageField(upload_to=image_128px_name)
    image_fullsize = models.ImageField(upload_to=image_fullsize_name, null=True, blank=True)
    image_rawfile = models.FileField(upload_to=image_rawfile_name, null=True, blank=True)

    artist = models.ForeignKey(User)

    timestamp_upload = models.DateTimeField(auto_now_add=True)


    def public_image(self):
        print 'public image'
        self.public_image_field(self.image_192px.name)
        self.public_image_field(self.image_128px.name)


    def public_image_field(self, field):
        filename, ext = os.path.splitext(field)
        print filename

        field_name = os.path.join(settings.MEDIA_ROOT, field)
        print field_name
        public_name = os.path.join(settings.MEDIA_ROOT, 'public/' + filename[:-17] + ext)
        print public_name
        shutil.copy2(field_name, public_name)


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
