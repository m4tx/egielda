import json
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from books.forms import BookForm
from books.models import BookType
from common.models import Student
from egielda import settings
from sell.forms import PersonalDataForm


def index(request):
    return HttpResponseRedirect(reverse(personal_data))


def personal_data(request):
    if request.method == 'POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            request.session['personal_data'] = model_to_dict(form.save(commit=False))
            return HttpResponseRedirect(reverse(books))
    else:
        if 'personal_data' in request.session:
            form = PersonalDataForm(instance=Student(**request.session['personal_data']))
        else:
            form = PersonalDataForm()
    return render(request, 'sell/personal_data.html', {'form': form})


def books(request):
    if request.method == 'POST':
        request.session['chosen_books'] = request.POST['book_data']
        if 'btn-back' in request.POST:
            return HttpResponseRedirect(reverse(personal_data))
        elif 'btn-next' in request.POST:
            return HttpResponseRedirect(reverse(summary))
    book_list = BookType.objects.all()
    form = BookForm()
    return render(request, 'sell/books.html',
                  {'form': form, 'book_list': book_list,
                   'chosen_books': request.session['chosen_books'] if 'chosen_books' in request.session else None,
                   'currency': getattr(settings, 'CURRENCY', 'USD')})


def summary(request):
    try:
        existing_list = []
        types = []
        book_list = json.loads(request.session['chosen_books'])
        for book in book_list:
            if 'pk' in book:
                existing_list.append(book['pk'])
            else:
                if book['price'] != "":
                    book['price'] = Decimal(book['price'])
                types.append(BookType(**book))
        types.extend(BookType.objects.filter(pk__in=existing_list))
        return render(request, 'sell/summary.html', {'personal_data': request.session['personal_data'],
                                                     'book_list': sorted(types, key=lambda x: x.title.lower())})
    except ValueError:
        return HttpResponse(status=400)