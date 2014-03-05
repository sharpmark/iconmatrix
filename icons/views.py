# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.forms.models import modelformset_factory
from django.utils import timezone

from icons.models import Icon, Comment, Like
from icons.forms import IconSubmitForm, IconUploadForm

def detail(request, icon_id):
    icon = get_object_or_404(Icon, pk=icon_id)

    if request.method == 'POST':
        icon_upload_form = IconUploadForm(request.POST, request.FILES, instance=icon)
        if icon_upload_form.is_valid():
            icon = icon_upload_form.save(commit=False)
            icon.status_upload_time = timezone.now()
            icon.status = Icon.FINISH
            icon.save()
            return HttpResponseRedirect('/icons/%d/' % icon.id)
    else:
        icon_upload_form = IconUploadForm()

    return render(request, 'icons/detail.html', {
        'icon': icon,
        'icon_upload_form': icon_upload_form,
    })

def list(request):
    return render(request, 'icons/list.html', {
        'icon_list': Icon.objects.all(),
    })

def submit(request):
    if request.method == 'POST':
        form = IconSubmitForm(request.POST)
        if form.is_valid():
            icon = form.save()
            icon.crawl_icon_from_wdjurl()
            icon.save()
            return HttpResponseRedirect('/icons/%d/' % icon.id)
    else:
        form = IconSubmitForm()
    return render(request, 'icons/submit.html', {
        'form': form,
    })

def claim(request, icon_id):
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
    return render(request, 'icons/review.html')
