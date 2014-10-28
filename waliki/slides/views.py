from os import path
import tempfile
from sh import hovercraft
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from waliki.models import Page


def slides(request, slug):
    page = get_object_or_404(Page, slug=slug)
    outpath = tempfile.mkdtemp()
    infile = page.abspath
    template = path.join(path.dirname(path.realpath(__file__)), 'template')
    hovercraft(infile, '-t', template, outpath)
    return HttpResponse(open(path.join(outpath, 'index.html')).read())
