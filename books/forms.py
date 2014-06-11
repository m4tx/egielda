from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from books.models import BookType
from egielda import settings


class BookForm(ModelForm):
    # Different max_length than in model (to allow dividers in ISBN number)
    isbn = forms.CharField(max_length=20, label=_("ISBN"))

    class Meta:
        model = BookType
        fields = ['isbn', 'publisher', 'title', 'publication_year', 'price']
        labels = {
            'isbn': _("ISBN"),
            'publisher': _("Publisher"),
            'title': _("Title"),
            'publication_year': _("Publication year"),
            'price': _("Price (%s)") % getattr(settings, 'CURRENCY', 'USD'),
        }
        widgets = {
            'isbn': forms.TextInput(attrs={'required': 'required'}),
            'publisher': forms.TextInput(attrs={'required': 'required'}),
            'title': forms.TextInput(attrs={'required': 'required'}),
            'publication_year': forms.NumberInput(attrs={'required': 'required', 'min': '1900', 'max': '2100'}),
            'price': forms.NumberInput(attrs={'required': 'required', 'max': '999.99'}),
        }

    def clean_isbn(self):
        data = self.cleaned_data['isbn']
        data = ''.join(filter(lambda x: x.isdigit(), data))
        return data