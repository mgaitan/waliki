from django import template

register = template.Library()

@register.inclusion_tag('waliki/extra_page_actions.html')
def extra_page_actions(page):
    from waliki.plugins import get_extra_page_actions
    return {'page': page, 'extra_page_actions': get_extra_page_actions()}

