from django.shortcuts import render

from settings.settings import is_purchase_available, is_sell_available


def home(request):
    sell_available = is_sell_available()
    purchase_available = is_purchase_available()

    return render(request, 'egielda/home.html',
                  {'sell_available': sell_available, 'purchase_available': purchase_available})