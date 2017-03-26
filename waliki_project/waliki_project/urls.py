
try:
    from django.conf.urls import patterns, include, url
except ImportError:
    patterns = None
    from django.conf.urls import url, include

from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^boxes-example/', TemplateView.as_view(template_name="boxes_example.html")),
    url(r'^', include('waliki.urls')),
]

if patterns:

    urlpatterns = patterns('',
        # url(r'^$', 'waliki_project.views.home', name='home'),
        *urlpatterns
    )
