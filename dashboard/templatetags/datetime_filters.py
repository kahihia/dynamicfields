from django import template

register = template.Library()


@register.filter
def timedelta(td):
    """
    Return formatted timedelta value
    """
    return td
