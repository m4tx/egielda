from django.db import models
from django.utils.translation import ugettext as _

from egielda import settings


class BookType(models.Model):
    isbn = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=150, blank=True)
    publication_year = models.IntegerField(default=1900)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def price_string(self):
        return "%(price).2f%(currency)s" % {'price': self.price,
                                            'currency': getattr(settings, 'CURRENCY', 'USD')}

    def __str__(self):
        return _(
            "%(publisher)s %(title)s" % {
                'publisher': self.publisher,
                'title': self.title})