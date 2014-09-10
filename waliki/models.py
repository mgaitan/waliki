# -*- coding: utf-8 -*-
import os.path
from django.db import models
import markups
from waliki import settings


class Page(models.Model):
    MARKUP_CHOICES = [(m.name, m.name) for m in markups.get_all_markups()]
    slug = models.CharField(max_length=200, unique=True)
    path = models.CharField(max_length=200, unique=True)
    markup = models.CharField(max_length=20, choices=MARKUP_CHOICES, default=settings.WALIKI_DEFAULT_MARKUP)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.path

    @property
    def raw_text(self):
        filename = os.path.join(settings.WALIKI_DATA_DIR, self.path)
        if not os.path.exists(filename):
            try:
                os.makedirs(os.path.dirname(filename))
            except FileExistsError:
                pass
            with open(filename, "w") as f:
                f.write("")
        return open(filename, "r").read()

    @property
    def _markup(self):
        markup_settings = settings.WALIKI_MARKUPS_SETTINGS.get(self.markup, None)
        return markups.find_markup_class_by_name(self.markup)(settings_overrides=markup_settings)

    def _get_part(self, part):
        return getattr(self._markup, part)(self.raw_text)

    @property
    def body(self):
        return self._get_part('get_document_body')

    @property
    def stylesheet(self):
        return self._get_part('get_stylesheet')

    @property
    def javascript(self):
        return self._get_part('get_javascript')

