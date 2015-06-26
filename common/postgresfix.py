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

"""
Passing empty list or QuerySet to exclude() or filter() (which produces
empty IN () in SQL request) causes django.db.utils.ProgrammingError (syntax
error) when using PostgreSQL. The functions are overridden here to avoid that.
"""

from django.db.models import QuerySet


def cleanup_kwargs(**kwargs):
    new_kwargs = dict()
    for key, value in kwargs.items():
        if not ((isinstance(value, list) and not value) or (
                    isinstance(value, QuerySet) and not value)):
            new_kwargs[key] = value
    return new_kwargs


old_exclude = QuerySet.exclude
old_filter = QuerySet.filter


def new_exclude(self, *args, **kwargs):
    return old_exclude(self, *args, **cleanup_kwargs(**kwargs))


def new_filter(self, *args, **kwargs):
    return old_filter(self, *args, **cleanup_kwargs(**kwargs))


QuerySet.exclude = new_exclude
QuerySet.filter = new_filter