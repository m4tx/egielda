from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from books.models import BookType
from egielda import settings


class BookForm(ModelForm):
    # Different max_length than in model (to allow dashes in ISBN)
    isbn = forms.CharField(max_length=20, label=_("ISBN"),
                           widget=forms.TextInput(
                               attrs={'required': 'required', 'pattern': '[0-9-]+', 'title': 'ISBN number'}))

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

    def clean_isbn(self):
        data = self.cleaned_data['isbn']
        data = ''.join(filter(lambda x: x.isdigit(), data))
        return data
