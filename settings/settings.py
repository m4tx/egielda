from common.models import Setting


class Settings:
    settings = dict()

    def __init__(self, values):
        settings = Setting.objects.filter(name__in=values)
        self.settings = dict((o.name, o.value) for o in settings)

    def get(self, name):
        return self.settings[name]