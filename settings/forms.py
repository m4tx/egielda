from django import forms
from django.utils.translation import ugettext as _


class SettingsForm(forms.Form):
    start_sell = forms.DateTimeField(label=_("Selling start date"), widget=forms.TextInput(
                        attrs={"type": "datetime-local", "data-datetimepicker": "true", "required": "required"}),
                    input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    end_sell = forms.DateTimeField(label=_("Selling end date"), widget=forms.TextInput(
                        attrs={"type": "datetime-local", "data-datetimepicker": "true", "required": "required"}),
                    input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    start_purchase = forms.DateTimeField(label=_("Purchasing start date"), widget=forms.TextInput(
                        attrs={"type": "datetime-local", "data-datetimepicker": "true", "required": "required"}),
                    input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])
    end_purchase = forms.DateTimeField(label=_("Purchasing end date"), widget=forms.TextInput(
                        attrs={"type": "datetime-local", "data-datetimepicker": "true", "required": "required"}),
                    input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'])