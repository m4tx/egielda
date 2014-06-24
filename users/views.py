from decimal import Decimal

from django.contrib.auth.decorators import user_passes_test

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404

from books.forms import BookForm
from books.models import BookType
from common.auth import user_is_admin
from common.models import AppUser, Book
from common.uiutils import alerts


@user_passes_test(user_is_admin)
def index(request):
    student_list = AppUser.objects.all()
    return render(request, 'users/index.html', {'student_list': student_list})


@user_passes_test(user_is_admin)
def unaccepted(request):
    book_list = Book.objects.filter(accepted=False)
    student_list = []
    for book in book_list:
        if book.owner not in student_list:
            student_list.append(book.owner)

    return render(request, 'users/unaccepted.html', alerts(request, {'student_list': student_list}))


@user_passes_test(user_is_admin)
def list_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    book_list = get_list_or_404(Book, owner=user)
    return render(request, 'users/list_books.html',
                  {'user_name': user.user_name(), 'book_list': book_list})


@user_passes_test(user_is_admin)
def accept_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    book_list = get_list_or_404(Book, owner=user, accepted=False)
    if request.method == 'POST':
        with transaction.atomic():
            for book in book_list:
                if not book.book_type.visible:
                    book.book_type.price = Decimal(request.POST['price-' + str(book.book_type.pk)])
                    book.book_type.visible = True
                    book.book_type.save()
                book.accepted = True
                book.save()
        request.session['success_msg'] = 'books_accepted'
        return HttpResponseRedirect(reverse(unaccepted))
    else:
        return render(request, 'users/accept.html',
                      {'user_name': user.user_name(), 'book_list': book_list, 'student_pk': user_pk})


@user_passes_test(user_is_admin)
def accept_edit_book(request, user_pk, book_id):
    book = get_object_or_404(BookType, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(accept_books, args=user_pk))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})
