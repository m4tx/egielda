from django.shortcuts import render
from common.models import Setting
from datetime import datetime
from django.utils import timezone

def home(request):
    sell_available = False
    purchase_available = False

    try:
        start_sell = string2datetime(Setting.objects.get(name="start_sell").value)
        end_sell = string2datetime(Setting.objects.get(name="end_sell").value)
        start_purchase = string2datetime(Setting.objects.get(name="start_purchase").value)
        end_purchase = string2datetime(Setting.objects.get(name="end_purchase").value)

        now = timezone.now()

        if (now-start_sell).total_seconds() > 0 and (end_sell-now).total_seconds() > 0:
            sell_available = True

        if (now-start_purchase).total_seconds() > 0 and (end_purchase-now).total_seconds() > 0:
            purchase_available = True
    except Exception:
        sell_available = purchase_available = True

    return render(request, 'egielda/home.html', {'sell_available': sell_available, 'purchase_available': purchase_available})

def string2datetime(date):
    tz_index = date.index('+')
    date = date[:tz_index] + date[tz_index:].replace(':', '')
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S%z')