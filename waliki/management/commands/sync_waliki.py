import os
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from waliki.settings import WALIKI_DATA_DIR, WALIKI_UPLOAD_TO
from waliki.models import Page
if 'waliki.attachments' in settings.INSTALLED_APPS:
    from waliki.attachments.models import Attachment
else:
    Attachment = None


class Command(BaseCommand):
    help = """Syncronize pages (and attachments) between files and the database"""

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

        # Deleted pages?
        for page in Page.objects.all():
            if not os.path.exists(page.abspath):
                self.stdout.write('Deleted page %s (missing %s)' % (page.get_absolute_url(), page.path))
                page.delete()

        if Attachment:
            class FakeAttachment(object):
                def __init__(self, page):
                    self.page = page

            for page in Page.objects.all():
                path = os.path.join(settings.MEDIA_ROOT, WALIKI_UPLOAD_TO(FakeAttachment(page), ''))
                if not os.path.exists(path):
                    continue
                for filename in os.listdir(path):
                    if not os.path.isfile(os.path.join(path, filename)):
                        continue
                    file = WALIKI_UPLOAD_TO(FakeAttachment(page), filename)
                    if page.attachments.filter(file=file):
                        continue
                    attachment = Attachment.objects.create(page=page, file=file, filename=filename)
                    self.stdout.write('Created attachment %s for %s' % (attachment, page.slug))

            for attachment in Attachment.objects.all():
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, attachment.file.name)):
                    self.stdout.write('Missing %s from %s. Deleted attachment object' % (attachment, attachment.page.slug))
                    attachment.delete()
