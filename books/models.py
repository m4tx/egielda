from django.db import models
from django.utils.translation import ugettext as _

from categories.models import Category
from orders.models import Order
from common.models import AppUser


class BookType(models.Model):
    isbn = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=150, blank=True)
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return _(
            "%(publisher)s %(title)s" % {
                'publisher': self.publisher,
                'title': self.title})


class Book(models.Model):
    book_type = models.ForeignKey(BookType)
    owner = models.ForeignKey(AppUser, related_name='appuser_owner')
    accepted = models.BooleanField()
    """Is the book physically available for buying"""
    order = models.ForeignKey(Order, null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)
    reserver = models.ForeignKey(AppUser, related_name='appuser_reserver', null=True, blank=True)
    sold = models.BooleanField()
    sold_date = models.DateTimeField(null=True, blank=True)
    purchaser = models.ForeignKey(AppUser, related_name='appuser_purchaser', null=True, blank=True)

    def __str__(self):
        return _("%(book_type)s from %(owner)s, accepted: %(accepted)s, sold: %(sold)s" %
                 {'book_type': self.book_type, 'owner': self.owner, 'accepted': self.accepted, 'sold': self.sold})
