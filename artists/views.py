# Create your views here.

# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.forms.models import modelformset_factory

from django.contrib.auth.models import User as Artist

def detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    return render(request, 'artist/detail.html', {
        'artist': artist,
    })

def list(request):
    return render(request, 'artist/list.html', {
        'artist_list': Artist.objects.all(),
    })
