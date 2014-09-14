from django import template
from waliki.plugins import get_extra_page_actions

register = template.Library()


@register.inclusion_tag('waliki/extra_page_actions.html')
def extra_page_actions(page):
    return {'page': page, 'extra_page_actions': get_extra_page_actions()}

