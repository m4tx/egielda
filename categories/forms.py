from django import forms
from django.utils.translation import ugettext_lazy as _

from categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': _("Name")
        }