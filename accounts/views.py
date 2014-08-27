# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
import hashlib, base64, time
from datetime import datetime
import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from weibo import APIClient

from iconmatrix.weiboconfig import *
from accounts.models import User

def login(request):

    return HttpResponseRedirect(_create_client().get_authorize_url())


def logout(request):
    auth_logout(request)
    response = HttpResponseRedirect('/') #TODO:支持回调页面
    response.delete_cookie(COOKIE_USER)
    return response


def callback(request):

    client = _create_client()
    r = client.request_access_token(request.GET['code'])
    access_token, expires_in, uid = r.access_token, r.expires_in, r.uid

    client.set_access_token(access_token, expires_in)

    u = client.users.show.get(uid=uid)

    user = authenticate(weibo_user=u, token=r)
    user.save()

    auth_login(request, user)

    response = HttpResponseRedirect('/') #TODO

    _make_cookie(uid, access_token, expires_in, response)
    return response


def _create_client():
    return APIClient(app_key=APP_KEY, \
        app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def _make_cookie(uid, token, expires_in, response):

    expires = str(int(expires_in))
    s = '%s:%s:%s:%s' % (str(uid), str(token), expires, SALT)
    md5 = hashlib.md5(s).hexdigest()
    cookie = '%s:%s:%s' % (str(uid), expires, md5)
    response.set_cookie(COOKIE_USER, \
        base64.b64encode(cookie).replace('=', '_'), expires=expires_in)

def _check_cookie(request):

    try:
        b64cookie = request.COOKIES[COOKIE_USER]
        cookie = base64.b64decode(b64cookie.replace('_', '='))
        uid, expires, md5 = cookie.split(':', 2)

        if int(expires) < time.time():
            return

        user = User.objects.get(id=uid)
        s = '%s:%s:%s:%s' % (uid, str(user.auth_token), expires, SALT)
        if md5 != hashlib.md5(s).hexdigest():
            return

        return user

    except BaseException:
        pass
