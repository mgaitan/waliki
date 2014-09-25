import os
from optparse import make_option
from django.core.management.base import BaseCommand  # CommandError
from waliki.settings import WALIKI_DATA_DIR
from waliki.models import Page


class Command(BaseCommand):
    help = 'Syncronize pages between files and the database'

    option_list = (
        make_option('--extensions',
                    dest='extensions',
                    default=".rst, .md",
                    help="Look for files with this extensions, separated by comma. Default: '.rst, .md'"),
        make_option('--ignored_dirs',
                    dest='ignored_dirs',
                    default=".git",
                    help="List of directories to ignore, separated by comman. Default: '.git'"),
    ) + BaseCommand.option_list

    def handle(self, *args, **options):
        extensions = [ext.strip() for ext in options['extensions'].split(',')]
        ignored_dirs = [d.strip() for d in options['ignored_dirs'].split(',')]
        for root, dirs, files in os.walk(WALIKI_DATA_DIR):
            [dirs.remove(d) for d in ignored_dirs if d in dirs]
            for filename in files:
                if os.path.splitext(filename)[1] not in extensions:
                    continue
                path = os.path.join(root.replace(WALIKI_DATA_DIR, ''), filename).strip('/')

                if not Page.objects.filter(path=path).exists():
                    page = Page.from_path(path)
                    self.stdout.write('Created page %s for %s' % (page.get_absolute_url(), path))

        for page in Page.objects.all():
            if not os.path.exists(page.abspath):
                self.stdout.write('Deleted page %s (missing %s)' % (page.get_absolute_url(), page.path))
                page.delete()