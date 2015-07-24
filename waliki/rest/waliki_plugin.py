from django.utils.translation import ugettext_lazy as _

from waliki.plugins import BasePlugin, register

class RestPlugin(BasePlugin):
    slug = 'rest'
    urls_page = ['waliki.rest.urls']

register(RestPlugin)