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

from django.forms import TextInput, Widget
from django.forms.utils import flatatt
from django.utils.html import format_html


class PhoneNumberInput(TextInput):
    input_type = 'tel'


class FileFieldLink(Widget):
    """
    Widget that displays file from FileField as a link to the uploaded data.
    """

    def render(self, name, value, attrs=None):
        return format_html('<a{}><p{}>{}</p></a>',
                           flatatt({'href': value.url}),
                           flatatt({'class': 'form-control-static'}),
                           value.name)
