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

from django.shortcuts import render

from settings.settings import is_purchase_available, is_sell_available, Settings


def home(request):
    settings = Settings('homepage_info')
    sell_available = is_sell_available()
    purchase_available = is_purchase_available()

    return render(request, 'egielda/home.html',
                  {'sell_available': sell_available,
                   'purchase_available': purchase_available,
                   'homepage_info': getattr(settings, 'homepage_info', None)})
