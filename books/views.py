from django.http.response import HttpResponse
from django.shortcuts import render

from shared.models import BookType


def index(request):
    book_list = BookType.objects.all()
    return render(request, 'books/index.html', {'book_list': book_list})


def add_book(request):
    return HttpResponse("Hello world!")


def edit_book(request, book_id):
    return HttpResponse("Hello world!")


def remove_book(request, book_id):
    return HttpResponse("Hello world!")
