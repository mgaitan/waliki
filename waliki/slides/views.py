from os import path
import shutil
import tempfile
from sh import hovercraft
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from waliki.models import Page
from waliki.acl import permission_required


@permission_required('view_page')
def slides(request, slug):
    page = get_object_or_404(Page, slug=slug)
    outpath = tempfile.mkdtemp()
    try:
        infile = page.abspath
        template = path.join(path.dirname(path.realpath(__file__)), 'template')
        hovercraft('-t', template, infile, outpath)
        with open(path.join(outpath, 'index.html')) as f:
            content = f.read()
    finally:
        shutil.rmtree(outpath)
    return HttpResponse(content)
