# -*- coding: utf-8 -*-

# taken from
# https://github.com/pinax/django-forms-bootstrap

from django import template
from django.conf import settings
from django.template import Context
from django.template.loader import get_template


register = template.Library()


def _preprocess_fields(form):
    for field in form.fields:
        name = form.fields[field].widget.__class__.__name__.lower()
        if not name.startswith("radio") and not name.startswith("checkbox"):
            try:
                form.fields[field].widget.attrs["class"] += " form-control"
            except KeyError:
                form.fields[field].widget.attrs["class"] = " form-control"
    return form


@register.filter
def render_form(form):
    """same than  {{ form|crispy }} if crispy_forms is installed.
    render using a bootstrap3 templating otherwise"""

    if 'crispy_forms' in settings.INSTALLED_APPS:
        from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
        return as_crispy_form(form)

    template = get_template("bootstrap/form.html")
    form = _preprocess_fields(form)

    c = Context({
        "form": form,
    })
    return template.render(c)


@register.filter
def as_bootstrap_inline(form):
    template = get_template("bootstrap/form.html")
    form = _preprocess_fields(form)

    for field in form.fields:
        name = form.fields[field].widget.__class__.__name__.lower()
        if not name.startswith("radio") and not name.startswith("checkbox"):
            form.fields[field].widget.attrs["placeholder"] = form.fields[field].label

    css_classes = {
        "label": "sr-only",
        "single_container": "",
        "wrap": "",
    }

    c = Context({
        "form": form,
        "css_classes": css_classes,
    })
    return template.render(c)


@register.filter
def as_bootstrap_horizontal(form, label_classes=""):
    template = get_template("bootstrap/form.html")
    form = _preprocess_fields(form)

    if label_classes == "":
        label_classes = "col-md-2"

    css_classes = {
        "label": label_classes,
        "single_container": "",
        "wrap": "",
    }

    for label_class in label_classes.split(" "):
        split_class, column_count = label_class.rsplit("-", 1)
        column_count = int(column_count)

        if column_count < 12:
            offset_class = "{split_class}-offset-{column_count}".format(
                split_class=split_class,
                column_count=column_count,
            )
            wrap_class = "{split_class}-{column_count}".format(
                split_class=split_class,
                column_count=12 - column_count,
            )
            css_classes["single_container"] += offset_class + " " + wrap_class + " "
            css_classes["wrap"] += wrap_class + " "

    c = Context({
        "form": form,
        "css_classes": css_classes,
    })
    return template.render(c)


@register.filter
def css_class(field):
    return field.field.widget.__class__.__name__.lower()
