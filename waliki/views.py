import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Page
from .forms import PageForm
from .signals import page_saved
from . import settings


def home(request):
    return detail(request, slug=settings.WALIKI_INDEX_SLUG)


def detail(request, slug):
    slug = slug.strip('/')
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None
    return render(request, 'waliki/detail.html', {'page': page, 'slug': slug})


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
    return render(request, 'waliki/edit.html', {'page': page, 'form': form, 'slug': slug})


def preview(request):
    data = {}
    if request.is_ajax() and request.method == "POST":
        data['html'] = Page.preview(request.POST['markup'], request.POST['text'])
        return HttpResponse(json.dumps(data), content_type="application/json")


def delete(request, slug):
    return render(request, 'waliki/detail.html', {})


