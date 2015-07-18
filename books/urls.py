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

from books import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add/$', views.add_book),
    url(r'^([0-9]+)/edit/$', views.edit_book),
    url(r'^([0-9,]+)/remove/$', views.remove_book),
    url(r'^([0-9]+)/$', views.book_details),
    url(r'^bulk/(\w+)/$', views.bulk_actions),
    url(r'^duplicated/$', views.duplicated),
]
