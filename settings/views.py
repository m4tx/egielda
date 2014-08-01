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
            set_success_msg(request, 'settings_updated')
            return HttpResponseRedirect("")
    else:
        try:
            settings = Settings('start_sell', 'end_sell', 'start_purchase', 'end_purchase')
            # Pack the retrieved values into new dictionary, formatting them as HTML datetime first
            values = dict(
                (o, datetime_html_format(string_to_datetime(v))) for o, v in settings.__dict__['settings'].items())
            form = DatesForm(values)
        except KeyError:
            form = SettingsForm()

    return render(request, 'settings/index.html', alerts(request, {'page_title': _("Settings"), 'form': form}))
