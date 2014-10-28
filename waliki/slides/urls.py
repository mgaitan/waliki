from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.slides.views',
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/slides$', 'slides', name='waliki_slides'),
)
