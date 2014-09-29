import re
import sys
from markups import (MarkdownMarkup as MarkdownMarkupBase,
                     TextileMarkup as TextileMarkupBase,
                     ReStructuredTextMarkup as ReStructuredTextMarkupBase)
from .utils import get_url
from waliki.settings import WALIKI_AVAILABLE_MARKUPS


class MarkdownMarkup(MarkdownMarkupBase):
    codemirror_mode_name = codemirror_mode = 'markdown'

    def __init__(self, filename=None, extensions=None, extension_configs=None):
        super(MarkdownMarkupBase, self).__init__(filename)
        import markdown
        self.markdown = markdown
        self.requested_extensions = extensions or []
        self.extension_configs = extension_configs or {}
        self.global_extensions = self._get_global_extensions(filename)
        self.document_extensions = []
        self._apply_extensions()

    def _apply_extensions(self):
        extensions = (self.requested_extensions or
                      self.global_extensions) + self.document_extensions
        # Remove duplicate entries
        extensions = list(set(extensions))
        # We have two "virtual" extensions
        self.mathjax = ('mathjax' in extensions)
        self.remove_mathjax = ('remove_extra' in extensions)
        if 'remove_extra' in extensions:
            extensions.remove('remove_extra')
        elif 'extra' not in extensions:
            extensions.append('extra')
        if self.mathjax:
            extensions.remove('mathjax')
        for extension in extensions:
            if not extension:
                extensions.remove(extension)
                continue
            if not self._check_extension_exists(extension):
                sys.stderr.write(
                    'Extension "%s" does not exist.\n' % extension)
                extensions.remove(extension)
        self.md = self.markdown.Markdown(extensions, extension_configs=self.extension_configs,
                                         output_format='html5')
        for i, pattern in enumerate(self._get_mathjax_patterns()):
            self.md.inlinePatterns.add('mathjax%d' % i, pattern, '<escape')
        self.extensions = extensions


class ReStructuredTextMarkup(ReStructuredTextMarkupBase):

    codemirror_mode = codemirror_mode_name = 'rst'

    def __init__(self, filename=None, **kwargs):
        settings_overrides = kwargs.pop('settings_overrides', None)
        super(ReStructuredTextMarkup, self).__init__(filename, settings_overrides)
        self.kwargs = kwargs

    def publish_parts(self, text):
        if 'rest_parts' in self._cache:
            return self._cache['rest_parts']
        parts = self._publish_parts(text, source_path=self.filename,
                                    settings_overrides=self.overrides,
                                    **self.kwargs)
        if self._enable_cache:
            self._cache['rest_parts'] = parts
        return parts

    def get_document_body(self, text):
        html = super(ReStructuredTextMarkup, self).get_document_body(text)
        # Convert unknow links to internal wiki links.
        # Examples:
        #   Something_ will link to '/something'
        #  `something great`_  to '/something_great'
        #  `another thing <thing>`_  '/thing'
        refs = re.findall(r'Unknown target name: [\&quot;|"](.*)[\&quot;|"]', html)
        if refs:
            refs = '\n'.join('.. _%s: %s' % (ref, get_url(ref))
                             for ref in refs)
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
