import os
import mimetypes
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.text import slugify


def get_slug(text):
    return '/'.join(slugify(t) for t in text.split('/'))


def get_url(text, **kwargs):
    return reverse('waliki_detail', args=(get_slug(text),))


def send_file(path, filename=None, mimetype=None):
    if filename is None:
        filename = os.path.basename(path)
    if mimetype is None:
        mimetype, encoding = mimetypes.guess_type(filename)
    response = HttpResponse(mimetype=mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write(open(path, "rb").read())
    return response
