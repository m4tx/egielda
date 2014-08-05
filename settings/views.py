from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect

from settings.forms import SettingsForm
from settings.settings import Settings
from settings.settings import string_to_datetime
from utils.alerts import set_success_msg
from utils.dates import datetime_html_format


@permission_required('common.view_settings_index', raise_exception=True)
def index(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            Settings().start_sell = form.cleaned_data['start_sell']
            Settings().end_sell = form.cleaned_data['end_sell']
            Settings().start_purchase = form.cleaned_data['start_purchase']
            Settings().end_purchase = form.cleaned_data['end_purchase']
            Settings().profit_per_book = form.cleaned_data['profit_per_book']
            Settings().validity_time = form.cleaned_data['validity_time']
            Settings().homepage_info = form.cleaned_data['homepage_info']
            set_success_msg(request, 'settings_updated')
            return HttpResponseRedirect("")
    else:
        settings = Settings('start_sell', 'end_sell', 'start_purchase', 'end_purchase', 'profit_per_book',
                            'validity_time', 'homepage_info')
        # Pack the retrieved values into new dictionary, formatting them as HTML datetime first
        values = dict(
            filter(lambda x: x is not None,
                   [add_date_value('start_sell', settings),
                    add_date_value('end_sell', settings),
                    add_date_value('start_purchase', settings),
                    add_date_value('end_purchase', settings),
                    ('profit_per_book', settings.profit_per_book if settings.exists('profit_per_book') else 1),
                    ('validity_time', settings.validity_time if settings.exists('validity_time') else 24),
                    ('homepage_info', settings.homepage_info if settings.exists('homepage_info') else "")]))
        form = SettingsForm(initial=values)

    return render(request, 'settings/index.html', {'page_title': _("Settings"), 'form': form})


def add_date_value(name, settings):
    if settings.exists(name):
        return name, datetime_html_format(string_to_datetime(getattr(settings, name)))
    else:
        return None