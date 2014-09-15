from django import template

register = template.Library()


@register.inclusion_tag('waliki/extra_page_actions.html')
def extra_page_actions(page):
    from waliki.plugins import get_extra_page_actions
    return {'page': page, 'extra_page_actions': get_extra_page_actions()}


@register.filter(name="getattr")
def get_attr(obj, val):
    try:
        return getattr(obj, val)
    except AttributeError:
        try:
            return obj[val]
        except (KeyError, TypeError):
            return None