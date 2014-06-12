from decimal import Decimal

from django.core.urlresolvers import reverse

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from books.models import BookType
from common.models import Book
from common.views import BookChooserWizard


class SellWizard(BookChooserWizard):
    def page_title(self):
        return _("Sell books")

    def get_personal_data_view(self):
        return personal_data

    def get_books_view(self):
        return books

    def get_summary_view(self):
        return summary

    def process_books_summary(self, user, book_list):
        for book in book_list:
            dbbook = Book(owner=user, accepted=False, sold=False)
            if 'pk' in book:
                dbbook.book_type_id = book['pk']
            else:
                if book['price'] != "":
                    book['price'] = Decimal(book['price'])
                else:
                    book['price'] = 0
                if book['publication_year'] == "":
                    book['publication_year'] = 1900
                book_type = BookType(**book)
                book_type.save()
                dbbook.book_type = type
            dbbook.save()

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
        return render(request, 'sell/success.html')


def index(request):
    return HttpResponseRedirect(reverse(personal_data))


def personal_data(request):
    return SellWizard().personal_data(request)


def books(request):
    return SellWizard().books(request)


def summary(request):
    return SellWizard().summary(request)
