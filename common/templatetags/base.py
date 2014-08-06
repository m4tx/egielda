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
    if 'success_msg' in request.session:
        args['success_msg'] = {
            'book_added': _("The book was added successfully."),
            'book_edited': _("The book was edited successfully."),
            'book_removed': _("The book was removed successfully."),
            'books_removed': _("The books were removed successfully."),
            'books_accepted': _("The books were accepted successfully."),
            'category_added': _("The category was added successfully."),
            'category_edited': _("The category was edited successfully."),
            'category_remove': _("The category was removed successfully."),
            'settings_updated': _("Settings were updated successfully."),
            'order_executed': _("The order was executed successfully."),
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
        }[request.session['error_msg']]
        del request.session['error_msg']

    return args
