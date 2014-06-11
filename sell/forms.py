from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from common.models import AppUser
from common.widgets import PhoneNumberInput


class PersonalDataForm(ModelForm):
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'student_class', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': 'required'}),
            'last_name': forms.TextInput(attrs={'required': 'required'}),
            'student_class': forms.TextInput(attrs={'required': 'required'}),
            'phone_number': PhoneNumberInput(attrs={'required': 'required', 'maxlength': '9'}),
        }
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'student_class': _("Class"),
            'phone_number': _("Phone number"),
        }