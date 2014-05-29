from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from books.models import BookType

from egielda import settings


class BookForm(ModelForm):
    class Meta:
        model = BookType
        fields = ['publisher', 'title', 'price']
        initial = {'publisher': 'gowno'}

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['price'].initial = 20


    # publisher = forms.CharField(help_text=_("Publisher"), max_length=150,
    #                             widget=forms.TextInput(attrs={'required': 'required'}))
    # title = forms.CharField(help_text=_("Title"), max_length=150,
    #                         widget=forms.TextInput(attrs={'required': 'required'}))
    # edition = forms.IntegerField(help_text=_("Edition"), min_value=1, initial=1,
    #                              widget=forms.NumberInput(attrs={'required': 'required'}))
    # publication_year = forms.IntegerField(help_text=_("Publication year"), min_value=1900, initial=2000, max_value=2100,
    #                                       widget=forms.NumberInput(attrs={'required': 'required'}))
    # price = forms.IntegerField(help_text=_("Price (%s)") % getattr(settings, 'CURRENCY', 'USD'), initial=20,
    #                            widget=forms.NumberInput(attrs={'required': 'required', 'step': '0.5'}))