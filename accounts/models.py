# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime

class User(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=1000)
    statuses_count = models.BigIntegerField()
    friends_count = models.BigIntegerField()
    followers_count = models.BigIntegerField()
    verified = models.BooleanField()
    verified_type = models.IntegerField()
    auth_token = models.CharField(max_length=2000)
    expired_time = models.DecimalField(max_digits=20, decimal_places=2)
    #expired_time = models.DateTimeField()

    create_time = models.DateTimeField(default=datetime.today())            # 第一次登录时间
