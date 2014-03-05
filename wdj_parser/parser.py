# -*- coding: utf-8 -*-
from applications.models import Application

import re

def parse_wdj_url(icon):
    icon.name = '淘宝彩票'
    icon.original_icon_image = 'http://img.wdjimg.com/mms/icon/v1/b/6d/187c16d748f4d2843da62d51abc746db_256_256.png'
    icon.description = '淘宝彩票是一个简单的口袋投注站，它能帮你摇摇手机完成投注，动动手指完成守号，一个按键完成付款，贴心推送告知中奖，大奖专人通知，万元以下奖金打入支付宝，另外你还可以和你的朋友通过微博，微信一起分享中奖的喜悦，购彩的乐趣。当遇到节假日，您朋友生日，更是可以通过手机批量送彩票送祝福。淘宝彩票由淘宝官方出品，服务广大彩民的一款彩票购买、开奖查询、订单查询的一站式彩票客户端。淘宝福地，精“彩”不断！下一个大奖属于你！'
    icon.download_count = '106 万'
    icon.package_name = 'com.taobao.caipiao'
    icon.status = Application.CREATE

    return icon

