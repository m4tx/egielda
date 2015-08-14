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

from collections import defaultdict

from django.shortcuts import render
from django.db.models import Count

from authentication.decorators import permission_required
from books.models import BookType, Book
from utils.dates import date_range


@permission_required('common.view_stats_index')
def index(request):
    args = get_sold_books_chart_data()
    args.update(get_given_books_chart_data())
    return render(request, 'stats/index.html', args)


def get_sold_books_chart_data():
    sold_books = Book.objects.select_related('book_type').prefetch_related('book_type__categories').filter(sold=True)
    books_by_date = defaultdict(list)
    for book in sold_books:
        books_by_date[book.sold_date.date()].append(book)
    sold_book_categories = defaultdict(int)
    for book in sold_books:
        for category in book.book_type.categories.all():
            sold_book_categories[category] += 1

    if len(books_by_date) != 0:
        first_day = min(books_by_date.keys())
        last_day = max(books_by_date.keys())

        sold_book_counts = list((date, len(books_by_date[date])) for date in date_range(first_day, last_day))
        sold_book_prices = list(
            (date,
             sum(book.book_type.price for book in books_by_date[date])) for date in date_range(first_day, last_day))
        return {'sold_book_counts': sold_book_counts, 'sold_book_prices': sold_book_prices,
                'sold_book_categories': sold_book_categories.items()}

    return {}


def get_given_books_chart_data():
    given_books = Book.objects.select_related('book_type').filter(accepted=True)
    books_by_date = defaultdict(list)
    for book in given_books:
        books_by_date[book.accept_date.date()].append(book)

    if len(books_by_date) != 0:
        first_day = min(books_by_date.keys())
        last_day = max(books_by_date.keys())

        given_book_counts = list((date, len(books_by_date[date])) for date in date_range(first_day, last_day))
        return {'given_book_counts': given_book_counts}

    return {}


@permission_required('common.view_stats_books_sold')
def books_sold(request):
    books = Book.objects.filter(sold=True).order_by('-sold_date').select_related('book_type', 'purchaser')

    stats = dict()

    for book in books:
        stats.setdefault(book.sold_date.date(), []).append(book)

    for key, stat in stats.items():
        sum = 0
        for el in stat:
            sum += el.book_type.price

        stats[key] = (stats[key], sum)

    return render(request, 'stats/books_sold.html', {'stats': list(reversed(sorted(stats.items())))})


@permission_required('common.view_stats_books')
def books(request):
    book_list = BookType.objects.annotate(received=Count('book')).annotate(
        sold=Count('book', field='CASE WHEN books_book.sold THEN 1 END')).order_by('title')

    return render(request, 'stats/books.html', {'book_list': book_list})
