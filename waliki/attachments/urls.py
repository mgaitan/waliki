import django
try:
    from django.conf.urls import patterns, url  # django 1.8, 1.9
except ImportError:
    from django.conf.urls import url

from waliki.settings import WALIKI_SLUG_PATTERN
from waliki.attachments.views import attachments, delete_attachment, get_file

_pattern_list = [
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/attachments$', attachments,
        name='waliki_attachments'),
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/attachments/(?P<attachment_id_or_filename>.*)/delete$',
        delete_attachment, name='waliki_delete_attachment'),
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/attachment/((?P<attachment_id>\d+)/)?(?P<filename>.*)$',
        get_file,   name='waliki_attachment_file')
]


if django.VERSION[:2] >= (1, 10):
    urlpatterns = _pattern_list
else:
    urlpatterns = patterns('waliki.attachments.views',
                           *_pattern_list
                           )
