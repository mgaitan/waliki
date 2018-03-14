from os import path
import shutil
import tempfile
from sh import Command
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.cache import cache
from waliki.models import Page
from waliki.settings import WALIKI_CACHE_TIMEOUT
from waliki.settings import WALIKI_SLIDES_HOVERCRAFT_BIN
from waliki.acl import permission_required


hovercraft = Command(WALIKI_SLIDES_HOVERCRAFT_BIN).bake(_tty_out=False)


@permission_required('view_page')
def slides(request, slug):
    page = get_object_or_404(Page, slug=slug)

    cache_key = page.get_cache_key('slides')
    content = cache.get(cache_key)
    if content is None:
        outpath = tempfile.mkdtemp()
        try:
            infile = page.abspath
            template = path.join(path.dirname(path.realpath(__file__)), 'template')
            hovercraft('-t', template, infile, outpath)
            with open(path.join(outpath, 'index.html')) as f:
                content = f.read()
            cache.set(cache_key, content, WALIKI_CACHE_TIMEOUT)
        finally:
            shutil.rmtree(outpath)
    return HttpResponse(content)
