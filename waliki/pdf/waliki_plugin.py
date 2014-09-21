from django.utils.translation import ugettext_lazy as _
from waliki.plugins import BasePlugin, register


class PdfPlugin(BasePlugin):
    slug = 'pdf'
    urls_page = ['waliki.pdf.urls']
    extra_page_actions = {'reStructuredText': [('waliki_pdf', _('Get as PDF'))]}

register(PdfPlugin)

