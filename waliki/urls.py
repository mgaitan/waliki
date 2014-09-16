from django.conf.urls import patterns, url, include
from django.contrib import admin
from .plugins import load_plugins, page_urls
admin.autodiscover()
load_plugins()


def waliki_urls():
    base = [url(r'^$', 'home', name='waliki_home'),
            url(r'^_preview$', 'preview', name='waliki_preview')]

    for pattern in page_urls():
        base.append(url(r'^', include(pattern)))

    base += [url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/edit$', 'edit', name='waliki_edit'),
             url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/delete$', 'delete', name='waliki_delete'),
             url(r'^(?P<slug>[a-zA-Z0-9-\/]+)$', 'detail', name='waliki_detail')]
    return base


urlpatterns = patterns('waliki.views',
    *waliki_urls()
)
