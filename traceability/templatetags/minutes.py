import os
from django import template

register = template.Library()

@register.filter
def minutes(value):
    return value/60
