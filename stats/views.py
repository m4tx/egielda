from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.db.models import Sum, Count
from common.auth import user_is_admin
from django.utils.translation import ugettext_lazy as _

from common.models import Purchase, BookType
from egielda import settings


@user_passes_test(user_is_admin)
def index(request):
    stats = dict()
    stats['books_sold_value'] = BookType.objects.filter(book__sold=True).annotate(count=Count('book')).aggregate(
                                                        Sum('price', field='count * price'))['price__sum']

    return render(request, 'stats/index.html', {'page_title': _("Statistics"), 'stats': stats,
                                                'currency': getattr(settings, 'CURRENCY', 'USD')})


@user_passes_test(user_is_admin)
def books_sold(request):
    Purchase.objects.all().order_by('-date')
    return render(request, 'stats/books_sold.html', {'page_title': _("Books sold")})