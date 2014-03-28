# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from icons.models import Icon, Like
from applications.models import Application
from django.shortcuts import render

def detail(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    return render(request, 'applications/detail-block.html', {
        'application': app,
    })

@login_required
def rate(request, icon_id, score):
    icon = get_object_or_404(Icon, pk=icon_id)
    if int(score) == 0:
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

    return HttpResponseRedirect('/apps/%d/' % icon.application.id)


@login_required
def isauthor(request, icon_id):
    from accounts.templatetags.user_filter import is_ui
    if is_ui(request.user):
        icon = get_object_or_404(Icon, pk=icon_id)
        icon.artist = request.user
        icon.save()

        icon.application.artist = request.user
        icon.application.save()

    return HttpResponseRedirect('/apps/%d/' % icon.application.id)
