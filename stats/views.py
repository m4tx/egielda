from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.db.models import Sum, Count
from common.auth import user_is_admin
from django.utils.translation import ugettext_lazy as _

from common.models import Book, BookType
from egielda import settings


@user_passes_test(user_is_admin)
def index(request):
    stats = dict()
    books = BookType.objects.filter(book__sold=True).annotate(count=Count('book'))
    stats['books_sold'] = books.aggregate(Sum('count'))['count__sum'] or 0
    stats['books_sold_value'] = books.aggregate(Sum('price', field='count * price'))['price__sum'] or 0

    return render(request, 'stats/index.html', {'page_title': _("Statistics"), 'stats': stats,
                                                'currency': getattr(settings, 'CURRENCY', 'USD')
    })


@user_passes_test(user_is_admin)
def books_sold(request):
    books = Book.objects.filter(sold=True).order_by('-sold_date')

    stats = dict()

    for book in books:
        stats.setdefault(book.sold_date.date(), []).append(book)

    for key, stat in stats.items():
        sum = 0
        for el in stat:
            sum += el.book_type.price

        stats[key] = (stats[key], sum)

    return render(request, 'stats/books_sold.html', {'page_title': _("Books sold"),
                                                    'stats': list(reversed(sorted(stats.items()))),
                                                    'currency': getattr(settings, 'CURRENCY', 'USD')
    })