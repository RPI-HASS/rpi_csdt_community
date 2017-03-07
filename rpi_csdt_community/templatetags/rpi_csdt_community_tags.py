'''Template Tags'''

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def is_warning_message():
    '''Returns yes if WARNING_MESSAGE is an attribute and WARNING_MESSAGE has message'''
    return hasattr(settings, 'WARNING_MESSAGE') and settings.WARNING_MESSAGE != None

@register.simple_tag
def get_warning_message():
    '''Returns WARNING_MESSAGE'''
    return settings.WARNING_MESSAGE

def is_cms_page(path):
    '''Returns yes if path is /cms/ url'''
    return path.startswith("/cms/")

register.filter(is_warning_message)
register.filter(get_warning_message)
register.filter(is_cms_page)
