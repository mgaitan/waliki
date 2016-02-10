# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from haystack.forms import SearchForm

from waliki.search.views import WalikiSearchView

try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('haystack.views',
    url(r'^search$', WalikiSearchView(form_class=SearchForm), name='haystack_search'),
)
