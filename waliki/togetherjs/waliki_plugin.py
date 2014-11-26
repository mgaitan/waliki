from waliki.plugins import BasePlugin, register


class TogetherJsPlugin(BasePlugin):
    slug = 'togetherjs'
    urls_page = []

register(TogetherJsPlugin)

