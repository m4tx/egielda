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

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from books.models import BookType, OrderedBook
from common.bookchooserwizard import BookChooserWizard
from orders.models import Order
from utils.books import get_available_books, get_available_amount


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
        amounts = get_available_amount(books)

        # Remove duplicated Books. Thanks to order_by('-pk'), we'll have firstly added book as a value here
        books_by_id = dict()
        for book in books:
            books_by_id.setdefault(book.book_type.pk, []).append(book)

        order = Order(user=user)
        order.save()

        error_occurred = False
        correct_book_list = []
        parts_of_order = []
        for book in book_list:
            if book['pk'] in books_by_id and book['amount'] > 0:
                if amounts[book['pk']] >= book['amount']:
                    parts_of_order.append(OrderedBook(book_type=BookType.objects.get(pk=book['pk']),
                                                      count=book['amount'], order=order))
                else:
                    book['amount'] = amounts[book['pk']]
                    error_occurred = True

                correct_book_list.append(book)
            else:
                error_occurred = True

        if not error_occurred:
            OrderedBook.objects.bulk_create(parts_of_order)
            session['order_id'] = order.pk

        return not error_occurred, correct_book_list

    def success(self, request):
        order = Order.objects.prefetch_related('user', 'orderedbook_set', 'orderedbook_set__book_type').annotate(
            books_count=Sum('orderedbook__count')).get(pk=request.session['order_id'])

        # Order id shown to the user
        order_id = order.date.strftime("%Y%m%d") + "-" + str(order.pk) + "-" + str(order.user.pk) + "-" + str(
            order.books_count)

        amounts = dict((orderedbook.book_type, orderedbook.count) for orderedbook in order.orderedbook_set.all())
        for book_type in amounts.keys():
            book_type.amount = amounts[book_type]

        del request.session['order_id']

        return render(request, 'purchase/success.html',
                      {'order': order, 'order_ID': order_id, 'chosen_book_list': amounts.keys()})
