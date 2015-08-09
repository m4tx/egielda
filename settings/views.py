# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from settings.forms import SettingsForm
from settings.settings import Settings
from settings.settings import string_to_datetime
from utils.alerts import set_success_msg
from utils.dates import datetime_html_format, datetime_to_string


@permission_required('common.view_settings_index', raise_exception=True)
def index(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            Settings().start_sell = datetime_to_string(form.cleaned_data['start_sell'])
            Settings().end_sell = datetime_to_string(form.cleaned_data['end_sell'])
            Settings().start_purchase = datetime_to_string(form.cleaned_data['start_purchase'])
            Settings().end_purchase = datetime_to_string(form.cleaned_data['end_purchase'])
            Settings().profit_per_book = form.cleaned_data['profit_per_book']
            Settings().tos_url = form.cleaned_data['tos_url']
            Settings().homepage_info = form.cleaned_data['homepage_info']
            set_success_msg(request, 'settings_updated')
            return HttpResponseRedirect("")
    else:
        settings = Settings('start_sell', 'end_sell', 'start_purchase', 'end_purchase',
                            'profit_per_book', 'tos_url', 'homepage_info')
        # Pack the retrieved values into new dictionary, formatting them as HTML datetime first
        values = dict(
            filter(lambda x: x is not None,
                   [add_date_value(settings, 'start_sell'),
                    add_date_value(settings, 'end_sell'),
                    add_date_value(settings, 'start_purchase'),
                    add_date_value(settings, 'end_purchase'),
                    add_value(settings, 'profit_per_book', 1),
                    add_value(settings, 'tos_url', ''),
                    add_value(settings, 'homepage_info', '')]))
        form = SettingsForm(initial=values)

    return render(request, 'settings/index.html', {'form': form})


def add_value(settings, name, default):
    return name, getattr(settings, name, default)

def add_date_value(settings, name):
    if hasattr(settings, name):
        return name, datetime_html_format(string_to_datetime(getattr(settings, name)))
    else:
        return None
