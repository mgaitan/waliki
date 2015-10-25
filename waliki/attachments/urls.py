from django.conf.urls import patterns, url
from waliki.settings import WALIKI_SLUG_PATTERN

urlpatterns = patterns('waliki.attachments.views',
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/attachments$', 'attachments',
        name='waliki_attachments'),
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/attachments/(?P<attachment_id_or_filename>.*)/delete$',
        'delete_attachment', name='waliki_delete_attachment'),
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/attachment/((?P<attachment_id>\d+)/)?(?P<filename>.*)$',
        'get_file',   name='waliki_attachment_file')
)
