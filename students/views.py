from collections import defaultdict

from django.shortcuts import render, get_object_or_404

from common.models import Student, Book


def index(request):
    student_list = Student.objects.all()
    return render(request, 'students/index.html', {'student_list': student_list})


def unaccepted(request):
    book_list = Book.objects.filter(physical=False)
    counts = defaultdict(int)
    for book in book_list:
        counts[book.owner] += 1
    return render(request, 'students/unaccepted.html',
                  {'student_list': counts.items(), 'parent_page': 'students.views.unaccepted'})


def unaccepted_list_books(request, student_pk):
    return list_books(request, student_pk, 'students.views.unaccepted')


def list_books(request, student_pk, parent_page='students.views.index'):
    student = get_object_or_404(Student, pk=student_pk)
    book_list = Book.objects.filter(owner=student)
    return render(request, 'students/list_books.html',
                  {'student_name': student.student_name(), 'book_list': book_list,
                   'parent_page': parent_page})


def accept_books(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    book_list = Book.objects.filter(owner=student, physical=False)
    return render(request, 'students/accept.html', {'student_name': student.student_name(), 'book_list': book_list})


