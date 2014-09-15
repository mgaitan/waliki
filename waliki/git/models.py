from django.dispatch import receiver
from waliki.signals import page_saved
from . import Git


@receiver(page_saved)
def commit(sender, page, author, message, **kwargs):
    Git().commit(page.path, author=author, message=message)
