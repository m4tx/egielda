from datetime import timedelta
from decimal import Decimal

from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from books.models import BookType, Book
from common.bookchooserwizard import BookChooserWizard
from orders.models import Order
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

    def process_books_summary(self, user, book_list):
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
            if book['pk'] in books_by_id:
                if len(books_by_id[book['pk']]) >= book['amount']:
                    books_by_id[book['pk']] = books_by_id[book['pk']][:book['amount']]
                else:
                    book['amount'] = len(books_by_id[book['pk']])
                    error_occurred = True

                correct_book_list.append(book)
            else:
                error_occurred = True

        if not error_occurred:
            # Reserve the Books and create our Order
            order = Order(user=user, valid_until=timezone.now() + timedelta(1))
            order.save()
            Book.objects.filter(pk__in=[book.pk for l in books_by_id.values() for book in l]).update(
                reserved_until=timezone.now() + timedelta(1), reserver=user, order=order)

        return not error_occurred, correct_book_list

    def success(self, request):
        return render(request, 'purchase/success.html')