from django.utils import timezone

from settings.models import Setting
from utils.dates import string_to_datetime


class Settings:
    settings = dict()

    def __init__(self, values):
        settings = Setting.objects.filter(name__in=values)
        self.settings = dict((o.name, o.value) for o in settings)

    def get(self, name):
        return self.settings[name]


def is_sell_available():
    try:
        settings = Settings(['start_sell', 'end_sell'])
        start_sell = string_to_datetime(settings.get('start_sell'))
        end_sell = string_to_datetime(settings.get('end_sell'))

        now = timezone.now()

        if (now - start_sell).total_seconds() > 0 and (end_sell - now).total_seconds() > 0:
            return True

    except KeyError:
        return False

    return False


def is_purchase_available():
    try:
        settings = Settings(['start_purchase', 'end_purchase'])
        start_purchase = string_to_datetime(settings.get('start_purchase'))
        end_purchase = string_to_datetime(settings.get('end_purchase'))

        now = timezone.now()

        if (now - start_purchase).total_seconds() > 0 and (end_purchase - now).total_seconds() > 0:
            return True

    except KeyError:
        return False

    return False


