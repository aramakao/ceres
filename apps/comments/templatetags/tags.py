from django import template
register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def to_app_label(value):
    return value._meta.app_label
