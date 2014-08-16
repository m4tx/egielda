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

from datetime import timedelta
from collections import Counter

from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from books.models import Book
from common.bookchooserwizard import BookChooserWizard
from orders.models import Order
from settings.settings import Settings
from utils.books import get_available_books


class PurchaseWizard(BookChooserWizard):
    @property
    def page_title(self):
        return _("Purchase books")

    @property
    def url_namespace(self):
        return "purchase"

    @property
    def session_var_name(self):
        return "purchase_chosen_books"

    @property
    def feature_books_in_stock(self):
        return True

    def process_books_summary(self, session, user, book_list):
        book_type_list = [book['pk'] for book in book_list]  # List of Book primary keys

        # Select the Books which are available for purchasing and match the BookTypes we're looking for
        books = get_available_books().select_for_update().filter(book_type__in=book_type_list).order_by('-pk')

        # Remove duplicated Books. Thanks to order_by('-pk'), we'll have firstly added book as a value here

        books_by_id = dict()
        for book in books:
            books_by_id.setdefault(book.book_type.pk, []).append(book)

        error_occurred = False
        correct_book_list = []

        for book in book_list:
            if book['pk'] in books_by_id and book['amount'] > 0:
                if len(books_by_id[book['pk']]) >= book['amount']:
                    books_by_id[book['pk']] = books_by_id[book['pk']][:book['amount']]
                else:
                    book['amount'] = len(books_by_id[book['pk']])
                    error_occurred = True

                correct_book_list.append(book)
            else:
                error_occurred = True

        if not error_occurred:
            settings = Settings('validity_time')
            validity_time = settings.validity_time if settings.exists('validity_time') else 24
            validity_time = timedelta(hours=int(validity_time))
            # Reserve the Books and create our Order
            user.save()
            order = Order(user=user, valid_until=timezone.now() + validity_time)
            order.save()
            session['order_id'] = order.pk
            Book.objects.filter(pk__in=[book.pk for l in books_by_id.values() for book in l]).update(
                reserved_until=timezone.now() + validity_time, reserver=user, order=order)

        return not error_occurred, correct_book_list

    def success(self, request):
        order = Order.objects.select_related('user', 'book_set').annotate(books_count=Count('book')).get(
            pk=request.session['order_id'])
        # Order id shown to the user
        order_id = order.valid_until.strftime("%Y%m%d") + "-" + str(order.pk) + "-" + str(order.user.pk) + "-" + str(
            order.books_count)

        amounts = Counter([book.book_type for book in order.book_set.all()])
        for book_type in amounts.keys():
            book_type.amount = amounts[book_type]

        return render(request, 'purchase/success.html',
                      {'order': order, 'order_ID': order_id, 'chosen_book_list': amounts.keys()})
