from abc import abstractmethod
import json
from types import FunctionType

from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpRequest
from django.shortcuts import render

from books.forms import BookForm
from books.models import BookType
from common.forms import PersonalDataForm
from common.models import AppUser
from egielda import settings


class BookChooserWizard:
    @property
    @abstractmethod
    def page_title(self):
        """
        :return: the title of the page to the <h1> and <title> tags.
        """
        return None

    @abstractmethod
    def get_personal_data_view(self) -> FunctionType:
        """
        :return: "Personal data" view function
        """
        return None

    @abstractmethod
    def get_books_view(self):
        """
        :return: "Books" view function
        """
        return None

    @abstractmethod
    def get_summary_view(self):
        """
        :return: "Summary" view function
        """
        return None

    @abstractmethod
    def get_book_list(self, book_list: list) -> list:
        """
        Returns list of BookType objects created based on json from the user.
        :param book_list: list of dict objects retrieved from the user as json
        :return: list of BookType objects
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
    def process_books_summary(self, user: AppUser, book_list: list):
        """
        Processes the data provided by user after clicking "Accept" button on the summary page. In other words, saves
        the data from the user to the database. The method is called inside ``transaction.atomic()``.
        :param user: the AppUser that is performing the operation (selling/purchasing)
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

        book_list = BookType.objects.filter(visible=True).exclude(price=0).prefetch_related('categories')
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
                               'chosen_book_list': sorted(self.get_book_list(book_list),
                                                          key=lambda x: x.title.lower())})
        except ValueError:
            return HttpResponseBadRequest()