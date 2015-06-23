# This file is part of e-Gie�da.
# Copyright (C) 2014  Mateusz Ma�kowski and Tomasz Zieli�ski
#
# e-Gie�da is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Gie�da.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url

from authentication import views

urlpatterns = [
    url(r'^$', views.index),
]
