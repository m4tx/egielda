from decimal import Decimal
from collections import Counter

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404

from books.forms import BookForm
from books.models import BookType
from common.auth import user_is_admin
from common.models import AppUser, Book
from utils.alerts import alerts, set_success_msg


@user_passes_test(user_is_admin)
def index(request):
    student_list = AppUser.objects.all()
    return render(request, 'users/index.html', {'student_list': student_list})


@user_passes_test(user_is_admin)
def unaccepted(request):
    book_list = Book.objects.filter(accepted=False).select_related('owner')
    student_list = []
    for book in book_list:
        if book.owner not in student_list:
            student_list.append(book.owner)

    return render(request, 'users/unaccepted.html', alerts(request, {'student_list': student_list}))


@user_passes_test(user_is_admin)
def list_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    book_list = get_list_or_404(Book.objects.select_related('book_type'), owner=user)

    amounts = Counter([(str(b.book_type.isbn) + b.book_type.title) for b in book_list])
    d = {}
    for book in book_list:
        book.amount = amounts[str(book.book_type.isbn) + book.book_type.title]
        d[(str(book.book_type.isbn) + book.book_type.title)] = book
    book_list = list(d.values())

    return render(request, 'users/list_books.html',
                  {'user_name': user.user_name(), 'book_list': book_list})


@user_passes_test(user_is_admin)
def accept_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    books = Book.objects.filter(owner=user, accepted=False).select_related('book_type')
    book_list = list(books)

    amounts = Counter([(str(b.book_type.isbn) + b.book_type.title) for b in book_list])
    d = {}
    for book in book_list:
        book.amount = amounts[str(book.book_type.isbn) + book.book_type.title]
        d[(str(book.book_type.isbn) + book.book_type.title)] = book
    book_list = list(d.values())

    if not book_list:
        raise Http404("There's no books of that user.")

    if request.method == 'POST':
        with transaction.atomic():
            books.update(accepted=True)
            for book in book_list:
                if not book.book_type.visible:
                    book.book_type.price = Decimal(request.POST['price-' + str(book.book_type.pk)])
                    book.book_type.visible = True
                    book.book_type.save()

            for book in book_list:
                if int(request.POST['amount-' + str(book.book_type.pk)]) < book.amount:
                    books_list = Book.objects.filter(owner=user,
                                        book_type__isbn=book.book_type.isbn,
                                        book_type__title=book.book_type.title
                    )

                    books_to_keep = books_list[:book.amount-int(request.POST['amount-' + str(book.book_type.pk)])]
                    books_list.exclude(pk__in=books_to_keep).delete()

                elif int(request.POST['amount-' + str(book.book_type.pk)]) > book.amount:
                    amount = int(request.POST['amount-' + str(book.book_type.pk)]) - book.amount
                    del book.amount
                    dbbook = book
                    for i in range(0, amount):
                        dbbook.pk = None
                        dbbook.save()

        set_success_msg(request, 'books_accepted')
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
