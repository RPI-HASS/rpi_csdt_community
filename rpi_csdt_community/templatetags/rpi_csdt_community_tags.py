from django import template
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
register = template.Library()

@register.simple_tag
def is_warning_message(context):
    return hasattr(settings, 'WARNING_MESSAGE') and settings.WARNING_MESSAGE != None

@register.simple_tag
def get_warning_message(context):
    return settings.WARNING_MESSAGE

register.filter(is_warning_message)
register.filter(get_warning_message)
