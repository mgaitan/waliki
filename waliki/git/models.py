from django.dispatch import receiver
from waliki.signals import page_saved, page_preedit
from . import Git


@receiver(page_saved)
def commit(sender, page, author, message, form_extra_data, **kwargs):
    parent = form_extra_data.get('parent', None)
    Git().commit(page, author=author, message=message, parent=parent)


@receiver(page_preedit)
def get_last_version(sender, page, **kwargs):
    last = Git().last_version(page)
    return {'form_extra_data': {'parent': last}}
