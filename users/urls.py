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

from users import views

urlpatterns = [
    url(r'^([0-9]+)/$', views.profile),
    url(r'^([0-9]+)/purchased/$', views.profile_purchased),
    url(r'^([0-9]+)/sold/$', views.profile_sold),
    url(r'^verified/$', views.verified),
    url(r'^/$', views.index)
]
