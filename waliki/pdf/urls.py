import django
try:
    from django.conf.urls import patterns, url  # django 1.8, 1.9
except ImportError:
    from django.conf.urls import url

from waliki.settings import WALIKI_SLUG_PATTERN
from waliki.pdf.views import pdf

_pattern_list = [
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/pdf$',
        pdf, name='waliki_pdf'),
]

if django.VERSION[:2] >= (1, 10):
    urlpatterns = _pattern_list
else:
    urlpatterns = patterns('waliki.pdf.views',
                           *_pattern_list
                           )
