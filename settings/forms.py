from django import forms
from django.utils.translation import ugettext as _

from egielda import settings


class SettingsForm(forms.Form):
    start_sell = forms.DateTimeField(label=_("Selling start date"),
                                     widget=forms.TextInput(
                                         attrs={'type': 'datetime-local', 'data-datetimepicker': 'true',
                                                'required': 'required'}),
                                     input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    end_sell = forms.DateTimeField(label=_("Selling end date"),
                                   widget=forms.TextInput(
                                       attrs={'type': 'datetime-local', 'data-datetimepicker': 'true',
                                              'required': 'required'}),
                                   input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    start_purchase = forms.DateTimeField(label=_("Purchasing start date"),
                                         widget=forms.TextInput(
                                             attrs={'type': 'datetime-local', 'data-datetimepicker': 'true',
                                                    'required': 'required'}),
                                         input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    end_purchase = forms.DateTimeField(label=_("Purchasing end date"),
                                       widget=forms.TextInput(
                                           attrs={'type': 'datetime-local', 'data-datetimepicker': 'true',
                                                  'required': 'required'}),
                                       input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    profit_per_book = forms.DecimalField(label=_("Profit per book (%(currency)s)") % {
        'currency': getattr(settings, 'CURRENCY', "USD")},
                                         decimal_places=2,
                                         min_value=0,
                                         widget=forms.NumberInput(attrs={'required': 'required'}))
    validity_time = forms.IntegerField(label=_("Order validity time (h)"),
                                       min_value=1,
                                       widget=forms.NumberInput(attrs={'required': 'required'}))
    homepage_info = forms.CharField(label=_("Homepage information"),
                                    required=False,
                                    widget=forms.Textarea())