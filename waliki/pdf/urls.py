from django.conf.urls import patterns, url
from waliki.settings import WALIKI_SLUG_PATTERN


urlpatterns = patterns('waliki.pdf.views',
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/pdf$', 'pdf', name='waliki_pdf'),
)
