# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

import re

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from egielda import settings
import managemenu.views

register = template.Library()


@register.simple_tag
def site_name():
    return getattr(settings, 'SITE_NAME', 'e-Giełda')


@register.assignment_tag(takes_context=True)
def is_manage(context):
    return bool(re.compile(reverse(managemenu.views.index)).match(context.request.path_info))


@register.filter
def keyvalue(dict, key):
    return dict[key]


@register.filter
def striplist(list):
    return [el for el in list if el != ""]
