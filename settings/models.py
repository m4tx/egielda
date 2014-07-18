from django.db import models
from django.utils.translation import ugettext as _


class Setting(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return _("%(name)s: %(value)s" %
                 {'name': self.name, 'value': self.value})