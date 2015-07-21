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

from datetime import datetime, timedelta

DT_FORMAT = '%Y-%m-%d %H:%M:%S%z'


def datetime_html_format(date):
    return date.strftime("%Y-%m-%dT%H:%M")


def datetime_to_string(date):
    return date.strftime(DT_FORMAT)


def string_to_datetime(date):
    return datetime.strptime(date, DT_FORMAT)


def date_range(start_date, end_date):
    return list(start_date + timedelta(x) for x in range((end_date - start_date).days + 1))
