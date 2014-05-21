from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=9)

class BookType(models.Model):
    publishing_house = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    issue = models.IntegerField(default=1)
    issue_year = models.IntegerField(default=-1)
    price = models.IntegerField()

class Book(models.Model):
    type = models.ForeignKey(BookType)
    owner = models.ForeignKey(Student)
    physical = models.BooleanField()
    """Is the book physically available for buying"""
    sold = models.BooleanField()

class Purchase(models.Model):
    book = models.ForeignKey(Book)
    date = models.DateField()
    purchaser = models.ForeignKey(Student)