from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.attachments.views',
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/attachments$', 'attachments', name='waliki_attachments'),
)
