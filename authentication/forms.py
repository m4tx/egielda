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

import re

from django.forms import ModelForm
from django.forms import PasswordInput, TextInput
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from authentication.models import AppUser
from common.widgets import PhoneNumberInput


class UserDataForm(ModelForm):
    class Meta:
        model = AppUser
        fields = ['username', 'password', 'first_name', 'last_name', 'student_class', 'phone_number', 'email',
                  'document']
        exclude = ['awaiting_verification', 'is_superuser', 'groups', 'user_permissions', 'last_login']

        widgets = {
            'phone_number': PhoneNumberInput(attrs={'maxlength': '9'}),
            'password': PasswordInput,
            'student_class': TextInput(attrs={
                'placeholder': _("\"graduate\" or [grade as an arabic numeral][capital class letter], e.g. 2A")}),
        }
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'student_class': _("Class"),
            'phone_number': _("Phone number"),
            'email': _("E-mail"),
            'document': _("Identity card"),
        }

    def clean_student_class(self):
        student_class = self.cleaned_data['student_class']

        if not re.match('^[123][A-Z]$', student_class) and student_class != _("graduate"):
            raise ValidationError(
                _("Invalid data. Use \"graduate\" or [grade as an arabic numeral][capital class letter], e.g. 2A"))

        return student_class
