# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.forms.models import modelformset_factory

from icons.models import Icon, Comment, Like
from icons.forms import IconForm

def detail(request, icon_id):
    icon = get_object_or_404(Icon, pk=icon_id)
    return render(request, 'icons/detail.html', {
        'icon': icon,
    })

def list(request):
    return render(request, 'icons/list.html', {
        'icon_list': Icon.objects.all(),
    })

def upload(request):
    return render(request, 'icons/upload.html')

def submit(request):
    if request.method == 'POST':
        iconform = IconForm(request.POST)
        if iconform.is_valid():
            icon = iconform.save()
            icon.crawl_icon_from_wdjurl()
            icon.save()
            return HttpResponseRedirect('/icons/%d/' % icon.id)
    else:
        iconform = IconForm()
    return render(request, 'icons/submit.html', {
        'iconform': iconform,
    })

def review(request):
    return render(request, 'icons/review.html')
