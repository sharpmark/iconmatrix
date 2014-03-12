# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):

    CREATE = 'CR'
    CONFIRM = 'CO'
    CLAIM = 'CL'
    UPLOAD = 'UP'
    FINISH = 'FI'
    ABANDON = 'AB'
    STATUS = (
        (CREATE, '新提交'),
        (CONFIRM, '确认'),
        (CLAIM, '已认领'),
        (UPLOAD, '已上传'),
        (FINISH, '完成'),
        (ABANDON, '已废弃'),
    )

    # 应用数据
    name = models.CharField(max_length=200)
    original_icon_image = models.URLField()
    description = models.CharField(max_length=5000)
    source_url = models.URLField()
    package_name = models.CharField(max_length=500, unique=True)
    download_count = models.CharField(max_length=200)
    version = models.CharField(max_length=50)

    # 状态和其他信息
    status = models.CharField(max_length=2, choices=STATUS, default=CREATE)
    last_icon = models.ForeignKey('icons.Icon', null=True, related_name='app')

    # 上传者和绘制者
    uploader = models.ForeignKey(User, related_name='uploads', null=True)
    artist = models.ForeignKey(User, related_name='draws', null=True)

    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_confirm = models.DateTimeField(null=True)
    timestamp_claim = models.DateTimeField(null=True)
    #timestamp_upload = models.DateTimeField(null=True)
    timestamp_finish = models.DateTimeField(null=True)
    timestamp_abandon = models.DateTimeField(null=True)
