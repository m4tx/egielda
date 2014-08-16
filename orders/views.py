# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import Counter

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from books.models import Book
from orders.models import Order
from utils.alerts import set_success_msg, set_info_msg
from utils.books import books_by_types, get_available_books


@permission_required('common.view_orders_index', raise_exception=True)
def index(request):
    return HttpResponseRedirect(reverse(not_executed))


@permission_required('common.view_orders_not_executed', raise_exception=True)
def not_executed(request):
    orders = get_orders().filter(valid_until__gt=timezone.now(), sold_count=0)
    return render(request, 'orders/not_executed.html', {'orders': orders})


@permission_required('common.view_orders_outdated', raise_exception=True)
def outdated(request):
    orders = get_orders().filter(valid_until__lte=timezone.now(), sold_count=0)
    return render(request, 'orders/outdated.html', {'orders': orders})


@permission_required('common.view_orders_executed', raise_exception=True)
def executed(request):
    orders = get_orders().exclude(sold_count=0)
    return render(request, 'orders/executed.html', {'orders': orders})


@permission_required('common.view_orders_order_details', raise_exception=True)
def order_details(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('book_set', 'book_set__book_type').select_related('user'),
                              pk=order_pk)
    return render(request, 'orders/details.html',
                  {'order': order, 'book_list': [book.book_type for book in order.book_set.all()]})


@permission_required('common.view_orders_execute', raise_exception=True)
def execute(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('book_set', 'book_set__book_type').select_related('user'),
                              ~Q(valid_until__lte=timezone.now()), pk=order_pk)
    book_types_dict = books_by_types(order.book_set.all())
    book_types = book_types_dict.keys()
    available = get_available_books()
    counter = Counter(book.book_type for book in available)
    for book_type in book_types:
        book_type.in_stock = counter[book_type] + book_type.amount

    if request.method == 'POST':
        with transaction.atomic():
            for book_type in book_types:
                new_amount = int(request.POST['amount-' + str(book_type.pk)])
                if book_type.in_stock < new_amount or new_amount < 0:
                    return HttpResponseBadRequest()

                if new_amount < book_type.amount:
                    book_list = Book.objects.filter(order=order, book_type=book_type)
                    books_to_keep = book_list[:new_amount]
                    book_list.exclude(pk__in=books_to_keep).update(order=None, reserved_until=timezone.now())
                elif new_amount > book_type.amount:
                    amount = new_amount - book_type.amount
                    book_instance = book_types_dict[book_type]
                    books_to_add = get_available_books().filter(book_type=book_type)[:amount]
                    Book.objects.filter(pk__in=books_to_add).update(order=order,
                                                                    reserved_until=book_instance.reserved_until,
                                                                    reserver=book_instance.reserver)

        return HttpResponseRedirect(reverse(execute_accept, args=(order_pk,)))
    else:
        return render(request, 'orders/execute.html', {'order': order, 'book_list': book_types})


@permission_required('common.view_orders_execute_accept', raise_exception=True)
def execute_accept(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('book_set', 'book_set__book_type').select_related('user'),
                              ~Q(valid_until__lte=timezone.now()), pk=order_pk)

    if order.book_set.count() == 0:
        order.delete()
        set_info_msg(request, 'order_removed')
        return HttpResponseRedirect(reverse(not_executed))

    if request.method == 'POST':
        order.book_set.all().update(sold=True, sold_date=timezone.now(), purchaser=order.user)
        set_success_msg(request, 'order_executed')
        return HttpResponseRedirect(reverse(not_executed))
    else:
        price_sum = sum(book.book_type.price for book in order.book_set.all())
        return render(request, 'orders/execute_accept.html', {'order': order, 'price_sum': price_sum})


def get_orders() -> QuerySet:
    """
    The function returns QuerySet of Order model with all necessary values for displaying also selected/prefetched.
    :return: the QuerySet of Order model
    """
    return Order.objects.select_related('user').prefetch_related('book_set').annotate(
        sold_count=Count('book', field='CASE WHEN books_book.sold THEN 1 END')).order_by('-pk')
