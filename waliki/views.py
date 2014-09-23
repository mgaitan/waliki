import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Page
from .forms import PageForm
from .signals import page_saved
from ._markups import get_all_markups
from .decorators import permission_required
from . import settings


def home(request):
    return detail(request, slug=settings.WALIKI_INDEX_SLUG)


@permission_required('view_page')
def detail(request, slug):
    slug = slug.strip('/')
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None
    return render(request, 'waliki/detail.html', {'page': page, 'slug': slug})


@permission_required('change_page')
def edit(request, slug):
    slug = slug.strip('/')
    page, _ = Page.objects.get_or_create(slug=slug)
    data = request.POST if request.method == 'POST' else None
    form = PageForm(data, instance=page)
    if form.is_valid():
        form.save()
        page_saved.send(sender=edit,
                        page=page,
                        author=request.user,
                        message=form.cleaned_data["message"])
        return redirect('waliki_detail', slug=page.slug)
    cm_modes = [(m.name, m.codemirror_mode_name) for m in get_all_markups()]

    cm_settings = settings.WALIKI_CODEMIRROR_SETTINGS
    cm_settings.update({'mode': dict(cm_modes)[page.markup]})
    return render(request, 'waliki/edit.html', {'page': page,
                                                'form': form,
                                                'slug': slug,
                                                'cm_modes': cm_modes,
                                                'cm_settings': json.dumps(cm_settings)})


def preview(request):
    data = {}
    if request.is_ajax() and request.method == "POST":
        data['html'] = Page.preview(request.POST['markup'], request.POST['text'])
        return HttpResponse(json.dumps(data), content_type="application/json")


@permission_required('delete_page')
def delete(request, slug):
    return render(request, 'waliki/detail.html', {})


