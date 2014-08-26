# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.forms.models import modelformset_factory

from accounts.models import User as Artist
from applications.models import Application

def apps(request, artist_id):

    if artist_id == 0:
        if request.user.is_authenticated:
            artist_id = request.user.id
        else:
            return HttpResponseRedirect('/')

    artist = get_object_or_404(Artist, pk=artist_id)
    app_list = artist.draws.filter(status__in=status).order_by('-timestamp_draw')
    return render(request, 'artists/applications.html', {
        'artist': artist,
        'app_list': app_list,
    })


def list(request):
    return render(request, 'artist/list.html', {
        'artist_list': Artist.objects.all(),
    })
