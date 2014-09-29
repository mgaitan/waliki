import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from .models import Page
from .forms import PageForm
from .signals import page_saved, page_preedit
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
    page, created = Page.objects.get_or_create(slug=slug)
    if created:
        page.raw = ""
        page_saved.send(sender=edit,
                        page=page,
                        author=request.user,
                        message=_("Page created"),
                        form_extra_data={})
    data = request.POST if request.method == 'POST' else None
    form_extra_data = {}
    receivers_responses = page_preedit.send(sender=edit, page=page)
    for r in receivers_responses:
        if isinstance(r[1], dict) and 'form_extra_data' in r[1]:
            form_extra_data.update(r[1]['form_extra_data'])

    form = PageForm(data, instance=page, initial={'extra_data': json.dumps(form_extra_data)})
    if form.is_valid():
        page = form.save()
        try:
            receivers_responses = page_saved.send(sender=edit,
                                                  page=page,
                                                  author=request.user,
                                                  message=form.cleaned_data["message"],
                                                  form_extra_data=json.loads(form.cleaned_data["extra_data"] or "{}"))
        except Page.EditionConflict as e:
            messages.warning(request, e)
            return redirect('waliki_edit', slug=page.slug)

        for r in receivers_responses:
            if isinstance(r[1], dict) and 'messages' in r[1]:
                for key, value in r[1]['messages'].items():
                    getattr(messages, key)(request, value)
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


