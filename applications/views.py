# -*- coding: utf-8 -*-
from django.shortcuts import render

from applications.models import Application


def detail(request, app_id):

    application = get_object_or_404(Application, pk=app_id)

    my_score = 0

    my_score = application.icon.my_score(request.user)

    return render(request, 'applications/detail.html', {
        'application': application,
        'my_score': my_score,
    })


def list(request):

    return render(request, 'applications/launcher.html', {
        'app_list': Application.objects.all().order_by('-timestamp_draw'),
    })

def rate(request, app_id, score):
    app = get_object_or_404(Icon, pk=app_id)
    if int(score) == 0:
        try:
            like = Like.objects.get(application=app, user=request.user)
            like.delete()
        except:
            pass
    else:

        try:
            like = Like.objects.get(application=app, user=request.user)
        except:
            like = Like()
            like.user = request.user
            like.application = app
            like.score = score
            like.save()

        like.score = score
        like.save()

    return HttpResponseRedirect('/apps/%d/' % icon.application.id)
