from django.conf.urls import patterns, url, include
from django.contrib import admin
from waliki.settings import WALIKI_SLUG_PATTERN
from .plugins import load_plugins, page_urls

admin.autodiscover()
load_plugins()


def waliki_urls():
    base = [url(r'^$', 'home', name='waliki_home'),
            url(r'^_new$', 'new', name='waliki_new'),
            url(r'^_get_slug$', 'get_slug', name='waliki_get_slug'),
            url(r'^_preview$', 'preview', name='waliki_preview')]

    for pattern in page_urls():
        base.append(url(r'^', include(pattern)))

    base += [url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/edit$', 'edit', name='waliki_edit'),
             url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/delete$', 'delete', name='waliki_delete'),
             url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/move$', 'move', name='waliki_move'),
             url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/raw$', 'detail', {'raw': True}, name='waliki_detail_raw'),
             url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')$', 'detail', name='waliki_detail'),
             ]
    return base


urlpatterns = patterns('waliki.views',
    *waliki_urls()
)
