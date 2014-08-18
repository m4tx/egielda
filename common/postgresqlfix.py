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

from django.db.models import QuerySet


def new_exclude(self, *args, **kwargs):
    new_kwargs = dict()
    for key, value in kwargs.items():
        if not ((isinstance(value, list) and not value) or (isinstance(value, QuerySet) and not value)):
            new_kwargs[key] = value

    if len(new_kwargs):
        return old_exclude(self, *args, **new_kwargs)
    else:
        return self


def new_filter(self, *args, **kwargs):
    new_kwargs = dict()
    for key, value in kwargs.items():
        if not ((isinstance(value, list) and not value) or (isinstance(value, QuerySet) and not value)):
            new_kwargs[key] = value

    if len(new_kwargs):
        return old_filter(self, *args, **new_kwargs)
    else:
        return self


old_exclude = QuerySet.exclude
QuerySet.exclude = new_exclude

old_filter = QuerySet.filter
QuerySet.filter = new_filter