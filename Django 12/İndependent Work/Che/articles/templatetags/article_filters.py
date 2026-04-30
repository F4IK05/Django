from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
def smart_timesince(value):
    if not value:
        return ''

    ts = timesince(value)

    return ts.split(',')[0]