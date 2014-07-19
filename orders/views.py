from django.shortcuts import render


def not_executed(request):
    return render(request, 'orders/not_executed.html')


def outdated(request):
    return render(request, 'orders/outdated.html')


def executed(request):
    return render(request, 'orders/executed.html')