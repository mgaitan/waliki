from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from waliki.models import Page
from waliki.forms import PageForm
from waliki.decorators import permission_required
from . import Git


@permission_required('view_page')
def history(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST':
        new, old = request.POST.getlist('commit')
        return redirect('waliki_diff', slug, old, new)
    history = Git().history(page)
    max_changes = max([(v['insertion'] + v['deletion']) for v in history])
    return render(request, 'waliki/history.html', {'page': page,
                                                   'slug': slug,
                                                   'history': history,
                                                   'max_changes': max_changes})


@permission_required('view_page')
def version(request, slug, version):
    page = get_object_or_404(Page, slug=slug)
    content = Git().version(page, version)
    if not content:
        raise Http404
    form = PageForm(instance=page, initial={'message': _('Restored version @%s') % version, 'raw': content},
                    is_hidden=True)
    content = Page.preview(page.markup, content)
    return render(request, 'waliki/version.html', {'page': page,
                                                   'content': content,
                                                   'slug': slug,
                                                   'version': version,
                                                   'form': form})

@permission_required('view_page')
def diff(request, slug, old, new):
    page = get_object_or_404(Page, slug=slug)
    old_content = Git().version(page, old)
    new_content = Git().version(page, new)
    return render(request, 'waliki/diff.html', {'page': page,
                                                'old_content': old_content,
                                                'new_content': new_content,
                                                'slug': slug,
                                                'old_commit': old,
                                                'new_commit': new})

def whatchanged(request):
    changes = []
    for version in Git().whatchanged():
        for path in version[-1]:
            try:
                page = Page.objects.get(path=path)
            except Page.DoesNotExist:
                continue
            changes.append({'page': page, 'author': version[0],
                            'version': version[2], 'message': version[3],
                            'date': version[4]})

    return render(request, 'waliki/whatchanged.html', {'changes': changes})