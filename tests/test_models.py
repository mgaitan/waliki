#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.test import TestCase
from waliki.models import Page
from waliki.settings import deep_update
from waliki import settings

rst = """
Title
=====

some rst markup
"""


class TestPage(TestCase):

    def test_content_saved_on_attribute_set(self):
        page = Page(path='test.rst')
        page.raw = rst
        path = os.path.join(settings.WALIKI_DATA_DIR, 'test.rst')
        self.assertEqual(page.abspath, path)
        self.assertTrue(os.path.exists(path))
        content = open(path).read()
        self.assertEqual(content, rst)

    def test_get_body(self):
        page = Page(path='test.rst')
        page.raw = rst
        self.assertEqual(page.body, """\n    <h2>Title</h2>\n    <p>some rst markup</p>\n""")


class TestMarkupSettings(TestCase):

    def test_deep_update(self):
        d = {'reStructuredText': {
                'settings_overrides': {              # noqa
                        'initial_header_level': 2,
                        'record_dependencies': True}
                },
             'Markdown': ['...']
             }
        u = {'reStructuredText': {
                'settings_overrides': {              # noqa
                        'initial_header_level': 1
            }}}
        expected = {'reStructuredText': {
                    'settings_overrides': {              # noqa
                        'initial_header_level': 1,
                        'record_dependencies': True}
                }, 'Markdown': ['...']
             }
        self.assertEqual(deep_update(d, u), expected)
