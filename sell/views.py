from decimal import Decimal
import re

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from books.models import BookType, Book
from common.bookchooserwizard import BookChooserWizard


class SellWizard(BookChooserWizard):
    @property
    def page_title(self):
        return _("Sell books")

    @property
    def url_namespace(self):
        return "sell"

    @property
    def session_var_name(self):
        return "sell_chosen_books"

    @property
    def feature_add_new(self):
        return True

    def process_books_summary(self, session, user, book_list):
        for book in book_list:
            amount = book['amount']
            del book['amount']

            user.save()
            dbbook = Book(owner=user, accepted=False, sold=False)
            if 'pk' in book:
                dbbook.book_type_id = book['pk']
            else:
                book['isbn'] = re.sub(r'[^\d.]+', '', book['isbn'])
                book['price'] = Decimal(book['price'])
                if book['publication_year'] == "":
                    book['publication_year'] = 1970

                book_type = BookType(**book)
                book_type.save()
                dbbook.book_type = book_type

            for i in range(0, amount):
                dbbook.pk = None
                dbbook.save()

        return True, None

    def success(self, request):
        return render(request, 'sell/success.html')