# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
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
def manage_header(*args):
    # Manage pages tree
    # Each item is a list of following: [view class, (display) name, (optional) children]
    tree = ['managemenu.views.index', _("Manage"), {
        'categories': ['categories.views.index', _("Categories"), {
            'add': ['categories.views.add_category', _("Add new")],
            'edit': ['categories.views.edit_category', _("Edit")],
            'remove': ['categories.views.remove_category', _("Remove")],
            'list': ['categories.views.list_books', _("Book list")],
        }],
        'books': ['books.views.index', _("Books"), {
            'add': ['books.views.add_book', _("Add new")],
            'edit': ['books.views.edit_book', _("Edit")],
            'remove': ['books.views.remove_book', _("Remove")],
            'details': ['books.views.book_details', _("Book's details")],
            'duplicated': ['books.views.duplicated', _("Duplicated")],
        }],
        'orders': ['orders.views.index', _("Orders"), {
            'not_fulfilled': ['orders.views.not_fulfilled', _("Not fulfilled")],
            'fulfill': ['orders.views.fulfill', _("Fulfill")],
            'outdated': ['orders.views.outdated', _("Outdated")],
            'fulfilled': ['orders.views.fulfilled', _("Fulfilled")],
            'details': ['orders.views.details', _("Details")]
        }],
        'sellers': ['sellers.views.index', _("Sellers with unaccepted books"), {
            'accept_books': ['sellers.views.accept_books', _("Accept books")],
            'remove': ['sellers.views.remove_seller', _("Remove")],
        }],
        'stats': ['stats.views.index', _("Statistics"), {
            'sold': ['stats.views.sold', _("Books sold")],
            'users': ['stats.views.users', _("Users"), {
                'list': ['stats.views.list_books', _("User's books")],
            }],
            'books': ['stats.views.books', _("Books")],
        }],
        'settings': ['settings.views.index', _("Settings")]
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
