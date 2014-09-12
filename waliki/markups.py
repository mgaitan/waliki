import re
from markups import (MarkdownMarkup, TextileMarkup,
                     ReStructuredTextMarkup as ReStructuredTextMarkupBase)
from django.core.urlresolvers import reverse
from .utils import get_slug


class ReStructuredTextMarkup(ReStructuredTextMarkupBase):
    def get_document_body(self, text):
        html = super(ReStructuredTextMarkup, self).get_document_body(text)
        # Convert unknow links to internal wiki links.
        # Examples:
        #   Something_ will link to '/something'
        #  `something great`_  to '/something_great'
        #  `another thing <thing>`_  '/thing'
        refs = re.findall(r'Unknown target name: \&quot;(.*)\&quot;', html)
        if refs:
            refs = '\n'.join('.. _%s: %s' % (ref, reverse('waliki_detail', args=(get_slug(ref),)))
                             for ref in refs)
            html = super(ReStructuredTextMarkup, self).get_document_body(text + '\n\n' + refs)
        return html


def get_all_markups():
    return {ReStructuredTextMarkup, TextileMarkup, MarkdownMarkup}


def find_markup_class_by_name(name):
    for markup in get_all_markups():
        if markup.name.lower() == name.lower():
            return markup
