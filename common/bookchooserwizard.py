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

from abc import abstractmethod
from collections import Counter
import json
from decimal import Decimal

from django.conf.urls import url
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import RedirectView

from books.forms import BookForm
from books.models import BookType
from common.forms import PersonalDataForm
from common.models import AppUser
from egielda import settings
from utils.books import get_available_books
from utils.alerts import set_warning_msg


class BookChooserWizard:
    @property
    @abstractmethod
    def page_title(self) -> str:
        """
        :return: the title of the page to the <h1> and <title> tags.
        """
        return None

    @property
    @abstractmethod
    def url_namespace(self) -> str:
        """
        :return: the URL namespace that the particular subclass of BookChooserWizard is in
        """
        return None

    @property
    @abstractmethod
    def session_var_name(self) -> str:
        """
        :return: session variable name list of chosen books should be stored in
        """
        return None

    @abstractmethod
    def success(self, request: HttpRequest) -> HttpResponse:
        """
        Called on "success" after sending data in last (Summary) step.
        :param request: HttpRequest object from the view
        :return: HttpResponse object (with "Success" informing page, likely)
        """
        pass

    @abstractmethod
    def process_books_summary(self, session, user: AppUser, book_list: list):
        """
        Processes the data provided by user after clicking "Accept" button on the summary page. In other words, saves
        the data from the user to the database. The method is called inside ``transaction.atomic()``.
        :param user: the AppUser that is performing the operation (selling/purchasing). Note that you should save it
                     before using
        :param book_list: list of dict objects retrieved from the user as json
        """
        pass

    @property
    def feature_add_new(self) -> bool:
        """
        Controls whether "Add new book" panel should be shown or not.
        :return: ``True`` if "Add new book" should be enabled; ``False``  otherwise.
        """
        return False

    @property
    def feature_books_in_stock(self) -> bool:
        return False

    @property
    def url_patterns(self):
        return [
            url(r'^$', RedirectView.as_view(url=reverse_lazy(self.url_namespace + ':personal_data')), name='index'),
            url(r'^personal/$', self.personal_data, name='personal_data'),
            url(r'^books/$', self.books, name='books'),
            url(r'^summary/$', self.summary, name='summary'),
        ]

    def get_book_list(self, book_list: list) -> list:
        """
        Returns list of BookType objects created based on json from the user.
        :param book_list: list of dict objects retrieved from the user as json
        :return: list of BookType objects
        """
        existing_dict = {}
        types = []
        for book in book_list:
            if 'pk' in book:
                existing_dict[book['pk']] = book['amount']
            else:
                book['price'] = Decimal(book['price'])
                amount = book['amount']
                del book['amount']
                types.append(BookType(**book))
                types[-1].amount = amount

        existing_list = BookType.objects.filter(pk__in=existing_dict.keys())
        for book in existing_list:
            book.amount = existing_dict[book.pk]
            types.append(book)

        return types

    def personal_data(self, request):
        if request.method == 'POST':
            if 'signout' in request.POST:
                del request.session['app_user']
                del request.session['personal_data']
                return HttpResponseRedirect(reverse(self.url_namespace + ':personal_data'))

            if 'app_user' in request.session:
                user = AppUser.objects.get(pk=int(request.session['app_user']))
                request.session['personal_data'] = model_to_dict(user)
                return HttpResponseRedirect(reverse(self.url_namespace + ':books'))
            else:
                form = PersonalDataForm(request.POST)
                if form.is_valid():
                    request.session['personal_data'] = model_to_dict(form.save(commit=False))
                    return HttpResponseRedirect(reverse(self.url_namespace + ':books'))
        else:
            if 'app_user' in request.session:
                user = AppUser.objects.get(pk=int(request.session['app_user']))
                return render(request, 'book_chooser_wizard/personal_data_signed_in.html',
                              {'page_title': self.page_title, 'appuser': user})
            elif 'personal_data' in request.session:
                form = PersonalDataForm(instance=AppUser(**request.session['personal_data']))
            else:
                form = PersonalDataForm()
        return render(request, 'book_chooser_wizard/personal_data.html', {'page_title': self.page_title, 'form': form})

    def books(self, request):
        if 'personal_data' not in request.session:
            return HttpResponseRedirect(reverse(self.url_namespace + ':personal_data'))

        if request.method == 'POST':
            if 'book_data' in request.POST:
                request.session[self.session_var_name] = request.POST['book_data']
            if 'btn-back' in request.POST:
                return HttpResponseRedirect(reverse(self.url_namespace + ':personal_data'))
            elif 'btn-next' in request.POST:
                return HttpResponseRedirect(reverse(self.url_namespace + ':summary'))

        book_list = BookType.objects.filter(visible=True).exclude(price=0).prefetch_related('categories')
        if self.feature_books_in_stock:
            books_available = get_available_books().filter(book_type__in=book_list)
            countdict = Counter(book.book_type for book in books_available)
            for book_type in book_list:
                book_type.count = countdict[book_type]

        category_list = []
        for book in book_list:
            book.cat_pks_string = ','.join(str(cat.pk) for cat in book.categories.all())
            for cat in book.categories.all():
                if cat not in category_list:
                    category_list.append(cat)

        form = BookForm()
        del form.fields['price']
        del form.fields['categories']
        return render(request, 'book_chooser_wizard/books.html',
                      {'page_title': self.page_title, 'form': form, 'book_list': book_list,
                       'category_list': sorted(category_list, key=lambda o: o.name),
                       'chosen_books': request.session[
                           self.session_var_name] if self.session_var_name in request.session else None,
                       'currency': getattr(settings, 'CURRENCY', 'USD'), 'feature_add_new': self.feature_add_new,
                       'feature_books_in_stock': self.feature_books_in_stock})

    def summary(self, request):
        if 'personal_data' not in request.session:
            return HttpResponseRedirect(reverse(self.url_namespace + ':personal_data'))
        elif self.session_var_name not in request.session:
            return HttpResponseRedirect(reverse(self.url_namespace + ':books'))

        try:
            book_list = json.loads(request.session[self.session_var_name])
            if len(book_list) == 0:
                return HttpResponseRedirect(reverse(self.url_namespace + ':books'))
            if request.method == 'POST':
                if 'btn-back' in request.POST:
                    return HttpResponseRedirect(reverse(self.url_namespace + ':books'))
                else:
                    with transaction.atomic():
                        if 'app_user' in request.session:
                            user = AppUser.objects.get(pk=int(request.session['app_user']))
                        else:
                            user = AppUser(**request.session['personal_data'])
                        success, book_list = self.process_books_summary(request.session, user, book_list)

                        if success:
                            # Prevent from adding the same books multiple times
                            del request.session[self.session_var_name]
                            # "Sign in" the user
                            request.session['app_user'] = user.pk
                            return self.success(request)
                        else:
                            request.session[self.session_var_name] = json.dumps(book_list)
                            set_warning_msg(request, 'purchase_incomplete')
                            return HttpResponseRedirect(reverse(self.url_namespace + ':summary'))

            else:
                return render(request, 'book_chooser_wizard/summary.html',
                              {'page_title': self.page_title, 'personal_data': request.session['personal_data'],
                               'chosen_book_list': sorted(self.get_book_list(book_list),
                                                          key=lambda x: x.title.lower())})
        except ValueError:
            return HttpResponseBadRequest()
