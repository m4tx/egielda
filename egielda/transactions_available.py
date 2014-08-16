# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.urlresolvers import reverse
from settings.settings import is_sell_available, is_purchase_available
from django.http import Http404
import re


class TransactionsAvailableMiddleware:
    def process_request(self, request):
        if re.compile(reverse("sell:index")).match(request.path_info) and not is_sell_available():
            raise Http404

        if re.compile(reverse("purchase:index")).match(request.path_info) and not is_purchase_available():
            raise Http404
