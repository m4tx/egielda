# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import ugettext as _

from categories.models import Category
from authentication.models import AppUser


class BookType(models.Model):
    isbn = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=250, blank=True)
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    visible = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return _(
            "%(isbn)s %(publisher)s %(title)s" % {
                'isbn': self.isbn,
                'publisher': self.publisher,
                'title': self.title})


class Book(models.Model):
    book_type = models.ForeignKey(BookType)
    owner = models.ForeignKey(AppUser, related_name='appuser_owner')
    accepted = models.BooleanField(default=False)
    """Is the book physically available for buying"""
    accept_date = models.DateTimeField(null=True, blank=True)
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField(null=True, blank=True)
    purchaser = models.ForeignKey(AppUser, related_name='appuser_purchaser', null=True, blank=True)

    def __str__(self):
        return _("%(book_type)s from %(owner)s, accepted: %(accepted)s, sold: %(sold)s" %
                 {'book_type': self.book_type, 'owner': self.owner, 'accepted': self.accepted, 'sold': self.sold})
