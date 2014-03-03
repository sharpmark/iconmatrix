# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Icon(models.Model):

    NEW = 'NE'
    CONFIRM = 'CO'
    CLAIM = 'CL'
    UPLOAD = 'UP'
    FINISH = 'FI'
    ABANDON = 'AB'
    STATUS = (
        (NEW, '新提交'),
        (CONFIRM, '确认'),
        (CLAIM, '已认领'),
        (UPLOAD, '已上传'),
        (FINISH, '完成'),
        (ABANDON, '已废弃'),
    )

    # 应用数据
    name = models.CharField(max_length=200)
    original_icon_image = models.ImageField(upload_to='icons/original')
    description = models.CharField(max_length=5000)
    wandoujia_url = models.URLField()
    download_count = models.CharField(max_length=200)   # 从豌豆荚抓取数据，所以是字符串，模糊数据

    # 绘制数据
    large_icon_image = models.ImageField(upload_to='icons/large')
    small_icon_image = models.ImageField(upload_to='icons/small')
    artist = models.ForeignKey(User, related_name='draw')

    # 状态和其他信息
    uploader = models.ForeignKey(User, related_name='upload')
    status = models.CharField(max_length=2, choices=STATUS, default=NEW)

    status_new_time = models.DateTimeField()
    status_confirm_time = models.DateTimeField()
    status_claim_time = models.DateTimeField()
    status_upload_time = models.DateTimeField()
    status_finish_time = models.DateTimeField()
    status_abandon_time = models.DateTimeField()

class Comment(models.Model):
    content = models.CharField(max_length=5000)
    icon = models.ForeignKey(Icon)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=True)

class Like(models.Model):
    icon = models.ForeignKey(Icon)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
