from decimal import Decimal

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from books.forms import BookForm
from books.models import BookType, Book
from common.auth import user_is_admin
from common.models import AppUser
from utils.alerts import set_success_msg
from egielda import settings
from utils.books import books_by_types


@user_passes_test(user_is_admin)
def index(request):
    book_list = Book.objects.filter(accepted=False).select_related('owner')
    student_list = []
    for book in book_list:
        if book.owner not in student_list:
            student_list.append(book.owner)

    return render(request, 'sellers/index.html', {'student_list': student_list})


@user_passes_test(user_is_admin)
def accept_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    books = Book.objects.filter(owner=user, accepted=False).select_related('book_type')

    d = books_by_types(books)
    book_type_list = list(d.keys())

    if not books:
        raise Http404("There's no books of that user.")

    if request.method == 'POST':
        with transaction.atomic():
            books.update(accepted=True, accept_date=timezone.now())
            for book_type in book_type_list:
                if not book_type.visible:
                    book_type.price = Decimal(request.POST['price-' + str(book_type.pk)])
                    book_type.visible = True
                    book_type.save()

                new_amount = int(request.POST['amount-' + str(book_type.pk)])
                if new_amount < book_type.amount:
                    books_list = Book.objects.filter(owner=user, book_type=book_type)
                    books_to_keep = books_list[:new_amount]
                    books_list.exclude(pk__in=books_to_keep).delete()
                elif new_amount > book_type.amount:
                    amount_difference = new_amount - book_type.amount
                    book = d[book_type]
                    for i in range(0, amount_difference):
                        book.pk = None
                        book.accepted = True
                        book.save()

        set_success_msg(request, 'books_accepted')
        return HttpResponseRedirect(reverse(index))
    else:
        hide_actions = True
        for book_type in book_type_list:
            if not book_type.visible:
                show_actions = False
                break
        return render(request, 'sellers/accept.html',
                      {'user_name': user.user_name(), 'book_list': book_type_list,
                       'hide_actions': hide_actions, 'student_pk': user_pk,
                       'currency': getattr(settings, 'CURRENCY', 'USD')})


@user_passes_test(user_is_admin)
def accept_edit_book(request, user_pk, book_id):
    book = get_object_or_404(BookType, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(accept_books, args=(user_pk,)))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})
