from collections import Counter

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Sum, Count
from common.auth import user_is_admin

from common.models import Book, BookType, AppUser
from egielda import settings


@user_passes_test(user_is_admin)
def index(request):
    stats = dict()
    books = BookType.objects.filter(book__sold=True).annotate(count=Count('book'))
    stats['books_sold'] = books.aggregate(Sum('count'))['count__sum'] or 0
    stats['books_sold_value'] = books.aggregate(Sum('price', field='count * price'))['price__sum'] or 0

    return render(request, 'stats/index.html', {'stats': stats,
                                                'currency': getattr(settings, 'CURRENCY', 'USD')})


@user_passes_test(user_is_admin)
def books_sold(request):
    books = Book.objects.filter(sold=True).order_by('-sold_date').select_related('book_type', 'purchaser')

    stats = dict()

    for book in books:
        stats.setdefault(book.sold_date.date(), []).append(book)

    for key, stat in stats.items():
        sum = 0
        for el in stat:
            sum += el.book_type.price

        stats[key] = (stats[key], sum)

    return render(request, 'stats/books_sold.html', {'stats': list(reversed(sorted(stats.items()))),
                                                     'currency': getattr(settings, 'CURRENCY', 'USD')})

@user_passes_test(user_is_admin)
def users(request):
    student_list = AppUser.objects.annotate(count=Count('appuser_owner')).exclude(count=0)

    return render(request, 'stats/users.html', {'student_list': student_list})


@user_passes_test(user_is_admin)
def list_books(request, user_pk):
    user = get_object_or_404(AppUser, pk=user_pk)
    book_list = get_list_or_404(Book.objects.select_related('book_type', 'purchaser'), owner=user)

    amounts = Counter([(str(b.book_type.isbn) + b.book_type.title) for b in book_list])
    d = {}
    e = {}
    for book in book_list:
        book.amount = amounts[str(book.book_type.isbn) + book.book_type.title]
        d[(str(book.book_type.isbn) + book.book_type.title)] = book

        e.setdefault((str(book.book_type.isbn) + book.book_type.title), [])
        if book.sold:
            e[str(book.book_type.isbn) + book.book_type.title].append(book.purchaser)

    book_list = list(d.values())
    book_list = zip(book_list, list(e.values()))

    return render(request, 'stats/list_books.html', {'user_name': user.user_name(),
                                                     'book_list': book_list,
                                                     'currency': getattr(settings, 'CURRENCY', 'USD')})