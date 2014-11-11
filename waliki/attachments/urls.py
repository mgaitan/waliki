from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.attachments.views',
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/attachments$', 'attachments',
        name='waliki_attachments'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/attachments/(?P<attachment_id>\d+)/delete$',
        'delete_attachment', name='waliki_delete_attachment'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/attachment/(?P<attachment_id>\d+)/(?P<filename>.*)$',
        'get_file',   name='waliki_attachment_file')
)
