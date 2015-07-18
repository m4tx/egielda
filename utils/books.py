# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from books.models import Book
from orders.models import Order


def books_by_types(books, amounts=None):
    """
    Groups provided books by their book types and adds information about amount of books in each book type.
    :param books: list of Books
    :param amounts: dictionary containing amounts of books' BookTypes
    :return: dictionary containing BookType -> Book pairs, where Book is the last Book from its BookType in books list
    """
    if not amounts:
        amounts = get_available_amount(books)

    d = {}
    for book_type in [book.book_type for book in books]:
        book_type.amount = amounts[book_type.pk]
    for book in books:
        d[book.book_type] = book

    return d


def get_available_books(with_amounts=False):
    """
    :param with_amounts: boolean determining whenever amounts of Books should be included in return
    :return: QuerySet including books which are available for buying if with_amounts is False, or tuple containing that
    QuerySet and amount of Book Types which belongs to available Books
    """
    books = Book.objects.select_related('book_type').filter(accepted=True, sold=False)
    amounts = get_available_amount(books)
    books = books.exclude(book_type__pk__in=[pk for pk in amounts.keys() if amounts[pk] == 0])
    if with_amounts:
        return books, amounts

    return books


def get_available_amount(books):
    """
    Checks how many books are available in stock
    :param books: list of Books
    :return: dictionary containing BookType -> in stock amount pairs
    """
    book_type_list = {book.book_type.pk for book in books}

    books_by_id = dict()
    for book in books:
        books_by_id.setdefault(book.book_type.pk, []).append(book)
    orders = Order.objects.prefetch_related('orderedbook_set', 'orderedbook_set__book_type')\
        .filter(orderedbook__book_type__in=book_type_list, fulfilled=False).distinct()
    orders_dict = dict()
    for order in orders:
        for orderedbook in order.orderedbook_set.all():
            orders_dict[orderedbook.book_type.pk] = orders_dict.\
                                                        setdefault(orderedbook.book_type.pk, 0) + orderedbook.count

    amounts = dict()
    for pk in books_by_id.keys():
        if pk in orders_dict:
            amounts[pk] = len(books_by_id[pk])-orders_dict[pk]
        else:
            amounts[pk] = len(books_by_id[pk])

    return amounts
