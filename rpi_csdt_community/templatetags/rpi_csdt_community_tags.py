from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def is_warning_message(context):
    return hasattr(settings, 'WARNING_MESSAGE') and settings.WARNING_MESSAGE is not None


@register.simple_tag
def get_warning_message(context):
    return settings.WARNING_MESSAGE


def is_cms_page(path):
    return path.startswith("/cms/")


register.filter(is_warning_message)
register.filter(get_warning_message)
register.filter(is_cms_page)
