from django.shortcuts import render

from settings.settings import is_purchase_available, is_sell_available, Settings


def home(request):
    settings = Settings('homepage_info')
    sell_available = is_sell_available()
    purchase_available = is_purchase_available()

    return render(request, 'egielda/home.html',
                  {'sell_available': sell_available,
                   'purchase_available': purchase_available,
                   'homepage_info': settings.homepage_info if settings.exists('homepage_info') else None})