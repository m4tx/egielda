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

from django import forms
from django.utils.translation import ugettext as _

from egielda import settings


class SettingsForm(forms.Form):
    start_sell = forms.DateTimeField(label=_("Selling start date"),
                                     widget=forms.TextInput(
                                         attrs={'type': 'datetime-local'}),
                                     input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    end_sell = forms.DateTimeField(label=_("Selling end date"),
                                   widget=forms.TextInput(
                                       attrs={'type': 'datetime-local'}),
                                   input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    start_purchase = forms.DateTimeField(label=_("Purchasing start date"),
                                         widget=forms.TextInput(
                                             attrs={'type': 'datetime-local'}),
                                         input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    end_purchase = forms.DateTimeField(label=_("Purchasing end date"),
                                       widget=forms.TextInput(
                                           attrs={'type': 'datetime-local'}),
                                       input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    profit_per_book = forms.DecimalField(label=_("Profit per book (%(currency)s)") % {
        'currency': getattr(settings, 'CURRENCY', "USD")},
                                         decimal_places=2,
                                         min_value=0)
    homepage_info = forms.CharField(label=_("Homepage information"),
                                    required=False,
                                    widget=forms.Textarea())
