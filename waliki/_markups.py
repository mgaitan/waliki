import re
import sys
from markups import (MarkdownMarkup as MarkdownMarkupBase,
                     TextileMarkup as TextileMarkupBase,
                     ReStructuredTextMarkup as ReStructuredTextMarkupBase)
from pyquery import PyQuery
from .utils import get_url
from waliki.settings import WALIKI_AVAILABLE_MARKUPS


class MarkdownMarkup(MarkdownMarkupBase):
    codemirror_mode_name = codemirror_mode = 'markdown'
    IMAGE_LINE = '![](%(url)s)'
    LINK_LINE = '[%(filename)s](<%(url)s>)'


    def __init__(self, filename=None, extensions=None, extension_configs=None):
        super(MarkdownMarkup, self).__init__(filename)
        self.md.set_output_format('html5')
        self.md.registerExtensions(extensions, extension_configs)


class ReStructuredTextMarkup(ReStructuredTextMarkupBase):

    IMAGE_LINE = '.. image:: %(url)s'
    LINK_LINE = '`%(filename)s <%(url)s>`_'

    codemirror_mode = codemirror_mode_name = 'rst'

    def __init__(self, filename=None, **kwargs):
        settings_overrides = kwargs.pop('settings_overrides', None)
        self.reader = kwargs.pop('reader', None)
        super(ReStructuredTextMarkup, self).__init__(filename, settings_overrides)
        if not self.reader:
            from waliki.directives.transforms import WalikiReader
            self.reader = WalikiReader()

        self.kwargs = kwargs

    def publish_parts(self, text):
        if 'rest_parts' in self._cache:
            return self._cache['rest_parts']
        parts = self._publish_parts(text, source_path=self.filename,
                                    settings_overrides=self.overrides,
                                    reader=self.reader, **self.kwargs)
        if self._enable_cache:
            self._cache['rest_parts'] = parts
        return parts

    def get_document_body(self, text):
        html = super(ReStructuredTextMarkup, self).get_document_body(text)
        if not html:
            return html

        # Convert unknown links to internal wiki links.
        # Examples:
        #   Something_ will link to '/something'
        #  `something great`_  to '/something-great'
        #  `another thing <thing>`_  '/thing'
        refs = [a.text[:-1] for a in PyQuery(html)('a.problematic') if not re.match(r'\|(.*)\|', a.text)]
        # substitions =  [a.text[:-1] for a in PyQuery(html)('a.problematic') if re.match(r'\|(.*)\|', a.text)]
        if refs:
            refs = '\n'.join('.. _%s: %s' % (ref, get_url(ref))
                             for ref in refs if get_url(ref))
            html = super(ReStructuredTextMarkup, self).get_document_body(
                        text + '\n\n' + refs)
        return html


class TextileMarkup(TextileMarkupBase):
    codemirror_mode_name = codemirror_mode = 'textile'


def get_all_markups():
    return [find_markup_class_by_name(s) for s in WALIKI_AVAILABLE_MARKUPS]


def find_markup_class_by_name(name):
    for markup in (ReStructuredTextMarkup, MarkdownMarkup, TextileMarkup):
        if markup.name.lower() == name.lower():
            return markup


def find_markup_class_by_extension(extension):
    for markup in (ReStructuredTextMarkup, MarkdownMarkup, TextileMarkup):
        if extension.lower() in markup.file_extensions:
            return markup
