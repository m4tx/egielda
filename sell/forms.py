from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from common.models import Student
from common.widgets import PhoneNumberInput


class PersonalDataForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_class', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': 'required'}),
            'last_name': forms.TextInput(attrs={'required': 'required'}),
            'student_class': forms.TextInput(attrs={'required': 'required'}),
            'phone_number': PhoneNumberInput(attrs={'required': 'required', 'maxlength': '9'}),
        }
        labels = {
            'student_class': _("Class")
        }