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

from sellers import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^([0-9]+)/accept/([0-9]+)/edit/', views.accept_edit_book),
    url(r'^([0-9]+)/accept/', views.accept_books),
    url(r'^([0-9,]+)/remove/', views.remove_seller),
    url(r'^bulk/(\w+)/$', views.bulk_actions),
]
