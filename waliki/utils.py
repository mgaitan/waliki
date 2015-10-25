import os
import re
import mimetypes
import unicodedata
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.six import PY2
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

def get_slug(text):
    def slugify(value):
        """
        same than django slugify but allowing uppercase and underscore
        """
        value = force_text(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s\/_-]', '', value).strip()
        return mark_safe(re.sub('[-\s]+', '-', value))

    if PY2:
        from django.utils.encoding import force_unicode
        text = force_unicode(text)
    for sep in ('_', '/'):
        text = sep.join(slugify(t) for t in text.split(sep))
    return text.strip('/')


def sanitize(html):
    return re.sub(r'<script.*?</script>', '', html, flags=re.MULTILINE)


def get_url(text, *args):
    # *args needed to receive prefix and suffix for markdowns wikilinks ext
    from waliki.settings import get_slug
    slug = get_slug(text)
    if slug:
        return reverse('waliki_detail', args=(get_slug(text),))
    return ''


def send_file(path, filename=None, content_type=None):
    # TODO : remove it and use django-sendfile instead
    if filename is None:
        filename = os.path.basename(path)
    if content_type is None:
        content_type, encoding = mimetypes.guess_type(filename)
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write(open(path, "rb").read())
    return response
