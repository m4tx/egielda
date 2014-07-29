from django.utils import timezone

from settings.models import Setting
from utils.dates import string_to_datetime


class Settings:
    def __init__(self, values=None):
        if values is None:
            return
        settings = Setting.objects.filter(name__in=values)
        self.__dict__['settings'] = dict((o.name, o.value) for o in settings)

    def __getattr__(self, item):
        return str(self.__dict__['settings'].get(item))

    def __setattr__(self, key, value):
        Setting.objects.update_or_create(name=key, defaults={'value': str(value)})


def is_sell_available():
    try:
        settings = Settings(['start_sell', 'end_sell'])
        start_sell = string_to_datetime(settings.start_sell)
        end_sell = string_to_datetime(settings.end_sell)

        now = timezone.now()

        if (now - start_sell).total_seconds() > 0 and (end_sell - now).total_seconds() > 0:
            return True

    except KeyError:
        return False

    return False


def is_purchase_available():
    try:
        settings = Settings(['start_purchase', 'end_purchase'])
        start_purchase = string_to_datetime(settings.start_purchase)
        end_purchase = string_to_datetime(settings.end_purchase)

        now = timezone.now()

        if (now - start_purchase).total_seconds() > 0 and (end_purchase - now).total_seconds() > 0:
            return True

    except KeyError:
        return False

    return False


