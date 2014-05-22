from django.http.response import HttpResponse
from django.shortcuts import render
from books.forms import BookForm

from shared.models import BookType


def index(request):
    book_list = BookType.objects.all()
    return render(request, 'books/index.html', {'book_list': book_list})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            pass # TODO
    else:
        form = BookForm()
    return render(request, 'books/add.html', {'form': form})


def edit_book(request, book_id):
    return HttpResponse("Hello world!")


def remove_book(request, book_id):
    return HttpResponse("Hello world!")
