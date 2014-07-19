from datetime import timedelta
from decimal import Decimal

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from books.models import BookType
from common.bookchooserwizard import BookChooserWizard
from common.models import Book
from orders.models import Order


class PurchaseWizard(BookChooserWizard):
    @property
    def page_title(self):
        return _("Purchase books")

    @property
    def url_namespace(self):
        return "purchase"

    def process_books_summary(self, user, book_list):
        book_type_list = [book['pk'] for book in book_list]  # List of Book primary keys

        # Select the Books which are not yet sold nor reserved,
        # yet accepted and matches the BookTypes we're looking for
        books = Book.objects.prefetch_related('book_type') \
            .filter(accepted=True, sold=False, book_type__in=book_type_list) \
            .filter(Q(reserved_until__lte=timezone.now()) | Q(reserved_until__isnull=True)).order_by('-pk')

        # Remove duplicated Books. Thanks to order_by('-pk'), we'll have firstly added book as a value here
        book_dict = dict((book.book_type, book.pk) for book in books)

        # Reserve the Books and create our Order
        Book.objects.filter(pk__in=book_dict.values()).update(reserved_until=timezone.now() + timedelta(1),
                                                              reserver=user)
        order = Order(user=user, valid_until=timezone.now() + timedelta(1))
        order.save()
        order.books.add(*book_dict.values())

    def get_book_list(self, book_list):
        existing_list = []
        types = []
        for book in book_list:
            if 'pk' in book:
                existing_list.append(book['pk'])
            else:
                if book['price'] != "":
                    book['price'] = Decimal(book['price'])
                types.append(BookType(**book))
        types.extend(BookType.objects.filter(pk__in=existing_list))

        return types

    def success(self, request):
        return render(request, 'purchase/success.html')