from django.utils.translation import ugettext_lazy as _


def alerts(request, args):
    if 'success_msg' in request.session:
        args['success_msg'] = {
            'book_added': _("The book was added successfully."),
            'book_edited': _("The book was edited successfully."),
            'book_removed': _("The book was removed successfully."),
            'books_removed': _("The books were removed successfully."),
            'books_accepted': _("The books were accepted successfully."),
        }[request.session['success_msg']]
        del request.session['success_msg']
    return args