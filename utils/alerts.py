from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _


def alerts(request: HttpRequest, args: dict):
    """
    Adds alert-specific arguments to pass to the template (common/alerts.html).
    :param request: HttpRequest object from the view
    :param args: current arguments dictionary to add new arguments to
    :return: modified args dict
    """
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
    return args


def set_success_msg(request: HttpRequest, msg_id: str):
    """
    Sets success message id to display.
    :param request: HttpRequest object from the view
    :param msg_id: message id to set
    """
    request.session['success_msg'] = msg_id