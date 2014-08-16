# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
