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

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from authentication.models import AppUser
from books.models import Book
from orders.models import Order
from utils.alerts import set_success_msg, set_info_msg, set_error_msg
from utils.books import get_available_amount, get_available_books


@permission_required('common.view_orders_index', raise_exception=True)
def index(request):
    return HttpResponseRedirect(reverse(not_fulfilled))


@permission_required('common.view_orders_not_fulfilled', raise_exception=True)
def not_fulfilled(request):
    orders = get_orders().filter(fulfilled=False)
    class_list = AppUser.objects.order_by('student_class').values_list('student_class', flat=True).distinct()
    return render(request, 'orders/not_fulfilled.html', {'orders': orders, 'class_list': class_list})


@permission_required('common.view_orders_fulfilled', raise_exception=True)
def fulfilled(request):
    orders = get_orders().exclude(fulfilled=False)
    class_list = AppUser.objects.order_by('student_class').values_list('student_class', flat=True).distinct()
    return render(request, 'orders/fulfilled.html', {'orders': orders, 'class_list': class_list})


@permission_required('common.view_orders_order_details', raise_exception=True)
def order_details(request, order_pk):
    order = get_object_or_404(Order.objects
                              .prefetch_related('book_set', 'orderedbook_set', 'orderedbook_set__book_type')
                              .select_related('user'), pk=order_pk)
    book_types = dict((orderedbook.book_type, orderedbook) for orderedbook in order.orderedbook_set.all())

    book_sum = 0
    price_sum = 0
    for book_type in book_types.keys():
        book_type.amount = book_types[book_type].count
        book_sum += book_type.amount
        price_sum += book_type.amount * book_type.price
        book_type.owners = []
        for book in order.book_set.all():
            if book.book_type == book_type:
                book_type.owners.append(book.owner_id)

    users = AppUser.objects.filter(groups__name__in=AppUser.get_verified_groups()).order_by('last_name', 'first_name')
    users = dict((user.pk, "#" + str(user.pk) + ": " + str(user)) for user in users)
    return render(request, 'orders/details.html', {'order': order, 'book_list': book_types.keys(),
                                                   'price_sum': price_sum, 'users': users, 'book_sum': book_sum})


@permission_required('common.view_orders_fulfill', raise_exception=True)
def fulfill(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('orderedbook_set', 'orderedbook_set__book_type')
                              .select_related('user'), pk=order_pk)
    book_types = dict((orderedbook.book_type, orderedbook) for orderedbook in order.orderedbook_set.all())
    book_types_to_delete = []
    available = get_available_books()
    amounts = get_available_amount(available)
    for book_type in book_types.keys():
        book_type.amount = book_types[book_type].count
        book_type.in_stock = amounts[book_type.pk] + book_type.amount

    users = AppUser.objects.filter(groups__name__in=AppUser.get_verified_groups()).order_by('last_name', 'first_name')
    users = [(user.pk, str(user)) for user in users]

    if request.method == 'POST':
        request.session['owners_by_book'] = request.session.setdefault('owners_by_book', dict())
        request.session['books_to_purchase'] = request.session.setdefault('books_to_purchase', dict())
        request.session['owners_by_book'][str(order_pk)] = dict()
        with transaction.atomic():
            error = False
            owners_by_book = dict()
            for book_type in book_types.keys():
                new_amount = int(request.POST['amount-' + str(book_type.pk)])
                if book_type.in_stock < new_amount or new_amount < 0:
                    return HttpResponseBadRequest()

                if new_amount == 0:
                    book_types[book_type].delete()  # delete orderedbook which points to that book type
                    book_types_to_delete.append(book_type)
                    continue
                elif new_amount != book_type.amount:
                    book_types[book_type].count = new_amount
                    book_types[book_type].save()

                book_type.amount = new_amount

                book_type.owners = request.POST['owners-' + str(book_type.pk)]
                owners = book_type.owners.split(',')

                valid_data = True
                try:
                    owners = [int(owner) for owner in owners]
                except ValueError:
                    valid_data = False

                if len(owners) != new_amount or not valid_data:
                    set_error_msg(request, 'amount_and_length_of_owners_differ')
                    book_type.error = True
                    error = True
                    continue

                request.session['owners_by_book'][str(order_pk)][book_type.pk] = owners

                owners_dict = dict()
                for owner in owners:
                    owners_dict[owner] = owners_dict.setdefault(owner, 0) + 1

                owners_by_book[book_type] = owners_dict

            if error:
                for el in book_types_to_delete:
                    book_types.pop(el)
                return render(request, 'orders/fulfill.html', {'order': order, 'book_list': book_types.keys(),
                                                               'users': users})
            else:
                books_to_purchase = []
                for book_type, owners in owners_by_book.items():
                    books = Book.objects.filter(book_type=book_type, sold=False, accepted=True)
                    for owner, amount in owners.items():
                        owner_books = books.filter(owner__pk=owner)
                        if len(owner_books) < amount:
                            set_error_msg(request, 'owner_doesnt_have_enough_books_in_db')
                            book_type.error = True
                            error = True
                            continue

                        books_to_purchase += owner_books[:amount]

                if error:
                    for el in book_types_to_delete:
                        book_types.pop(el)
                    return render(request, 'orders/fulfill.html', {'order': order, 'book_list': book_types.keys(),
                                                                   'users': users})
                else:
                    request.session['books_to_purchase'][str(order_pk)] = [book.pk for book in books_to_purchase]

        return HttpResponseRedirect(reverse(fulfill_accept, args=(order_pk,)))
    else:
        for el in book_types_to_delete:
            book_types.pop(el)
        return render(request, 'orders/fulfill.html', {'order': order, 'book_list': book_types.keys(), 'users': users})


