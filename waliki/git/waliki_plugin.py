from django.utils.translation import ugettext_lazy as _
from waliki.plugins import BasePlugin, register


class GitPlugin(BasePlugin):

    slug = 'git'
    urls_page = ['waliki.git.urls']
    extra_page_actions = {'all': [('waliki_history', _('History'))]}
    navbar_links = (('waliki_whatchanged', _('What changed')),)

register(GitPlugin)

