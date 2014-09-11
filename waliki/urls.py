from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('waliki.views',
    url(r'^$', 'home', name='home'),
    url(r'^_preview$', 'preview', name='waliki_preview'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/edit$', 'edit', name='waliki_edit'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/delete$', 'delete', name='waliki_delete'),
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)$', 'detail', name='waliki_detail')
)
