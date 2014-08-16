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
    url(r'^notexecuted/$', views.not_executed),
    url(r'^outdated/$', views.outdated),
    url(r'^executed/$', views.executed),
    url(r'^([0-9]+)/execute/$', views.execute),
    url(r'^([0-9]+)/execute/accept/$', views.execute_accept),
    url(r'^([0-9]+)/$', views.order_details),
]
