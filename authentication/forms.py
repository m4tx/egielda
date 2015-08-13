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

import re

from PIL import Image
import datetime
from django.forms import ModelForm, Select
from django.forms import PasswordInput, TextInput
from django.forms import ValidationError
from django.utils.translation import ugettext as _

from authentication.models import AppUser
from common.widgets import PhoneNumberInput, FileFieldLink
from egielda import settings
from utils.dates import get_current_year


def get_available_years():
    year = get_current_year()

    for y in range(year, 1999, -1):
        if y <= year-3:
            cl = _("graduate")
        else:
            cl = _("%(class)d class") % {'class': year-y+1}

        yield (y, "%(year)d (%(class)s)" % {'year': y, 'class': cl})


class UserDataForm(ModelForm):
    class Meta:
        model = AppUser
        fields = ['username', 'password', 'first_name', 'last_name', 'year', 'class_letter', 'phone_number', 'email',
                  'document']
        exclude = ['awaiting_verification', 'is_superuser', 'groups', 'user_permissions', 'last_login']

        widgets = {
            'username': TextInput(attrs={
                'title': _("Alpha-numeric characters only"),
                'pattern': '^[a-zA-Z0-9]*$'
            }),
            'phone_number': PhoneNumberInput(attrs={'maxlength': '9'}),
            'password': PasswordInput,
            'year': Select(choices=get_available_years()),
            'class_letter': TextInput(attrs={
                'pattern': '^[A-Z]$'
            }),
            'document': FileFieldLink,
        }
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'year': _("Beginning year"),
            'class_letter': _("Class letter"),
            'phone_number': _("Phone number"),
            'email': _("E-mail"),
            'document': _("School ID"),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.match('^[a-zA-Z0-9]*$', username):
            raise ValidationError(
                _("Username contains illegal characters."))

        return username

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_year(self):
        year = self.cleaned_data['year']
        curr_year = datetime.datetime.now().year

        if 2000 > year > curr_year:
            raise ValidationError(_("Invalid year."))

        return year

    def clean_class_letter(self):
        class_letter = self.cleaned_data['class_letter']

        if not re.match('^[A-Z]$', class_letter):
            raise ValidationError(_("Invalid class letter."))

        return class_letter

    """def clean_document(self):
        document = self.cleaned_data['document']
        if document is None:
            return document

        image = Image.open(document.file)

        if hasattr(image, '_getexif'):
            exif = image._getexif()
            if exif is not None:
                # 0x0112 is "Orientation" EXIF tag ID
                orientation = exif.get(0x0112, None)

                if orientation is not None:
                    if orientation == 3:
                        image = image.transpose(Image.ROTATE_180)
                    elif orientation == 6:
                        image = image.transpose(Image.ROTATE_270)
                    elif orientation == 8:
                        image = image.transpose(Image.ROTATE_90)

        document.file.seek(0)
        image.save(document.file, "jpeg")
        return document"""


class RegistrationForm(UserDataForm):
    class Meta(UserDataForm.Meta):
        if settings.USE_LDAP_VERIFICATION:
            exclude = ['document']


class SupplementForm(UserDataForm):
    class Meta(UserDataForm.Meta):
        fields = ['document']
