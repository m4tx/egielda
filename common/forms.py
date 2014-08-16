# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from common.models import AppUser
from common.widgets import PhoneNumberInput


class PersonalDataForm(ModelForm):
    """Form that's used in Sell/Purchase books wizard, providing fields for entering personal info.

    Included by views.personal_data().
    """
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
