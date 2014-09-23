# -*- coding: utf-8 -*-
import os
import datetime
import shutil

from django.db import models
from django.conf import settings

from accounts.models import User

class Application(models.Model):

    name = models.CharField(max_length=200)
    original_icon_image = models.URLField()
    description = models.CharField(max_length=5000)
    source_url = models.URLField()
    package_name = models.CharField(max_length=500, unique=True)
    download_count = models.CharField(max_length=200)
    version = models.CharField(max_length=50)

    icon = models.ImageField(upload_to='upload/icons/')
    artist = models.ForeignKey(User, related_name='draws', null=True)

    like_count = models.SmallIntegerField(default=0)
    unlike_count = models.SmallIntegerField(default=0)

    timestamp_draw = models.DateTimeField(null=True)

    def score(self, user):
        try:
            like = Like.objects.get(application=self, user=user)
            return int(like.score)
        except:
            return 0

    def get_like_count(self):
        return Like.objects.filter(application=self, score=1).count()

    def get_unlike_count(self):
        return Like.objects.filter(application=self, score=-1).count()

    def get_absolute_url(self):
        return '/apps/%s/' % self.package_name

    def get_icon_url(self):
        return 'icons/%s' % self.icon

    def share_button(self):
        urlformat = u'http://service.weibo.com/share/share.php?appkey=%d&url=%s&title=%s&pic=%s&source=锤子图标&content=utf8&searchPic=false'
        appkey = 1980984514
        url = 'http://iconmatrix.sharpmark.net/'
        title = u'分享锤子科技重绘“%s' % self.name + u'”的图标一枚：http://iconmatrix.sharpmark.net%s @锤子图标' % self.get_absolute_url()
        pic = 'http://iconmatrix.sharpmark.net/uploads/' + self.get_icon_url()

        return urlformat % (appkey, url, title, pic)


class Comment(models.Model):
    application = models.ForeignKey(Application)
    content = models.CharField(max_length=5000)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)


class Like(models.Model):
    application = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    score = models.SmallIntegerField()
    timestamp = models.DateTimeField(auto_now=True)
