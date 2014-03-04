# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.forms.models import modelformset_factory

from icons.models import Icon, Comment, Like
from icons.forms import IconSubmitForm, IconUploadForm

def detail(request, icon_id):
    icon = get_object_or_404(Icon, pk=icon_id)
    return render(request, 'icons/detail.html', {
        'icon': icon,
    })

def list(request):
    return render(request, 'icons/list.html', {
        'icon_list': Icon.objects.all(),
    })

def upload(request, icon_id):
    icon = get_object_or_404(Icon, pk=icon_id)
    if request.method == 'POST':
        form = IconUploadForm(instance=icon)
        if form.is_valid():
            icon = form.save()
            icon.save()
            return HttpResponseRedirect('/icons/%d/' % icon.id)
    else:
        form = IconUploadForm()
    return render(request, 'icons/upload.html', {
        'form': form,
    })

    return render(request, 'icons/upload.html')

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

def review(request):
    return render(request, 'icons/review.html')
