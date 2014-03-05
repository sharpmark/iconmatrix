# -*- coding: utf-8 -*-
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from applications.models import Application
from icons.models import Icon

from applications.forms import SubmitForm
from icons.forms import UploadForm

from wdj_parser.parser import parse_wdj_url

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
            application.last_icon = icon
            application.save()

            return HttpResponseRedirect('/apps/%d/' % application.id)
    else:
        icon_upload_form = UploadForm()

    operation_flag = ''
    if request.user.is_authenticated():
        if application.status == 'CR' or application.status == 'CO':
            operation_flag = 'claim'
        elif application.status == 'CL':
            if request.user == application.artist:
                operation_flag = 'upload'
            else:
                operation_flag = 'notyours'
        elif application.status == 'UP':
            if request.user == application.artist:
                operation_flag = 'uploaded'
            else:
                operation_flag = 'notyours'
        elif application.status == 'FI' or application.status == 'AB':
            operation_flag = 'finish'

    return render(request, 'applications/detail.html', {
        'application': application,
        'icon_upload_form': icon_upload_form,
        'operation_flag': operation_flag,
    })


def list(request):
    return render(request, 'applications/list.html', {
        'app_list': Application.objects.all(),
    })


def list_confirm(request):
    return render(request, 'applications/list.html', {
        'app_list': Application.objects.filter(status__in=[Application.CREATE, Application.CONFIRM]),
    })


def list_claim(request):
    return render(request, 'applications/list.html', {
        'app_list': Application.objects.filter(status__in=[Application.UPLOAD, Application.CLAIM]),
    })


def list_finish(request):
    return render(request, 'applications/list.html', {
        'app_list': Application.objects.filter(status__in=[Application.FINISH]),
    })


def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            icon = form.save()
            icon = parse_wdj_url(icon)
            icon.save()
            return HttpResponseRedirect('/apps/%d/' % icon.id)
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
            print request.user
            app.artist = request.user
            app.status = Application.CLAIM
            app.save()
    return HttpResponseRedirect('/apps/%d/' % app.id)


def review(request):
    return render(request, 'applications/review.html')
