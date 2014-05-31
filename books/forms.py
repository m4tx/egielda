from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from books.models import BookType
from egielda import settings


class BookForm(ModelForm):
    class Meta:
        model = BookType
        fields = ['isbn', 'publisher', 'title', 'publication_year', 'price']
        labels = {
            'isbn': _("ISBN"),
            'price': _("Price (%s)") % getattr(settings, 'CURRENCY', 'USD'),
        }
        widgets = {
            'isbn': forms.TextInput(attrs={'required': 'required'}),
            'publisher': forms.TextInput(attrs={'required': 'required'}),
            'title': forms.TextInput(attrs={'required': 'required'}),
            'publication_year': forms.NumberInput(attrs={'required': 'required', 'min': '1900', 'max': '2100'}),
            'price': forms.NumberInput(attrs={'required': 'required', 'max': '999.99'}),
        }