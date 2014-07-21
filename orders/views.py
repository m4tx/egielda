from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from orders.models import Order


def order_details(request, order_pk):
    return HttpResponse("Hello, world!")


def not_executed(request):
    orders = Order.objects.filter(valid_until__gt=timezone.now())
    return render(request, 'orders/not_executed.html', {'orders': orders})


def outdated(request):
    orders = Order.objects.filter(valid_until__lte=timezone.now())
    return render(request, 'orders/outdated.html', {'orders': orders})


def executed(request):
    return render(request, 'orders/executed.html')