@permission_required('common.view_orders_fulfill_accept', raise_exception=True)
def fulfill_accept(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('orderedbook_set', 'orderedbook_set__book_type')
                              .select_related('user'), pk=order_pk)

    if order.orderedbook_set.count() == 0:
        order.delete()
        set_info_msg(request, 'order_removed')
        del request.session['books_to_purchase'][str(order_pk)]
        del request.session['owners_by_book'][str(order_pk)]
        return HttpResponseRedirect(reverse(not_fulfilled))

    if request.method == 'POST':
        books_to_purchase = [int(book) for book in request.session['books_to_purchase'][str(order_pk)]]
        Book.objects.filter(pk__in=books_to_purchase).update(sold=True, sold_date=timezone.now(), purchaser=order.user,
                                                             order=order)
        order.fulfilled = True
        order.save()
        set_success_msg(request, 'order_fulfilled')
        del request.session['books_to_purchase'][str(order_pk)]
        del request.session['owners_by_book'][str(order_pk)]
        return HttpResponseRedirect(reverse(not_fulfilled))

    book_types = dict((orderedbook.book_type, orderedbook) for orderedbook in order.orderedbook_set.all())

    book_sum = 0
    price_sum = 0
    for book_type in book_types.keys():
        book_type.amount = book_types[book_type].count
        book_sum += book_type.amount
        price_sum += book_type.amount * book_type.price
        book_type.owners = [int(owner) for owner in request.session['owners_by_book'][str(order_pk)][str(book_type.pk)]]

    users = AppUser.objects.filter(groups__name__in=AppUser.get_verified_groups()).order_by('last_name', 'first_name')
    users = dict((user.pk, "#" + str(user.pk) + ": " + str(user)) for user in users)
    return render(request, 'orders/fulfill_accept.html', {'order': order, 'book_list': book_types.keys(),
                                                          'price_sum': price_sum, 'users': users, 'book_sum': book_sum})


@permission_required('common.view_orders_remove_order', raise_exception=True)
def remove_order(request, order_ids):
    order_list = get_orders().filter(pk__in=order_ids.split(','))
    if len(order_list) == 0:
        raise Http404

    if request.method == 'POST':
        set_success_msg(request, 'order_removed' if len(order_list) == 1 else 'orders_removed')
        order_list.delete()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, 'orders/remove.html', {'orders': order_list})


def bulk_actions(request, action_name):
    order_list = []
    if action_name == 'remove' and request.method == 'POST':
        for key, value in request.POST.items():
            if value == 'on':
                # Form field names are in format "select-id", so key[7:] will leave us id
                order_list.append(key[7:])
        if order_list:
            return HttpResponseRedirect(reverse(remove_order, args=[",".join(order_list)]))
        else:
            return HttpResponseRedirect(reverse(index))
    else:
        raise Http404


def get_orders() -> QuerySet:
    """
    The function returns QuerySet of Order model with all necessary values for displaying also selected/prefetched.
    :return: the QuerySet of Order model
    """
    return Order.objects.select_related('user').prefetch_related('orderedbook_set').annotate(
        books_count=Sum('orderedbook__count')).order_by('-pk')
