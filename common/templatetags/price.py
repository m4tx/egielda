from django import template
from egielda import settings

from django.utils import formats
from django.utils.encoding import force_text

register = template.Library()


@register.filter
def price(value):
    if float(value) != 0:
        return "%(price)s%(currency)s" % {
            'price': force_text(formats.number_format(value, 2, use_l10n=settings.USE_L10N)),
            'currency': getattr(settings, 'CURRENCY', 'USD')}
    else:
        return "N/A"