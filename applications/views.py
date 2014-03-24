# -*- coding: utf-8 -*-
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from applications.models import Application
from icons.models import Icon

from applications.forms import SubmitForm, CreateFormSet, SearchForm
from django.forms.formsets import formset_factory
from icons.forms import UploadForm
from app_parser.parser import get_app_from_url
from django.db.models import Q

import random

def detail(request, app_id):
    application = get_object_or_404(Application, pk=app_id)

    if request.method == 'POST':
        #todo: 检查是不是当前设计师
        icon_upload_form = UploadForm(request.POST, request.FILES, instance=Icon())
        if icon_upload_form.is_valid():
            icon = icon_upload_form.save(commit=False)
            icon.application = application
            icon.artist = request.user
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

    max_id = Application.objects.latest('id').id

    if Application.objects.count() > 9:
        app_list = []

        while len(app_list) < 9:

            try:
                appid = random.randint(1, max_id)
                app = Application.objects.get(id=appid)
                if not app in app_list and app.status in [Application.UPLOAD, Application.FINISH]:
                    app_list.append(app)
            except:
                pass

    else:
        app_list = Application.objects.filter(status__in=[Application.UPLOAD, Application.FINISH])

    page_count = Application.objects.filter(status__in=[Application.UPLOAD, Application.FINISH]).count()

    return render(request, 'applications/list-launcher.html', {
        'app_list': app_list, 'current_page': 0,
        'pages': _get_page_list(page_count, 9, 0),
        'prepage': 0, 'nextpage': 1, 'firstpage': 1, 'lastpage': page_count,
        'app_list': app_list,
    })

def list_paged(request, page_id=1):

    page_id = int(page_id)
    apps_pre_page = 9                   # 每页显示多少个
    statuses=[Application.UPLOAD, Application.FINISH]

    apps_count = Application.objects.filter(status__in=statuses).count()
    page_count = _get_page_count(apps_count, apps_pre_page)

    if page_count < page_id or page_id < 1:
        page_id = 1

    app_list = Application.objects.filter(status__in=statuses).order_by('-last_icon__timestamp_upload')[(page_id - 1) * 9: page_id * 9]

    return render(request, 'applications/list-launcher.html', {
        'current_page': page_id, 'pages': _get_page_list(apps_count, apps_pre_page, page_id),
        'prepage': page_id - 1, 'nextpage': 0 if page_id == page_count else page_id + 1,
        'firstpage': 1, 'lastpage': page_count,
        'app_list': app_list,
    })


@login_required
def list_create(request):
    from accounts.templatetags.user_filter import is_admin

    if not is_admin(request.user): return HttpResponseRedirect('/')

    if request.method == 'POST':
        action = request.POST.get('action')
        formset = CreateFormSet(request.POST, queryset=Application.objects.filter(status=Application.CREATE))

        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data.get('is_checked'):
                    app = form.save(commit=False)
                    if action == 'confirm':
                        app.status = Application.CONFIRM
                    if action == 'abandon':
                        app.status = Application.ABANDON
                    app.save()

            return HttpResponseRedirect(request.path)

    else:
        formset = CreateFormSet(queryset=Application.objects.filter(status=Application.CREATE))

    return render(request, 'applications/list-create.html', {
        'formset': formset,
        'app_list': Application.objects.filter(status=Application.CREATE).order_by('-timestamp_create'),
    })


@login_required
def list_confirm(request, page_id=1):
    from accounts.templatetags.user_filter import is_ui

    if is_ui(request.user):
        return render(request, 'applications/list-confirm.html', {
            'app_list': Application.objects.filter(status=Application.CONFIRM).order_by('-timestamp_create'),
        })
    else:
        return HttpResponseRedirect('/')


def _get_page_count(total, pre=9):
    if total % pre == 0:
        return total / pre
    else:
        return total / pre + 1

def _get_page_list(total, pre=9, current=1):

    pages = _get_page_count(total, pre)

    if current < 6:
        start = 1
        end = min(pages, 9)
    elif current + 4 > pages:
        end = pages
        start = max(pages - 9, 1)
    else:
        start = current - 4
        end = current + 4

    return range(start, end + 1)


@login_required
def submit(request):
    SubmitFormSet = formset_factory(SubmitForm, extra=1)
    if request.method == 'POST':
        formset = SubmitFormSet(request.POST)
        if formset.is_valid():
            for form in formset.forms:

                if form.cleaned_data.get('source_url'):
                    application = get_app_from_url(form.cleaned_data['source_url'])

                    if application.uploader == None:
                        application.uploader = request.user

                    application.save()
    else:
        formset = SubmitFormSet()

    return render(request, 'applications/submit.html', {
        'formset': formset,
    })


@login_required
def detail_claim(request, app_id):

    app = Application.objects.get(pk=app_id)
    if app:
        if app.status == Application.CONFIRM or app.status == Application.CREATE:
            app.artist = request.user
            app.status = Application.CLAIM
            app.save()

    if request.GET['next']:
        return HttpResponseRedirect(request.GET['next'])
    else:
        return HttpResponseRedirect('/apps/%d/' % app.id)


@login_required
def detail_unclaim(request, app_id):

    app = Application.objects.get(pk=app_id)
    if app:
        if app.status == Application.CLAIM:
            app.artist = None
            app.status = Application.CONFIRM
            app.save()
    return HttpResponseRedirect('/apps/%d/' % app.id)


def search(request):
    app_list = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            print form.cleaned_data['query']
            app_list = Application.objects.filter(Q(name__icontains=form.cleaned_data['query']) | Q( package_name__icontains=form.cleaned_data['query']))

            if len(app_list) == 1:
                return HttpResponseRedirect('/apps/%d/' % app_list[0].id)

    return render(request, 'applications/list-search.html', {
        'app_list': app_list,
    })
