from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from waliki.signals import page_saved, page_preedit, page_moved
from . import Git


@receiver(page_saved)
def commit(sender, page, author, message, form_extra_data, **kwargs):
    parent = form_extra_data.get('parent', None)
    was_moved = kwargs.get('was_moved', False)
    there_were_changes = Git().commit(page, author=author, message=message,
                                           parent=parent)
    if there_were_changes and not was_moved:
        msg = _('There were changes in the page during your edition. Auto-merge has been applied.')
        return {'messages': {'warning': msg}}


@receiver(page_preedit)
def get_last_version(sender, page, **kwargs):
    last = Git().last_version(page)
    return {'form_extra_data': {'parent': last}}


@receiver(page_moved)
def move(sender, page, old_path, author, message, commit=True, **kwargs):
    Git().mv(sender, page, old_path, author, message, commit)
