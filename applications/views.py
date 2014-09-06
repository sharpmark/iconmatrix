# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from applications.models import Application, Like
from applications.forms import SearchForm

DEFAULT_APPS = 18

def detail(request, package):

    application = get_object_or_404(Application, package_name=package)

    if request.method == 'GET':
        return render(request, 'applications/detail.html', {
            'application': application,
        })

    # 以下为处理 POST 请求
    action = request.POST['action']

    if action == 'rate':
        return _rate(request, application)

    return redirect(app)


def thumb(request, package):

    app = get_object_or_404(Application, package_name=package)
    return render(request, 'applications/thumb.html', {
        'application': app,
    })


def list(request, page_id=0):

    page_id = int(page_id)

    apps_count = Application.objects.all().count()
    page_count = _get_page_count(apps_count)

    if page_id == 0:
        app_list = _list_random()
    else:
        if page_count < page_id or page_id < 1: page_id = 1
        app_list = _list(page_id)

    return render(request, 'applications/launcher.html', {
        'app_list': app_list,
        'current_page': page_id,
        'pages': _get_page_list(apps_count, current=page_id),
        'prepage': page_id - 1,
        'nextpage': 0 if page_id == page_count else page_id + 1,
        'lastpage': page_count,
        'app_list': app_list,
    })
    return render(request, 'applications/launcher.html', {
        'app_list': Application.objects.all().order_by('-timestamp_draw'),
    })


def search(request):
    #TODO: rewrite to RESTFul
    from django.db.models import Q

    app_list = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            app_list = Application.objects.filter(Q(name__icontains=form.cleaned_data['query']) | Q( package_name__icontains=form.cleaned_data['query']))

            if len(app_list) == 1:
                return redirect('/apps/%d/' % app_list[0].id)

    return render(request, 'applications/list-search.html', {
        'app_list': app_list,
    })


@login_required
def _rate(request, application):
    score = int(request.POST['score'])

    if int(score) == 0:
        try:
            like = Like.objects.get(application=application, user=request.user)
            like.delete()
        except:
            pass
    else:

        try:
            like = Like.objects.get(application=application, user=request.user)
        except:
            like = Like()
            like.user = request.user
            like.application = application
            like.score = score
            like.save()

        like.score = score
        like.save()

    return render(request, 'applications/like.html', {'application': application,})


def _list_random(apps_pre_page=DEFAULT_APPS):
    import random
    max_id = Application.objects.latest('id').id

    if Application.objects.all().count() > apps_pre_page:
        app_list = []

        while len(app_list) < apps_pre_page:

            try:
                appid = random.randint(1, max_id)
                app = Application.objects.get(id=appid)
                if not app in app_list:
                    app_list.append(app)
            except:
                pass

    else:
        app_list = Application.objects.all()

    return app_list


def _list(page_id, apps_pre_page=DEFAULT_APPS):

    return Application.objects.all().order_by('-timestamp_draw')\
        [(page_id - 1) * apps_pre_page: page_id * apps_pre_page]


def _get_page_count(total, pre=DEFAULT_APPS):
    if total % pre == 0:
        return total / pre
    else:
        return total / pre + 1

def _get_page_list(total, pre=DEFAULT_APPS, current=1):

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
