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

from django.forms import TextInput, ClearableFileInput
from django.forms.utils import flatatt
from django.utils.html import format_html

from django.utils.translation import ugettext as _


class PhoneNumberInput(TextInput):
    input_type = 'tel'


class FileFieldLink(ClearableFileInput):
    """
    Widget that displays file from FileField as a link to the uploaded data if 'disabled'
    attribute is set, or as <input type="file"> (ClearableFileInput) otherwise.
    """

    def render(self, name, value, attrs=None):
        attrs = self.build_attrs(attrs)
        if attrs.get('disabled'):
            attrs.pop('readonly')
            attrs.pop('disabled')
            if 'class' in attrs:
                # Avoid displaying the link as input
                attrs['class'] = attrs['class'].replace('form-control', '')

            p_attrs = {'class': 'form-control-static'}
            if value:
                attrs['href'] = value.url
                return format_html('<a{}><p{}>{}</p></a>',
                                   flatatt(attrs), flatatt(p_attrs), value.name)
            else:
                attrs.update(p_attrs)
                return format_html('<p{}>{}</p>', flatatt(attrs), _("No file uploaded"))
        else:
            return super(FileFieldLink, self).render(name, value, attrs)
