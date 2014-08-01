from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect

from common.auth import user_is_admin
from settings.forms import SettingsForm
from settings.settings import Settings
from settings.settings import string_to_datetime
from utils.alerts import set_success_msg, alerts
from utils.dates import datetime_html_format


@user_passes_test(user_is_admin)
def index(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            Settings().start_sell = form.cleaned_data['start_sell']
            Settings().end_sell = form.cleaned_data['end_sell']
            Settings().start_purchase = form.cleaned_data['start_purchase']
            Settings().end_purchase = form.cleaned_data['end_purchase']
            Settings().profit_per_book = form.cleaned_data['profit_per_book']
            set_success_msg(request, 'settings_updated')
            return HttpResponseRedirect("")
    else:
        try:
            settings = Settings('start_sell', 'end_sell', 'start_purchase', 'end_purchase', 'profit_per_book')
            # Pack the retrieved values into new dictionary, formatting them as HTML datetime first
            values = {
                'start_sell': datetime_html_format(string_to_datetime(settings.start_sell)),
                'end_sell': datetime_html_format(string_to_datetime(settings.end_sell)),
                'start_purchase': datetime_html_format(string_to_datetime(settings.start_purchase)),
                'end_purchase': datetime_html_format(string_to_datetime(settings.end_purchase)),
                'profit_per_book': settings.profit_per_book,
            }
            form = SettingsForm(values)
        except KeyError:
            form = SettingsForm()

    return render(request, 'settings/index.html', alerts(request, {'page_title': _("Settings"), 'form': form}))