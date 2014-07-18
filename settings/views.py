from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from common.auth import user_is_admin
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from common.models import Setting
from settings.forms import DatesForm
from settings.settings import Settings

from settings.settings import string2datetime


@user_passes_test(user_is_admin)
def index(request):
    return HttpResponseRedirect(reverse(dates))

@user_passes_test(user_is_admin)
def dates(request):
    if request.method == 'POST':
        form = DatesForm(request.POST)
        if form.is_valid():
            Setting.objects.update_or_create(name="start_sell",
                                             defaults={'value': form.cleaned_data['start_sell']})
            Setting.objects.update_or_create(name="end_sell",
                                             defaults={'value': form.cleaned_data['end_sell']})
            Setting.objects.update_or_create(name="start_purchase",
                                             defaults={'value': form.cleaned_data['start_purchase']})
            Setting.objects.update_or_create(name="end_purchase",
                                             defaults={'value': form.cleaned_data['end_purchase']})
            return HttpResponseRedirect("")
    else:
        try:
            settings = Settings(['start_sell', 'end_sell', 'start_purchase', 'end_purchase'])
            start_sell = string2datetime(settings.get('start_sell'))
            end_sell = string2datetime(settings.get('end_sell'))
            start_purchase = string2datetime(settings.get('start_purchase'))
            end_purchase = string2datetime(settings.get('end_purchase'))

            values = dict()
            values['start_sell'] = start_sell.strftime("%Y-%m-%dT%H:%M")
            values['end_sell'] = end_sell.strftime("%Y-%m-%dT%H:%M")
            values['start_purchase'] = start_purchase.strftime("%Y-%m-%dT%H:%M")
            values['end_purchase'] = end_purchase.strftime("%Y-%m-%dT%H:%M")
            form = DatesForm(values)
        except Setting.DoesNotExist:
            form = DatesForm()

    return render(request, 'settings/dates.html', {'page_title': _("Dates"), 'form': form})