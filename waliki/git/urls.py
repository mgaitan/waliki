from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.git.views',
    url(r'^_whatchanged$', 'whatchanged', name='waliki_whatchanged'),       # noqa
    url(r'^_hooks/pull/(?P<remote>[a-zA-Z0-9]+)$', 'webhook_pull', name='waliki_webhook_pull'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/history$', 'history', name='waliki_history'),

    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/version/(?P<version>.{4,40})/raw$', 'version', {'raw': True},
        name='waliki_version_raw'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/version/(?P<version>.{4,40})$', 'version', name='waliki_version'),

    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/diff/(?P<old>.{4,40})\.\.(?P<new>.{4,40})/raw$',
        'diff', {'raw': True}, name='waliki_diff_raw'),

    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/diff/(?P<old>.{4,40})\.\.(?P<new>.{4,40})$', 'diff', name='waliki_diff'),
)
