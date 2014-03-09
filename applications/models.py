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
    wandoujia_url = models.URLField()
    package_name = models.CharField(max_length=500, unique=True)
    download_count = models.CharField(max_length=200)   # 从豌豆荚抓取数据，所以是字符串，模糊数据
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

    def crawl_icon_from_wdjurl(self):

        self.name = '淘宝彩票'
        self.original_icon_image = 'http://img.wdjimg.com/mms/icon/v1/b/6d/187c16d748f4d2843da62d51abc746db_256_256.png'
        self.description = '淘宝彩票是一个简单的口袋投注站，它能帮你摇摇手机完成投注，动动手指完成守号，一个按键完成付款，贴心推送告知中奖，大奖专人通知，万元以下奖金打入支付宝，另外你还可以和你的朋友通过微博，微信一起分享中奖的喜悦，购彩的乐趣。当遇到节假日，您朋友生日，更是可以通过手机批量送彩票送祝福。淘宝彩票由淘宝官方出品，服务广大彩民的一款彩票购买、开奖查询、订单查询的一站式彩票客户端。淘宝福地，精“彩”不断！下一个大奖属于你！'
        self.wandoujia_url = 'http://www.wandoujia.com/apps/com.taobao.caipiao'
        self.download_count = '106 万'
        self.package_name = 'com.taobao.caipiao'
        self.status = Application.CREATE
