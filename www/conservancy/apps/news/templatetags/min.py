from django import template
register = template.Library()

@register.filter
def min(value, arg):
    if value > arg:
        return arg
    return value
