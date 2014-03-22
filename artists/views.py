# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.forms.models import modelformset_factory

from django.contrib.auth.models import User as Artist

from applications.models import Application

def detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    return render(request, 'artist/detail.html', {
        'artist': artist,
    })

def list(request):
    return render(request, 'artist/list.html', {
        'artist_list': Artist.objects.all(),
    })


def claim(request, artist_id=0):
    return _artist_application_list(request, artist_id, [Application.CLAIM])

def upload(request, artist_id=0):
    return _artist_application_list(request, artist_id, [Application.UPLOAD, Application.FINISH])

def finish(request, artist_id=0):
    return _artist_application_list(request, artist_id, [Application.UPLOAD, Application.FINISH])

def _artist_application_list(request, artist_id, status):
    if artist_id == 0:
        if request.user.is_authenticated:
            artist_id = request.user.id
        else:
            return HttpResponseRedirect('/')

    artist = get_object_or_404(Artist, pk=artist_id)
    app_list = artist.draws.filter(status__in=status).order_by('-last_icon__timestamp_upload')
    return render(request, 'artists/applications.html', {
        'artist': artist,
        'app_list': app_list,
    })
