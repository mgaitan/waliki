import os
import mimetypes
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.text import slugify


def get_slug(text):
    return '/'.join(slugify(t) for t in text.split('/')).strip('/')


def get_url(text, *args):
    # *args needed to receive prefix and suffix for markdowns wikilinks ext
    return reverse('waliki_detail', args=(get_slug(text),))


def send_file(path, filename=None, content_type=None):
    if filename is None:
        filename = os.path.basename(path)
    if content_type is None:
        content_type, encoding = mimetypes.guess_type(filename)
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write(open(path, "rb").read())
    return response
