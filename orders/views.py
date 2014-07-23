from django.db.models import Sum
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from orders.models import Order


def order_details(request, order_pk):
    return HttpResponse("Hello, world!")


def not_executed(request):
    orders = get_orders().filter(valid_until__gt=timezone.now(), sold_count=0)
    return render(request, 'orders/not_executed.html', {'orders': orders})


def outdated(request):
    orders = get_orders().filter(valid_until__lte=timezone.now(), sold_count=0)
    return render(request, 'orders/outdated.html', {'orders': orders})


def executed(request):
    orders = get_orders().exclude(sold_count=0)
    return render(request, 'orders/executed.html', {'orders': orders})


def get_orders() -> QuerySet:
    """
    The function returns QuerySet of Order model with all necessary values for displaying also selected/prefetched.
    :return: the QuerySet of Order model
    """
    return Order.objects.select_related('user').prefetch_related('books').annotate(sold_count=Sum('books__sold'))