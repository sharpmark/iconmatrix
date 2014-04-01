# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from icons.models import Icon, Like
from applications.models import Application
from django.shortcuts import render, redirect


def list(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    if request.method == 'GET':
        #TODO return HttpResponse obj.
        return Icon.objects.filter(application=app)

    action = request.POST['action']

    if action == 'upload':
        return _upload_icon(request, app)


def detail(request, icon_id):
    icon = get_object_or_404(Icon, pk=icon_id)
    app = icon.application

    if request.method == 'GET': return redirect(app)

    # 以下为处理 POST 请求
    action = request.POST['action']

    if action == 'rate':
        return _rate_icon(request, icon)

    if action == 'is_author':
        return _is_author(request, icon)

    return redirect(app)


@login_required
def _upload_icon(request, app):
    from icons.forms import UploadForm
    icon_upload_form = UploadForm(request.POST, request.FILES, instance=Icon())

    if icon_upload_form.is_valid():
        icon = icon_upload_form.save(commit=False)
        icon.application = app
        icon.artist = request.user
        icon.save()

        icon.public_image()

        # 将验证是否为认领应用的设计师收到这里，是为了以后可以允许不同的设计师上传图标
        if request.user == app.artist:
            app.status = Application.UPLOAD
            app.last_icon = icon
            app.save()

    return redirect(app)


@login_required
def _rate_icon(request, icon):
    score = int(request.POST['score'])

    if score == 0:
        try:
            like = Like.objects.get(icon=icon, user=request.user)
            like.delete()
        except:
            pass
    else:

        try:
            like = Like.objects.get(icon=icon, user=request.user)
        except:
            like = Like()
            like.user = request.user
            like.icon = icon
            like.score = score
            like.save()

        like.score = score
        like.save()

    return render(request, 'icons/like.html', {'icon': icon,})


@login_required
def _is_author(request, icon):
    from accounts.templatetags.user_filter import is_ui
    if is_ui(request.user):
        icon.artist = request.user
        icon.save()

        icon.application.artist = request.user
        icon.application.save()

    return render(request, 'icons/action.html', {'application': icon.application})
