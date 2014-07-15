from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from common.auth import user_is_admin
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect

from common.models import Setting
from dates.forms import DatesForm

from egielda.views import string2datetime


@user_passes_test(user_is_admin)
def index(request):
    if request.method == 'POST':
        form = DatesForm(request.POST)
        if form.is_valid():
            Setting.objects.update_or_create(name="start_sell", defaults={'value': form.cleaned_data['start_sell']})
            Setting.objects.update_or_create(name="end_sell", defaults={'value': form.cleaned_data['end_sell']})
            Setting.objects.update_or_create(name="start_purchase", defaults={'value': form.cleaned_data['start_purchase']})
            Setting.objects.update_or_create(name="end_purchase", defaults={'value': form.cleaned_data['end_purchase']})
            return HttpResponseRedirect("")
    else:
        try:
            start_sell = Setting.objects.get(name="start_sell").value
            end_sell = Setting.objects.get(name="end_sell").value
            start_purchase = Setting.objects.get(name="start_purchase").value
            end_purchase = Setting.objects.get(name="end_purchase").value
            values = dict()
            values['start_sell'] = string2datetime(start_sell).strftime("%Y-%m-%dT%H:%M")
            values['end_sell'] = string2datetime(end_sell).strftime("%Y-%m-%dT%H:%M")
            values['start_purchase'] = string2datetime(start_purchase).strftime("%Y-%m-%dT%H:%M")
            values['end_purchase'] = string2datetime(end_purchase).strftime("%Y-%m-%dT%H:%M")
            form = DatesForm(values)
        except Exception as e:
            form = DatesForm()

    return render(request, 'dates/index.html', {'page_title': _("Dates"), 'form': form})