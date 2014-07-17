# -*- coding: utf-8 -*-
import os
import datetime
import shutil

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from applications.models import Application


def image_name(instance, filename):
    f, ext = os.path.splitext(filename)

    image_name = 'icons/' + instance.application.package_name
    field_name = image_name + datetime.datetime.now().strftime('.%Y-%m%d-%H%M%S') + ext
    return field_name


class Icon(models.Model):

    application = models.ForeignKey(Application)

    # 绘制数据
    image = models.ImageField(upload_to=image_name)
    artist = models.ForeignKey(User)

    timestamp_upload = models.DateTimeField(auto_now_add=True)

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
        filename, ext = os.path.splitext(self.image.name)
        field_name = os.path.join(settings.MEDIA_ROOT, self.image.name)
        #TODO: hard code!
        public_name = os.path.join(settings.MEDIA_ROOT, 'public', filename[6:-18] + ext)
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
