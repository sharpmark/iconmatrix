# -*- coding: utf-8 -*-
from applications.models import Application

import re
import urllib
import json

from urlparse import urlparse

def parse_url(wandoujia_url):

    application_html = urllib.urlopen(wandoujia_url).read()
    package_name = _get_package_name(wandoujia_url)

    if _get_name(application_html) != 'Null' and package_name != 'Null':

        app, created = Application.objects.get_or_create(package_name=package_name)
        app.name = _get_name(application_html)
        app.original_icon_image = _get_original_icon(application_html)
        app.description = _get_description(application_html)
        app.download_count = _get_download_count(application_html)
        app.version = _get_version(application_html)
        app.package_name = _get_package_name(wandoujia_url)
        app.source_url = wandoujia_url

        if created:
            app.status = Application.CONFIRM

        return app
    else:
        return None

def crawl_wdj_weekly_top():
    STEP = 50
    MAX = 1000
    start = 0

    while start < MAX:
        url = "http://apps.wandoujia.com/api/v1/apps?type=weeklytopapp&max=%s&start=%s&opt_fields=packageName" %(STEP, start)
        data_in_string = urllib.urlopen(url).read()

        data = json.loads(data_in_string)

        for item in data:
            app_url = "http://www.wandoujia.com/apps/%s" %item['packageName']
            print app_url
            app = parse_url(app_url)
            app.save()

        start = start + STEP

def _get_name(application_html):
    pattern_string = '<p class="app-name">[\s\S]*?<span class="title" itemprop="name">([\S\s]*?)</span>'
    return _reg_search(pattern_string, application_html)

def _get_original_icon(application_html):
    pattern_string = '<div class="app-icon">[\s\S]*?<img src="(\S*?)"'
    return _reg_search(pattern_string, application_html)

def _get_description(application_html):
    pattern_string = 'itemprop="description">[\s\S]*?([\s\S]*?)</div>'
    return _reg_search(pattern_string, application_html)

def _get_download_count(application_html):
    pattern_string = '<i itemprop="interactionCount" content="UserDownloads:(\d*?)"'
    return _reg_search(pattern_string, application_html)

def _get_version(application_html):
    pattern_string = '<dt>版本</dt>[\s\S]*?<dd>(\S*)</dd>'
    return _reg_search(pattern_string, application_html)

def _get_package_name(application_url):
    path = urlparse(application_url)[2]
    pattern_string = '/apps/(\S*)'
    return _reg_search(pattern_string, path)

def _reg_search(pattern_string, application_html):
    pattern = re.compile(pattern_string)
    result = pattern.search(application_html)

    if result is not None:
        return result.group(1)
    else:
        return 'Null'
