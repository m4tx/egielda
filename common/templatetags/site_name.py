from django import template
from egielda import settings

register = template.Library()


@register.simple_tag
def site_name():
    return getattr(settings, 'SITE_NAME', 'e-Giełda')