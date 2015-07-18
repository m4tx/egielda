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

from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.inclusion_tag('templatetags/header.html')
def profile_header(*args):
    # Profile pages tree
    # Each item is a list of following: [view class, (display) name, (optional) children]
    tree = ['authentication.views.profile', _("Your profile"), {
        'purchased': ['authentication.views.purchased', _("Purchased books")],
        'sold': ['authentication.views.sold', _("Sold books")],
    }]

    # Split the path
    if len(args) == 0 or args[0] == "":
        split = []
    else:
        split = args[0].split("/")

    # Iterate through the items in path and add the items from the tree to the nodes list
    nodes = [tree]
    parent = tree
    for node in split:
        parent = parent[2][node]
        nodes.append(parent)

    return {'items': nodes}
