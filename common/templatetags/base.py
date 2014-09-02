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

from egielda import settings


register = template.Library()


@register.simple_tag
def site_name():
    return getattr(settings, 'SITE_NAME', 'e-Giełda')


@register.inclusion_tag('templatetags/alerts.html', takes_context=True)
def alerts(context):
    request = context['request']

    args = {}

    if 'info_msg' in request.session:
        args['info_msg'] = {
            'order_removed': _("The order was removed."),
            'merge_no_books_chosen': _("No books were chosen. Merged nothing."),
        }[request.session['info_msg']]
        del request.session['info_msg']

    if 'success_msg' in request.session:
        args['success_msg'] = {
            'book_added': _("The book was added successfully."),
            'book_edited': _("The book was edited successfully."),
            'book_removed': _("The book was removed successfully."),
            'books_removed': _("The books were removed successfully."),
            'books_merged': _("The books were merged successfully."),
            'category_added': _("The category was added successfully."),
            'category_edited': _("The category was edited successfully."),
            'category_remove': _("The category was removed successfully."),
            'settings_updated': _("Settings were updated successfully."),
            'order_executed': _("The order was executed successfully."),
            'seller_removed': _("The seller's books were removed successfully."),
            'sellers_removed': _("The sellers' books were removed successfully."),
        }[request.session['success_msg']]
        del request.session['success_msg']

    if 'warning_msg' in request.session:
        args['warning_msg'] = {
            'purchase_incomplete': _("An error occurred while processing your query. It was most likely the result " +
                                     "of someone else who just bought the last copies of books you've chosen. " +
                                     "Your order was modified thus; review it and click Accept again afterwards."),
        }[request.session['warning_msg']]
        del request.session['warning_msg']

    if 'error_msg' in request.session:
        args['error_msg'] = {
            'merge_dest_not_chosen': _("You haven't chosen the book to merge to!"),
        }[request.session['error_msg']]
        del request.session['error_msg']

    return args
