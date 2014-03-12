# -*- coding: utf-8 -*-
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from applications.models import Application
from icons.models import Icon

from applications.forms import SubmitForm
from icons.forms import UploadForm

from app_parser.wdj_parser import parse_url, get_package_name

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

            icon.public_image()

            application.status = Application.UPLOAD
            application.last_icon = icon
            application.save()

            return HttpResponseRedirect('/apps/%d/' % application.id)
    else:
        icon_upload_form = UploadForm()

    my_score = 0

    if application.last_icon:
        my_score = application.last_icon.my_score(request.user)

    return render(request, 'applications/detail.html', {
        'application': application,
        'icon_upload_form': icon_upload_form,
        'my_score': my_score,
    })


def list(request):
    return __list_apps(request, statuses = [Application.UPLOAD, Application.FINISH])


def list_confirm(request):
    return __list_apps(request, statuses = [Application.CREATE, Application.CONFIRM])


def list_claim(request):
    return __list_apps(request, statuses = [Application.CLAIM])


def list_finish(request):
    return __list_apps(request, statuses = [Application.FINISH])

def __list_apps(request, statuses):
    return render(request, 'applications/list.html', {
        'app_list': Application.objects.filter(status__in=statuses).order_by('-last_icon__timestamp_upload'),
    })


def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            source_url = form.cleaned_data['source_url']
            package_name = get_package_name(source_url)

            application, created = Application.objects.get_or_create(package_name=package_name)
            application.source_url = source_url
            parse_url(application)

            if created:
                application.status = Application.CONFIRM

            application.save()

            return HttpResponseRedirect('/apps/%d/' % application.id)
    else:
        form = SubmitForm()
    return render(request, 'applications/submit.html', {
        'form': form,
    })


def claim(request, app_id):

    if not request.user.is_authenticated():
        return redirect('/accounts/login/?next=%s' % request.path)

    app = Application.objects.get(pk=app_id)
    if app:
        if app.status == Application.CONFIRM or app.status == Application.CREATE:
            app.artist = request.user
            app.status = Application.CLAIM
            app.save()
    return HttpResponseRedirect('/apps/%d/' % app.id)


def unclaim(request, app_id):

    if not request.user.is_authenticated():
        return redirect('/accounts/login/?next=%s' % request.path)

    app = Application.objects.get(pk=app_id)
    if app:
        if app.status == Application.CLAIM:
            app.artist = None
            app.status = Application.CONFIRM
            app.save()
    return HttpResponseRedirect('/apps/%d/' % app.id)

def review(request):
    return render(request, 'applications/review.html')
