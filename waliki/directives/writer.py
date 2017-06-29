from rst2html5_ import HTML5Writer
from ..utils import get_url

class WalikiAutolinksMixin(object):
    def __init__(self, *args, **kwargs):
        super(WalikiAutolinksMixin, self).__init__(*args, **kwargs)
        self.unknown_reference_resolvers = (
            (self.wiki_resolver,) + self.unknown_reference_resolvers)

    def wiki_resolver(self, node):
        refuri = None
        if hasattr(node, 'indirect_reference_name'):
            refuri = node.indirect_reference_name
        elif len(node['ids']) != 0:
            # If the node has an id then it's probably an internal link. Let
            # docutils generate an error.
            pass
        elif node.hasattr('name'):
            refuri = node['name']
        else:
            refuri = node['refname']

        refuri = self.wiki_resolve_url(refuri)
        if not refuri:
            return False

        node['refuri'] = refuri
        del node['refname']
        node.resolved = 1
        return True

    wiki_resolver.priority = 1


class WalikiHTML5Writer(HTML5Writer,WalikiAutolinksMixin):
    def __init__(self):
        HTML5Writer.__init__(self)
        WalikiAutolinksMixin.__init__(self)

    def wiki_resolve_url(self, slug):
        return get_url(slug)
