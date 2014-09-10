from django.shortcuts import render
from .models import Page
from . import settings


def home(request):
    return detail(request, slug=settings.WALIKI_INDEX_SLUG)


def detail(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None
    return render(request, 'waliki/detail.html', {'page': page})


def edit(request, slug):
    return render(request, 'waliki/detail.html', {})


def delete(request, slug):
    return render(request, 'waliki/detail.html', {})
