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

from authentication.models import AppUser
from books.models import BookType


class Order(models.Model):
    user = models.ForeignKey(AppUser)
    date = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return _("Order from %(user)s made at %(date)s, fulfilled: %(fulfilled)s") % {
            'user': self.user, 'date': self.date, 'fulfilled': self.fulfilled
        }

class OrderedBook(models.Model):
    book_type = models.ForeignKey(BookType)
    count = models.IntegerField()
    order = models.ForeignKey(Order)
