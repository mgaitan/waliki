# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import django
try:
    from django.conf.urls import patterns, url  # django 1.8, 1.9
except ImportError:
    from django.conf.urls import url

from haystack.forms import SearchForm
from waliki.search.views import WalikiSearchView


_pattern_list = [
    url(r'^search$', WalikiSearchView(
        form_class=SearchForm), name='haystack_search'),
]

if django.VERSION[:2] >= (1, 10):
    urlpatterns = _pattern_list
else:
    urlpatterns = patterns('haystack.views',
                           *_pattern_list
                           )
