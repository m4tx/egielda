from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from books.forms import BookForm
from books.models import BookType

from common.models import Student

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
    return render(request, 'sell/books.html', {'form': form, 'book_list': book_list})


def summary(request):
    return HttpResponse("Hello, world!")