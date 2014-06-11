from collections import defaultdict
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, get_list_or_404

from books.forms import BookForm

from books.models import BookType

from common.models import Student, Book


def index(request):
    student_list = Student.objects.all()
    return render(request, 'students/index.html', {'student_list': student_list})


def unaccepted(request):
    book_list = Book.objects.filter(accepted=False)
    counts = defaultdict(int)
    for book in book_list:
        counts[book.owner] += 1
    return render(request, 'students/unaccepted.html',
                  {'student_list': counts.items(), 'parent_page': 'students.views.unaccepted'})


def unaccepted_list_books(request, student_pk):
    return list_books(request, student_pk, 'students.views.unaccepted')


def list_books(request, student_pk, parent_page='students.views.index'):
    student = get_object_or_404(Student, pk=student_pk)
    book_list = get_list_or_404(Book, owner=student)
    return render(request, 'students/list_books.html',
                  {'student_name': student.student_name(), 'book_list': book_list,
                   'parent_page': parent_page})


def accept_books(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    book_list = get_list_or_404(Book, owner=student, accepted=False)
    if request.method == 'POST':
        with transaction.atomic():
            for book in book_list:
                if not book.book_type.visible:
                    book.book_type.price = Decimal(request.POST['price-' + str(book.book_type.pk)])
                    book.book_type.visible = True
                    book.book_type.save()
                book.accepted = True
                book.save()
        return render(request, 'students/accept_success.html', {'student_name': student.student_name()})
    else:
        return render(request, 'students/accept.html',
                      {'student_name': student.student_name(), 'book_list': book_list, 'student_pk': student_pk})


def accept_edit_book(request, student_pk, book_id):
    book = get_object_or_404(BookType, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(accept_books, args=student_pk))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})