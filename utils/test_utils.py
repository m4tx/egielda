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

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from books.models import BookType, Book
from categories.models import Category
from authentication.models import AppUser
from orders.models import Order


def create_test_superuser():
    if AppUser.objects.filter(username="test").count() == 0:
        AppUser.objects.create_superuser("test", "Some", "User", "1A", "111222333",
                                         "test@localhost", "test")

def login(selenium, live_server_url, username, password):
    selenium.get('%s%s' % (live_server_url, '/accounts/login/'))
    selenium.find_element_by_name('username').send_keys(username)
    selenium.find_element_by_name('password').send_keys(password)
    selenium.find_element_by_xpath('//button[@type="submit"]').click()


def create_test_book_type():
    book_type = BookType(isbn="9780262533058", publisher="MIT Press", title="Introduction to Algorithms",
                         publication_year=2009, price=60.50, visible=True)
    book_type.save()
    return book_type


def create_test_category():
    category = Category(name="Test category")
    category.save()
    return category


def create_test_app_user():
    app_user = AppUser(first_name="Some", last_name="User", student_class="1A", phone_number="111222333")
    app_user.save()
    return app_user


def create_test_book(book_type, owner, accepted=True):
    book = Book(book_type=book_type, owner=owner, accepted=accepted, accept_date=timezone.now() if accepted else None)
    book.save()
    return book


def create_test_order(user):
    order = Order(user=user, date=timezone.now())
    order.save()
    return order
