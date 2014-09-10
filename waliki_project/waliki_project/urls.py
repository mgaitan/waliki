from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'waliki_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('waliki.urls')),
)
