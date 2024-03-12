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
        return 'badge-secondary'
    elif value == 'Staff':
        return 'badge-success'
    elif value == 'Students':
        return 'badge-primary'
    elif value == 'Alumni':
        return 'badge-complementary'
    elif value == 'Public':
        return 'badge-info'

@register.filter
@stringfilter
def audience_btn(value, arg):
    """
    Returns the correct btn class per audience
    """
    retval = ''

    if value == 'Faculty':
        retval = 'btn-outline-secondary'
    elif value == 'Staff':
        retval = 'btn-outline-success'
    elif value == 'Students':
        retval = 'btn-outline-primary'
    elif value == 'Alumni':
        retval = 'btn-outline-complementary'
    elif value == 'Public':
        retval = 'btn-outline-info'

    if value == arg:
        retval = retval.replace('outline-', '')

    return retval

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
