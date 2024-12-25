from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtract arg from value."""
    try:
        return value - arg
    except (TypeError, ValueError):
        return value  # return the original value if there's an error
