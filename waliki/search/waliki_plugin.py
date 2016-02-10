from django.utils.translation import ugettext_lazy as _
from waliki.plugins import BasePlugin, register


class SearchPlugin(BasePlugin):
    slug = 'search'
    urls_page = ['waliki.search.urls']
    navbar_links = (('haystack_search', _('Search')),)

register(SearchPlugin)
