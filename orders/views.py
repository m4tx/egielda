from django.shortcuts import render
from django.utils import timezone

from orders.models import Order


def not_executed(request):
    orders = Order.objects.filter(valid_until__gt=timezone.now())
    return render(request, 'orders/not_executed.html', {'orders': orders})


def outdated(request):
    orders = Order.objects.filter(valid_until__lte=timezone.now())
    return render(request, 'orders/outdated.html', {'orders': orders})


def executed(request):
    return render(request, 'orders/executed.html')