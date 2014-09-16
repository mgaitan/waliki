from django.conf.urls import patterns, url

urlpatterns = patterns('waliki.pdf.views',
    url(r'^(?P<slug>[a-zA-Z0-9-\/]+)/pdf$', 'pdf', name='waliki_pdf'),
)
