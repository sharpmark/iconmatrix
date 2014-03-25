# -*- coding: utf-8 -*-
import os
import datetime
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from applications.models import Application

from django.utils.html import format_html


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

    def __unicode__(self):
        return self.application.name

    def my_score(self, user):
        try:
            like = Like.objects.get(icon=self, user=user)
            return int(like.score)
        except:
            return 0


    def like_count(self):
        return Like.objects.filter(icon=self, score=1).count()


    def unlike_count(self):
        return Like.objects.filter(icon=self, score=-1).count()


    def public_image(self):
        _public_image_field(self.image_192px.name, icon_dir='192')
        _public_image_field(self.image_128px.name, icon_dir='128')

    def image_icon(self):
        return format_html('<img style="" src="/uploads/{0}" />', self.image_128px)

    image_icon.allow_tags = True

def _public_image_field(field, icon_dir):
    filename, ext = os.path.splitext(field)
    field_name = os.path.join(settings.MEDIA_ROOT, field)
    #TODO: hard code!
    public_name = os.path.join(settings.MEDIA_ROOT, 'public', icon_dir, filename[6:-23] + ext)
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
    score = models.SmallIntegerField()
    timestamp = models.DateTimeField(auto_now=True)
