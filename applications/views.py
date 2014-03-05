# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404

from applications.models import Application
from applications.forms import SubmitForm
from icons.forms import UploadForm

def detail(request, app_id):
    application = get_object_or_404(Application, pk=app_id)

    if request.method == 'POST':
        icon_upload_form = UploadForm(request.POST, request.FILES, instance=Icon())
        if icon_upload_form.is_valid():
            icon = icon_upload_form.save(commit=False)
            icon.application = application
            icon.artist = request.user
            icon.timestamp_upload = timezone.now()
            icon.save()

            application.status = Application.UPLOAD
            application.save()

            return HttpResponseRedirect('/applications/%d/' % icon.id)
    else:
        icon_upload_form = UploadForm()

    return render(request, 'applications/detail.html', {
        'application': application,
        'icon_upload_form': icon_upload_form,
    })

def list(request):
    return render(request, 'applications/list.html', {
        'app_list': Application.objects.all(),
    })

def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            icon = form.save()
            icon.crawl_icon_from_wdjurl()
            icon.save()
            return HttpResponseRedirect('/apps/%d/' % icon.id)
    else:
        form = SubmitForm()
    return render(request, 'applications/submit.html', {
        'form': form,
    })


def claim(request, app_id):
    icon = Icon.objects.get(pk=icon_id)
    if icon:
        if icon.status == Icon.CONFIRM or icon.status == Icon.NEW:
            #icon.artist = 1 # todo
            icon.status = Icon.CLAIM
            icon.save()
            return HttpResponse('true')
        else:
            return HttpResponse('图标已被认领或已绘制。')
    else:
        return HttpResponse('图标不存在。')


def review(request):
    return render(request, 'applications/review.html')
