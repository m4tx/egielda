from django.db import models
from django.utils.translation import ugettext as _

from categories.models import Category
from egielda import settings


class BookType(models.Model):
    categories = models.ManyToManyField(Category, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=150, blank=True)
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.BooleanField(default=False)

    def price_string(self):
        if float(self.price) != 0:
            return "%(price).2f%(currency)s" % {'price': self.price,
                                                'currency': getattr(settings, 'CURRENCY', 'USD')}
        else:
            return "N/A"

    def __str__(self):
        return _(
            "%(publisher)s %(title)s" % {
                'publisher': self.publisher,
                'title': self.title})
