from django.db import models
from django.utils.translation import ugettext as _

from egielda import settings


class BookType(models.Model):
    publisher = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    edition = models.IntegerField()
    publication_year = models.IntegerField()
    price = models.IntegerField()

    def price_string(self):
        return "%(price).2f%(currency)s" % {'price': (self.price / 100),
                                            'currency': getattr(settings, 'CURRENCY', 'USD')}

    def edition_string(self):
        return _("Edition %(edition)d, %(year)d") % {'edition': self.edition, 'year': self.publication_year}

    def __str__(self):
        return _(
            "%(publisher)s %(title)s, Edition %(edition)d %(publication_year)d" % {
                'publisher': self.publisher,
                'title': self.title, 'edition': self.edition,
                'publication_year': self.publication_year})