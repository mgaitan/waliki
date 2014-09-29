from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.git.views',
    url(r'^_whatchanged$', 'whatchanged', name='waliki_whatchanged'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/history$', 'history', name='waliki_history'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/version/(?P<version>.{4,40})$', 'version', name='waliki_version'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/diff/(?P<old>.{4,40})\.\.(?P<new>.{4,40})$', 'diff', name='waliki_diff'),
)
