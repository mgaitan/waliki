from django.shortcuts import render, redirect
from .models import Page
from .forms import PageForm
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
        return redirect('waliki_detail', slug=page.slug)
    return render(request, 'waliki/edit.html', {'page': page, 'form': form})


def delete(request, slug):
    return render(request, 'waliki/detail.html', {})
