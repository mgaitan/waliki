from django.conf.urls import patterns, url
from waliki.settings import WALIKI_SLUG_PATTERN


urlpatterns = patterns('waliki.slides.views',
    url(r'^(?P<slug>' + WALIKI_SLUG_PATTERN + ')/slides$', 'slides', name='waliki_slides'),
)
