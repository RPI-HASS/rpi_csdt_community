try:
    from urllib import quote_plus  # python 2  # NOQA
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3  # NOQA
except:
    pass


from django import template

register = template.Library()


@register.filter
def urlify(value):
    return quote_plus(value)
