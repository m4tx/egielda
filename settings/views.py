from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from common.auth import user_is_admin
from settings.forms import DatesForm
from settings.settings import Settings
from settings.settings import string_to_datetime
from utils.alerts import set_success_msg, alerts
from utils.dates import datetime_html_format


@user_passes_test(user_is_admin)
def index(request):
    return HttpResponseRedirect(reverse(dates))


@user_passes_test(user_is_admin)
def dates(request):
    if request.method == 'POST':
        form = DatesForm(request.POST)
        if form.is_valid():
            Settings().start_sell = form.cleaned_data['start_sell']
            Settings().end_sell = form.cleaned_data['end_sell']
            Settings().start_purchase = form.cleaned_data['start_purchase']
            Settings().end_purchase = form.cleaned_data['end_purchase']
            set_success_msg(request, 'settings_updated')
            return HttpResponseRedirect("")
    else:
        try:
            settings = Settings(['start_sell', 'end_sell', 'start_purchase', 'end_purchase'])
            start_sell = string_to_datetime(settings.start_sell)
            end_sell = string_to_datetime(settings.end_sell)
            start_purchase = string_to_datetime(settings.start_purchase)
            end_purchase = string_to_datetime(settings.end_purchase)

            values = {
                'start_sell': datetime_html_format(start_sell),
                'end_sell': datetime_html_format(end_sell),
                'start_purchase': datetime_html_format(start_purchase),
                'end_purchase': datetime_html_format(end_purchase),
            }
            form = DatesForm(values)
        except KeyError:
            form = DatesForm()

    return render(request, 'settings/dates.html', alerts(request, {'page_title': _("Dates"), 'form': form}))


