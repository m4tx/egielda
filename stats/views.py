from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from common.auth import user_is_admin
from django.utils.translation import ugettext_lazy as _

from common.models import Purchase


@user_passes_test(user_is_admin)
def index(request):
    return render(request, 'stats/index.html', {'page_title': _("Statistics")})

@user_passes_test(user_is_admin)
def books_sold(request):
    Purchase.objects.all().order_by('date')
    return render(request, 'stats/books_sold.html', {'page_title': _("Books sold")})