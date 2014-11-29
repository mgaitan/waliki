from django.utils.translation import ugettext_lazy as _
from waliki.plugins import BasePlugin, register


class SlidesPlugin(BasePlugin):
    slug = 'slides'
    urls_page = ['waliki.slides.urls']
    extra_page_actions = {'reStructuredText': [('waliki_slides', _('View as slides'))]}

register(SlidesPlugin)

