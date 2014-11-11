from django import template
from django.core.urlresolvers import reverse
from waliki.acl import check_perms as check_perms_helper
from waliki.models import Page
from waliki.forms import PageForm


register = template.Library()


@register.inclusion_tag('waliki/extra_page_actions.html')
def extra_page_actions(page):
    from waliki.plugins import get_extra_page_actions
    return {'page': page, 'extra_page_actions': get_extra_page_actions()}


@register.inclusion_tag('waliki/extra_edit_actions.html')
def extra_edit_actions(page):
    from waliki.plugins import get_extra_edit_actions
    return {'page': page, 'extra_edit_actions': get_extra_edit_actions()}


@register.inclusion_tag('waliki/entry_point.html', takes_context=True)
def entry_point(context, block_name):
    """include an snippet at the bottom of a block, if it exists

    For example, if the plugin with slug 'attachments' is registered

       waliki/attachments_edit_content.html  will be included with

        {% entry_point 'edit_content' %}

    which is declared at the bottom of the block 'content' in edit.html
    """
    from waliki.plugins import get_plugins
    includes = []
    for plugin in get_plugins():
        template_name = 'waliki/%s_%s.html' % (plugin.slug, block_name)
        try:
            # template exists
            template.loader.get_template(template_name)
            includes.append(template_name)
        except template.TemplateDoesNotExist:
            continue
    context.update({'includes': includes})
    return context

@register.inclusion_tag('waliki/navbar_links.html')
def navbar_links():
    from waliki.plugins import get_navbar_links
    return {'navbar_links': get_navbar_links()}


@register.filter(name="getattr")
def get_attr(obj, val):
    try:
        return getattr(obj, val)
    except AttributeError:
        try:
            return obj[val]
        except (KeyError, TypeError):
            return None


class CheckPermissionsNode(template.Node):

    def __init__(self, perms, user, slug, context_var):
        self.perms = template.Variable(perms)
        self.user = template.Variable(user)
        self.slug = template.Variable(slug)
        self.context_var = context_var

    def render(self, context):
        perms = [perm.strip() for perm in self.perms.literal.split(',')]
        user = self.user.resolve(context)
        slug = self.slug.literal or self.slug.resolve(context)
        if slug:
            context[self.context_var] = check_perms_helper(perms, user, slug)
        else:
            context[self.context_var] = False
        return ''


@register.tag
def check_perms(parser, token):
    """
    Returns a list of permissions (as ``codename`` strings) for a given
    ``user``/``group`` and ``obj`` (Model instance).

    Parses ``check_perms`` tag which should be in format::

        {% check_perms "perm1[, perm2, ...]" for user in slug as "context_var" %}

    or

        {% check_perms "perm1[, perm2, ...]" for user in "slug" as "context_var" %}

    .. note::

       Make sure that you set and use those permissions in same template
       block (``{% block %}``).

    Example of usage (assuming ``page` objects are available from *context*)::

        {% check_perms "delete_page" for request.user in page.slug as "can_delete" %}
        {% if can_delete %}
            ...
        {% endif %}

    """
    bits = token.split_contents()
    format = '{% check_perms "perm1[, perm2, ...]" for user in slug as "context_var" %}'
    if len(bits) != 8 or bits[2] != 'for' or bits[4] != "in" or bits[6] != 'as':
        raise template.TemplateSyntaxError("get_obj_perms tag should be in "
                                           "format: %s" % format)
    perms = bits[1]
    user = bits[3]
    slug = bits[5]
    context_var = bits[7]
    if perms[0] != perms[-1] or perms[0] not in ('"', "'"):
        raise template.TemplateSyntaxError("check_perms tag's perms "
                                           "argument should be in quotes")

    if context_var[0] != context_var[-1] or context_var[0] not in ('"', "'"):
        raise template.TemplateSyntaxError("check_perms tag's context_var "
                                           "argument should be in quotes")
    context_var = context_var[1:-1]
    return CheckPermissionsNode(perms, user, slug, context_var)


@register.inclusion_tag("waliki/box.html", takes_context=True)
def waliki_box(context, slug, show_edit=True, *args, **kwargs):
    """
    A templatetag to render a wiki page content as a box in any webpage,
    and allow rapid edition if you have permission.

    It's inspired in `django-boxes`_

    .. _django-boxes: https://github.com/eldarion/django-boxes
    """

    request = context["request"]
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None

    if (page and check_perms_helper('change_page', request.user, slug)
            or (not page and check_perms_helper('add_page', request.user, slug))):
        form = PageForm(instance=page, initial={'slug': slug})
        form_action = reverse("waliki_edit", args=[slug])
    else:
        form = None
        form_action = None

    return {
        "request": request,
        "slug": slug,
        "label": slug.replace('/', '_'),
        "page": page,
        "form": form,
        "form_action": form_action,
    }
