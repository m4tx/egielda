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

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def permission_required(*perms):
    """
    Slight modification of django.contrib.auth.decorators - a decorator which redirects the user
    to the login page if they are not authenticated, and returns 403 if authenticated user does
    not have specified permission.
    """

    def check_perms(user):
        # If the user has specified permission, do nothing
        if user.has_perms(perms):
            return True
        # If the user is authenticated and does not have the permission, return 403
        if user.is_authenticated():
            raise PermissionDenied
        # Otherwise, show the login form
        return False

    return user_passes_test(check_perms)
