import os
import re
from waliki.signals import page_saved
from optparse import make_option
from django.core.management.base import BaseCommand  # CommandError
from waliki.settings import WALIKI_DATA_DIR
from waliki.models import Page
from django.utils.translation import ugettext_lazy as _
try:
    from waliki.attachments.models import Attachment
except ImportError:
    Attachment = None


def clean_meta(rst_content):
    """remove moinmoin metada from the top of the file"""

    rst = rst_content.split('\n')
    for i, line in enumerate(rst):
        if line.startswith('#'):
            continue
        break
    return '\n'.join(rst[i:])


def delete_relative_links(rst_content):
    """remove links relatives. Waliki point them correctly implicitly"""

    return re.sub(r'^(\.\. .*: \.\./.*)\n$', '', rst_content, flags=re.MULTILINE)


def attachments(rst_content, slug):

    def rep(matchobj):
        for filename in matchobj.groups(1):
            try:
                a = Attachment.objects.filter(file__endswith=filename, page__slug=slug)[0]
            except IndexError:
                print('Cant find %s in %s' % (filename, slug))
                return None
        return '`%s <%s>`_' % (filename, a.get_absolute_url())

    return re.sub(r'`attachment:(.*)`_', rep, rst_content, flags=re.MULTILINE)


def directives(rst_content):
    for directive in re.findall(r':(\w+):`.*`', rst_content, flags=re.MULTILINE):
        rst_content += """

.. role:: {directive}
   :class: {directive}

""".format(directive=directive)
    return rst_content


class Command(BaseCommand):
    help = 'Cleanups for a moin2git import'

    option_list = (
        make_option('--limit-to',
                    dest='slug',
                    default='',
                    help="optional slug namespace"),
    ) + BaseCommand.option_list

    def handle(self, *args, **options):
        slug = options['slug']
        if slug:
            pages = Page.objects.filter(slug__startswith=slug)
        else:
            pages = Page.objects.all()

        for page in pages:
            print('Cleaning up %s' % page.slug)
            raw = clean_meta(page.raw)
            raw = delete_relative_links(raw)
            raw = attachments(raw, page.slug)
            raw = directives(raw)
            page.raw = raw
            if not page.title:
                page.title = page._get_part('get_document_title')

            page.save()
            page_saved.send_robust(sender='moin',
                                   page=page,
                                   author=None,
                                   message=_("RestructuredText clean up"),
                                   form_extra_data={})