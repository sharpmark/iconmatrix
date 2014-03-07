# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from icons.models import Icon, Like

def rate(request, icon_id, score):
    icon = get_object_or_404(Icon, pk=icon_id)
    print score
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
