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
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from books.models import BookType
from egielda import settings
from utils.isbn import is_isbn_valid


class ISBNField(forms.CharField):
    default_error_messages = {
        'isbn_invalid': _("This ISBN is not valid."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(max_length=20, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(ISBNField, self).widget_attrs(widget)
        attrs.update({'required': 'required', 'pattern': '[0-9-]+', 'title': _("ISBN number")})
        return attrs

    def clean(self, value):
        val = super(ISBNField, self).clean(value)
        val = ''.join(filter(lambda x: x.isdigit(), val))
        return val

    def validate(self, value):
        super(ISBNField, self).validate(value)
        if not is_isbn_valid(value):
            raise ValidationError(self.error_messages['isbn_invalid'])


class BookForm(ModelForm):
    isbn = ISBNField(label=_("ISBN"))

    class Meta:
        model = BookType
        fields = '__all__'
        exclude = ['visible']
        labels = {
            'publisher': _("Publisher"),
            'title': _("Title"),
            'publication_year': _("Publication year"),
            'price': _("Price (%s)") % getattr(settings, 'CURRENCY', 'USD'),
            'categories': _("Categories")
        }
        widgets = {
            'publisher': forms.TextInput(attrs={'required': 'required'}),
            'title': forms.TextInput(attrs={'required': 'required'}),
            'publication_year': forms.NumberInput(attrs={'required': 'required', 'min': '1900', 'max': '2100'}),
            'price': forms.NumberInput(attrs={'required': 'required', 'max': '999.99'}),
        }
