# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from waliki.models import Page
from waliki.settings import WALIKI_UPLOAD_TO


class Attachment(models.Model): 
    page = models.ForeignKey(Page, related_name='attachments')
    file = models.FileField(upload_to=WALIKI_UPLOAD_TO)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")


    def __unicode__(self):
        return self.file.filename
    
