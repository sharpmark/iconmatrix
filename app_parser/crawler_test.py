# -*- coding: utf-8 -*-

import urllib
import json


#url = "http://apps.wandoujia.com/api/v1/apps?type=weeklytopapp&max=12&start=0&opt_fields=stat.weeklyStr,likesCount,reason,ad,title,packageName,apks.size,icons.px68,apks.superior,installedCountStr,snippet,apks.versionCode,tags.*"
url = "http://apps.wandoujia.com/api/v1/apps?type=weeklytopapp&max=60&start=0&opt_fields=packageName"
data_in_string = urllib.urlopen(url).read()

print data_in_string

data = json.loads(data_in_string)

for item in data:
    print item['packageName']
