from django.shortcuts import render, get_object_or_404
from django.http import Http404
from waliki.models import Page
from waliki.forms import PageForm
from . import Git


def history(request, slug):
    page = get_object_or_404(Page, slug=slug)
    history = Git().history(page)
    max_changes = max([(v['insertion'] + v['deletion']) for v in history])
    return render(request, 'waliki/history.html', {'page': page,
                                                   'slug': slug,
                                                   'history': history,
                                                   'max_changes': max_changes})

def version(request, slug, version):
    import ipdb; ipdb.set_trace()

    page = get_object_or_404(Page, slug=slug)
    content = Git().get_version(page, version)
    if not content:
        raise Http404
    form = PageForm(instance=page, initial={'message': 'Restored version @%s' % version, 'raw': content})
    return render(request, 'waliki/version.html', {'page': page,
                                                   'slug': slug,
                                                   'version': version,
                                                   'form': form})

