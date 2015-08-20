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

from django.core.exceptions import PermissionDenied


class AntiBotMiddleware:
    def process_request(self, request):
        if request.method == "POST":
            antibot_field_value = request.POST.get('antibot_field', "")

            if antibot_field_value != "":
                raise PermissionDenied

