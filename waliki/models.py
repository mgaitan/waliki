# -*- coding: utf-8 -*-
import os.path
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import get_user_model

from . import _markups
from .utils import get_slug
from .settings import WALIKI_DEFAULT_MARKUP, WALIKI_MARKUPS_SETTINGS, WALIKI_DATA_DIR



class Page(models.Model):
    MARKUP_CHOICES = [(m.name, m.name) for m in _markups.get_all_markups()]
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    path = models.CharField(max_length=200, unique=True)
    markup = models.CharField(verbose_name=_('Markup'), max_length=20,
                              choices=MARKUP_CHOICES, default=WALIKI_DEFAULT_MARKUP)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        permissions = (
            ('view_page', 'Can view page'),
        )

    class EditionConflict(Exception):
        pass

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.path

    def get_absolute_url(self):
        return reverse('waliki_detail', args=(self.slug,))

    def get_edit_url(self):
        return reverse('waliki_edit', args=(self.slug,))

    def save(self, *args, **kwargs):
        self.slug = self.slug.strip('/')
        if not self.path:
            self.path = self.slug + self._markup.file_extensions[0]
        super(Page, self).save(*args, **kwargs)

    @classmethod
    def from_path(cls, path, markup=None):

        filename, ext = os.path.splitext(path)
        if markup and isinstance(markup, string_types):
            markup = _markups.find_markup_class_by_name(markup)
        else:
            markup = _markups.find_markup_class_by_extension(ext)
        page = Page(path=path, slug=get_slug(filename), markup=markup.name)
        page.title = page._get_part('get_document_title')
        page.save()
        return page

    @property
    def raw(self):
        filename = self.abspath
        if not os.path.exists(filename):
            return ""
        return open(filename, "r").read()

    @raw.setter
    def raw(self, value):
        filename = os.path.join(WALIKI_DATA_DIR, self.path)
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError:
            pass
        with open(filename, "w") as f:
            f.write(value)

    @property
    def abspath(self):
        return os.path.abspath(os.path.join(WALIKI_DATA_DIR, self.path))

    @staticmethod
    def get_markup_instance(markup):
        markup_settings = WALIKI_MARKUPS_SETTINGS.get(markup, None)
        markup_class = _markups.find_markup_class_by_name(markup)
        return markup_class(**markup_settings)

    @staticmethod
    def preview(markup, text):
        return Page.get_markup_instance(markup).get_document_body(text)

    @property
    def _markup(self):
        if not hasattr(self, '__markup_instance'):
            self.__markup_instance = Page.get_markup_instance(self.markup)
        return self.__markup_instance

    def _get_part(self, part):
        return getattr(self._markup, part)(self.raw)

    @property
    def body(self):
        return self._get_part('get_document_body')

    @property
    def stylesheet(self):
        return self._get_part('get_stylesheet')

    @property
    def javascript(self):
        return self._get_part('get_javascript')


class ACLRule(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True)
    slug = models.CharField(max_length=200)
    as_namespace = models.BooleanField(verbose_name=_('As namespace'), default=False)
    permissions = models.ManyToManyField(Permission, limit_choices_to={'content_type__app_label': 'waliki'})
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __unicode__(self):
        return _('Rule: %(name)s for /%(slug)s') % {'name': self.name, 'slug': self.slug}

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = _('ACL rule')
        verbose_name_plural = _('ACL rules')

    @classmethod
    def get_users_for(cls, perm, slug):
        # TODO check parent namespace for an slug
        User = get_user_model()
        lookup = Q(aclrule__permissions__codename=perm, aclrule__slug=slug)
        lookup |= Q(groups__aclrule__permissions__codename=perm, groups__aclrule__slug=slug)
        return User.objects.filter(lookup).distinct()
