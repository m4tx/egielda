from django.http import HttpRequest


def set_info_msg(request: HttpRequest, msg_id: str):
    """
    Sets info message id to display.
    :param request: HttpRequest object from the view
    :param msg_id: message id to set
    """
    request.session['info_msg'] = msg_id


def set_success_msg(request: HttpRequest, msg_id: str):
    """
    Sets success message id to display.
    :param request: HttpRequest object from the view
    :param msg_id: message id to set
    """
    request.session['success_msg'] = msg_id


def set_warning_msg(request: HttpRequest, msg_id: str):
    """
    Sets warning message id to display.
    :param request: HttpRequest object from the view
    :param msg_id: message id to set
    """
    request.session['warning_msg'] = msg_id


def set_error_msg(request: HttpRequest, msg_id: str):
    """
    Sets error message id to display.
    :param request: HttpRequest object from the view
    :param msg_id: message id to set
    """
    request.session['error_msg'] = msg_id
