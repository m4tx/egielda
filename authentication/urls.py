# This file is part of e-Gie³da.
# Copyright (C) 2014  Mateusz Maækowski and Tomasz Zieliñski
#
# e-Gie³da is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Gie³da.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_change, password_change_done

from authentication import views

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^change_password/$', password_change, name='password_change'),
    url(r'^change_password/done/$', password_change_done, name='password_change_done'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile_page'),
]
