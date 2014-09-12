from django.core.urlresolvers import reverse
from django.utils.text import slugify


def get_slug(text):
    return '/'.join(slugify(t) for t in text.split('/'))


def get_url(text, **kwargs):
    return reverse('waliki_detail', args=(get_slug(text),))
