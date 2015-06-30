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

from django.conf.urls import url

from orders import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^notfulfilled/$', views.not_fulfilled),
    url(r'^outdated/$', views.outdated),
    url(r'^fulfilled/$', views.fulfilled),
    url(r'^([0-9]+)/fulfill/$', views.fulfill),
    url(r'^([0-9]+)/fulfill/accept/$', views.fulfill_accept),
    url(r'^([0-9]+)/$', views.order_details),
]
