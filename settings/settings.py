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

from django.utils import timezone

from settings.models import Setting
from utils.dates import string_to_datetime


class Settings:
    """
    "Wrapper" class for Setting Model. The usage is following:
    * Adding (or updating if one already exists) a setting can be done using __setattr__. Example usage:
      ``Settings().setting = value``
    * In order to retrieve a setting from the database, you have to pre-fetch it in constructor, then use __getattr__.
      Example usage: ``Settings('setting').setting``.
    """

    def __init__(self, *values):
        if values is None:
            return
        settings = Setting.objects.filter(name__in=values)
        self.__dict__['settings'] = dict((o.name, o.value) for o in settings)

    def __getattr__(self, item):
        if item in self.__dict__['settings']:
            return self.__dict__['settings'][item]
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        Setting.objects.update_or_create(name=key, defaults={'value': value})


def is_sell_available():
    try:
        settings = Settings('start_sell', 'end_sell')
        start_sell = string_to_datetime(settings.start_sell)
        end_sell = string_to_datetime(settings.end_sell)

        now = timezone.now()

        if (now - start_sell).total_seconds() > 0 and (end_sell - now).total_seconds() > 0:
            return True

    except AttributeError:
        return False

    return False


def is_purchase_available():
    try:
        settings = Settings('start_purchase', 'end_purchase')
        start_purchase = string_to_datetime(settings.start_purchase)
        end_purchase = string_to_datetime(settings.end_purchase)

        now = timezone.now()

        if (now - start_purchase).total_seconds() > 0 and (end_purchase - now).total_seconds() > 0:
            return True

    except AttributeError:
        return False

    return False
