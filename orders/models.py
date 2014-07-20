from django.db import models
from django.utils.translation import ugettext as _

from common.models import Book, AppUser


class Order(models.Model):
    user = models.ForeignKey(AppUser)
    date = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    books = models.ManyToManyField(Book)

    def __str__(self):
        return _("Order from %(user)s made at %(date)s valid until %(valid_until)s containing %(books)d book(s)") % {
            'user': self.user, 'date': self.date, 'valid_until': self.valid_until, 'books': self.books.count()
        }