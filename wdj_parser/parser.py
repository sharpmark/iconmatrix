# -*- coding: utf-8 -*-
from applications.models import Application

import re
import urllib

def parse_wdj_url(application):
    url = application.wandoujia_url
    application_html = urllib.urlopen(url).read()

    application.name = _get_application_name(application_html)
    application.original_icon_image = _get_app_original_icon(application_html)
    application.description = _get_application_description(application_html)
    application.download_count = _get_application_download_count(application_html)

    application.package_name = 'com.taobao.caipiao'
    application.status = Application.CREATE

    return application

def _get_application_name(application_html):
    pattern_string = '<p class="app-name">[\s\S]*?<span class="title" itemprop="name">(\S*?)</span>'
    return _reg_search(pattern_string, application_html)

def _get_app_original_icon(application_html):
    pattern_string = '<div class="app-icon">[\s\S]*?<img src="(\S*?)"'
    return _reg_search(pattern_string, application_html)

def _get_application_description(application_html):
    pattern_string = 'itemprop="description">[\s\S]*?([\s\S]*?)</div>'
    return _reg_search(pattern_string, application_html)

def _get_application_download_count(application_html):
    pattern_string = '<i itemprop="interactionCount" content="UserDownloads:(\d*?)"'
    return _reg_search(pattern_string, application_html)


def _reg_search(pattern_string, application_html):
    pattern = re.compile(pattern_string)
    result = pattern.search(application_html)

    if result is not None:
        return result.group(1)
    else:
        return 'Null'
