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

from decimal import Decimal

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from books.forms import BookForm
from books.models import BookType, Book
from authentication.models import AppUser
from utils.alerts import set_success_msg
from egielda import settings
from utils.books import books_by_types


@permission_required('common.view_sellers_index', raise_exception=True)
def index(request):
    book_list = Book.objects.filter(accepted=False).select_related('owner').order_by('-pk')
    seller_list = []
    for book in book_list:
        if book.owner not in seller_list:
            seller_list.append(book.owner)

    return render(request, 'sellers/index.html', {'seller_list': seller_list})


@permission_required('common.view_sellers_accept_books', raise_exception=True)
def accept_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    books = Book.objects.filter(owner=user, accepted=False).select_related('book_type')

    d = dict()
    for book in books:
        d[book.book_type] = d.setdefault(book.book_type, 0) + 1

    book_type_list = []
    correct_book_list = []
    for book_type, amount in d.items():
        book_type.amount = amount
        book_type_list.append(book_type)

    if not books:
        raise Http404("There's no books of that user.")

    if request.method == 'POST':
        with transaction.atomic():
            books_count = 0

            books.update(accepted=True, accept_date=timezone.now())
            for book_type in book_type_list:
                if not book_type.visible:
                    book_type.price = Decimal(request.POST.get('price-' + str(book_type.pk), 1))
                    book_type.visible = True
                    book_type.save()

                new_amount = int(request.POST.get('amount-' + str(book_type.pk), -1))
                if new_amount < 0:
                    return HttpResponseBadRequest()

                if new_amount < book_type.amount:
                    books_list = Book.objects.filter(owner=user, book_type=book_type)
                    books_to_keep = books_list[:new_amount]
                    books_list.exclude(pk__in=books_to_keep).delete()

                elif new_amount > book_type.amount:
                    amount_difference = new_amount - book_type.amount
                    book = Book(book_type=book_type, owner=user)

                    book_list = []
                    for i in range(0, amount_difference):
                        book.pk = None
                        book.accepted = True
                        book.accept_date = timezone.now()
                        book_list.append(book)

                    Book.objects.bulk_create(book_list)

                if new_amount > 0:
                    correct_book_list.append(book_type)

                book_type.amount = new_amount
                books_count += new_amount

        # Seller id shown to the user
        seller_id = timezone.now().strftime("%Y%m%d") + "-" + str(user.pk) + "-" + str(books_count)
        return render(request, 'sellers/success.html',
                      {'seller': user, 'seller_ID': seller_id, 'given_book_list': correct_book_list})
    else:
        hide_actions = True
        for book_type in book_type_list:
            if not book_type.visible:
                hide_actions = False
                break
        return render(request, 'sellers/accept.html',
                      {'user_name': user.user_name(), 'book_list': book_type_list,
                       'hide_actions': hide_actions, 'student_pk': user_pk,
                       'currency': getattr(settings, 'CURRENCY', 'USD')})


@permission_required('common.view_sellers_accept_edit_book', raise_exception=True)
def accept_edit_book(request, user_pk, book_id):
    book = get_object_or_404(BookType, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(accept_books, args=(user_pk,)))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})


@permission_required('common.view_sellers_remove_seller', raise_exception=True)
def remove_seller(request, seller_ids):
    seller_list = AppUser.objects.filter(pk__in=seller_ids.split(','))
    if len(seller_list) == 0:
        raise Http404

    if request.method == 'POST':
        set_success_msg(request, 'seller_removed' if len(seller_list) == 1 else 'sellers_removed')
        Book.objects.filter(owner__pk_in=seller_list).delete()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, 'sellers/remove.html', {'seller_list': seller_list})


def bulk_actions(request, action_name):
    seller_list = []
    if action_name == 'remove' and request.method == 'POST':
        for key, value in request.POST.items():
            if value == 'on':
                # Form field names are in format "select-id", so key[7:] will leave us id
                seller_list.append(key[7:])
        if seller_list:
            return HttpResponseRedirect(reverse(remove_seller, args=[",".join(seller_list)]))
        else:
            return HttpResponseRedirect(reverse(index))
    else:
        raise Http404
