from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.git.views',
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/history$', 'history', name='waliki_history'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/version/(?P<version>[0-9a-f]{5,40})$', 'version', name='waliki_version'),
)
