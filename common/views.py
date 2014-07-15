from abc import abstractmethod
import json

from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from books.forms import BookForm
from books.models import BookType
from categories.models import Category
from common.forms import PersonalDataForm
from common.models import AppUser
from egielda import settings


class BookChooserWizard:
    @property
    @abstractmethod
    def page_title(self):
        return None

    @abstractmethod
    def get_personal_data_view(self):
        return None

    @abstractmethod
    def get_books_view(self):
        return None

    @abstractmethod
    def get_summary_view(self):
        return None

    @abstractmethod
    def get_book_list(self, book_list):
        return None

    @abstractmethod
    def success(self, request):
        pass

    @abstractmethod
    def process_books_summary(self, user, book_list):
        pass

    @property
    def feature_add_new(self):
        return False

    def personal_data(self, request):
        if request.method == 'POST':
            form = PersonalDataForm(request.POST)
            if form.is_valid():
                request.session['personal_data'] = model_to_dict(form.save(commit=False))
                return HttpResponseRedirect(reverse(self.get_books_view()))
        else:
            if 'personal_data' in request.session:
                form = PersonalDataForm(instance=AppUser(**request.session['personal_data']))
            else:
                form = PersonalDataForm()
        return render(request, 'book_chooser_wizard/personal_data.html', {'page_title': self.page_title, 'form': form})

    def books(self, request):
        if 'personal_data' not in request.session:
            return HttpResponseRedirect(reverse(self.get_personal_data_view()))

        if request.method == 'POST':
            request.session['chosen_books'] = request.POST['book_data']
            if 'btn-back' in request.POST:
                return HttpResponseRedirect(reverse(self.get_personal_data_view()))
            elif 'btn-next' in request.POST:
                return HttpResponseRedirect(reverse(self.get_summary_view()))

        book_list = BookType.objects.filter(visible=True).exclude(price=0)
        category_list = Category.objects.all()
        form = BookForm()
        del form.fields['price']
        return render(request, 'book_chooser_wizard/books.html',
                      {'page_title': self.page_title, 'form': form, 'book_list': book_list,
                       'category_list': category_list,
                       'chosen_books': request.session['chosen_books'] if 'chosen_books' in request.session else None,
                       'currency': getattr(settings, 'CURRENCY', 'USD'), 'feature_add_new': self.feature_add_new})

    def summary(self, request):
        if 'personal_data' not in request.session:
            return HttpResponseRedirect(reverse(self.get_personal_data_view()))
        elif 'chosen_books' not in request.session:
            return HttpResponseRedirect(reverse(self.get_books_view()))

        try:
            book_list = json.loads(request.session['chosen_books'])
            if len(book_list) == 0:
                return HttpResponseRedirect(reverse(self.get_books_view()))
            if request.method == 'POST':
                if 'btn-back' in request.POST:
                    return HttpResponseRedirect(reverse(self.get_books_view()))
                else:
                    with transaction.atomic():
                        user = AppUser(**request.session['personal_data'])
                        user.save()
                        self.process_books_summary(user, book_list)
                    del request.session['chosen_books']  # Prevent from adding the same books multiple times
                    return self.success(request)
            else:
                return render(request, 'book_chooser_wizard/summary.html',
                              {'page_title': self.page_title, 'personal_data': request.session['personal_data'],
                               'chosen_book_list': sorted(self.get_book_list(book_list), key=lambda x: x.title.lower())})
        except ValueError:
            return HttpResponseBadRequest()
