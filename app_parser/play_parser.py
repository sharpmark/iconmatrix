# -*- coding: utf-8 -*-
from applications.models import Application

import re
import urllib

from urlparse import urlparse

def play_parse(package_name):

    url = 'https://play.google.com/store/apps/details?id=' + package_name
    application_html = urllib.urlopen(url).read()

    if _get_name(application_html) != 'Null' and package_name != 'Null':
        app, created = Application.objects.get_or_create(package_name=package_name)

        app = Application.objects.get(package_name=package_name)
        app.name = _get_name(application_html)
        app.original_icon_image = _get_original_icon(application_html)
        app.description = _get_description(application_html)
        app.download_count = _get_download_count(application_html)
        app.version = _get_version(application_html)

        app.source_url = url

        return app
    else:
        return None

def _get_name(application_html):
    pattern_string = '<div class="document-title" itemprop="name">[\s\S]*?<div>([\S\s]*?)</div>'
    return _reg_search(pattern_string, application_html)

def _get_original_icon(application_html):
    pattern_string = '<div class="cover-container">[\s\S]*?<img class="cover-image" src="(\S*?)"'
    return _reg_search(pattern_string, application_html)

def _get_description(application_html):
    pattern_string = '<div class="class="id-app-orig-desc" itemprop="description"[\s\S]*?">([\s\S]*?)</div>'
    return _reg_search(pattern_string, application_html)

def _get_download_count(application_html):
    pattern_string = '<div class="content" itemprop="numDownloads">([\s\S]*?)</div>'
    return _reg_search(pattern_string, application_html)

def _get_version(application_html):
    pattern_string = '<div class="content" itemprop="softwareVersion">[\s]*?(\S*)[\s]*? </div>'
    return _reg_search(pattern_string, application_html)

def _get_package_name(application_url):
    path = urlparse(application_url)[2]
    pattern_string = '/apps/details\?id=(\S*)'
    return _reg_search(pattern_string, path)

def _reg_search(pattern_string, application_html):
    pattern = re.compile(pattern_string)
    result = pattern.search(application_html)

    if result is not None:
        return result.group(1)
    else:
        return 'Null'
