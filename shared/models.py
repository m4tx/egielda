from django.db import models
from django.utils.translation import ugettext as _


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=9)

    def __str__(self):
        return _("%(first_name)s %(last_name)s, %(student_class)s" %
                 {'first_name': self.first_name, 'last_name': self.last_name, 'student_class': self.student_class})


class BookType(models.Model):
    publishing_house = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    issue = models.IntegerField(default=1)
    issue_year = models.IntegerField(default=-1)
    price = models.IntegerField()

    def __str__(self):
        return _(
            "%(publishing_house)s %(title)s, Issue %(issue)d %(issue_year)d" % {
                'publishing_house': self.publishing_house,
                'title': self.title, 'issue': self.issue,
                'issue_year': self.issue_year})


class Book(models.Model):
    type = models.ForeignKey(BookType)
    owner = models.ForeignKey(Student)
    physical = models.BooleanField()
    """Is the book physically available for buying"""
    sold = models.BooleanField()

    def __str__(self):
        return _(
            "%(type)s from %(owner)s, physical: %(physical)s, sold: %(sold)s" % {'type': self.type, 'owner': self.owner,
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