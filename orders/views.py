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

from django.contrib import messages
from django.utils.translation import ugettext as _, ungettext

from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from authentication.decorators import permission_required
from authentication.models import AppUser
from books.models import Book
from orders.models import Order
from utils.books import get_available_books
from utils.dates import get_current_year


@permission_required('common.view_orders_index')
def index(request):
    return HttpResponseRedirect(reverse(not_fulfilled))


@permission_required('common.view_orders_not_fulfilled')
def not_fulfilled(request):
    orders = get_orders().filter(fulfilled=False)
    class_list = AppUser.objects.order_by('-year', 'class_letter').values_list('year', 'class_letter').distinct()
    cl_list = []
    for cl in class_list:
        cl_list.append("%(year)d%(class_letter)s" % {'year': get_current_year() - cl[0] + 1, 'class_letter': cl[1]})
    return render(request, 'orders/not_fulfilled.html', {'orders': orders, 'class_list': cl_list})


@permission_required('common.view_orders_fulfilled')
def fulfilled(request):
    orders = get_orders().exclude(fulfilled=False)
    class_list = AppUser.objects.order_by('-year', 'class_letter').values_list('year', 'class_letter').distinct()
    cl_list = []
    for cl in class_list:
        cl_list.append("%(year)d%(class_letter)s" % {'year': get_current_year() - cl[0] + 1, 'class_letter': cl[1]})
    return render(request, 'orders/fulfilled.html', {'orders': orders, 'class_list': cl_list})


@permission_required('common.view_orders_order_details')
def order_details(request, order_pk):
    order = get_object_or_404(Order.objects
                              .prefetch_related('book_set', 'book_set__book_type',
                                                'orderedbook_set', 'orderedbook_set__book_type')
                              .select_related('user'), pk=order_pk, fulfilled=True)
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


@permission_required('common.view_orders_fulfill')
def fulfill(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('orderedbook_set', 'orderedbook_set__book_type')
                              .select_related('user'), pk=order_pk, fulfilled=False)
    book_types = dict((orderedbook.book_type, orderedbook) for orderedbook in order.orderedbook_set.all())
    book_types_to_delete = []
    available, amounts = get_available_books(with_amounts=True)
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
                new_amount = int(request.POST.get('amount-' + str(book_type.pk), -1))
                if book_type.in_stock < new_amount or new_amount < 0:
                    messages.error(request, _("Invalid amount."))
                    return render(request, 'orders/fulfill.html', {'order': order, 'book_list': book_types.keys(),
                                                                   'users': users})

                if new_amount == 0:
                    book_types[book_type].delete()  # delete orderedbook which points to that book type
                    book_types_to_delete.append(book_type)
                    continue
                elif new_amount != book_type.amount:
                    book_types[book_type].count = new_amount
                    book_types[book_type].save()

                book_type.amount = new_amount

                book_type.owners = request.POST.get('owners-' + str(book_type.pk), '')
                owners = book_type.owners.split(',')

                valid_data = True
                try:
                    owners = [int(owner) for owner in owners]
                except ValueError:
                    valid_data = False

                if len(owners) != new_amount or not valid_data:
                    messages.error(
                        request, _("Amount of books being purchased and count of provided books' "
                                   "owners are not equal. You'll need to fill in the form again."))
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
                books = Book.objects.select_related('book_type', 'owner').filter(sold=False, accepted=True)
                books_dict = dict()

                for book in books:
                    books_dict[book.book_type_id] = books_dict.setdefault(book.book_type_id, dict())
                    books_dict[book.book_type_id][book.owner_id] = books_dict[book.book_type_id]\
                        .setdefault(book.owner_id, [])
                    books_dict[book.book_type_id][book.owner_id].append(book)

                for book_type, owners in owners_by_book.items():
                    for owner, amount in owners.items():
                        if len(books_dict[book_type.pk].get(owner, [])) < amount:
                            book_type.error = True
                            error = True
                            continue

                        books_to_purchase += books_dict[book_type.pk][owner][:amount]

                if error:
                    messages.error(request, _("Some of the users you have provided don't "
                                              "have enough books in the database."))
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


@permission_required('common.view_orders_fulfill_accept')
def fulfill_accept(request, order_pk):
    order = get_object_or_404(Order.objects.prefetch_related('orderedbook_set', 'orderedbook_set__book_type')
                              .select_related('user'), pk=order_pk, fulfilled=False)

    if order.orderedbook_set.count() == 0:
        order.delete()
        messages.info(request, _("The order was removed."))
        del request.session['books_to_purchase'][str(order_pk)]
        del request.session['owners_by_book'][str(order_pk)]
        return HttpResponseRedirect(reverse(not_fulfilled))

    if request.method == 'POST':
        books_to_purchase = [int(book) for book in request.session['books_to_purchase'][str(order_pk)]]
        Book.objects.filter(pk__in=books_to_purchase).update(sold=True, sold_date=timezone.now(), purchaser=order.user,
                                                             order=order)
        order.fulfilled = True
        order.save()
        messages.success(request, _("The order was fulfilled successfully."))
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


@permission_required('common.view_orders_remove_order')
def remove_order(request, order_ids):
    order_list = get_orders().filter(pk__in=order_ids.split(','), fulfilled=False)
    if len(order_list) == 0:
        raise Http404

    if request.method == 'POST':
        messages.success(request, ungettext("The order was removed successfully.",
                                            "The orders were removed successfully.",
                                            len(order_list)))
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
