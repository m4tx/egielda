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

from collections import Counter

from django.db.models import Q
from django.utils import timezone

from books.models import Book


def books_by_types(books):
    """
    Groups provided books by their book types and adds information about amount of books in each book type.
    :param books: list of Books
    :return: dictionary containing BookType -> Book pairs, where Book is the last Book from its BookType in books list
    """
    amounts = Counter([book.book_type for book in books])
    d = {}
    for book_type in amounts.keys():
        book_type.amount = amounts[book_type]
    for book in books:
        d[book.book_type] = book
    return d


def get_available_books():
    """
    :return: QuerySet including books which are available for buying
    """
    return Book.objects.prefetch_related('book_type').filter(accepted=True, sold=False).filter(
        Q(reserved_until__lte=timezone.now()) | Q(reserved_until__isnull=True))
