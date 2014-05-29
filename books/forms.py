from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from books.models import BookType
from egielda import settings


class BookForm(ModelForm):
    class Meta:
        model = BookType
        fields = ['publisher', 'title', 'price']
        labels = {
            'price': _("Price (%s)") % getattr(settings, 'CURRENCY', 'USD')
        }
        widgets = {
            'publisher': forms.TextInput(attrs={'required': 'required'}),
            'title': forms.TextInput(attrs={'required': 'required'}),
            'price': forms.NumberInput(attrs={'required': 'required', 'max': '999.99'}),
        }