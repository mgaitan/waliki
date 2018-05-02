import json
from django.utils import timezone

from datetime import datetime
from django import VERSION
from django.templatetags.tz import localtime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.core.management import call_command
from django.http import HttpResponse
if VERSION[:2] >= (1, 10):
    from django.urls import reverse, reverse_lazy
else:
    from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.encoding import smart_text
from django.utils.six import StringIO, text_type
from django.views.decorators.csrf import csrf_exempt
from waliki.models import Page
from waliki.forms import PageForm
from waliki.acl import permission_required
from waliki import settings
from .models import Git
from django.contrib.syndication.views import Feed


@permission_required('view_page')
def history(request, slug, pag=1):
    page = get_object_or_404(Page, slug=slug)
    # The argument passed for pag might be a string, but we want to
    # do calculations on it. So we must cast just to be sure.
    pag = int(pag or 1)
    skip = (pag - 1) * settings.WALIKI_PAGINATE_BY
    max_count = settings.WALIKI_PAGINATE_BY
    if request.method == 'POST':
        new, old = request.POST.getlist('commit')
        return redirect('waliki_diff', slug, old, new)
    history = Git().history(page)
    max_changes = max([(v['insertion'] + v['deletion']) for v in history])
    return render(request, 'waliki/history.html', {'page': page,
                                                   'slug': slug,
                                                   'history': history[skip:(skip+max_count)],
                                                   'max_changes': max_changes,
                                                   'prev': pag - 1 if pag > 1 else None,
                                                   'next': pag + 1 if skip + max_count < len(history) else None})


@permission_required('view_page')
def version(request, slug, version, raw=False):
    page = get_object_or_404(Page, slug=slug)
    content = Git().version(page, version)
    if not content:
        raise Http404
    form = PageForm(instance=page, initial={'message': _('Restored version @%s') % version, 'raw': content},
                    is_hidden=True)

    if raw:
        return HttpResponse(content, content_type='text/plain; charset=utf-8')

    content = Page.preview(page.markup, content)
    return render(request, 'waliki/version.html', {'page': page,
                                                   'content': content,
                                                   'slug': slug,
                                                   'version': version,
                                                   'form': form})


@permission_required('view_page')
def diff(request, slug, old, new, raw=False):
    page = get_object_or_404(Page, slug=slug)
    if raw:
        content = Git().diff(page, new, old)
        return HttpResponse(content, content_type='text/plain; charset=utf-8')
    space = smart_text(b'\xc2\xa0', encoding='utf-8')  # non-breaking space character
    tab = space * 4
    old_content = Git().version(page, old).replace('\t', tab).replace(' ', space)
    new_content = Git().version(page, new).replace('\t', tab).replace(' ', space)
    return render(request, 'waliki/diff.html', {'page': page,
                                                'old_content': old_content,
                                                'new_content': new_content,
                                                'slug': slug,
                                                'old_commit': old,
                                                'new_commit': new})


def whatchanged(request, pag=1):
    now = timezone.now()
    changes = []
    # The argument passed for pag might be a string, but we want to
    # do calculations on it. So we must cast just to be sure.
    pag = int(pag or 1)
    skip = (pag - 1) * settings.WALIKI_PAGINATE_BY
    max_count = settings.WALIKI_PAGINATE_BY
    # Git().total_commits() returns a unicode string
    # but we want to do calculations on the number it represents,
    # therefore, we cast
    total = int(Git().total_commits())
    for version in Git().whatchanged(skip, max_count):
        for path in version[-1]:
            try:
                page = Page.objects.get(path=path)
            except Page.DoesNotExist:
                continue
            changes.append({'page': page, 'author': version[0],
                            'version': version[2], 'message': version[3],
                            'date': datetime.fromtimestamp(int(version[4]))})

    return render(request, 'waliki/whatchanged.html', {'changes': changes, 'now': now,
                                                       'prev': pag - 1 if pag > 1 else None,
                                                       'next': pag + 1 if skip + max_count < total else None})


class WhatchangedFeed(Feed):
    title = _("Last changes in the wiki")
    link = reverse_lazy('waliki_whatchanged')
    description_template = "waliki/whatchanged_rss.html"

    def items(self):
        changes = []
        for version, diff in Git().whatchanged_diff():
            for path in version[-1]:
                try:
                    page = Page.objects.get(path=path)
                except Page.DoesNotExist:
                    continue
                changes.append({'page': page, 'author': version[0],
                                'version': version[2], 'message': version[3],
                                'date': datetime.fromtimestamp(int(version[4])),
                                'diff': diff[1:-1].strip()})
        return changes

    def item_title(self, item):
        return item['page'].title

    def item_date(self, item):
        return localtime(item['date'])

    def item_link(self, item):
        return reverse_lazy("waliki_version", args=[item['page'].slug, item['version']])

    def author_email(self, item):
        if item:
            return item['author']
        return ''


@csrf_exempt
def webhook_pull(request, remote='origin'):
    if request.method == 'POST':
        try:
            log = Git().pull(remote)
            s = StringIO()
            call_command('sync_waliki', stdout=s)
            s.seek(0)
            r = {'pull': log, 'sync': s.read()}
            status_code = 200
        except Exception as e:
            r = {'error': text_type(e)}
            status_code = 500
        return HttpResponse(json.dumps(r), status=status_code,
                            content_type="application/json")

    return HttpResponse("POST to %s" % reverse("waliki_webhook_pull", args=(remote,)))
