# -*- coding: utf-8 -*-
import os.path
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.six import text_type
from django.core.urlresolvers import reverse
from waliki.models import Page
from waliki.settings import WALIKI_UPLOAD_TO


@python_2_unicode_compatible
class Attachment(models.Model):
    page = models.ForeignKey(Page, related_name='attachments')
    file = models.FileField(upload_to=WALIKI_UPLOAD_TO, max_length=300)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        return reverse('waliki_attachment_file', args=(self.page.slug, text_type(self)))


# @receiver(pre_delete, sender=Attachment)
# def attachment_delete(sender, instance, **kwargs):
#    try:
#        # instance.file.delete(False)
#        pass
#    except SuspiciousFileOperation:
#        pass
