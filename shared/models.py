from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9)

    def __str__(self):
        return _("%(first_name)s %(last_name)s, %(student_class)s" %
                 {'first_name': self.first_name, 'last_name': self.last_name, 'student_class': self.student_class})


class BookType(models.Model):
    publisher = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    issue = models.IntegerField()
    issue_year = models.IntegerField()
    price = models.IntegerField()

    def price_string(self):
        return "%(price).2f%(currency)s" % {'price': (self.price / 100),
                                            'currency': getattr(settings, 'CURRENCY', 'USD')}

    def __str__(self):
        return _(
            "%(publisher)s %(title)s, Issue %(issue)d %(issue_year)d" % {
                'publisher': self.publisher,
                'title': self.title, 'issue': self.issue,
                'issue_year': self.issue_year})


class Book(models.Model):
    book_type = models.ForeignKey(BookType)
    owner = models.ForeignKey(Student)
    physical = models.BooleanField()
    """Is the book physically available for buying"""
    sold = models.BooleanField()

    def __str__(self):
        return _(
            "%(book_type)s from %(owner)s, physical: %(physical)s, sold: %(sold)s" % {'book_type': self.book_type,
                                                                                      'owner': self.owner,
                                                                                      'physical': self.physical,
                                                                                      'sold': self.sold})


class Purchase(models.Model):
    book = models.ForeignKey(Book)
    date = models.DateField()
    purchaser = models.ForeignKey(Student)

    def __str__(self):
        return _(
            "%(book)s from %(owner)s sold to %(purchaser)s at %(date)s" % {'book': self.book.type,
                                                                           'owner': self.book.owner,
                                                                           'purchaser': self.purchaser,
                                                                           'date': self.date})