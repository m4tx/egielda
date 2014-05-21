from django.shortcuts import render
from shared.models import BookType


def index(request):
    book_list = BookType.objects.all()
    return render(request, 'books/index.html', {'book_list': book_list})
