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

from collections import defaultdict

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum

from authentication.models import AppUser
from books.models import BookType, Book
from orders.models import Order
from utils.alerts import set_success_msg
from utils.dates import date_range
from authentication.forms import UserDataForm


@permission_required('common.view_stats_index', raise_exception=True)
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


@permission_required('common.view_stats_books_sold', raise_exception=True)
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


@permission_required('common.view_stats_users', raise_exception=True)
def users(request):
    users = AppUser.objects.all().order_by('last_name', 'first_name')
    users = [user for user in users if user.verified]

    return render(request, 'stats/users.html', {'users': users})


@permission_required('common.view_stats_user_profile', raise_exception=True)
def user_profile(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)

    disabled_fields_post = ['password']
    disabled_fields_files = ['document']

    if request.POST:
        for field in disabled_fields_post:
            request.POST[field] = getattr(user, field)
        for field in disabled_fields_files:
            request.FILES[field] = getattr(user, field)
        form = UserDataForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            set_success_msg(request, 'user_profile_saved')
            return HttpResponseRedirect(reverse(users))
    else:
        form = UserDataForm(instance=user)

    for field in disabled_fields_post + disabled_fields_files:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True

    del form.fields['password']

    return render(request, 'stats/user_profile.html', {'form': form, 'student': user})


@permission_required('common.view_stats_user_profile_purchased', raise_exception=True)
def user_profile_purchased(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)
    orders = Order.objects.filter(user=user).prefetch_related(
        'user', 'orderedbook_set', 'orderedbook_set__book_type').annotate(books_count=Sum('orderedbook__count'))

    stats = dict()
    for order in orders:
        order_id = order.date.strftime("%Y%m%d") + "-" + str(order.pk) + "-" + str(order.user.pk) + "-" + str(
            order.books_count)

        order_book_list = []
        for orderedbook in order.orderedbook_set.all():
            order_book_list.append((orderedbook.book_type, orderedbook.count, order.fulfilled))

        stats[(order.user.get_full_name(), order_id)] = order_book_list

    return render(request, 'stats/purchased.html', {'stats': stats, 'student': user})


@permission_required('common.view_stats_user_profile_sold', raise_exception=True)
def user_profile_sold(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)
    books = Book.objects.filter(owner=user).select_related("book_type")

    stats = dict()  # Dictionary indexed with the book type string, valued with the list containing 4 values: a book
                    # itself, amount of books declared to bring, books actually brought and books already sold
    for book in books:
        stats[str(book.book_type)] = stats.setdefault(str(book.book_type), [book, 0, 0, 0])
        stats[str(book.book_type)][1] += 1
        stats[str(book.book_type)][2] += 1 if book.accepted else 0
        stats[str(book.book_type)][3] += 1 if book.sold else 0

    return render(request, 'stats/sold.html', {'stats': stats, 'student': user})


@permission_required('common.view_stats_books', raise_exception=True)
def books(request):
    book_list = BookType.objects.annotate(received=Count('book')).annotate(
        sold=Count('book', field='CASE WHEN books_book.sold THEN 1 END')).order_by('title')

    return render(request, 'stats/books.html', {'book_list': book_list})
