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

from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_change, password_change_done

from authentication import views

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^change-password/$', password_change, name='password_change'),
    url(r'^change-password/done/$', password_change_done, name='password_change_done'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register-supplement/$', views.register_supplement),
    url(r'^profile/$', views.profile, name='profile_page'),
    url(r'^profile/purchased/$', views.purchased),
    url(r'^profile/sold/$', views.sold),
]
