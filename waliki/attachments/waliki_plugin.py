from django.utils.translation import ugettext_lazy as _
from waliki.plugins import BasePlugin, register


class AttachmentsPlugin(BasePlugin):
    slug = 'attachments'
    urls_page = ['waliki.attachments.urls']
    extra_edit_actions = {'all': [('waliki_attachments', _('Attachments'))]}
    includes_edit = {'content': 'waliki/attachments_modal.html',
    				 'extra_script': 'waliki/attachments_js.html'}

register(AttachmentsPlugin)

