from django.db import models
from django.utils.translation import ugettext as _

from books.models import BookType


class AppUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9)

    def user_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return _("%(first_name)s %(last_name)s, %(student_class)s" %
                 {'first_name': self.first_name, 'last_name': self.last_name, 'student_class': self.student_class})


class Book(models.Model):
    book_type = models.ForeignKey(BookType)
    owner = models.ForeignKey(AppUser, related_name='appuser_owner')
    accepted = models.BooleanField()
    """Is the book physically available for buying"""
    reserved_until = models.DateTimeField(null=True)
    reserver = models.ForeignKey(AppUser, related_name='appuser_reserver', null=True)
    sold = models.BooleanField()
    sold_date = models.DateTimeField(null=True)
    purchaser = models.ForeignKey(AppUser, related_name='appuser_purchaser', null=True)

    def __str__(self):
        return _("%(book_type)s from %(owner)s, accepted: %(accepted)s, sold: %(sold)s" %
                 {'book_type': self.book_type, 'owner': self.owner, 'accepted': self.accepted, 'sold': self.sold})