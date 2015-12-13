import json
import os
import mock
import unittest
from django.test import TestCase
from waliki.models import Page
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from waliki import settings
from waliki.models import Redirect
from waliki.forms import MovePageForm, DeleteForm

from .factories import PageFactory, UserFactory, ACLRuleFactory
try:
    from sh import hovercraft
    hovercraft = hovercraft.bake(_tty_out=False)
except ImportError:
    hovercraft = False


class TestSlide(TestCase):
    def setUp(self):
        content = """
Slide 1
=======

- Item 1.1
- Item 1.2

----

Slide 2
=======

- Item 2.1
- Item 2.2"""

        self.page = PageFactory(raw=content, slug='slide-example')
        self.slide_url = reverse('waliki_slides', args=(self.page.slug,))

    @unittest.skipIf(not hovercraft, 'no hovercraft')
    def test_slide(self):
        response = self.client.get(self.slide_url)
        self.assertContains(response, 'Slide 1')
        self.assertContains(response, 'Item 1.1')
        self.assertContains(response, 'Item 1.2')
        self.assertContains(response, 'Slide 2')
        self.assertContains(response, 'Item 2.1')
        self.assertContains(response, 'Item 2.2')

    @unittest.skipIf(not hovercraft, 'no hovercraft')
    def test_slide_no_perm(self):
        with mock.patch('waliki.acl.WALIKI_ANONYMOUS_USER_PERMISSIONS', return_value=()):
            response = self.client.get(self.slide_url)
        self.assertRedirects(response, '/accounts/login/?next=' + self.slide_url)
