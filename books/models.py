from django.db import models
from django.utils.translation import ugettext as _

from egielda import settings


class BookType(models.Model):
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def price_string(self):
        return "%(price).2f%(currency)s" % {'price': self.price,
                                            'currency': getattr(settings, 'CURRENCY', 'USD')}

    def __str__(self):
        return _(
            "%(publisher)s %(title)s" % {
                'publisher': self.publisher,
                'title': self.title})