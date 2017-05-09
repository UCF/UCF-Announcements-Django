from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def audience_badge(value):
    """
    Returns the correct badge class per audience
    """
    if value == 'Faculty':
        return 'badge-default'
    elif value == 'Staff':
        return 'badge-success'
    elif value == 'Students':
        return 'badge-primary'
    elif value == 'Alumni':
        return 'badge-complementary'
    elif value == 'Public':
        return 'badge-primary'

@register.filter
@stringfilter
def strip_phone(value):
    """
    Strips any additional characters out of the phone
    """
    retval = value
    for character in ['(', ')', ' ', '-']:
        retval = retval.replace(character, '')

    return retval
